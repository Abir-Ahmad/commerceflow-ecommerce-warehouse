"""Manual, serial batch DAG; run with Airflow 2.10.5 in its separate environment."""
from datetime import datetime, timezone
import os
from pathlib import Path
import subprocess
from airflow import DAG
from airflow.operators.python import PythonOperator
ROOT = Path(__file__).resolve().parents[1]

def command(step):
    python = Path(os.environ.get('COMMERCEFLOW_PYTHON', str(ROOT / '.venv/bin/python')))
    source = Path(os.environ.get('COMMERCEFLOW_INPUT', str(ROOT / 'data/fixture'))).resolve()
    commands = {
      'load': [str(python), 'scripts/load_raw.py', '--input', str(source)],
      'build': [str(python.with_name('dbt')), 'build', '--profiles-dir', 'profiles', '--target', 'local'],
      'verify': [str(python), 'scripts/verify_actual.py', '--input', str(source), '--output', 'target/airflow-reconciliation.json']}
    subprocess.run(commands[step], cwd=ROOT, check=True)

with DAG('commerceflow', start_date=datetime(2024,1,1,tzinfo=timezone.utc),
         schedule=None, catchup=False, max_active_runs=1,
         default_args={'retries': 0}, tags=['portfolio', 'dbt']) as dag:
    load = PythonOperator(task_id='load_raw', python_callable=command, op_args=['load'])
    build = PythonOperator(task_id='dbt_build', python_callable=command, op_args=['build'])
    verify = PythonOperator(task_id='reconcile', python_callable=command, op_args=['verify'])
    load >> build >> verify
