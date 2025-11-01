CREATE INDEX IF NOT EXISTS idx_products__category_id ON products(category_id);
CREATE INDEX IF NOT EXISTS idx_customers__zip        ON customers(customer_zip_code_prefix);
CREATE INDEX IF NOT EXISTS idx_sellers__zip          ON sellers(seller_zip_code_prefix);
CREATE INDEX IF NOT EXISTS idx_payments__order_id    ON order_payments(order_id);
CREATE INDEX IF NOT EXISTS idx_reviews__customer_id  ON order_reviews(customer_id);
CREATE INDEX IF NOT EXISTS idx_oi__order_id          ON order_items(order_id);
CREATE INDEX IF NOT EXISTS idx_oi__product_id        ON order_items(product_id);
CREATE INDEX IF NOT EXISTS idx_oi__seller_id         ON order_items(seller_id);
