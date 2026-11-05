select seller_id, seller_state as state, seller_city as city
from {{ source('raw', 'olist_sellers_dataset') }}
