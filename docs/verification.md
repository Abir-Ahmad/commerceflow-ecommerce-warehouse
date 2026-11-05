# Verification record — 5 November 2026

## Executed successfully

| Check | Actual result |
|---|---|
| Full-data ingestion + `dbt build` | 17 models built, 48 tests passed, no warnings/errors/skips |
| Independent CSV reconciliation | Seven checks passed: orders, items, merchandise total, payment total, observed deliveries, late deliveries and high-freight items |
| Source identity | Eight CSV row counts and SHA-256 hashes recorded in `docs/evidence/full_data.json` |
| Synthetic fixture | Multi-item/payment/review order, missing children, same-day deadline, late bands, untranslated/null categories and monthly total passed |
| Negative test | Duplicated fact item caused `unique_item_key` to fail as expected; table restored and complete build passed afterwards |
| Clean environment | Installed `requirements.lock.txt` into a new Python 3.12 virtual environment; fixture build, exact-answer checks, negative test, restored build and `dbt docs generate` all passed |
| Airflow 2.10.5 | `dag.test()` on the complete original dataset: `load_raw`, `dbt_build`, `reconcile` all success |
| GitHub-hosted CI | Both `dbt-duckdb` and `airflow-local` passed in [run #1](https://github.com/Abir-Ahmad/commerceflow-ecommerce-warehouse/actions/runs/42029595045) for commit `0826c8902f90e901e4d26d6ee9b1cf8856f3bffa` |
| Docker | Hosted `docker build` and `docker run --rm commerceflow:test` succeeded, including 17 models, 48 tests, seven reconciliations and fixture assertions |
| BigQuery adapter | Installed 1.9.2; project/profile parsing passed |

Full-data build command:

```bash
python scripts/run_local.py --input /path/to/original/csvs --evidence docs/evidence/full_data.json
```

Clean validation uses exactly the README's fixture commands, including the expected negative test and restored build. Airflow commands are in `docs/airflow.md`. The captured full-data run used dbt Core 1.9.8, dbt-duckdb 1.9.6, DuckDB 1.3.2 and Python 3.12.14 on Linux. See JSON evidence files for machine-readable results and timestamps. No throughput, scale or cloud performance claims were measured.

## Blocked or deliberately omitted

- **BigQuery execution:** no ADC/project available. Read-only preflight exited 2. Even `dbt compile --no-introspect --no-populate-cache` attempted authentication and failed. No cloud data load, build, test or catalog generation succeeded. `dbt parse` is only configuration/graph validation.
- **Airflow scheduler:** not deployed; the tested scope is real local operator execution using `dag.test()` and SQLite metadata, with a separate DuckDB warehouse.
- **Docker scope:** verified on the GitHub-hosted runner with synthetic data, not on the full original dataset. There is no local Docker executable/daemon.
- **Parquet:** omitted because the CSV batch source already works directly in both loader paths; no additional format was needed.

An initial unpinned DuckDB 2.0.0 installation crashed during ingestion. The dependency was pinned to 1.3.2, the affected generated database was recreated, and the full run and fresh-environment validation succeeded. The failed run is not counted as a successful verification.

## Final cloud retry

The BigQuery plugin was discovered but is disabled by the workspace administrator. The Google Cloud Console and BigQuery Console both returned `Site Unavailable` in the cloud browser, including the final retry. A Google CLI OAuth account-choice prompt was attempted, but secure authorisation timed out; no ADC credentials were saved. No BigQuery jobs or resources were created and no billing was enabled. Exact user-machine setup and output comparisons are in `docs/bigquery.md`.

Hosted CI emitted non-failing notices about Node.js action versions and the ubuntu-latest runner transition. These did not prevent either job, container execution or artifact upload from succeeding.
