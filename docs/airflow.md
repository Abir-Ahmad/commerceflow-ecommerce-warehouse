# Tested local Airflow orchestration

The `commerceflow` DAG executes three real operators: raw loading, `dbt build`, and independent reconciliation. It is manually triggered (`schedule=None`), serial and limited to one active run. Failed subprocesses fail the task. It runs full snapshots; it is not an incremental or production scheduler deployment.

Airflow and dbt use separate virtual environments because their dependency constraints differ. Python 3.12 on Linux/WSL:

```bash
# First follow the README to create .venv and install requirements.lock.txt.
python3.12 -m venv .airflow-venv
.airflow-venv/bin/pip install -r requirements-airflow.txt
export AIRFLOW_HOME="$PWD/data/airflow"
export AIRFLOW__CORE__LOAD_EXAMPLES=false
export AIRFLOW__CORE__UNIT_TEST_MODE=true
export DBT_SEND_ANONYMOUS_USAGE_STATS=false
export COMMERCEFLOW_PYTHON="$PWD/.venv/bin/python"
.venv/bin/python scripts/make_fixture.py
export COMMERCEFLOW_INPUT="$PWD/data/fixture"
export COMMERCEFLOW_DB="$PWD/data/airflow.duckdb"
.airflow-venv/bin/airflow db migrate
.airflow-venv/bin/python scripts/test_airflow.py
```

To execute the full dataset, set `COMMERCEFLOW_INPUT="$PWD/data/olist"` before the final command. `dag.test()` executes operators and checks all three task states are `success`; it writes `target/airflow-test.json` and `target/airflow-reconciliation.json`. It does not start a webserver or scheduler. An actual full-data run passed here; see `docs/evidence/airflow.json`. The separate `airflow-local` GitHub Actions job also passed on the synthetic fixture; see [run #1](https://github.com/Abir-Ahmad/commerceflow-ecommerce-warehouse/actions/runs/42029595045).

Airflow is optional: the main local runner works without it. The minimal Docker image runs local dbt only; Airflow retains its separately tested Python environment. See `docs/docker.md` for container verification status.
