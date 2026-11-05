"""Prove the item-grain test rejects a deliberately duplicated fact row."""
import json
import os
from pathlib import Path
import subprocess
import sys
import duckdb
path=os.environ.get('COMMERCEFLOW_DB','data/commerceflow.duckdb')
with duckdb.connect(path) as c:
    c.execute('create table analytics.negative_test_backup as select * from analytics.fct_order_items')
    c.execute('insert into analytics.fct_order_items select * from analytics.fct_order_items limit 1')
try:
    dbt=Path(sys.executable).parent/('dbt.exe' if os.name=='nt' else 'dbt')
    r=subprocess.run([str(dbt),'test','--select','unique_item_key','--profiles-dir','profiles'],check=False)
    results=json.loads(Path('target/run_results.json').read_text())['results']
    assert r.returncode != 0 and len(results)==1 and results[0]['status']=='fail', results
    print('PASS: dbt rejected deliberately duplicated item key.')
finally:
    with duckdb.connect(path) as c:
        c.execute('create or replace table analytics.fct_order_items as select * from analytics.negative_test_backup')
        c.execute('drop table analytics.negative_test_backup')
