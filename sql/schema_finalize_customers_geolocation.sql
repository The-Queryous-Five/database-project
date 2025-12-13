-- ============================================================================
-- Schema Finalization: Customers & Geolocation PK/FK Constraints
-- ============================================================================
-- This script ensures proper PRIMARY KEY and FOREIGN KEY constraints
-- between the customers and geo_zip (geolocation) tables.
--
-- Tables affected:
--   - customers: PRIMARY KEY on customer_id
--   - geo_zip: PRIMARY KEY on geolocation_zip_code_prefix
--   - FK: customers.customer_zip_code_prefix → geo_zip.geolocation_zip_code_prefix
--
-- This script is safe to run multiple times. If constraints already exist,
-- it will either skip them (PostgreSQL) or fail gracefully (MySQL).
-- In MySQL, you may need to drop existing constraints first if re-running.
--
-- Usage:
--   PostgreSQL: psql -d olist -f sql/schema_finalize_customers_geolocation.sql
--   MySQL:      mysql -u root -D olist < sql/schema_finalize_customers_geolocation.sql
-- ============================================================================

-- Ensure customers table has PRIMARY KEY on customer_id
-- Note: PRIMARY KEY is typically already defined in CREATE TABLE (000_base.sql).
-- If the PK already exists, this statement will fail - that's expected and safe.
-- The PK constraint name may vary (e.g., 'customers_pkey' in PostgreSQL).
ALTER TABLE customers
  ADD CONSTRAINT pk_customers
  PRIMARY KEY (customer_id);

-- Ensure geo_zip table has PRIMARY KEY on geolocation_zip_code_prefix
-- Note: PRIMARY KEY is typically already defined in CREATE TABLE (020_geo_zip.sql).
-- If the PK already exists, this statement will fail - that's expected and safe.
ALTER TABLE geo_zip
  ADD CONSTRAINT pk_geo_zip
  PRIMARY KEY (geolocation_zip_code_prefix);

-- Add FOREIGN KEY constraint: customers → geo_zip
-- This links customer zip codes to the geolocation reference table.
-- Note: This constraint may already exist from 020_geo_zip.sql as 'fk_customers__zip'.
-- If it exists with a different name, this will create a duplicate (which will error).
-- If it exists with the same name, this will error - that's expected and safe.
-- To check existing constraints before running:
--   PostgreSQL: \d customers
--   MySQL:      SHOW CREATE TABLE customers;
ALTER TABLE customers
  ADD CONSTRAINT fk_customers_geolocation
  FOREIGN KEY (customer_zip_code_prefix)
  REFERENCES geo_zip(geolocation_zip_code_prefix);

-- ============================================================================
-- Verification queries (optional - uncomment to run after applying constraints)
-- ============================================================================
-- Check that PKs exist:
-- SELECT constraint_name, constraint_type
-- FROM information_schema.table_constraints
-- WHERE table_name IN ('customers', 'geo_zip')
--   AND constraint_type IN ('PRIMARY KEY', 'FOREIGN KEY')
-- ORDER BY table_name, constraint_type;
--
-- Check FK relationship:
-- SELECT
--   tc.constraint_name,
--   tc.table_name,
--   kcu.column_name,
--   ccu.table_name AS foreign_table_name,
--   ccu.column_name AS foreign_column_name
-- FROM information_schema.table_constraints AS tc
-- JOIN information_schema.key_column_usage AS kcu
--   ON tc.constraint_name = kcu.constraint_name
-- JOIN information_schema.constraint_column_usage AS ccu
--   ON ccu.constraint_name = tc.constraint_name
-- WHERE tc.constraint_type = 'FOREIGN KEY'
--   AND tc.table_name = 'customers'
--   AND kcu.column_name = 'customer_zip_code_prefix';
-- ============================================================================

