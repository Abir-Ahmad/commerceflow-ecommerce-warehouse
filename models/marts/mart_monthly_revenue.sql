select {{ month_start('purchased_at') }} as purchase_month,
 count(*) as orders, sum(case when order_status = 'delivered' then 1 else 0 end) as delivered_orders,
 sum(merchandise_value) as ordered_merchandise_value,
 sum(case when order_status = 'delivered' then merchandise_value else 0 end) as delivered_merchandise_value,
 sum(freight_value) as freight_value, sum(payment_value) as payment_value
from {{ ref('fct_orders') }} group by 1
