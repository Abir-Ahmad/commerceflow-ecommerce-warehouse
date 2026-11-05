select 1 as failure where abs((select sum(payment_value) from {{ ref('stg_payments') }}) - (select sum(payment_value) from {{ ref('fct_orders') }})) > 0.01
