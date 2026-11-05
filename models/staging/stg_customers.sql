select customer_id, customer_unique_id, customer_state as state, customer_city as city
from {{ source('raw', 'olist_customers_dataset') }}
