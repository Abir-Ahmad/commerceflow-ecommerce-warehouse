SELECT
    COALESCE(t.product_category_name_english, 'Unknown') AS category,
    COUNT(*) AS total_items,
    ROUND(AVG(
        100.0 * i.freight_value /
        NULLIF(i.price + i.freight_value, 0)
    ), 2) AS avg_freight_percentage,
    ROUND(SUM(i.price + i.freight_value), 2) AS total_item_cost
FROM olist_order_items_dataset AS i
LEFT JOIN olist_products_dataset AS p
    ON i.product_id = p.product_id
LEFT JOIN product_category_name_translation AS t
    ON p.product_category_name = t.product_category_name
GROUP BY category
HAVING COUNT(*) >= 1000
ORDER BY avg_freight_percentage DESC;
