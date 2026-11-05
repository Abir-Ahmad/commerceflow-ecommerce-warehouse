select order_id, cast(payment_sequential as integer) as payment_sequential, payment_type,
 cast(payment_value as {{ money_type() }}) as payment_value
from {{ source('raw', 'olist_order_payments_dataset') }}
