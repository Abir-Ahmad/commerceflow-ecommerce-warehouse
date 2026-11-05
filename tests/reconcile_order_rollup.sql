with raw_totals as (select sum(price) as value from {{ ref('stg_items') }}),
 fact_totals as (select sum(merchandise_value) as value from {{ ref('fct_orders') }})
select r.value from raw_totals r cross join fact_totals f where abs(r.value-f.value) > 0.01
