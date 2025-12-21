-- Sprint C: Constraints and Indexes
-- Purpose: Add indexes for analytics query performance
-- Safe to run: Won't break existing data or ETL

USE olist;

-- ============================================================================
-- SECTION 1: INDEXES (Performance Optimization)
-- ============================================================================

-- Orders table indexes
CREATE INDEX IF NOT EXISTS idx_orders_customer 
    ON orders(customer_id);

CREATE INDEX IF NOT EXISTS idx_orders_status 
    ON orders(order_status);

CREATE INDEX IF NOT EXISTS idx_orders_delivered_date 
    ON orders(order_delivered_customer_date);

-- Order Items table indexes (CRITICAL for analytics joins)
CREATE INDEX IF NOT EXISTS idx_order_items_order 
    ON order_items(order_id);

CREATE INDEX IF NOT EXISTS idx_order_items_product 
    ON order_items(product_id);

CREATE INDEX IF NOT EXISTS idx_order_items_seller 
    ON order_items(seller_id);

-- Order Reviews table indexes
CREATE INDEX IF NOT EXISTS idx_order_reviews_order 
    ON order_reviews(order_id);

-- Products table indexes
CREATE INDEX IF NOT EXISTS idx_products_category 
    ON products(product_category_name);

-- ============================================================================
-- SECTION 2: OPTIONAL FOREIGN KEY CONSTRAINTS (Data Integrity)
-- WARNING: Only enable if data integrity is guaranteed
-- Comment out if ETL fails with FK violations
-- ============================================================================

-- Uncomment the following section to add strict foreign key constraints:

/*
-- Orders → Customers
ALTER TABLE orders
ADD CONSTRAINT fk_orders_customer
FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
ON DELETE RESTRICT
ON UPDATE CASCADE;

-- Order Items → Orders
ALTER TABLE order_items
ADD CONSTRAINT fk_order_items_order
FOREIGN KEY (order_id) REFERENCES orders(order_id)
ON DELETE CASCADE
ON UPDATE CASCADE;

-- Order Items → Products
ALTER TABLE order_items
ADD CONSTRAINT fk_order_items_product
FOREIGN KEY (product_id) REFERENCES products(product_id)
ON DELETE RESTRICT
ON UPDATE CASCADE;

-- Order Items → Sellers
ALTER TABLE order_items
ADD CONSTRAINT fk_order_items_seller
FOREIGN KEY (seller_id) REFERENCES sellers(seller_id)
ON DELETE RESTRICT
ON UPDATE CASCADE;

-- Order Payments → Orders
ALTER TABLE order_payments
ADD CONSTRAINT fk_order_payments_order
FOREIGN KEY (order_id) REFERENCES orders(order_id)
ON DELETE CASCADE
ON UPDATE CASCADE;

-- Order Reviews → Orders
ALTER TABLE order_reviews
ADD CONSTRAINT fk_order_reviews_order
FOREIGN KEY (order_id) REFERENCES orders(order_id)
ON DELETE CASCADE
ON UPDATE CASCADE;

-- Products → Categories
ALTER TABLE products
ADD CONSTRAINT fk_products_category
FOREIGN KEY (product_category_name) REFERENCES categories(product_category_name)
ON DELETE SET NULL
ON UPDATE CASCADE;
*/

-- ============================================================================
-- SECTION 3: VERIFICATION QUERIES
-- ============================================================================

-- List all indexes
SELECT 
    TABLE_NAME,
    INDEX_NAME,
    COLUMN_NAME,
    SEQ_IN_INDEX,
    INDEX_TYPE
FROM INFORMATION_SCHEMA.STATISTICS
WHERE TABLE_SCHEMA = 'olist'
  AND INDEX_NAME LIKE 'idx_%'
ORDER BY TABLE_NAME, INDEX_NAME, SEQ_IN_INDEX;

-- Show index sizes
SELECT 
    TABLE_NAME,
    INDEX_NAME,
    ROUND(STAT_VALUE * @@innodb_page_size / 1024 / 1024, 2) AS size_mb
FROM mysql.innodb_index_stats
WHERE DATABASE_NAME = 'olist'
  AND INDEX_NAME LIKE 'idx_%'
ORDER BY size_mb DESC;

-- Count rows per table (verify data integrity)
SELECT 
    'customers' AS table_name, COUNT(*) AS row_count FROM customers
UNION ALL
SELECT 'orders', COUNT(*) FROM orders
UNION ALL
SELECT 'order_items', COUNT(*) FROM order_items
UNION ALL
SELECT 'products', COUNT(*) FROM products
UNION ALL
SELECT 'sellers', COUNT(*) FROM sellers
UNION ALL
SELECT 'order_payments', COUNT(*) FROM order_payments
UNION ALL
SELECT 'order_reviews', COUNT(*) FROM order_reviews
UNION ALL
SELECT 'categories', COUNT(*) FROM categories;

-- ============================================================================
-- Sprint C Complete!
-- ============================================================================

SELECT 'Sprint C indexes applied successfully!' AS status;
