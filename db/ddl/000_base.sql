-- MAIN TABLES (5 adet; hepsinde ≥3 non-key)
CREATE TABLE IF NOT EXISTS customers (
  customer_id TEXT PRIMARY KEY,
  customer_unique_id TEXT,
  customer_zip_code_prefix INT,
  customer_city TEXT,
  customer_state TEXT
);

CREATE TABLE IF NOT EXISTS orders (
  order_id TEXT PRIMARY KEY,
  customer_id TEXT NOT NULL,
  order_status TEXT,
  order_purchase_timestamp TIMESTAMP,
  order_estimated_delivery_date TIMESTAMP
);

CREATE TABLE IF NOT EXISTS products (
  product_id TEXT PRIMARY KEY,
  product_weight_g INT,
  product_length_cm INT,
  product_height_cm INT,
  product_width_cm INT,
  product_photos_qty INT,
  product_category_name TEXT,
  category_id INT
);

CREATE TABLE IF NOT EXISTS order_payments (
  order_id TEXT NOT NULL,
  payment_sequential INT NOT NULL,
  payment_type TEXT,
  payment_installments INT,
  payment_value NUMERIC(12,2),
  PRIMARY KEY (order_id, payment_sequential)
);

CREATE TABLE IF NOT EXISTS order_reviews (
  review_id TEXT PRIMARY KEY,
  order_id TEXT,
  customer_id TEXT,
  review_score INT,
  review_comment_message TEXT,
  review_creation_date TIMESTAMP
);

-- EXTRA / DIM / BRIDGE
CREATE TABLE IF NOT EXISTS order_items (
  order_id TEXT NOT NULL,
  order_item_id INT NOT NULL,
  product_id TEXT NOT NULL,
  seller_id TEXT NOT NULL,
  shipping_limit_date TIMESTAMP,
  price NUMERIC(12,2),
  freight_value NUMERIC(12,2),
  PRIMARY KEY (order_id, order_item_id)
);

CREATE TABLE IF NOT EXISTS sellers (
  seller_id TEXT PRIMARY KEY,
  seller_zip_code_prefix INT,
  seller_city TEXT,
  seller_state TEXT
);
