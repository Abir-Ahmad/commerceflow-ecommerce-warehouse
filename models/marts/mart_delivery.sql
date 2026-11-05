select delivery_band, count(*) as orders,
 avg(avg_review_score) as avg_order_review_score,
 avg(delivery_days * 1.0) as avg_delivery_days
from {{ ref('fct_orders') }} group by delivery_band
