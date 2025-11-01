-- Kategori ciro
SELECT c.name AS category_name,
       SUM(oi.quantity * oi.price_each) AS revenue
FROM order_items oi
JOIN products p   ON p.product_id = oi.product_id
JOIN categories c ON c.id = p.category_id
GROUP BY c.name
ORDER BY revenue DESC;

-- Kategori başına ürün adedi
SELECT c.name AS category_name, COUNT(*) AS product_count
FROM products p
JOIN categories c ON c.id = p.category_id
GROUP BY c.name
ORDER BY product_count DESC;
