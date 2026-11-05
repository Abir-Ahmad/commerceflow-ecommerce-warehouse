# CommerceFlow — E-commerce Analytics Warehouse

A dbt Core dimensional warehouse built from my existing Olist delivery analytics project. It complements [GridFlow](https://github.com/Abir-Ahmad/gridflow-energy-pipeline) with dimensional modelling, tested SQL transformations and a small Apache Airflow workflow.

**Verified locally:** DuckDB execution on the original 99,441 orders and 112,650 items; 17 dbt models, 48 passing data tests, seven independent CSV reconciliations, synthetic edge-case checks and an executed three-task Airflow DAG.

**Verified on GitHub Actions:** both `dbt-duckdb` and `airflow-local` passed; the local-workflow Docker image was built and its fixture test executed successfully. [View the actual CI run](https://github.com/Abir-Ahmad/commerceflow-ecommerce-warehouse/actions/runs/42029595045).

**Cloud status:** BigQuery adapter/profile and batch loader are provided, and `dbt parse --target bigquery` passed. BigQuery authentication and execution are **not verified**: no Application Default Credentials or GCP project were available. No billing was enabled. This is a working local project with a cloud deployment checkpoint, not a deployed BigQuery warehouse.

## Run locally

Python 3.12. Commands below run from the repository root (Linux/macOS or WSL).

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.lock.txt
python scripts/make_fixture.py
python scripts/run_local.py --input data/fixture
python scripts/assert_fixture.py
python scripts/check_negative_test.py
# Restore a complete successful build after the expected negative test:
dbt build --profiles-dir profiles --target local
dbt docs generate --profiles-dir profiles --target local
```

For the full dataset, download the [Olist Brazilian E-Commerce Public Dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) and place its CSVs in `data/olist`. Use the original eight filenames listed in [the input inventory](docs/source_audit.md), then run:

```bash
python scripts/run_local.py --input data/olist
```

This loads raw CSVs, builds/tests all models and writes independent reconciliation evidence to `target/evidence.json`. Raw data, database files and Power BI assets are excluded from Git. The fixture is synthetic, deterministic and generated locally. Source data retains its original CC BY-NC-SA 4.0 terms; see the dataset publisher's page. No raw data is redistributed here.

## What it answers

| Question | Model |
|---|---|
| How does ordered/delivered merchandise value change monthly? | `mart_monthly_revenue` |
| What happens to orders across fulfilment statuses? | `mart_fulfilment` |
| How late are deliveries, and how do reviews compare? | `mart_delivery` |
| Which categories have a high freight burden? | `mart_category_freight` |

Amounts are BRL. Merchandise value excludes freight; payments include other order charges and are a separate measure. Delivered merchandise is a fulfilment-based proxy, not accounting revenue. No refund or profit claims are made.

## Measured results

- Ordered merchandise value: **R$13,591,643.70**; recorded payments: **R$16,008,872.12**.
- Of 96,476 orders with observed delivery and estimated dates, **89,941 (93.23%)** were delivered by the estimated calendar date; 6,535 were late.
- November 2017 had the highest delivered merchandise value in this snapshot: **R$987,765.37**.
- **24,434 of 112,650 items (21.69%)** had freight burden above 30%.

The calendar-date deadline differs from the original SQL's midnight timestamp comparison. The original README also contains a small count discrepancy against its actual data. [The source audit](docs/source_audit.md) records both differences. Partial months and unresolved orders remain visible; comparisons should account for the incomplete data window.

## Explore and reproduce

- [Architecture, grains and dependencies](docs/architecture.md)
- [Beginner guide to the main files](docs/how_it_works.md)
- [Exact test record and limitations](docs/verification.md)
- [BigQuery deployment checkpoint](docs/bigquery.md)
- [Run the tested Airflow DAG](docs/airflow.md)
- [Minimal Docker workflow](docs/docker.md)
- [Business queries](analyses/business_questions.sql)
- [Three evidence-backed CV bullets](docs/cv_bullets.md)
- [Full-data evidence](docs/evidence/full_data.json)

GitHub Actions passed the synthetic fixture suite, Docker image build and container test, and Airflow DAG test. Docker was verified on a GitHub-hosted runner; no local Docker daemon was available. The container test uses synthetic data; the original full dataset was verified separately on DuckDB and local Airflow. Parquet adds no necessary benefit for this small, directly loaded CSV snapshot.
