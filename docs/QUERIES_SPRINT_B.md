# Sprint B - Complex SQL Queries Documentation

## Overview

Sprint B focuses on **database-heavy analytics** to demonstrate mastery of SQL concepts learned in BLG212E. This document explains each complex query, why it's "complex," and how to access it in the UI.

---

## Query 1: Revenue by Category

**Endpoint:** `GET /analytics/revenue-by-category?limit=10`

**UI Card:** Analytics → "Revenue by Category"

### SQL Complexity

- **Multi-table JOIN:** Combines `order_items`, `products`, and `orders`
- **GROUP BY:** Aggregates data per product category
- **Multiple aggregations:** `SUM()`, `COUNT()`, `COUNT(DISTINCT)`, `AVG()`
- **Filtering:** `WHERE order_status = 'delivered'` to exclude incomplete orders
- **Sorting:** `ORDER BY total_revenue DESC` to show top earners first

### Query

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
LIMIT %s
```

### Database Concepts Demonstrated

✅ **Multi-table joins** (3 tables)  
✅ **Aggregate functions** (SUM, COUNT, AVG)  
✅ **DISTINCT clause** (counting unique orders)  
✅ **Parameterized queries** (SQL injection prevention)  
✅ **Computed columns** (price + freight_value)  

---

## Query 2: Top Sellers

**Endpoint:** `GET /analytics/top-sellers?limit=10`

**UI Card:** Analytics → "Top Sellers"

### SQL Complexity

- **Multi-table JOIN:** Combines `order_items`, `sellers`, and `orders`
- **GROUP BY with multiple columns:** Groups by `seller_id`, `seller_city`, `seller_state`
- **DISTINCT counting:** `COUNT(DISTINCT order_id)` to avoid double-counting
- **Revenue calculation:** Combines item price and freight
- **Sorting by derived column:** Orders by computed `total_revenue`

### Query

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
LIMIT %s
```

### Database Concepts Demonstrated

✅ **Multi-column GROUP BY**  
✅ **Seller performance analysis**  
✅ **Geographic grouping** (city + state)  
✅ **Revenue ranking**  

---

## Query 3: Review Score vs Delivery Time

**Endpoint:** `GET /analytics/review-vs-delivery?min_reviews=50`

**UI Card:** Analytics → "Review Score vs Delivery Time"

### SQL Complexity

- **4-table JOIN:** `order_items` → `sellers` → `orders` → `order_reviews`
- **LEFT JOIN:** Preserves sellers even if some orders lack reviews
- **Date arithmetic:** `TIMESTAMPDIFF(DAY, ...)` to compute delivery duration
- **HAVING clause:** Filters groups with `>= min_reviews` (post-aggregation filter)
- **Multi-column sorting:** Orders by `avg_review_score DESC`, then `avg_delivery_days ASC`

### Query

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
HAVING COUNT(DISTINCT r.review_id) >= %s
ORDER BY avg_review_score DESC, avg_delivery_days ASC
LIMIT 20
```

### Database Concepts Demonstrated

✅ **HAVING clause** (post-aggregation filtering)  
✅ **Date functions** (TIMESTAMPDIFF for duration)  
✅ **LEFT JOIN** (preserving rows with NULL reviews)  
✅ **Statistical correlation** (review score vs delivery time)  
✅ **Multi-level sorting**  

---

## Query 4: Order Status Funnel

**Endpoint:** `GET /analytics/order-funnel`

**UI Card:** Analytics → "Order Status Funnel"

### SQL Complexity

- **Conditional aggregation:** Groups by status, computes metrics per status
- **Multiple date calculations:** Computes both delivery and approval durations
- **Handling NULL values:** `TIMESTAMPDIFF` works with incomplete orders
- **Business funnel analysis:** Shows conversion rates through order lifecycle

### Query

```sql
SELECT
    order_status,
    COUNT(*) AS order_count,
    ROUND(AVG(TIMESTAMPDIFF(DAY, order_purchase_timestamp, order_delivered_customer_date)), 1) AS avg_delivery_days,
    ROUND(AVG(TIMESTAMPDIFF(DAY, order_purchase_timestamp, order_approved_at)), 1) AS avg_approval_days
FROM orders
GROUP BY order_status
ORDER BY order_count DESC
```

### Database Concepts Demonstrated

✅ **Funnel analysis** (conversion tracking)  
✅ **Multiple aggregations on same dataset**  
✅ **NULL-safe date math**  
✅ **Status-based metrics**  

---

## Why These Queries Showcase Database Knowledge

### 1. **No ORM** - Direct SQL Control
All queries use **native SQL** via Python DB-API 2.0 (`cursor.execute()`), not an ORM like SQLAlchemy. This demonstrates:

- Understanding of SQL syntax
- Manual JOIN construction
- Parameterized query handling

### 2. **Complex Joins**
- 3-4 table joins in most queries
- Mix of INNER JOIN and LEFT JOIN
- Proper foreign key relationships

### 3. **Advanced Aggregations**
- GROUP BY with multiple columns
- HAVING clause for post-aggregation filtering
- DISTINCT counting for deduplication

### 4. **Date/Time Functions**
- TIMESTAMPDIFF for computing durations
- Handling NULL dates gracefully
- Multi-milestone tracking (purchase → approval → delivery)

### 5. **Performance Considerations**
- `LIMIT` to prevent massive result sets
- Indexed columns in JOIN conditions (order_id, product_id, seller_id)
- Filtering before aggregation (WHERE before GROUP BY)

---

## Frontend Demo Usage

### How to Test in UI

1. **Start demo:**
   ```powershell
   .\scripts\start-demo.ps1
   ```

2. **Navigate to Analytics section** (bottom of page)

3. **Click "🚀 Use demo values" buttons** on each card to auto-run queries

4. **Observe results tables** showing:
   - Revenue by Category: Top 10 categories by sales
   - Top Sellers: Best-performing sellers by revenue
   - Review vs Delivery: Sellers with high ratings + fast delivery
   - Order Funnel: Status breakdown with avg processing times

### Screenshots for Presentation

**Recommended screenshots for professor:**

1. **Revenue by Category table** - Shows multi-table JOIN + GROUP BY
2. **Review vs Delivery table** - Shows HAVING + date math + LEFT JOIN

Both demonstrate "we learned database" effectively 😄

---

## API Response Format

All analytics endpoints return consistent JSON:

```json
{
  "ok": true,
  "params": { "limit": 10 },
  "data": [
    { "category_name": "electronics", "total_revenue": 5000.50, ... },
    ...
  ]
}
```

**Error responses (4xx/5xx):**

```json
{
  "ok": false,
  "error": "limit must be between 1 and 100"
}
```

---

## Testing

All queries are tested in `tests/test_analytics.py` with:

- Monkeypatched DB (no real MySQL required)
- Validation logic testing
- Schema verification
- Error handling

Run tests:

```powershell
.\venv\Scripts\python.exe -m pytest tests/ -q
```

---

## Next Steps (Sprint C Ideas)

- **Search + Pagination:** Add `OFFSET` and full-text search
- **Caching:** Redis cache for slow aggregate queries
- **Stored Procedures:** Move complex logic to MySQL procedures
- **Indexes:** Show `EXPLAIN` output to prove optimization
