with items as (
 select order_id, count(*) as item_count, sum(price) as merchandise_value,
 sum(freight_value) as freight_value from {{ ref('fct_order_items') }} group by order_id
), payments as (
 select order_id, count(*) as payment_count, sum(payment_value) as payment_value
 from {{ ref('stg_payments') }} group by order_id
), reviews as (
 select order_id, count(*) as review_count, avg(review_score * 1.0) as avg_review_score
 from {{ ref('stg_reviews') }} group by order_id
), joined as (
 select o.*, coalesce(i.item_count, 0) as item_count,
 coalesce(i.merchandise_value, 0) as merchandise_value,
 coalesce(i.freight_value, 0) as freight_value,
 coalesce(p.payment_count, 0) as payment_count, p.payment_value,
 coalesce(r.review_count, 0) as review_count, r.avg_review_score,
 {{ days_between('purchased_at', 'delivered_at') }} as delivery_days,
 {{ days_between('estimated_at', 'delivered_at') }} as delay_days
 from {{ ref('stg_orders') }} o
 left join items i on o.order_id = i.order_id
 left join payments p on o.order_id = p.order_id
 left join reviews r on o.order_id = r.order_id
)
select *,
 case when delivered_at is null or estimated_at is null then 'not_observed'
 when cast(delivered_at as date) <= cast(estimated_at as date) then 'on_time'
 when delay_days <= 3 then '1_3_days_late'
 when delay_days <= 7 then '4_7_days_late' else '8_plus_days_late' end as delivery_band
from joined
