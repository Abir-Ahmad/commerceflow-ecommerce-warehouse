select 1 as failure where (select count(*) from {{ ref('stg_orders') }}) <> (select count(*) from {{ ref('fct_orders') }})
