select order_id from {{ ref('fct_order_items') }} where price < 0 or freight_value < 0 union all select order_id from {{ ref('stg_payments') }} where payment_value < 0
