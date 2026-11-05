# BigQuery checkpoint — execution blocked by authentication

## What was checked

Before warehouse implementation, the environment had no `GOOGLE_APPLICATION_CREDENTIALS`, Application Default Credentials, configured GCP project or gcloud installation. `scripts/check_cloud.py` then exited 2 with `BLOCKED: no Google Application Default Credentials; BigQuery NOT verified.` No cloud resources or billing settings were changed.

The BigQuery adapter 1.9.2 installed and `dbt parse --profiles-dir profiles --target bigquery` passed. A compile attempt using `--no-introspect --no-populate-cache` still required authentication and failed. Parsing does not establish SQL execution, IAM correctness, successful loads or sandbox compatibility. Those remain unverified.

## Resume on an authenticated machine

Prerequisites: Python 3.12, Google Cloud CLI, your own existing BigQuery sandbox project, no enabled billing, permissions to create/read datasets and tables and submit jobs. Use the Cloud Console to confirm sandbox status and project identity. Do not upgrade or enable billing for this project.

```bash
source .venv/bin/activate
pip install -r requirements-bigquery.txt
gcloud auth application-default login
export GCP_PROJECT='your-existing-sandbox-project-id'
export GCP_LOCATION='EU'
python scripts/check_cloud.py
python scripts/load_raw.py --target bigquery --input data/olist
dbt debug --profiles-dir profiles --target bigquery
dbt build --profiles-dir profiles --target bigquery
dbt docs generate --profiles-dir profiles --target bigquery
```

Keep both raw and transformation datasets in the same location. The loader creates a raw dataset with a 60-day default table expiry if it does not exist, then uses CSV load jobs with `WRITE_TRUNCATE`. Loads replace one source table at a time: there is no cross-table transaction in the cloud path. Run transformations only after all loads succeed. The DAG currently tests the local path; it does not deploy cloud orchestration.

The models use views and fully replaced tables. There are no dbt seeds, incremental MERGEs, INSERTs or streaming writes. BigQuery sandbox disallows DML, streaming and the Data Transfer Service. Its tables/views/partitions expire after 60 days. Current sandbox documentation also lists a lifetime 10 GiB storage quota, not refunded on deletion, and 1 TiB monthly query processing; repeated reloads should be avoided. The profile caps each query at 1 GB processed; it is not a total project budget control. See [official sandbox documentation](https://docs.cloud.google.com/bigquery/docs/sandbox) and [dbt BigQuery setup](https://docs.getdbt.com/docs/core/connect-data-platform/bigquery-setup).

After a successful real build, preserve the BigQuery run results and independent counts/totals before marking cloud deployment verified. The current independent verifier connects to DuckDB only: separately query BigQuery and compare with `docs/evidence/full_data.json`. Do not mark cloud verification complete using the local verifier. Source hashes identify the exact files used here.
