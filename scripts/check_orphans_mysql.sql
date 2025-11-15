-- FK Orphan Checks (MySQL)

-- Reviews → Customers
SELECT COUNT(*) AS orphan_reviews
FROM order_reviews r
LEFT JOIN customers c ON c.customer_id = r.customer_id
WHERE c.customer_id IS NULL;

-- Payments → Orders
SELECT COUNT(*) AS orphan_payments
FROM order_payments p
LEFT JOIN orders o ON o.order_id = p.order_id
WHERE o.order_id IS NULL;

-- Order_Items → Orders/Products/Sellers
SELECT
  SUM(IF(o.order_id  IS NULL, 1, 0))  AS orphan_oi_orders,
  SUM(IF(pr.product_id IS NULL, 1, 0)) AS orphan_oi_products,
  SUM(IF(s.seller_id  IS NULL, 1, 0))  AS orphan_oi_sellers
FROM order_items oi
LEFT JOIN orders   o  ON o.order_id    = oi.order_id
LEFT JOIN products pr ON pr.product_id = oi.product_id
LEFT JOIN sellers  s  ON s.seller_id   = oi.seller_id;

-- Table row counts
SELECT 'customers' AS t, COUNT(*) AS cnt FROM customers
UNION ALL SELECT 'orders', COUNT(*) FROM orders
UNION ALL SELECT 'products', COUNT(*) FROM products
UNION ALL SELECT 'order_payments', COUNT(*) FROM order_payments
UNION ALL SELECT 'order_reviews', COUNT(*) FROM order_reviews;
-- Customers → Geo_Zip
SELECT COUNT(*) AS missing_geo
FROM customers c
LEFT JOIN geo_zip g 
  ON g.geolocation_zip_code_prefix = c.customer_zip_code_prefix
WHERE g.geolocation_zip_code_prefix IS NULL;

