select 1 as failure where abs((select sum(merchandise_value) from {{ ref('fct_orders') }}) - (select sum(ordered_merchandise_value) from {{ ref('mart_monthly_revenue') }})) > 0.01
