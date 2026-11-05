# How the code works — beginner guide

Start with the README's synthetic fixture commands. They work without cloud accounts or raw-data downloads. Then open these files in order:

| File/folder | Purpose |
|---|---|
| `scripts/catalog.py` | Names the eight input tables. |
| `scripts/load_raw.py` | Checks the files exist, then loads raw string columns. Locally this is one DuckDB transaction; for BigQuery it uses batch load jobs, not INSERT/streaming. |
| `profiles/profiles.yml` | Tells dbt where the warehouse is. `local` is DuckDB; `bigquery` uses your own OAuth credentials. No secrets are stored here. |
| `dbt_project.yml` | Sets project paths and whether each layer becomes views or tables. |
| `models/staging/sources.yml` | Maps dbt source names to existing raw tables. |
| `models/staging/stg_*.sql` | Renames fields and casts strings into dates, numbers and money. Empty timestamp strings become null. |
| `models/warehouse/dim_*.sql` | Builds descriptive customer, seller and product tables. |
| `models/warehouse/fct_order_items.sql` | Keeps one record per item, with amounts and freight burden. |
| `models/warehouse/fct_orders.sql` | Adds item totals, payment totals and review averages to one row per order. |
| `models/marts/` | Groups facts into tables that answer business questions. |
| `models/schema.yml` | Describes grains and runs built-in key, null, relationship and accepted-value tests. |
| `tests/` | SQL checks that return problematic rows. Zero returned rows means pass. |
| `scripts/verify_actual.py` | Independently reads CSVs with Python/Decimal and compares seven counts/totals to the warehouse. Writes JSON evidence. |
| `scripts/run_local.py` | Runs ingestion, `dbt build` and independent verification in order; stops on failure. |
| `scripts/make_fixture.py`, `assert_fixture.py` | Creates tiny edge cases and checks their exact expected results. |
| `scripts/check_negative_test.py` | Deliberately duplicates an item, confirms the grain test fails, then restores the table. Run a fresh build afterwards. |
| `dags/commerceflow.py` | Expresses the three workflow tasks and their execution order in Airflow. |
| `Dockerfile`, `.dockerignore` | Packages the local workflow and excludes credentials, raw data and caches from the build context. |
| `scripts/container_smoke.py` | Runs the fixture workflow and known-answer checks inside the container. |
| `.github/workflows/ci.yml` | Runs both validation paths on a GitHub runner after a push/PR. |

## Read one model

In `fct_orders.sql`, `items`, `payments` and `reviews` are CTEs: named intermediate queries used only inside that SQL statement. Each groups by `order_id`. `sum(price)` becomes the order's merchandise value; `avg(review_score)` becomes its review average.

`{{ ref('stg_orders') }}` tells dbt to find that model and build it first. You do not manually type a physical table path. `{{ source('raw', 'olist_orders_dataset') }}` points to an input table that the loader created; dbt does not load the CSV itself.

A `left join` keeps every order even if a child record is missing. Aggregating the child tables first means an order with two items and two payments produces one order row, rather than four combinations. `case` statements classify delivery dates into the documented bands.

`dbt build` creates the model tables/views and executes their tests. It does not prove cloud portability; switching the target still requires real cloud execution. `dbt docs generate` creates local browsable documentation and lineage in `target/`; `dbt docs serve --profiles-dir profiles` opens it when run on your own machine.

## Windows

Use WSL for the exact commands in this repository, especially Airflow (tested on Linux). For local dbt in PowerShell, create the environment with `py -3.12 -m venv .venv`, activate using `.venv\Scripts\Activate.ps1`, and run the Python/dbt commands normally. The full PowerShell route has not been tested here; the Airflow DAG's default Python path targets Linux/WSL.
