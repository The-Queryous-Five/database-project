# ER to Relational Mapping - Olist Database

## Overview

This document explains how the ER diagram entities and relationships from `ER_DIAGRAM_GUIDE.md` were mapped to the relational database schema implemented in `db/ddl_mysql/`.

---

## Mapping Rules Applied

### Rule 1: Entity Sets → Tables

Each **strong entity** becomes a table with attributes as columns.

| ER Entity | Table Name | Primary Key |
|-----------|-----------|-------------|
| Customers | `customers` | `customer_id` |
| Products | `products` | `product_id` |
| Sellers | `sellers` | `seller_id` |
| Categories | `categories` | `product_category_name` |
| Orders | `orders` | `order_id` |
| Order_Reviews | `order_reviews` | `review_id` |
| Geolocation | `geolocation` | `geolocation_zip_code_prefix` |

**Example:**

```sql
CREATE TABLE customers (
    customer_id VARCHAR(32) PRIMARY KEY,
    customer_unique_id VARCHAR(32),
    customer_zip_code_prefix INT,
    customer_city VARCHAR(50),
    customer_state CHAR(2)
);
```

---

### Rule 2: Weak Entity Sets → Tables with Composite Keys

**Weak entities** depend on a strong entity for identification. They become tables with:
- A **composite primary key** (own discriminator + foreign key from owner entity)
- Foreign key constraint to owner

| Weak Entity | Table Name | Primary Key | Owner Entity |
|-------------|-----------|-------------|--------------|
| Order_Items | `order_items` | `(order_id, order_item_id)` | Orders |
| Order_Payments | `order_payments` | `(order_id, payment_sequential)` | Orders |

**Example:**

```sql
CREATE TABLE order_items (
    order_id VARCHAR(32),
    order_item_id INT,
    product_id VARCHAR(32),
    seller_id VARCHAR(32),
    price DECIMAL(10, 2),
    freight_value DECIMAL(10, 2),
    
    PRIMARY KEY (order_id, order_item_id),
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id),
    FOREIGN KEY (seller_id) REFERENCES sellers(seller_id)
);
```

**Why composite key?**
- `order_item_id` alone is not unique (resets per order: 1, 2, 3...)
- `(order_id, order_item_id)` together uniquely identify each item

---

### Rule 3: 1:N Relationships → Foreign Key in "N" Side

**One-to-Many** relationships are implemented by adding a foreign key in the "many" side table.

| Relationship | "1" Side | "N" Side | FK Column | Notes |
|--------------|---------|---------|-----------|-------|
| Customer PLACES Order | Customers | Orders | `customer_id` | One customer → many orders |
| Product APPEARS_IN Order_Items | Products | Order_Items | `product_id` | One product → many order items |
| Seller SELLS Order_Items | Sellers | Order_Items | `seller_id` | One seller → many items sold |
| Category HAS Products | Categories | Products | `product_category_name` | One category → many products |
| Order HAS Payments | Orders | Order_Payments | `order_id` | One order → many payments (installments) |

**Example (Orders table):**

```sql
CREATE TABLE orders (
    order_id VARCHAR(32) PRIMARY KEY,
    customer_id VARCHAR(32),
    order_status VARCHAR(20),
    order_purchase_timestamp DATETIME,
    
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);
```

---

### Rule 4: 1:1 Relationships → FK in Either Table (or Merge)

**One-to-One** relationships can be implemented by:
1. Adding FK in either table
2. Merging entities if participation is total on both sides

| Relationship | Implementation | Notes |
|--------------|---------------|-------|
| Order RECEIVES Review | FK in `order_reviews` table | `order_id` references `orders(order_id)` |

```sql
CREATE TABLE order_reviews (
    review_id VARCHAR(32) PRIMARY KEY,
    order_id VARCHAR(32) UNIQUE,  -- UNIQUE enforces 1:1
    review_score INT,
    review_comment_title VARCHAR(255),
    
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
);
```

**Why FK in reviews?**
- Participation: Orders (partial) ← Reviews (total)
- Not all orders have reviews, but every review must have an order
- FK in reviews table avoids NULL values

---

### Rule 5: M:N Relationships → Junction Table

**Many-to-Many** relationships require a **junction table** (also called associative entity).

| Relationship | Junction Table | Columns | Composite PK |
|--------------|---------------|---------|--------------|
| Orders ↔ Products (with Sellers) | `order_items` | `order_id`, `product_id`, `seller_id`, `price`, `freight_value` | `(order_id, order_item_id)` |

**Why order_items is M:N:**
- One order can contain many products
- One product can appear in many orders
- **Additional complexity:** Each order item also references a seller (3-way relationship)

```sql
CREATE TABLE order_items (
    order_id VARCHAR(32),
    order_item_id INT,
    product_id VARCHAR(32),
    seller_id VARCHAR(32),
    price DECIMAL(10, 2),
    freight_value DECIMAL(10, 2),
    
    PRIMARY KEY (order_id, order_item_id),
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id),
    FOREIGN KEY (seller_id) REFERENCES sellers(seller_id)
);
```

---

## Complete Mapping Table

| ER Element | Type | Relational Schema | Key Constraints |
|------------|------|------------------|----------------|
| **Customers** | Strong Entity | `customers(customer_id, ...)` | PK: `customer_id` |
| **Orders** | Strong Entity | `orders(order_id, customer_id, ...)` | PK: `order_id`<br>FK: `customer_id` → `customers` |
| **Order_Items** | Weak Entity | `order_items(order_id, order_item_id, product_id, seller_id, ...)` | PK: `(order_id, order_item_id)`<br>FK: `order_id` → `orders`<br>FK: `product_id` → `products`<br>FK: `seller_id` → `sellers` |
| **Products** | Strong Entity | `products(product_id, product_category_name, ...)` | PK: `product_id`<br>FK: `product_category_name` → `categories` |
| **Sellers** | Strong Entity | `sellers(seller_id, ...)` | PK: `seller_id` |
| **Order_Payments** | Weak Entity | `order_payments(order_id, payment_sequential, ...)` | PK: `(order_id, payment_sequential)`<br>FK: `order_id` → `orders` |
| **Order_Reviews** | Strong Entity | `order_reviews(review_id, order_id, ...)` | PK: `review_id`<br>FK: `order_id` → `orders`<br>UNIQUE: `order_id` (1:1) |
| **Categories** | Strong Entity | `categories(product_category_name, ...)` | PK: `product_category_name` |
| **Geolocation** | Strong Entity | `geolocation(geolocation_zip_code_prefix, ...)` | PK: `geolocation_zip_code_prefix` |

---

## Special Cases

### 1. Three-Way Relationship (Order_Items)

The `order_items` table represents a **ternary relationship**:
- Orders ↔ Products ↔ Sellers

This is because:
- An order contains products
- Products are sold by sellers
- The same product can be sold by different sellers in different orders

**Mapped as:** Junction table with 3 foreign keys

---

### 2. Multi-Valued Attributes (Not Present)

If we had multi-valued attributes (e.g., "product tags"), they would become a separate table:

```sql
-- Hypothetical example (not in actual schema)
CREATE TABLE product_tags (
    product_id VARCHAR(32),
    tag VARCHAR(50),
    PRIMARY KEY (product_id, tag),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);
```

---

### 3. Composite Attributes

Composite attributes are **flattened** into individual columns.

**Example: Customer location (composite attribute in ER)**

```
Customer_Location
├── zip_code_prefix
├── city
└── state
```

**Mapped as separate columns in `customers` table:**

```sql
CREATE TABLE customers (
    customer_id VARCHAR(32) PRIMARY KEY,
    customer_zip_code_prefix INT,   -- component 1
    customer_city VARCHAR(50),       -- component 2
    customer_state CHAR(2)           -- component 3
);
```

---

## Referential Integrity Constraints

All foreign keys should have **referential integrity constraints** to maintain data consistency:

```sql
-- Example: Enforce that every order belongs to an existing customer
ALTER TABLE orders
ADD CONSTRAINT fk_orders_customer
FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
ON DELETE RESTRICT
ON UPDATE CASCADE;
```

**Current Status:**
- Base tables (000_base.sql): Tables created **without FKs** for ETL flexibility
- FK constraints: Added in `030_fk_v2_1.sql` **after** data is loaded
- Sprint C constraints: Optional strict FKs in `sprint_c_constraints_indexes.sql`

---

## Indexes for Performance

Foreign key columns and frequently queried attributes should have indexes (covered in `PERFORMANCE.md`):

```sql
-- Example indexes (Sprint C)
CREATE INDEX idx_orders_customer ON orders(customer_id);
CREATE INDEX idx_order_items_order ON order_items(order_id);
CREATE INDEX idx_order_items_product ON order_items(product_id);
```

---

## Verification

To verify the relational schema matches the ER model:

1. **Check table structure:**
   ```sql
   DESCRIBE customers;
   DESCRIBE orders;
   DESCRIBE order_items;
   ```

2. **Verify foreign keys:**
   ```sql
   SELECT 
       TABLE_NAME,
       COLUMN_NAME,
       REFERENCED_TABLE_NAME,
       REFERENCED_COLUMN_NAME
   FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
   WHERE TABLE_SCHEMA = 'olist'
     AND REFERENCED_TABLE_NAME IS NOT NULL;
   ```

3. **Test referential integrity:**
   ```sql
   -- Try to insert order with non-existent customer (should fail)
   INSERT INTO orders (order_id, customer_id, order_status)
   VALUES ('test123', 'invalid_customer_id', 'delivered');
   -- Expected: Foreign key constraint violation
   ```

---

## Summary

**Mapping Pattern Used:**

| ER Pattern | Relational Implementation |
|------------|--------------------------|
| Strong Entity | → Table with PK |
| Weak Entity | → Table with composite PK (own key + FK) |
| 1:N Relationship | → FK in "N" side table |
| 1:1 Relationship | → FK in one table (or merge) |
| M:N Relationship | → Junction table with 2+ FKs |
| Composite Attribute | → Multiple columns |
| Multi-Valued Attribute | → Separate table |

**Result:** 9 tables with proper primary keys, foreign keys, and indexes for the Olist e-commerce database.

---

## Next Steps

1. ✅ ER model defined (`ER_DIAGRAM_GUIDE.md`)
2. ✅ Relational mapping complete (this document)
3. ➡️ Normalization analysis (`NORMALIZATION.md`)
4. ➡️ Performance optimization (`PERFORMANCE.md`)
