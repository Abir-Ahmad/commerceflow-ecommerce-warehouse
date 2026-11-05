select order_id, order_item_id, product_id, seller_id, price, freight_value,
 price + freight_value as item_total,
 case when price + freight_value > 0 then freight_value / (price + freight_value) end as freight_burden
from {{ ref('stg_items') }}
