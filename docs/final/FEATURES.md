# Feature Catalog & Screenshot Checklist

---

## Application Features

Each feature maps to a **UI section**, **API endpoint**, and **expected output**.

---

## 1. Customer Features

### 1.1 Query Customers by State

**UI Section:** Customers Card  
**API Endpoint:** `GET /customers/by-state?state=SP&limit=20`  
**Input:** State code (e.g., SP, RJ, MG)  
**Output:** List of customers in that state

**Response Schema:**
```json
[
  {
    "customer_id": "abc123...",
    "customer_unique_id": "xyz789...",
    "customer_city": "sao paulo",
    "customer_state": "SP",
    "customer_zip_code_prefix": 1151
  }
]
```

**Screenshot Target:** Customers table showing SP state results

---

### 1.2 Top Cities by Customer Count

**UI Section:** Customers Card  
**API Endpoint:** `GET /customers/top-cities?limit=10`  
**Output:** Cities ranked by number of customers

**Response Schema:**
```json
[
  {
    "customer_city": "sao paulo",
    "customer_state": "SP",
    "customer_count": 15540
  }
]
```

**Screenshot Target:** Top cities table with customer counts

---

## 2. Order Features

### 2.1 Order Statistics

**UI Section:** Orders Card  
**API Endpoint:** `GET /orders/stats`  
**Output:** Aggregate statistics

**Response Schema:**
```json
{
  "total_orders": 99441,
  "total_items": 112650,
  "avg_items_per_order": 1.13,
  "total_revenue": 0
}
```

**Screenshot Target:** Stats summary box

---

### 2.2 Recent Orders

**UI Section:** Orders Card  
**API Endpoint:** `GET /orders/recent?limit=20`  
**Output:** Recent orders with timestamps

**Response Schema:**
```json
[
  {
    "order_id": "abc123...",
    "customer_id": "xyz789...",
    "order_status": "delivered",
    "order_purchase_timestamp": "2017-10-02T10:56:33",
    "order_delivered_customer_date": "2017-10-10T21:25:13"
  }
]
```

**Screenshot Target:** Recent orders table with dates

---

### 2.3 Orders by Customer

**UI Section:** Orders Card  
**API Endpoint:** `GET /orders/by-customer/<customer_id>?limit=10`  
**Input:** Customer ID  
**Output:** All orders for that customer

**Screenshot Target:** Customer-specific orders table

---

## 3. Product Features

### 3.1 Product Statistics

**UI Section:** Products Card  
**API Endpoint:** `GET /products/stats`  
**Output:** Total products and categories

**Response Schema:**
```json
{
  "total_products": 32951,
  "total_categories": 71
}
```

**Screenshot Target:** Product stats summary

---

### 3.2 Product Catalog

**UI Section:** Products Card  
**API Endpoint:** `GET /products?limit=50`  
**Output:** Product listing with details

**Response Schema:**
```json
[
  {
    "product_id": "abc123...",
    "product_category_name": "beleza_saude",
    "product_name_length": 58,
    "product_description_length": 598,
    "product_photos_qty": 4,
    "product_weight_g": 700,
    "product_length_cm": 18,
    "product_height_cm": 9,
    "product_width_cm": 15
  }
]
```

**Screenshot Target:** Product table with dimensions

---

### 3.3 Top Product Categories

**UI Section:** Products Card  
**API Endpoint:** `GET /products/top-categories?limit=10`  
**Output:** Categories ranked by product count

**Response Schema:**
```json
[
  {
    "category_name": "bed_bath_table",
    "product_count": 3029
  }
]
```

**Screenshot Target:** Top categories bar chart or table

---

## 4. Payment Features

### 4.1 Payment Statistics

**UI Section:** Payments Card  
**API Endpoint:** `GET /payments/stats`  
**Output:** Payment breakdown by type

**Response Schema:**
```json
{
  "total_payments": 103886,
  "total_value": 13591643.7,
  "payment_types": [
    {"payment_type": "credit_card", "count": 76795, "total_value": 10852626.8},
    {"payment_type": "boleto", "count": 19784, "total_value": 2083374.2}
  ]
}
```

**Screenshot Target:** Payment type distribution table

---

## 5. Review Features

### 5.1 Recent Reviews

**UI Section:** Reviews Card  
**API Endpoint:** `GET /reviews/recent?limit=20`  
**Output:** Latest customer reviews

**Response Schema:**
```json
[
  {
    "review_id": "abc123...",
    "order_id": "xyz789...",
    "review_score": 5,
    "review_comment_title": "Excellent!",
    "review_comment_message": "Fast delivery...",
    "review_creation_date": "2017-10-15T12:00:00"
  }
]
```

**Screenshot Target:** Review cards with scores

---

### 5.2 Review Statistics

**UI Section:** Reviews Card  
**API Endpoint:** `GET /reviews/stats`  
**Output:** Average score and distribution

**Response Schema:**
```json
{
  "total_reviews": 99224,
  "average_score": 4.08,
  "score_distribution": {
    "1": 11858,
    "2": 3247,
    "3": 8287,
    "4": 8879,
    "5": 57328
  }
}
```

**Screenshot Target:** Review score histogram

---

## 6. Analytics Features (Sprint B - Complex Queries)

### 6.1 Revenue by Category

**UI Section:** Analytics Card (Revenue)  
**API Endpoint:** `GET /analytics/revenue-by-category?limit=10`  
**SQL Complexity:** 3-table JOIN + GROUP BY + aggregate functions  
**Output:** Categories ranked by total revenue

**Response Schema:**
```json
[
  {
    "category_name": "beleza_saude",
    "items_sold": 11245,
    "distinct_orders": 10980,
    "total_revenue": 1234567.89,
    "avg_item_price": 109.85
  }
]
```

**Screenshot Target:** Revenue table with top 10 categories

---

### 6.2 Top Sellers

**UI Section:** Analytics Card (Sellers)  
**API Endpoint:** `GET /analytics/top-sellers?limit=10`  
**SQL Complexity:** 3-table JOIN + GROUP BY + multi-column aggregation  
**Output:** Sellers ranked by revenue

**Response Schema:**
```json
[
  {
    "seller_id": "abc123...",
    "seller_city": "sao paulo",
    "seller_state": "SP",
    "order_count": 234,
    "items_sold": 456,
    "total_revenue": 89012.34,
    "avg_item_price": 195.65
  }
]
```

**Screenshot Target:** Top sellers table with location

---

### 6.3 Review Score vs Delivery Time

**UI Section:** Analytics Card (Reviews)  
**API Endpoint:** `GET /analytics/review-vs-delivery?min_reviews=50&limit=20`  
**SQL Complexity:** 4-table JOIN + LEFT JOIN + TIMESTAMPDIFF + HAVING  
**Output:** Sellers with review scores and delivery performance

**Response Schema:**
```json
[
  {
    "seller_id": "xyz789...",
    "seller_city": "curitiba",
    "seller_state": "PR",
    "review_count": 127,
    "avg_review_score": 4.85,
    "avg_delivery_days": 8.3
  }
]
```

**Screenshot Target:** Review vs delivery correlation table

---

### 6.4 Order Funnel

**UI Section:** Analytics Card (Funnel)  
**API Endpoint:** `GET /analytics/order-funnel`  
**SQL Complexity:** GROUP BY + aggregate functions + TIMESTAMPDIFF  
**Output:** Order status distribution with timing

**Response Schema:**
```json
[
  {
    "order_status": "delivered",
    "order_count": 96478,
    "avg_delivery_days": 12.5,
    "avg_approval_days": 0.5
  },
  {
    "order_status": "canceled",
    "order_count": 625,
    "avg_delivery_days": null,
    "avg_approval_days": 0.2
  }
]
```

**Screenshot Target:** Order funnel bar chart or table

---

## 7. Health Check (Testing)

**UI Section:** Not in frontend (API only)  
**API Endpoint:** `GET /health`  
**Output:** System status and DB diagnostics

**Response Schema:**
```json
{
  "status": "healthy",
  "timestamp": "2024-12-21T10:30:00",
  "database": {
    "connected": true,
    "vendor": "mysql",
    "host": "127.0.0.1:3306",
    "database": "olist",
    "table_counts": {
      "customers": 99441,
      "orders": 99441,
      "products": 32951
    }
  }
}
```

**Screenshot Target:** Health endpoint JSON in browser or Postman

---

## Screenshot Checklist

Use this table to track which screenshots have been captured for the presentation.

| Feature | Screenshot Target | Status | Notes |
|---------|------------------|--------|-------|
| **Customers** |
| By State | Customers table with SP results | ⬜ | Use "SP" as demo value |
| Top Cities | Top cities ranking table | ⬜ | Limit 10 |
| **Orders** |
| Stats | Order statistics summary | ⬜ | Shows totals |
| Recent | Recent orders with timestamps | ⬜ | Limit 20 |
| By Customer | Customer-specific orders | ⬜ | Use sample customer_id |
| **Products** |
| Stats | Product/category counts | ⬜ | Summary box |
| Catalog | Product listing table | ⬜ | Limit 50 |
| Top Categories | Category ranking | ⬜ | Limit 10 |
| **Payments** |
| Stats | Payment type breakdown | ⬜ | Pie chart or table |
| **Reviews** |
| Recent | Review cards with scores | ⬜ | Limit 20 |
| Stats | Review score distribution | ⬜ | Histogram |
| **Analytics (Complex Queries)** |
| Revenue by Category | Top 10 categories by revenue | ⬜ | **Key screenshot** |
| Top Sellers | Top 10 sellers by revenue | ⬜ | **Key screenshot** |
| Review vs Delivery | Seller review/delivery correlation | ⬜ | **Key screenshot** |
| Order Funnel | Order status distribution | ⬜ | **Key screenshot** |
| **Testing** |
| Health Endpoint | JSON response in browser | ⬜ | Optional |

**Total Screenshots Needed:** 15 (10 basic + 4 analytics + 1 health)

---

## Screenshot Capture Tips

### Best Practices

1. **Resolution:** 1920x1080 or higher
2. **Browser:** Chrome with zoom at 100%
3. **Crop:** Include only the relevant card/table, remove unnecessary UI
4. **Highlight:** Use red arrows or boxes to emphasize key data
5. **Data Quality:** Ensure results are visible and readable

### Demo Values

Use these values for consistent screenshots:

- **State:** "SP" (largest state)
- **Customer ID:** Use any from top cities query
- **Limit Values:** 10 or 20 (keep consistent)

### Tools

- **Windows Snipping Tool:** Win + Shift + S
- **Chrome DevTools:** F12 → Network tab (for API responses)
- **Postman:** For clean JSON formatting

---

## Integration Testing

Before capturing screenshots:

```powershell
# 1. Start backend
.\scripts\start-demo.ps1

# 2. Test each endpoint
Invoke-WebRequest http://127.0.0.1:5000/health
Invoke-WebRequest http://127.0.0.1:5000/customers/by-state?state=SP

# 3. Open frontend
# Navigate to each card and click "Use demo values" buttons
```

**Verify:** All tables populate with data (no "Failed to load" errors)

---

**For complex query details, see [COMPLEX_QUERIES.md](COMPLEX_QUERIES.md)**
