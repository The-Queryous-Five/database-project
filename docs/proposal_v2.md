## Main Tables (5)
- Customers (PK: customer_id) — FK: zip→Geo_Zip — Non-key: unique_id, city, state
- Orders (PK: order_id) — FK: customer_id→Customers — Non-key: status, purchase_ts, est_delivery
- Products (PK: product_id) — FK: category_id→Categories — Non-key: weight_g, length_cm, photos_qty
- Order_Payments (PK: order_id,payment_sequential) — FK: order_id→Orders — Non-key: type, installments, value
- Order_Reviews (PK: review_id) — FK: customer_id→Customers — Non-key: score, creation_date, comment_message

## Additional / Dim / Bridge
- Categories (PK: category_id, UNIQUE: category_name)
- Geo_Zip (PK: geolocation_zip_code_prefix)
- Sellers (PK: seller_id) — FK: zip→Geo_Zip
- Order_Items (PK: order_id,order_item_id) — FK: order→Orders, product→Products, seller→Sellers

## Database Support
- **PostgreSQL** (primary): psycopg3 via dbapi2
- **MySQL** (supported): mysql-connector-python via dbapi2
- NO ORM — raw SQL with parameterized queries
- ≥5 Foreign Keys enforced
- DDL sets available for both vendors
