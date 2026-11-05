select order_status, count(*) as orders,
 sum(case when delivered_at is not null then 1 else 0 end) as orders_with_delivery_timestamp,
 sum(case when item_count = 0 then 1 else 0 end) as orders_without_items
from {{ ref('fct_orders') }} group by order_status
