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
| BigQuery adapter | Installed 1.9.2; project/profile parsing passed |

Full-data build command:

```bash
python scripts/run_local.py --input /path/to/original/csvs --evidence docs/evidence/full_data.json
```

Clean validation uses exactly the README's fixture commands, including the expected negative test and restored build. Airflow commands are in `docs/airflow.md`. The captured full-data run used dbt Core 1.9.8, dbt-duckdb 1.9.6, DuckDB 1.3.2 and Python 3.12.14 on Linux. See JSON evidence files for machine-readable results and timestamps. No throughput, scale or cloud performance claims were measured.

## Blocked or deliberately omitted

- **BigQuery execution:** no ADC/project available. Read-only preflight exited 2. Even `dbt compile --no-introspect --no-populate-cache` attempted authentication and failed. No cloud data load, build, test or catalog generation succeeded. `dbt parse` is only configuration/graph validation.
- **GitHub publication and hosted Actions:** authenticated account confirmed as `Abir-Ahmad`; the connected interface has no repository-creation operation. Repository does not yet exist. Workflow commands passed locally, but there is no hosted run URL or green hosted result to claim. Resume from `CHECKPOINT.md`.
- **Airflow scheduler:** not deployed; the tested scope is real local operator execution using `dag.test()` and SQLite metadata, with a separate DuckDB warehouse.
- **Docker:** no executable/daemon was available; no speculative Dockerfile was added.
- **Parquet:** omitted because the CSV batch source already works directly in both loader paths; no additional format was needed.

An initial unpinned DuckDB 2.0.0 installation crashed during ingestion. The dependency was pinned to 1.3.2, the affected generated database was recreated, and the full run and fresh-environment validation succeeded. The failed run is not counted as a successful verification.
