select order_id, cast(order_item_id as integer) as order_item_id, product_id, seller_id,
 cast(price as {{ money_type() }}) as price,
 cast(freight_value as {{ money_type() }}) as freight_value
from {{ source('raw', 'olist_order_items_dataset') }}
