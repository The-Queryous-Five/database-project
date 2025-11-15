-- complex queries will be collected here

-- Top 10 categories by product count
SELECT c.name AS category_name, COUNT(*) AS product_count
FROM products p
JOIN categories c ON c.id = p.category_id
GROUP BY c.name
ORDER BY product_count DESC
LIMIT 10;
