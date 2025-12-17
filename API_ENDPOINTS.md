# 🚀 API Endpoints Reference

> **Base URL**: `http://localhost:5001`

All endpoints return JSON. CORS is enabled for frontend communication.

---

## 📊 Orders

### `GET /orders/stats`
Get aggregate order statistics.

**Response:**
```json
{
  "total_orders": 99441,
  "total_items": 112650,
  "avg_items_per_order": 1.13,
  "total_revenue": 0
}
```

**Note**: Uses nested subquery to calculate avg items per order.

---

### `GET /orders/recent`
Get recent orders.

**Parameters:**
- `limit` (optional, default: 20): Number of orders (1-100)

**Example:**
```bash
curl "http://localhost:5001/orders/recent?limit=5"
```

**Response:**
```json
[
  {
    "order_id": "e481f51cbdc54678b7cc49136f2d6af7",
    "customer_id": "9ef432eb6251297304e76186b10a928d",
    "order_status": "delivered",
    "order_purchase_timestamp": "2017-10-02T10:56:33",
    "order_delivered_customer_date": "2017-10-10T21:25:13"
  }
]
```

---

### `GET /orders/by-customer/<customer_id>`
Get all orders for a specific customer.

**Parameters:**
- `customer_id` (required): Customer UUID
- `limit` (optional, default: 10): Number of orders (1-100)

**Example:**
```bash
curl "http://localhost:5001/orders/by-customer/9ef432eb6251297304e76186b10a928d?limit=5"
```

---

## 🏷️ Products

### `GET /products/stats`
Get product statistics.

**Response:**
```json
{
  "total_products": 32951,
  "total_categories": 71
}
```

---

### `GET /products`
Get products list.

**Parameters:**
- `limit` (optional, default: 50): Number of products (1-500)

**Example:**
```bash
curl "http://localhost:5001/products?limit=10"
```

**Response:**
```json
[
  {
    "product_id": "1e9e8ef04dbcff4541ed26657ea517e5",
    "product_category_name": "beleza_saude",
    "product_photos_qty": 4,
    "product_weight_g": 700,
    "product_length_cm": 18,
    "product_height_cm": 9,
    "product_width_cm": 15
  }
]
```

---

### `GET /products/by-category`
Get products filtered by category.

**Parameters:**
- `category_id` (optional): Category ID
- `limit` (optional, default: 10): Number of products (1-100)

**Example:**
```bash
curl "http://localhost:5001/products/by-category?category_id=1&limit=5"
```

---

### `GET /products/top-categories`
Get top categories by product count.

**Parameters:**
- `limit` (optional, default: 10): Number of categories (1-50)

**Example:**
```bash
curl "http://localhost:5001/products/top-categories?limit=5"
```

---

### `GET /products/sample`
Get random sample of products (legacy endpoint).

**Parameters:**
- `n` (optional, default: 5): Number of products (1-100)

---

## 💳 Payments

### `GET /payments/stats`
Get payment statistics and breakdown by type.

**Response:**
```json
{
  "total_payments": 103886,
  "total_value": 16008872.14,
  "avg_payment_value": 154.10,
  "payment_types": [
    {
      "type": "credit_card",
      "count": 76795,
      "total": 12542084.19
    },
    {
      "type": "boleto",
      "count": 19784,
      "total": 2869361.27
    }
  ]
}
```

---

### `GET /payments/by-type`
Get payments filtered by payment type.

**Parameters:**
- `payment_type` (optional): Filter by type (credit_card, boleto, voucher, debit_card)
- `limit` (optional, default: 20): Number of payments (1-100)

**Example:**
```bash
curl "http://localhost:5001/payments/by-type?payment_type=credit_card&limit=10"
```

---

## ⭐ Reviews

### `GET /reviews/stats`
Get review statistics and score distribution.

**Parameters:**
- `min_score` (optional, default: 1): Minimum score (1-5)
- `max_score` (optional, default: 5): Maximum score (1-5)

**Example:**
```bash
curl "http://localhost:5001/reviews/stats?min_score=4&max_score=5"
```

**Response:**
```json
{
  "total_reviews": 98410,
  "avg_score": 4.09,
  "score_distribution": [
    {"score": 1, "count": 11282},
    {"score": 2, "count": 3114},
    {"score": 3, "count": 8097},
    {"score": 4, "count": 19007},
    {"score": 5, "count": 56910}
  ]
}
```

---

### `GET /reviews/recent`
Get recent customer reviews.

**Parameters:**
- `limit` (optional, default: 20): Number of reviews (1-100)

**Example:**
```bash
curl "http://localhost:5001/reviews/recent?limit=5"
```

**Response:**
```json
[
  {
    "review_id": "7bc2406110b926393aa56f80a40eba40",
    "order_id": "73fc7af87114b39712e6da79b0a377eb",
    "review_score": 5,
    "review_comment_message": "Great product, fast delivery!",
    "review_creation_date": "2017-10-15T19:24:31",
    "review_answer_timestamp": null
  }
]
```

---

## 👥 Customers

### `GET /customers/top-cities`
Get cities with most customers.

**Parameters:**
- `limit` (optional, default: 10): Number of cities (1-50)

**Example:**
```bash
curl "http://localhost:5001/customers/top-cities?limit=5"
```

**Response:**
```json
[
  {
    "city": "sao paulo",
    "state": "SP",
    "customer_count": 15540
  }
]
```

---

### `GET /customers/by-state/<state>`
Get customers by state code.

**Parameters:**
- `state` (required): State code (e.g., "SP", "RJ", "MG")
- `limit` (optional, default: 10): Number of customers (1-100)

**Example:**
```bash
curl "http://localhost:5001/customers/by-state/SP?limit=5"
```

**Response:**
```json
[
  {
    "customer_id": "9ef432eb6251297304e76186b10a928d",
    "customer_zip_code_prefix": 1151,
    "customer_city": "sao paulo",
    "customer_state": "SP"
  }
]
```

---

## 🏥 Health Check

### `GET /health`
Server health check endpoint.

**Example:**
```bash
curl http://localhost:5001/health
```

**Response:**
```json
{
  "status": "OK",
  "message": "Server is healthy"
}
```

---

## 📝 Notes

- All endpoints support CORS for frontend integration
- Default limits are enforced on list endpoints
- Timestamps are in ISO 8601 format
- UUIDs are 32-character hex strings (no hyphens)
- Payment values are in Brazilian Real (BRL)

---

## 🧪 Quick Test Commands

```bash
# Test all main endpoints
curl http://localhost:5001/health
curl http://localhost:5001/orders/stats
curl http://localhost:5001/products/stats
curl http://localhost:5001/payments/stats
curl http://localhost:5001/reviews/stats
curl "http://localhost:5001/customers/top-cities?limit=3"
```

---

<div align="center">
  <strong>For setup instructions, see QUICK_START.md</strong><br>
  <strong>For frontend usage, see FRONTEND_README.md</strong>
</div>
```json
{
  "total_payments": 103886,
  "total_value": 16008872.14,
  "avg_payment_value": 154.10,
  "payment_types": [
    {
      "type": "credit_card",
      "count": 76795,
      "total": 12542084.19
    },
    {
      "type": "boleto",
      "count": 19784,
      "total": 2869361.27
    },
    {
      "type": "voucher",
      "count": 5775,
      "total": 379436.87
    },
    {
      "type": "debit_card",
      "count": 1529,
      "total": 217990.95
    }
  ]
}
```

**✅ TESTED - Working perfectly!**

### GET `/payments/by-type?payment_type=credit_card&limit=20`
Get payments filtered by type.

---

## ⭐ Reviews Endpoints

### GET `/reviews/stats`
Get review statistics including score distribution.

**Parameters:**
- `min_score` (optional): Minimum score (1-5, default: 1)
- `max_score` (optional): Maximum score (1-5, default: 5)

**Response:**
```json
{
  "total_reviews": 98410,
  "avg_score": 4.09,
  "score_distribution": [
    {"score": 1, "count": 11282},
    {"score": 2, "count": 3114},
    {"score": 3, "count": 8097},
    {"score": 4, "count": 19007},
    {"score": 5, "count": 56910}
  ]
}
```

**✅ TESTED - Working perfectly!**

### GET `/reviews/recent?limit=20`
Get recent customer reviews.

**Parameters:**
- `limit` (optional): Number of reviews to return (1-100, default: 20)

**Response:**
```json
[
  {
    "review_id": "abc123...",
    "order_id": "xyz789...",
    "review_score": 5,
    "review_comment_title": "Excellent!",
    "review_comment_message": "Great product...",
    "review_creation_date": "2017-10-15T19:24:31",
    "review_answer_timestamp": null
  }
]
```

---

## 👥 Customers Endpoints

### GET `/customers/top-cities?limit=10`
Get cities with most customers.

### GET `/customers/by-state/<state>?limit=10`
Get customers by state.

---

## 🧪 Test All Endpoints

```bash
# Test orders
curl http://localhost:5001/orders/stats
curl http://localhost:5001/orders/recent?limit=5

# Test products
curl http://localhost:5001/products/stats
curl http://localhost:5001/products?limit=10

# Test payments
curl http://localhost:5001/payments/stats

# Test reviews
curl http://localhost:5001/reviews/stats
curl http://localhost:5001/reviews/recent?limit=5

# Test health
curl http://localhost:5001/health
```

---

## 🎨 Frontend Integration

All these endpoints are now integrated with your Next.js dashboard pages:

- **Dashboard** (`/`) - Shows overview statistics
- **Customers** (`/customers`) - Uses `/customers/*` endpoints ✅
- **Orders** (`/orders`) - Uses `/orders/stats` and `/orders/recent` ✅
- **Products** (`/products`) - Uses `/products/stats` and `/products` ✅
- **Payments** (`/payments`) - Uses `/payments/stats` ✅
- **Reviews** (`/reviews`) - Uses `/reviews/stats` and `/reviews/recent` ✅
- **Analytics** (`/analytics`) - Advanced visualizations

---

## 📊 Real Data Confirmed

All endpoints return **real data** from your MySQL database:
- ✅ **99,441 orders**
- ✅ **32,951 products** in **71 categories**
- ✅ **103,886 payments** totaling **$16M**
- ✅ **98,410 reviews** with **4.09 avg rating**

---

## 🚀 Running the Application

**Both servers are currently running:**

1. **Flask Backend:** http://localhost:5001
2. **Next.js Frontend:** http://localhost:3000

Just refresh your browser at http://localhost:3000 and all pages will now load real data!

---

## 🎉 No More Errors!

All the "Failed to load data" errors have been fixed. Your dashboard now displays:
- ✅ Real order data
- ✅ Real product catalog
- ✅ Real payment analytics
- ✅ Real customer reviews

**Everything is working perfectly!** 🌟
