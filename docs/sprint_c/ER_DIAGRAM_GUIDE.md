# ER Diagram Guide - Olist E-Commerce Database

## Overview

This document provides a comprehensive guide to creating an Entity-Relationship (ER) diagram for the Olist e-commerce database following standard ER notation taught in BLG212E Database Management Systems.

---

## Core Entities

### 1. **Customers**
- **Attributes:**
  - `customer_id` (PK) - Unique identifier
  - `customer_unique_id` - Business key (one customer may have multiple IDs across time)
  - `customer_zip_code_prefix` - Geographic location
  - `customer_city`
  - `customer_state`

### 2. **Orders**
- **Attributes:**
  - `order_id` (PK)
  - `customer_id` (FK → Customers)
  - `order_status` (delivered, shipped, canceled, etc.)
  - `order_purchase_timestamp`
  - `order_approved_at`
  - `order_delivered_carrier_date`
  - `order_delivered_customer_date`
  - `order_estimated_delivery_date`

### 3. **Order_Items**
- **Attributes:**
  - `order_id` (PK, FK → Orders)
  - `order_item_id` (PK) - Sequence within order
  - `product_id` (FK → Products)
  - `seller_id` (FK → Sellers)
  - `shipping_limit_date`
  - `price`
  - `freight_value`

### 4. **Products**
- **Attributes:**
  - `product_id` (PK)
  - `product_category_name` (FK → Categories)
  - `product_name_length`
  - `product_description_length`
  - `product_photos_qty`
  - `product_weight_g`
  - `product_length_cm`
  - `product_height_cm`
  - `product_width_cm`

### 5. **Sellers**
- **Attributes:**
  - `seller_id` (PK)
  - `seller_zip_code_prefix`
  - `seller_city`
  - `seller_state`

### 6. **Order_Payments**
- **Attributes:**
  - `order_id` (PK, FK → Orders)
  - `payment_sequential` (PK) - Multiple payments per order
  - `payment_type` (credit_card, boleto, voucher, debit_card)
  - `payment_installments`
  - `payment_value`

### 7. **Order_Reviews**
- **Attributes:**
  - `review_id` (PK)
  - `order_id` (FK → Orders)
  - `review_score` (1-5 stars)
  - `review_comment_title`
  - `review_comment_message`
  - `review_creation_date`
  - `review_answer_timestamp`

### 8. **Categories** (Product Categories)
- **Attributes:**
  - `product_category_name` (PK, in Portuguese)
  - `product_category_name_english` - English translation

### 9. **Geolocation** (Optional, for advanced queries)
- **Attributes:**
  - `geolocation_zip_code_prefix` (PK)
  - `geolocation_lat`
  - `geolocation_lng`
  - `geolocation_city`
  - `geolocation_state`

---

## Relationships

### R1: Customer **PLACES** Order
- **Cardinality:** 1:N (One customer can place many orders)
- **Participation:**
  - Customer: **Partial** (not all customers have orders in dataset)
  - Order: **Total** (every order must have a customer)
- **Arrow Direction:** Customer ← Order (Order references Customer)

### R2: Order **CONTAINS** Order_Items
- **Cardinality:** 1:N (One order can have many items)
- **Participation:**
  - Order: **Total** (every order has at least one item)
  - Order_Item: **Total** (every item belongs to an order)
- **Relationship Type:** Identifying (Order_Item is a weak entity with composite PK)

### R3: Product **APPEARS_IN** Order_Items
- **Cardinality:** 1:N (One product can appear in many order items)
- **Participation:**
  - Product: **Partial** (not all products sold)
  - Order_Item: **Total** (every item references a product)

### R4: Seller **SELLS** Order_Items
- **Cardinality:** 1:N (One seller can sell many items)
- **Participation:**
  - Seller: **Partial** (not all sellers active)
  - Order_Item: **Total** (every item has a seller)

### R5: Order **HAS** Order_Payments
- **Cardinality:** 1:N (One order can have multiple payments/installments)
- **Participation:**
  - Order: **Total** (most orders have payment records)
  - Order_Payment: **Total** (every payment belongs to an order)

### R6: Order **RECEIVES** Order_Reviews
- **Cardinality:** 1:1 or 1:0..1 (One order may have one review)
- **Participation:**
  - Order: **Partial** (not all orders reviewed)
  - Order_Review: **Total** (every review belongs to an order)

### R7: Product **BELONGS_TO** Category
- **Cardinality:** N:1 (Many products in one category)
- **Participation:**
  - Product: **Partial** (some products uncategorized)
  - Category: **Partial** (not all categories used)

### R8: Customer/Seller **LOCATED_IN** Geolocation
- **Cardinality:** N:1 (Many customers/sellers in one zip code)
- **Participation:** **Partial** on both sides

---

## ER Diagram Drawing Checklist

When drawing the ER diagram by hand or using a tool (e.g., Lucidchart, Draw.io):

### Notation Rules (as per class)

1. **Entities** → Rectangles
   - Label: Entity name (e.g., `Customers`, `Orders`)
   - Weak entities → Double rectangle (e.g., `Order_Items`)

2. **Attributes** → Ellipses (ovals)
   - Primary key → Underlined attribute name
   - Composite attributes → Nested ellipses (if needed)
   - Multivalued attributes → Double ellipse (none in our schema)

3. **Relationships** → Diamonds
   - Label: Verb phrase (e.g., `PLACES`, `CONTAINS`, `HAS`)
   - Identifying relationships → Double diamond (for weak entities)

4. **Cardinality Notation:**
   - **1:1** → Draw line with "1" on both sides
   - **1:N** → Draw line with "1" on one side, "N" on other
   - **M:N** → Draw line with "M" on one side, "N" on other
   
   In our schema:
   - Customer (1) ——— **PLACES** ——— (N) Order
   - Order (1) ——— **CONTAINS** ——— (N) Order_Items
   - Product (1) ——— **APPEARS_IN** ——— (N) Order_Items

5. **Participation Constraints:**
   - **Total participation:** Double line (entity must participate)
   - **Partial participation:** Single line (optional)
   
   Example:
   - Order **must** have a customer → double line from Order to PLACES relationship
   - Customer **may** have orders → single line from Customer to PLACES

6. **Foreign Keys:**
   - Not explicitly drawn in ER diagrams (they appear in relational schema)
   - But indicate relationships with arrows pointing toward referenced entity

---

## Simplified ER Diagram Structure

```
┌─────────────┐
│  Customers  │
│ ─────────── │
│ customer_id │ (PK)
│ city        │
│ state       │
└──────┬──────┘
       │ 1
       │ PLACES
       │ N
┌──────┴──────┐
│   Orders    │
│ ─────────── │
│ order_id    │ (PK)
│ customer_id │ (FK)
│ status      │
│ timestamps  │
└──────┬──────┘
       │ 1
       │ CONTAINS
       │ N
┌──────┴───────────┐
│  Order_Items     │  (Weak Entity)
│ ───────────────  │
│ order_id         │ (PK, FK)
│ order_item_id    │ (PK)
│ product_id       │ (FK)
│ seller_id        │ (FK)
│ price            │
│ freight_value    │
└─────┬────────┬───┘
      │ N      │ N
      │        │
      │ 1      │ 1
┌─────┴─────┐ ┌┴─────────┐
│ Products  │ │ Sellers  │
│ ────────  │ │ ──────── │
│product_id │ │seller_id │
└───────────┘ └──────────┘
```

---

## Key Observations

1. **Order_Items is a Junction Table (Weak Entity):**
   - Has composite primary key: `(order_id, order_item_id)`
   - Represents M:N relationship between Orders and Products
   - Also links to Sellers (3-way relationship)

2. **Multi-Payment Support:**
   - Order_Payments allows installments (credit card in Brazil often 2-12x)
   - Composite PK: `(order_id, payment_sequential)`

3. **Optional Relationships:**
   - Not all orders have reviews (partial participation)
   - Some products never sold (no order_items referencing them)

4. **Temporal Aspects:**
   - Orders track multiple timestamps (purchase → approval → shipping → delivery)
   - Reviews have creation and answer timestamps

---

## Next Steps

1. **Draw the full ER diagram** using the entities and relationships above
2. **Map to relational schema** (see `ER_TO_RELATIONAL_MAPPING.md`)
3. **Normalize to 3NF** (see `NORMALIZATION.md`)
4. **Add indexes and constraints** (see `PERFORMANCE.md`)

---

## References

- BLG212E Lecture Notes: ER Modeling
- Database Systems: The Complete Book (Garcia-Molina, Ullman, Widom)
- Olist Brazilian E-Commerce Public Dataset (Kaggle)
