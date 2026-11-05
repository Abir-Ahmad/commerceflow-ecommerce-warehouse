select p.product_id, p.category_name,
 coalesce(c.category_english, p.category_name, 'unknown') as category_english,
 p.weight_g
from {{ ref('stg_products') }} p
left join {{ ref('stg_categories') }} c on p.category_name = c.category_name
