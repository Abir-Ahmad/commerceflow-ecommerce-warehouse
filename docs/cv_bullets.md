# Evidence-backed CV bullets

- Built a dbt Core dimensional e-commerce warehouse on DuckDB, transforming 99,441 orders and 112,650 order items into three dimensions, two fact tables and four reporting marts.
- Implemented 48 dbt data-quality tests and seven independent CSV reconciliations covering key integrity, financial totals and delivery metrics; verified edge cases and rejection of duplicate fact keys.
- Orchestrated batch ingestion, dbt transformations and reconciliation with a three-task Apache Airflow DAG, successfully executing the full dataset using local `dag.test()`.

Do not claim BigQuery deployment, Docker containerisation, a live Airflow scheduler or passing hosted GitHub Actions until those have actually been verified. A BigQuery profile and loader are prepared, but cloud execution is blocked by missing authentication.
