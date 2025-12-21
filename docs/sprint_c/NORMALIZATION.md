# Normalization Proof - Olist Database

## Overview

This document demonstrates the **normalization process** applied to the Olist e-commerce database, showing how unnormalized or partially normalized schemas are transformed into **Third Normal Form (3NF)** to eliminate redundancy and anomalies.

---

## Normalization Goals

1. **Eliminate Redundancy:** Avoid storing the same data multiple times
2. **Prevent Update Anomalies:** Ensure updates don't create inconsistencies
3. **Prevent Insertion Anomalies:** Allow inserting data without unnecessary dependencies
4. **Prevent Deletion Anomalies:** Avoid losing information when deleting records

---

## Example: Order Management Schema

### Before Normalization (Unnormalized)

**Scenario:** A hypothetical "flat" table design for order data (common in poorly designed systems or spreadsheets)

**Table: `orders_denormalized`**

| order_id | customer_id | customer_name | customer_city | customer_state | product_id | product_name | product_category | seller_id | seller_city | seller_state | price | freight |
|----------|-------------|---------------|---------------|----------------|------------|--------------|------------------|-----------|-------------|--------------|-------|---------|
| ORD001 | CUST123 | João Silva | São Paulo | SP | PROD456 | Laptop | Electronics | SELL789 | Rio | RJ | 2500.00 | 50.00 |
| ORD001 | CUST123 | João Silva | São Paulo | SP | PROD789 | Mouse | Electronics | SELL789 | Rio | RJ | 30.00 | 10.00 |
| ORD002 | CUST123 | João Silva | São Paulo | SP | PROD456 | Laptop | Electronics | SELL999 | Brasília | DF | 2480.00 | 60.00 |
| ORD003 | CUST456 | Maria Santos | Curitiba | PR | PROD789 | Mouse | Electronics | SELL789 | Rio | RJ | 30.00 | 10.00 |

**Problems:**

1. **Redundancy:**
   - Customer "João Silva" info repeated 3 times (name, city, state)
   - Seller "SELL789" info repeated 3 times
   - Product "Laptop" info repeated 2 times

2. **Update Anomalies:**
   - If João Silva moves to Rio, must update 3 rows
   - If we update only some rows, data becomes inconsistent

3. **Insertion Anomalies:**
   - Cannot add a new customer without an order
   - Cannot add a new product without a sale

4. **Deletion Anomalies:**
   - If we delete ORD003, we lose info about customer CUST456
   - If we delete all orders for a product, product info is lost

---

## Functional Dependencies

Analyzing the denormalized table reveals these **functional dependencies (FDs)**:

### Customer-related FDs
```
customer_id → customer_name
customer_id → customer_city
customer_id → customer_state
```

### Product-related FDs
```
product_id → product_name
product_id → product_category
```

### Seller-related FDs
```
seller_id → seller_city
seller_id → seller_state
```

### Order-related FDs
```
order_id → customer_id
(order_id, product_id) → seller_id
(order_id, product_id) → price
(order_id, product_id) → freight
```

**Key observation:** Many non-key attributes depend on partial keys or transitive dependencies, violating 2NF and 3NF.

---

## Step 1: First Normal Form (1NF)

**Definition:** All attributes must be atomic (no repeating groups or arrays).

**Status:** The denormalized table is already in 1NF (no nested attributes or arrays).

---

## Step 2: Second Normal Form (2NF)

**Definition:** Must be in 1NF **and** all non-key attributes must depend on the **entire** candidate key (no partial dependencies).

**Current candidate key:** `(order_id, product_id)` (composite key)

**Violations detected:**

- `customer_name` depends only on `customer_id`, which depends on `order_id` (transitive)
- `product_name` depends only on `product_id` (partial dependency on composite key)
- `seller_city` depends only on `seller_id` (transitive through order_item)

**Solution:** Decompose into separate tables:

### Table: `orders` (2NF)
| order_id | customer_id |
|----------|-------------|
| ORD001 | CUST123 |
| ORD002 | CUST123 |
| ORD003 | CUST456 |

**FD:** `order_id → customer_id`

### Table: `order_items` (2NF)
| order_id | product_id | seller_id | price | freight |
|----------|------------|-----------|-------|---------|
| ORD001 | PROD456 | SELL789 | 2500.00 | 50.00 |
| ORD001 | PROD789 | SELL789 | 30.00 | 10.00 |
| ORD002 | PROD456 | SELL999 | 2480.00 | 60.00 |
| ORD003 | PROD789 | SELL789 | 30.00 | 10.00 |

**FD:** `(order_id, product_id) → seller_id, price, freight`

### Table: `customers` (2NF)
| customer_id | customer_name | customer_city | customer_state |
|-------------|---------------|---------------|----------------|
| CUST123 | João Silva | São Paulo | SP |
| CUST456 | Maria Santos | Curitiba | PR |

**FD:** `customer_id → customer_name, customer_city, customer_state`

### Table: `products` (2NF)
| product_id | product_name | product_category |
|------------|--------------|------------------|
| PROD456 | Laptop | Electronics |
| PROD789 | Mouse | Electronics |

**FD:** `product_id → product_name, product_category`

### Table: `sellers` (2NF)
| seller_id | seller_city | seller_state |
|-----------|-------------|--------------|
| SELL789 | Rio | RJ |
| SELL999 | Brasília | DF |

**FD:** `seller_id → seller_city, seller_state`

**Result:** All partial dependencies eliminated. Each non-key attribute depends on the **entire** primary key.

---

## Step 3: Third Normal Form (3NF)

**Definition:** Must be in 2NF **and** no non-key attribute depends on another non-key attribute (no transitive dependencies).

**Current status:** Almost 3NF, but one violation remains:

### Violation: Product Categories

In the `products` table:

```
product_id → product_category (direct)
```

However, if we later add category descriptions:

```
product_category → category_description
product_id → product_category → category_description (transitive!)
```

**Solution:** Extract categories into a separate table:

### Table: `products` (3NF)
| product_id | product_name | product_category_name |
|------------|--------------|----------------------|
| PROD456 | Laptop | electronics |
| PROD789 | Mouse | electronics |

**FD:** `product_id → product_name, product_category_name`

### Table: `categories` (3NF)
| product_category_name | product_category_name_english | category_description |
|-----------------------|-------------------------------|---------------------|
| electronics | Electronics | Electronic devices and accessories |
| furniture | Furniture | Home and office furniture |

**FD:** `product_category_name → product_category_name_english, category_description`

**Result:** All transitive dependencies eliminated. Each non-key attribute depends **only** on the primary key.

---

## Final Normalized Schema (3NF)

### 5 Tables in 3NF:

1. **`customers`** (customer_id → customer_name, customer_city, customer_state)
2. **`orders`** (order_id → customer_id, order_status, timestamps)
3. **`order_items`** ((order_id, order_item_id) → product_id, seller_id, price, freight)
4. **`products`** (product_id → product_name, product_category_name, dimensions)
5. **`sellers`** (seller_id → seller_city, seller_state)
6. **`categories`** (product_category_name → product_category_name_english)

### Benefits Achieved:

✅ **No Redundancy:** Customer/product/seller info stored once  
✅ **Update Anomaly Fixed:** Updating João Silva's city requires one row change  
✅ **Insertion Anomaly Fixed:** Can add customers/products without orders  
✅ **Deletion Anomaly Fixed:** Deleting orders doesn't lose customer/product data  

---

## BCNF (Boyce-Codd Normal Form) Analysis

**Definition:** A relation is in BCNF if, for every functional dependency X → Y, X is a superkey.

**Checking our tables:**

### `customers` table
- FDs: `customer_id → {customer_name, customer_city, customer_state}`
- Candidate key: `customer_id`
- **BCNF?** ✅ Yes, because `customer_id` is a superkey

### `order_items` table
- FDs: `(order_id, order_item_id) → {product_id, seller_id, price, freight}`
- Candidate key: `(order_id, order_item_id)`
- **BCNF?** ✅ Yes, because `(order_id, order_item_id)` is a superkey

### `categories` table
- FDs: `product_category_name → product_category_name_english`
- Candidate key: `product_category_name`
- **BCNF?** ✅ Yes, because `product_category_name` is a superkey

**Conclusion:** Our normalized schema is also in **BCNF** (strongest normal form commonly used).

---

## Verification: Actual Olist Schema

The actual Olist database (as implemented in `db/ddl_mysql/000_base.sql`) already follows this normalized design:

```sql
-- Actual DDL (excerpt)
CREATE TABLE customers (
    customer_id VARCHAR(32) PRIMARY KEY,
    customer_unique_id VARCHAR(32),
    customer_zip_code_prefix INT,
    customer_city VARCHAR(50),
    customer_state CHAR(2)
);

CREATE TABLE orders (
    order_id VARCHAR(32) PRIMARY KEY,
    customer_id VARCHAR(32),
    order_status VARCHAR(20),
    order_purchase_timestamp DATETIME,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

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

**Result:** Database is in **3NF/BCNF** with proper foreign key constraints.

---

## Trade-offs and Denormalization Considerations

### When to Denormalize (Not Done Here):

1. **Read-heavy workloads:** If queries require many joins, denormalization can improve performance
2. **Analytics/Reporting:** Materialized views or fact tables for OLAP
3. **Caching layers:** Precompute aggregates (e.g., total revenue per category)

### Why We Stay Normalized:

✅ **Data Integrity:** FKs enforce referential integrity  
✅ **Update Efficiency:** Customer changes affect one row  
✅ **Storage Efficiency:** No redundant data (100K+ orders)  
✅ **Flexibility:** Easy to add new attributes without schema changes  

---

## Summary

| Normal Form | Violations Eliminated | Key Benefit |
|-------------|---------------------|-------------|
| **1NF** | Repeating groups, multi-valued attributes | Atomic values only |
| **2NF** | Partial dependencies | Non-key attributes depend on entire key |
| **3NF** | Transitive dependencies | Non-key attributes depend only on key |
| **BCNF** | Non-superkey determinants | Every determinant is a superkey |

**Olist Database Status:** ✅ **3NF/BCNF** with 9 normalized tables and proper foreign key constraints.

---

## Next Steps

1. ✅ Normalization to 3NF complete
2. ➡️ Add indexes for performance (`PERFORMANCE.md`)
3. ➡️ Add constraints for data integrity (`sprint_c_constraints_indexes.sql`)
4. ➡️ Test query performance with EXPLAIN (`explain_analytics.ps1`)

---

## References

- BLG212E Lecture Notes: Normalization Theory
- Database Design and Relational Theory (C.J. Date)
- Functional dependencies identified from Olist dataset schema
