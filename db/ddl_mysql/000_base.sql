-- MAIN TABLES (5 adet; hepsinde ≥3 non-key)
CREATE TABLE IF NOT EXISTS customers (
  customer_id VARCHAR(50) PRIMARY KEY,
  customer_unique_id VARCHAR(50),
  customer_zip_code_prefix INT,
  customer_city VARCHAR(100),
  customer_state VARCHAR(10)
);

CREATE TABLE IF NOT EXISTS orders (
  order_id VARCHAR(50) PRIMARY KEY,
  customer_id VARCHAR(50) NOT NULL,
  order_status VARCHAR(50),
  order_purchase_timestamp DATETIME,
  order_estimated_delivery_date DATETIME
);

CREATE TABLE IF NOT EXISTS products (
  product_id VARCHAR(50) PRIMARY KEY,
  product_weight_g INT,
  product_length_cm INT,
  product_height_cm INT,
  product_width_cm INT,
  product_photos_qty INT,
  product_category_name VARCHAR(100),
  category_id INT
);

CREATE TABLE IF NOT EXISTS order_payments (
  order_id VARCHAR(50) NOT NULL,
  payment_sequential INT NOT NULL,
  payment_type VARCHAR(50),
  payment_installments INT,
  payment_value DECIMAL(12,2),
  PRIMARY KEY (order_id, payment_sequential)
);

CREATE TABLE IF NOT EXISTS order_reviews (
  review_id VARCHAR(50) PRIMARY KEY,
  order_id VARCHAR(50),
  customer_id VARCHAR(50),
  review_score INT,
  review_comment_message TEXT,
  review_creation_date DATETIME
);

-- EXTRA / DIM / BRIDGE
CREATE TABLE IF NOT EXISTS order_items (
  order_id VARCHAR(50) NOT NULL,
  order_item_id INT NOT NULL,
  product_id VARCHAR(50) NOT NULL,
  seller_id VARCHAR(50) NOT NULL,
  shipping_limit_date DATETIME,
  price DECIMAL(12,2),
  freight_value DECIMAL(12,2),
  PRIMARY KEY (order_id, order_item_id)
);

CREATE TABLE IF NOT EXISTS sellers (
  seller_id VARCHAR(50) PRIMARY KEY,
  seller_zip_code_prefix INT,
  seller_city VARCHAR(100),
  seller_state VARCHAR(10)
);
