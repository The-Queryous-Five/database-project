# Complex Query Analysis

---

## Overview

This document details the **SQL complexity** of key queries, aligned with BLG212E rubric requirements for "complex queries" (multi-table JOINs, aggregations, subqueries, etc.).

---

## Analytics Queries (Sprint B)

### 1. Revenue by Category

**Endpoint:** `GET /analytics/revenue-by-category?limit=10`

**SQL Query:**
```sql
SELECT
    COALESCE(p.product_category_name, 'Unknown') AS category_name,
    COUNT(*) AS items_sold,
    COUNT(DISTINCT oi.order_id) AS distinct_orders,
    ROUND(SUM(oi.price + oi.freight_value), 2) AS total_revenue,
    ROUND(AVG(oi.price), 2) AS avg_item_price
FROM order_items oi
JOIN products p ON p.product_id = oi.product_id
JOIN orders o ON o.order_id = oi.order_id
WHERE o.order_status = 'delivered'
GROUP BY p.product_category_name
ORDER BY total_revenue DESC
LIMIT 10;
```

**Complexity Analysis:**

| SQL Feature | Usage | Explanation |
|-------------|-------|-------------|
| **Multi-table JOIN** | 3 tables (order_items, products, orders) | Combines transactional data with catalog metadata |
| **Aggregate Functions** | COUNT(), COUNT(DISTINCT), SUM(), AVG() | Multiple aggregations per group |
| **GROUP BY** | By category | Aggregates data per product category |
| **COALESCE** | Handles NULL categories | Maps missing categories to "Unknown" |
| **Arithmetic** | price + freight_value | Calculates total item revenue |
| **Filtering** | WHERE order_status = 'delivered' | Only includes completed orders |
| **Ordering** | ORDER BY total_revenue DESC | Ranks categories by revenue |

**Why Complex:**
- Joins 3 normalized tables
- 5 aggregate functions (2 distinct counts)
- NULL handling with COALESCE
- Arithmetic expressions in aggregation

**Screenshot Target:**  
Frontend → Analytics → Revenue by Category table

**Index Usage:**  
- `idx_order_items_product` (on order_items.product_id)
- `idx_order_items_order` (on order_items.order_id)
- `idx_orders_status` (on orders.order_status)

---

### 2. Top Sellers

**Endpoint:** `GET /analytics/top-sellers?limit=10`

**SQL Query:**
```sql
SELECT
    s.seller_id,
    s.seller_city,
    s.seller_state,
    COUNT(DISTINCT oi.order_id) AS order_count,
    COUNT(*) AS items_sold,
    ROUND(SUM(oi.price + oi.freight_value), 2) AS total_revenue,
    ROUND(AVG(oi.price), 2) AS avg_item_price
FROM order_items oi
JOIN sellers s ON s.seller_id = oi.seller_id
JOIN orders o ON o.order_id = oi.order_id
WHERE o.order_status = 'delivered'
GROUP BY s.seller_id, s.seller_city, s.seller_state
ORDER BY total_revenue DESC
LIMIT 10;
```

**Complexity Analysis:**

| SQL Feature | Usage | Explanation |
|-------------|-------|-------------|
| **Multi-table JOIN** | 3 tables (order_items, sellers, orders) | Links sales to seller profiles |
| **Aggregate Functions** | COUNT(DISTINCT), COUNT(), SUM(), AVG() | 4 different aggregations |
| **Multi-column GROUP BY** | seller_id, city, state | Groups by composite key |
| **Arithmetic** | price + freight_value | Total item revenue calculation |
| **Filtering** | WHERE order_status = 'delivered' | Excludes canceled/pending orders |
| **Ordering** | ORDER BY total_revenue DESC | Ranks sellers by performance |

**Why Complex:**
- 3-table JOIN across transaction and dimension tables
- Multi-column grouping (seller attributes)
- Multiple aggregate functions with distinct counts
- Business logic (only delivered orders)

**Screenshot Target:**  
Frontend → Analytics → Top Sellers table

**Index Usage:**  
- `idx_order_items_seller` (on order_items.seller_id)
- `idx_order_items_order` (on order_items.order_id)
- `idx_orders_status` (on orders.order_status)

---

### 3. Review Score vs Delivery Time

**Endpoint:** `GET /analytics/review-vs-delivery?min_reviews=50&limit=20`

**SQL Query:**
```sql
SELECT
    s.seller_id,
    s.seller_city,
    s.seller_state,
    COUNT(DISTINCT r.review_id) AS review_count,
    ROUND(AVG(r.review_score), 2) AS avg_review_score,
    ROUND(AVG(TIMESTAMPDIFF(DAY, o.order_purchase_timestamp, o.order_delivered_customer_date)), 1) AS avg_delivery_days
FROM order_items oi
JOIN sellers s ON s.seller_id = oi.seller_id
JOIN orders o ON o.order_id = oi.order_id
LEFT JOIN order_reviews r ON r.order_id = o.order_id
WHERE o.order_status = 'delivered'
  AND o.order_delivered_customer_date IS NOT NULL
GROUP BY s.seller_id, s.seller_city, s.seller_state
HAVING COUNT(DISTINCT r.review_id) >= 50
ORDER BY avg_review_score DESC, avg_delivery_days ASC
LIMIT 20;
```

**Complexity Analysis:**

| SQL Feature | Usage | Explanation |
|-------------|-------|-------------|
| **Multi-table JOIN** | 4 tables (order_items, sellers, orders, order_reviews) | Most complex join in project |
| **LEFT JOIN** | For optional reviews | Not all orders have reviews |
| **TIMESTAMPDIFF** | Date arithmetic | Calculates delivery time in days |
| **Aggregate Functions** | COUNT(DISTINCT), AVG() | Aggregates reviews and delivery times |
| **Multi-column GROUP BY** | seller_id, city, state | Groups by seller attributes |
| **HAVING Clause** | Filters aggregated results | Only sellers with 50+ reviews |
| **Multiple Filters** | WHERE + HAVING | Pre-aggregation and post-aggregation filtering |
| **Multi-column ORDER BY** | By score DESC, days ASC | Ranks by quality and speed |

**Why Complex:**
- **4-table JOIN** (maximum in project)
- **LEFT JOIN** handling (preserves sellers without reviews)
- **Date arithmetic** with TIMESTAMPDIFF
- **HAVING clause** (post-aggregation filter)
- **Multiple ORDER BY** columns with different directions
- **NULL handling** (order_delivered_customer_date)

**Screenshot Target:**  
Frontend → Analytics → Review vs Delivery table

**Index Usage:**  
- `idx_order_items_seller` (on order_items.seller_id)
- `idx_order_items_order` (on order_items.order_id)
- `idx_orders_status` (on orders.order_status)
- `idx_order_reviews_order` (on order_reviews.order_id)

**Performance Impact:**  
Without indexes: ~2.5s  
With indexes: **~120ms** (21x speedup)

---

### 4. Order Funnel

**Endpoint:** `GET /analytics/order-funnel`

**SQL Query:**
```sql
SELECT
    order_status,
    COUNT(*) AS order_count,
    ROUND(AVG(TIMESTAMPDIFF(DAY, order_purchase_timestamp, order_delivered_customer_date)), 1) AS avg_delivery_days,
    ROUND(AVG(TIMESTAMPDIFF(DAY, order_purchase_timestamp, order_approved_at)), 1) AS avg_approval_days
FROM orders
GROUP BY order_status
ORDER BY order_count DESC;
```

**Complexity Analysis:**

| SQL Feature | Usage | Explanation |
|-------------|-------|-------------|
| **Aggregate Functions** | COUNT(), AVG() | Counts and averages per status |
| **TIMESTAMPDIFF** | Date arithmetic (2 instances) | Calculates delivery and approval times |
| **GROUP BY** | By order_status | Aggregates by order lifecycle stage |
| **Multiple Calculations** | 2 different time differences | Tracks approval and delivery timelines |
| **Ordering** | ORDER BY order_count DESC | Shows funnel from largest to smallest |

**Why Complex:**
- Multiple date arithmetic operations
- 2 separate TIMESTAMPDIFF calculations
- Handles NULL timestamps gracefully (AVG ignores NULLs)
- Business logic (funnel analysis)

**Screenshot Target:**  
Frontend → Analytics → Order Funnel table

**Index Usage:**  
- `idx_orders_status` (on orders.order_status)

**Performance Impact:**  
Without index: ~450ms  
With index: **~45ms** (10x speedup)

---

## Non-Analytics Complex Queries

### 5. Top Cities by Customer Count

**Endpoint:** `GET /customers/top-cities?limit=10`

**SQL Query:**
```sql
SELECT
    customer_city,
    customer_state,
    COUNT(*) AS customer_count
FROM customers
GROUP BY customer_city, customer_state
ORDER BY customer_count DESC
LIMIT 10;
```

**Complexity Analysis:**

| SQL Feature | Usage | Explanation |
|-------------|-------|-------------|
| **Aggregate Functions** | COUNT() | Counts customers per city |
| **Multi-column GROUP BY** | city, state | Groups by composite geographic key |
| **Ordering** | ORDER BY customer_count DESC | Ranks cities by size |

**Why Complex:**
- Multi-column grouping
- Large cardinality (4000+ cities)

---

### 6. Payment Statistics

**Endpoint:** `GET /payments/stats`

**SQL Query:**
```sql
SELECT
    payment_type,
    COUNT(*) AS count,
    ROUND(SUM(payment_value), 2) AS total_value
FROM order_payments
GROUP BY payment_type
ORDER BY total_value DESC;
```

**Complexity Analysis:**

| SQL Feature | Usage | Explanation |
|-------------|-------|-------------|
| **Aggregate Functions** | COUNT(), SUM() | Counts and totals per type |
| **GROUP BY** | By payment_type | Aggregates by payment method |
| **Ordering** | ORDER BY total_value DESC | Ranks by total value |

**Why Complex:**
- Multiple aggregations
- Financial calculations (currency precision)

---

### 7. Review Score Distribution

**Endpoint:** `GET /reviews/stats`

**SQL Query:**
```sql
-- Overall stats
SELECT
    COUNT(*) AS total_reviews,
    ROUND(AVG(review_score), 2) AS average_score
FROM order_reviews;

-- Score distribution
SELECT
    review_score,
    COUNT(*) AS count
FROM order_reviews
GROUP BY review_score
ORDER BY review_score;
```

**Complexity Analysis:**

| SQL Feature | Usage | Explanation |
|-------------|-------|-------------|
| **Multiple Queries** | 2 separate queries | One for totals, one for distribution |
| **Aggregate Functions** | COUNT(), AVG() | Statistical analysis |
| **GROUP BY** | By review_score | Histogram data |

**Why Complex:**
- Statistical analysis (average, distribution)
- Two-query pattern for comprehensive stats

---

## Complexity Summary Table

| Query | Tables | JOINs | Aggregates | TIMESTAMPDIFF | HAVING | LEFT JOIN | Complexity Score |
|-------|--------|-------|------------|---------------|--------|-----------|------------------|
| Revenue by Category | 3 | 2 | 5 | ❌ | ❌ | ❌ | ★★★☆☆ |
| Top Sellers | 3 | 2 | 4 | ❌ | ❌ | ❌ | ★★★☆☆ |
| Review vs Delivery | 4 | 3 | 3 | ✅ | ✅ | ✅ | ★★★★★ |
| Order Funnel | 1 | 0 | 3 | ✅✅ | ❌ | ❌ | ★★★☆☆ |
| Top Cities | 1 | 0 | 1 | ❌ | ❌ | ❌ | ★★☆☆☆ |
| Payment Stats | 1 | 0 | 2 | ❌ | ❌ | ❌ | ★★☆☆☆ |
| Review Distribution | 1 | 0 | 2 | ❌ | ❌ | ❌ | ★★☆☆☆ |

**Most Complex:** Review vs Delivery (4 tables, LEFT JOIN, TIMESTAMPDIFF, HAVING)

---

## SQL Concepts Demonstrated

### Core SQL
- ✅ SELECT, FROM, WHERE
- ✅ JOIN (INNER and LEFT)
- ✅ GROUP BY (single and multi-column)
- ✅ HAVING (post-aggregation filtering)
- ✅ ORDER BY (single and multi-column)

### Aggregate Functions
- ✅ COUNT()
- ✅ COUNT(DISTINCT)
- ✅ SUM()
- ✅ AVG()
- ✅ ROUND()

### Advanced Features
- ✅ COALESCE (NULL handling)
- ✅ TIMESTAMPDIFF (date arithmetic)
- ✅ LEFT JOIN (optional relationships)
- ✅ Multi-table JOINs (up to 4 tables)
- ✅ Arithmetic expressions in SELECT

### Query Optimization
- ✅ Index design (8 indexes)
- ✅ EXPLAIN analysis
- ✅ Query rewriting for performance

---

## Mapping to UI

| Query | UI Location | Screenshot Importance |
|-------|-------------|----------------------|
| Revenue by Category | Analytics → Revenue Card | **High** (shows multi-table JOIN) |
| Top Sellers | Analytics → Sellers Card | **High** (shows seller analysis) |
| Review vs Delivery | Analytics → Reviews Card | **Critical** (most complex query) |
| Order Funnel | Analytics → Funnel Card | **High** (shows TIMESTAMPDIFF) |
| Top Cities | Customers → Top Cities Table | Medium |
| Payment Stats | Payments → Stats Table | Medium |
| Review Distribution | Reviews → Stats Chart | Medium |

---

## Testing Coverage

All complex queries have **pytest tests** in `tests/test_analytics.py`:

- **Limit validation:** Tests that limit parameter works
- **Schema validation:** Verifies response structure
- **Error handling:** Tests database failure scenarios
- **Edge cases:** Empty results, NULL handling

**Run tests:**
```powershell
.\venv\Scripts\python.exe -m pytest tests/test_analytics.py -v
```

---

## Performance Benchmarks

See [docs/sprint_c/PERFORMANCE.md](../sprint_c/PERFORMANCE.md) for detailed EXPLAIN analysis and benchmark results.

**Summary:**
- Revenue by Category: **12x speedup** with indexes
- Top Sellers: **15x speedup** with indexes
- Review vs Delivery: **21x speedup** with indexes (most impact)
- Order Funnel: **10x speedup** with indexes

**Total Index Overhead:** ~20 MB (~11% of data size)

---

## For Presentation

### Slide Recommendations

1. **Slide 1: Query Complexity Overview**
   - Show complexity summary table
   - Highlight 4-table JOIN (Review vs Delivery)

2. **Slide 2: SQL Techniques**
   - List SQL concepts demonstrated
   - Code snippet of most complex query

3. **Slide 3: Performance Impact**
   - Before/after index benchmarks
   - EXPLAIN output comparison

4. **Screenshot Priority**
   - **Must have:** All 4 analytics cards with results
   - **Nice to have:** 2-3 non-analytics features

---

**For implementation details, see `/app/routes/analytics.py`**  
**For test coverage, see `/tests/test_analytics.py`**
