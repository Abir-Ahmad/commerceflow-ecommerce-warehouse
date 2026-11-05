"""Batch-load original CSVs as strings; dbt owns typing and business logic."""
import argparse
import csv
import os
from pathlib import Path
from catalog import TABLES

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--target', choices=['local', 'bigquery'], default='local')
    args = parser.parse_args()
    paths = {t: args.input / (t + '.csv') for t in TABLES.values()}
    for path in paths.values():
        if not path.is_file():
            raise FileNotFoundError(path)
    if args.target == 'local':
        import duckdb
        db = Path(os.environ.get('COMMERCEFLOW_DB', 'data/commerceflow.duckdb'))
        db.parent.mkdir(parents=True, exist_ok=True)
        with duckdb.connect(str(db)) as con:
            con.execute('begin')
            con.execute('create schema if not exists raw')
            for table, path in paths.items():
                # Identifiers come only from the fixed catalog; paths use parameters.
                con.execute(f'create or replace table raw.{table} as select * from read_csv(?, header=true, all_varchar=true)', [str(path)])
                print(table, con.execute(f'select count(*) from raw.{table}').fetchone()[0])
            con.execute('commit')
    else:
        from google.cloud import bigquery
        from google.api_core.exceptions import NotFound
        client = bigquery.Client(project=os.environ['GCP_PROJECT'])
        dataset_id = client.project + '.raw'
        try:
            dataset = client.get_dataset(dataset_id)
        except NotFound:
            dataset = bigquery.Dataset(dataset_id)
            dataset.location = os.environ.get('GCP_LOCATION', 'EU')
            dataset.default_table_expiration_ms = 60 * 24 * 60 * 60 * 1000
            client.create_dataset(dataset)
        for table, path in paths.items():
            with path.open(encoding='utf-8-sig', newline='') as f:
                header = next(csv.reader(f))
            config = bigquery.LoadJobConfig(
                schema=[bigquery.SchemaField(c, 'STRING') for c in header],
                source_format=bigquery.SourceFormat.CSV, skip_leading_rows=1,
                allow_quoted_newlines=True, write_disposition='WRITE_TRUNCATE')
            with path.open('rb') as f:
                job = client.load_table_from_file(f, dataset_id + '.' + table, job_config=config, location=dataset.location)
            job.result()
            print(table, 'loaded')
if __name__ == '__main__':
    main()
