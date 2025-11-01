CREATE TABLE IF NOT EXISTS categories (
  category_id INT AUTO_INCREMENT PRIMARY KEY,
  category_name VARCHAR(100) UNIQUE,
  category_name_english VARCHAR(100)
);

ALTER TABLE products
  ADD CONSTRAINT fk_products__category
  FOREIGN KEY (category_id) REFERENCES categories(category_id);
