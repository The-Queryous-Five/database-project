CREATE TABLE IF NOT EXISTS geo_zip (
  geolocation_zip_code_prefix INT PRIMARY KEY,
  geolocation_lat NUMERIC(10,6),
  geolocation_lng NUMERIC(10,6),
  geolocation_city TEXT,
  geolocation_state TEXT
);
ALTER TABLE customers
  ADD CONSTRAINT fk_customers__zip
  FOREIGN KEY (customer_zip_code_prefix)
  REFERENCES geo_zip(geolocation_zip_code_prefix);
ALTER TABLE sellers
  ADD CONSTRAINT fk_sellers__zip
  FOREIGN KEY (seller_zip_code_prefix)
  REFERENCES geo_zip(geolocation_zip_code_prefix);
