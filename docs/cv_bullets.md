# Evidence-backed CV bullets

- Built a dbt Core dimensional e-commerce warehouse on DuckDB, transforming 99,441 orders and 112,650 items into three dimensions, two fact tables and four reporting marts.
- Implemented 48 dbt data-quality tests and seven independent CSV reconciliations; verified financial totals, delivery metrics, join fan-out edge cases and rejection of duplicate fact keys.
- Orchestrated a three-task Apache Airflow workflow and containerised local dbt validation with Docker, verifying both CI jobs and the container build/run through GitHub Actions.

The original full dataset passed on local DuckDB and Airflow `dag.test()`. GitHub Actions and Docker passed with the synthetic fixture. Do not claim BigQuery deployment, full-data Docker execution or a deployed Airflow scheduler. BigQuery execution remains blocked by authentication and Console access; its adapter, profile and loader are prepared only.
