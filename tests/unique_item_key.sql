select order_id, order_item_id from {{ ref('fct_order_items') }} group by 1,2 having count(*) > 1
