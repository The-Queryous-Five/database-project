CREATE TABLE IF NOT EXISTS categories (
  category_id SERIAL PRIMARY KEY,
  category_name TEXT UNIQUE,
  category_name_english TEXT
);
ALTER TABLE products
  ADD CONSTRAINT fk_products__category
  FOREIGN KEY (category_id) REFERENCES categories(category_id);
