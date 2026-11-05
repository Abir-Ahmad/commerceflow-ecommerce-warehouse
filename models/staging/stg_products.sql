select product_id, nullif(product_category_name, '') as category_name,
 cast(nullif(product_weight_g, '') as integer) as weight_g
from {{ source('raw', 'olist_products_dataset') }}
