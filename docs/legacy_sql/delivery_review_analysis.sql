WITH order_reviews AS (
    SELECT
        order_id,
        AVG(review_score) AS avg_review_score
    FROM olist_order_reviews_dataset
    GROUP BY order_id
),
order_categories AS (
    SELECT DISTINCT
        i.order_id,
        COALESCE(t.product_category_name_english, 'Unknown') AS category
    FROM olist_order_items_dataset AS i
    LEFT JOIN olist_products_dataset AS p
        ON i.product_id = p.product_id
    LEFT JOIN product_category_name_translation AS t
        ON p.product_category_name = t.product_category_name
)
SELECT
    c.category,
    COUNT(*) AS total_orders,
    ROUND(AVG(CASE
        WHEN julianday(o.order_delivered_customer_date)
             <= julianday(o.order_estimated_delivery_date)
        THEN r.avg_review_score
    END), 2) AS on_time_review,
    ROUND(AVG(CASE
        WHEN julianday(o.order_delivered_customer_date)
             > julianday(o.order_estimated_delivery_date)
        THEN r.avg_review_score
    END), 2) AS late_review
FROM olist_orders_dataset AS o
JOIN order_categories AS c ON o.order_id = c.order_id
LEFT JOIN order_reviews AS r ON o.order_id = r.order_id
WHERE o.order_delivered_customer_date IS NOT NULL
  AND o.order_delivered_customer_date != ''
GROUP BY c.category
HAVING COUNT(*) >= 1000
ORDER BY total_orders DESC;
