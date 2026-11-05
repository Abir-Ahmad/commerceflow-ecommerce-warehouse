select p.category_english, count(*) as items,
 avg(i.freight_burden) as avg_freight_burden,
 sum(case when i.freight_burden > 0.30 then 1 else 0 end) as high_freight_items
from {{ ref('fct_order_items') }} i
join {{ ref('dim_products') }} p on i.product_id = p.product_id
group by p.category_english
