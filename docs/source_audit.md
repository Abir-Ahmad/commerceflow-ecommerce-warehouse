# Original project inspection and reuse

Inspected the attached README, SQLite database, DB Browser project XML, nine CSVs and the Power BI file container metadata. The dashboard was not rebuilt. The SQLite database has five tables, no declared foreign keys and no stored views: orders, reviews, items, products and category translations. CSVs additionally supply customers, sellers, payments and geolocation. Relationships are inferred from IDs and then tested.

The XML embeds one review aggregation query; other tabs only reference SQL paths on the original machine. The actual three SQL files were recovered from [the existing repository](https://github.com/Abir-Ahmad/Supply-Chain-Analytics/tree/5b09ea52f4162811320446c097285b8b134e2a04/sql) and preserved in `docs/legacy_sql/`. Personal machine paths were not copied. The original review aggregation, freight formula and category joins informed the dbt models. Category freight now retains all volumes; consumers can apply the original `items >= 1000` threshold.

| Required CSV basename | Rows |
|---|---:|
| `olist_orders_dataset.csv` | 99,441 |
| `olist_order_items_dataset.csv` | 112,650 |
| `olist_customers_dataset.csv` | 99,441 |
| `olist_sellers_dataset.csv` | 3,095 |
| `olist_products_dataset.csv` | 32,951 |
| `olist_order_payments_dataset.csv` | 103,886 |
| `olist_order_reviews_dataset.csv` | 99,224 |
| `product_category_name_translation.csv` | 71 |

The 1,000,163-row geolocation file has repeated ZIP prefixes and is unnecessary for the selected questions; it is deliberately not joined or loaded. CSVs stay as CSV: an extra Parquet copy is unnecessary for this snapshot and BigQuery supports batch CSV loading.

## Delivery metric audit

The original README reports 7,821 late deliveries out of 96,476 observations. Running the timestamp comparison used by its SQL against the supplied SQLite database and CSV instead gives **7,827**. This existing six-order documentation discrepancy is recorded rather than carried into new claims.

CommerceFlow compares calendar dates because the estimate is an inclusive date stored at midnight. It finds **6,535** late and **89,941** on-time deliveries. The difference of 1,292 from the reproduced timestamp result is same-date delivery later than midnight. The fixture specifically checks this boundary. The calendar-date definition is explicit; these counts should not be compared to the original README as though the definitions were identical.

## Scope and data limitations

There is no inventory balance, acquisition cost, returns/refund ledger or trustworthy profit field. The project cannot measure stockouts or net accounting revenue. Reviews have multiple records per order; review IDs are not assumed globally unique. The small differences between payment totals and item-plus-freight totals are preserved, not altered to force agreement. The snapshot includes partial boundary months and undelivered orders; it is historical batch data, not a live operational feed.
