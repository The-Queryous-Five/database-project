# Dataset Description - Olist Brazilian E-Commerce

---

## Source

**Name:** Olist Brazilian E-Commerce Public Dataset  
**Provider:** Olist Store (Brazilian marketplace platform)  
**Coverage:** 2016-2018 (approximately 2 years)  
**License:** Public domain (CC0)

**Original Source:**  
Kaggle: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

---

## Dataset Overview

Real commercial data from 100,000+ orders across multiple product categories, sellers, and customer locations in Brazil.

### Raw CSV Files (data/raw/)

| File Name | Description | Key Columns |
|-----------|-------------|-------------|
| `olist_customers_dataset.csv` | Customer information | customer_id, customer_unique_id, city, state, zip_code_prefix |
| `olist_orders_dataset.csv` | Order metadata and status | order_id, customer_id, order_status, timestamps |
| `olist_order_items_dataset.csv` | Items in each order | order_id, product_id, seller_id, price, freight_value |
| `olist_products_dataset.csv` | Product catalog | product_id, category_name, dimensions, weight |
| `olist_sellers_dataset.csv` | Seller profiles | seller_id, city, state, zip_code_prefix |
| `olist_order_payments_dataset.csv` | Payment transactions | order_id, payment_type, payment_value, installments |
| `olist_order_reviews_dataset.csv` | Customer reviews | review_id, order_id, review_score, review_comment |
| `olist_geolocation_dataset.csv` | Zip code geolocation | zip_code_prefix, lat, lng, city, state |
| `product_category_name_translation.csv` | Category translations (PT→EN) | category_name_pt, category_name_en |

---

## Database Size (Approximate Row Counts)

**Note:** Exact counts may vary based on ETL filtering. To compute exact counts:

```sql
-- Run in MySQL after ETL completes
SELECT 'customers' AS table_name, COUNT(*) AS row_count FROM customers
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
SELECT 'categories', COUNT(*) FROM categories
UNION ALL
SELECT 'geolocation', COUNT(*) FROM geolocation;
```

### Typical Row Counts (Post-ETL)

| Table | Approximate Rows | Notes |
|-------|-----------------|-------|
| `customers` | 99,441 | Unique customer identifiers |
| `orders` | 99,441 | One-to-one with customers (in this dataset) |
| `order_items` | 112,650 | Multiple items per order (avg ~1.13) |
| `products` | 32,951 | Product catalog |
| `sellers` | 3,095 | Seller profiles |
| `order_payments` | ~103,000 | Multiple payments per order possible |
| `order_reviews` | ~99,000 | Not all orders have reviews |
| `categories` | 71 | Product categories (translated to English) |
| `geolocation` | 1,000,000+ | Zip code geolocation data (very large) |

**Total Data Volume:** ~1.4M rows across 9 tables

---

## Data Characteristics

### Order Statuses
- `delivered` (majority)
- `canceled`
- `shipped`
- `processing`
- `unavailable`
- `invoiced`
- `approved`
- `created`

### Product Categories (Top 10)
1. bed_bath_table
2. health_beauty
3. sports_leisure
4. furniture_decor
5. computers_accessories
6. housewares
7. watches_gifts
8. telephony
9. garden_tools
10. auto

### Payment Types
- `credit_card` (most common)
- `boleto` (Brazilian payment method)
- `voucher`
- `debit_card`

### Review Scores
- Scale: 1-5 stars
- Distribution: Majority 4-5 stars
- ~10% missing reviews

### Geographic Coverage
- **States:** All 27 Brazilian states
- **Cities:** 4,000+ municipalities
- **Concentration:** São Paulo (SP) and Rio de Janeiro (RJ) dominate

---

## ETL Pipeline

### Script Execution Order (db/etl/)

The ETL scripts must run in this dependency order:

```bash
1. etl_categories.py         # Load category translations first
2. etl_customers.py           # Load customer profiles
3. etl_products.py            # Load products (requires categories)
4. etl_sellers.py             # Load seller profiles
5. etl_orders.py              # Load orders (requires customers)
6. etl_order_items.py         # Load order items (requires orders, products, sellers)
7. etl_order_payments.py      # Load payments (requires orders)
8. etl_order_reviews.py       # Load reviews (requires orders)
9. etl_geolocation.py         # Load geolocation (can run anytime)
```

**Automated:** Run `scripts\run_etl_all.ps1` to execute all in order.

### Data Cleaning & Assumptions

**1. Missing Values:**
- **product_category_name:** NULL values mapped to "Unknown" category
- **review_comment_message:** NULL accepted (optional field)
- **delivery dates:** NULL accepted for non-delivered orders

**2. Data Type Conversions:**
- **Timestamps:** ISO 8601 strings → MySQL DATETIME
- **Prices:** Decimal(10,2) for monetary values
- **IDs:** VARCHAR(32) for hash-based identifiers

**3. Foreign Key Handling:**
- FK constraints NOT enforced during ETL (for flexibility)
- Optional FK constraints provided in `sprint_c_constraints_indexes.sql`
- Referential integrity validated in ETL scripts before insertion

**4. Duplicate Handling:**
- **Products:** Duplicates by product_id removed (keep first occurrence)
- **Reviews:** Multiple reviews per order allowed (one-to-many)
- **Payments:** Multiple payments per order allowed (installment plans)

**5. Outliers:**
- **Prices:** No upper limit enforced (real marketplace data)
- **Delivery times:** Negative or extreme values kept (data quality issue in source)

---

## Data Quality Issues (Known)

### From Original Kaggle Dataset

1. **Missing delivery dates:** ~3% of "delivered" orders have NULL `order_delivered_customer_date`
2. **Future timestamps:** Some timestamps in future (data collection artifact)
3. **Incomplete reviews:** ~10% of orders missing reviews
4. **Geolocation duplicates:** Multiple lat/lng per zip code (we keep all)
5. **Product dimensions:** Some products have 0 or NULL dimensions

**Impact on Analytics:**
- Queries filter by `order_status = 'delivered'` AND `order_delivered_customer_date IS NOT NULL`
- Review analysis uses `LEFT JOIN` to handle missing reviews
- Geolocation used for lookup only, not aggregation

---

## Schema Design

### ER Model
See [docs/sprint_c/ER_DIAGRAM_GUIDE.md](../sprint_c/ER_DIAGRAM_GUIDE.md) for complete ER diagram.

**Key Relationships:**
- customers **1:N** orders (one customer, many orders)
- orders **1:N** order_items (one order, many items) → weak entity
- products **1:N** order_items (one product, many purchases)
- sellers **1:N** order_items (one seller, many sales)
- orders **1:N** order_payments (one order, multiple payment installments)
- orders **1:1** order_reviews (one order, one review - optional)

### Normalization
All tables in **3NF/BCNF**. See [docs/sprint_c/NORMALIZATION.md](../sprint_c/NORMALIZATION.md) for proof.

---

## Usage Examples

### Count Rows in All Tables

```sql
SELECT 
    table_name, 
    table_rows 
FROM information_schema.tables 
WHERE table_schema = 'olist' 
ORDER BY table_rows DESC;
```

### Check Data Load Success

```bash
# PowerShell
.\scripts\check-health.ps1
```

### Inspect Sample Data

```sql
-- Recent delivered orders
SELECT * FROM orders 
WHERE order_status = 'delivered' 
ORDER BY order_purchase_timestamp DESC 
LIMIT 10;

-- Top product categories
SELECT 
    c.category_name_english,
    COUNT(*) as product_count
FROM products p
LEFT JOIN categories c ON p.product_category_name = c.category_name_portuguese
GROUP BY c.category_name_english
ORDER BY product_count DESC
LIMIT 10;
```

---

## Dataset Limitations

1. **Time range:** 2016-2018 only (not current)
2. **Geography:** Brazil only (not international)
3. **Anonymization:** Customer/seller names removed (privacy)
4. **Marketplace bias:** Olist platform only (not representative of all e-commerce)

---

## References

- **Original Kaggle Page:** https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce
- **Olist Company:** https://olist.com/
- **Dataset Documentation:** See Kaggle dataset description for column definitions

---

**For ETL implementation details, see `/db/etl/` folder.**  
**For schema details, see `/db/ddl_mysql/` folder.**
