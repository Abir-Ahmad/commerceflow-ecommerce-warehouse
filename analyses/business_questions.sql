-- Run in DuckDB against data/commerceflow.duckdb. Change analytics to
-- your GCP_PROJECT.commerceflow dataset for BigQuery after deployment.
select purchase_month, orders, delivered_orders, delivered_merchandise_value
from analytics.mart_monthly_revenue order by purchase_month;

select order_status, orders, orders_with_delivery_timestamp, orders_without_items
from analytics.mart_fulfilment order by orders desc;

select delivery_band, orders, avg_order_review_score, avg_delivery_days
from analytics.mart_delivery order by delivery_band;

select category_english, items, avg_freight_burden, high_freight_items
from analytics.mart_category_freight where items >= 1000
order by avg_freight_burden desc;
