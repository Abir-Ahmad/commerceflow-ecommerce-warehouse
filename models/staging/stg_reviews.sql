select review_id, order_id, cast(review_score as integer) as review_score
from {{ source('raw', 'olist_order_reviews_dataset') }}
