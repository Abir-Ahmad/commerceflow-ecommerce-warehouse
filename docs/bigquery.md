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

## Final access retry and minimum user action

The Google Cloud Console and BigQuery Console returned `Site Unavailable` in the cloud browser. The BigQuery connector is disabled by the workspace administrator. The CLI OAuth account-choice attempt timed out and no ADC credentials were saved. There is no completed cloud authorisation to reuse.

On your own trusted machine, open [BigQuery Console](https://console.cloud.google.com/bigquery), sign in, and create/select a **sandbox project with no billing account**. Accept Google terms yourself if required. Install the official Google Cloud CLI, then run the existing commands above in a terminal from this repository. `gcloud auth application-default login` opens your own browser and stores credentials locally; no keys or authorisation codes need to be sent in chat. Set `GCP_PROJECT` to the exact project ID, not its display name.

After the build passes, this query captures real cloud output (the Google Cloud CLI includes `bq`):

```bash
mkdir -p target
bq --project_id="$GCP_PROJECT" --location="$GCP_LOCATION" query \
  --use_legacy_sql=false --maximum_bytes_billed=1000000000 --format=prettyjson \
  'select count(*) as orders,
          (select count(*) from commerceflow.fct_order_items) as items,
          sum(merchandise_value) as merchandise_brl,
          sum(payment_value) as payments_brl,
          countif(delivery_band != "not_observed") as observed_deliveries,
          countif(delivery_band = "on_time") as on_time_deliveries,
          countif(delivery_band not in ("not_observed", "on_time")) as late_deliveries,
          (select sum(high_freight_items) from commerceflow.mart_category_freight) as high_freight_items
    from commerceflow.fct_orders' > target/bigquery-verification.json
```

Expected values from the actual local dataset:

| Field | Expected |
|---|---:|
| orders | 99,441 |
| items | 112,650 |
| merchandise_brl | 13,591,643.70 |
| payments_brl | 16,008,872.12 |
| observed_deliveries | 96,476 |
| on_time_deliveries | 89,941 |
| late_deliveries | 6,535 |
| high_freight_items | 24,434 |

Also compare `commerceflow.mart_monthly_revenue` ordered by purchase_month with `monthly_revenue` in `docs/evidence/full_data.json`. Preserve `target/run_results.json` from the BigQuery build and the BigQuery query job details/IDs. A successful 17-model/48-test cloud build plus matching output establishes cloud verification; these steps have **not** run here. Do not publish credentials or ADC files.
