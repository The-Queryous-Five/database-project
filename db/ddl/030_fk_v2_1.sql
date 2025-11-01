-- Orders → Customers
ALTER TABLE orders
  ADD CONSTRAINT fk_orders__customer
  FOREIGN KEY (customer_id) REFERENCES customers(customer_id);

-- Payments → Orders
ALTER TABLE order_payments
  ADD CONSTRAINT fk_payments__order
  FOREIGN KEY (order_id) REFERENCES orders(order_id);

-- Reviews → Customers  (farklı hedef)
ALTER TABLE order_reviews
  ADD CONSTRAINT fk_reviews__customer
  FOREIGN KEY (customer_id) REFERENCES customers(customer_id);

-- Bridge: Order_Items → Orders/Products/Sellers
ALTER TABLE order_items
  ADD CONSTRAINT fk_oi__order   FOREIGN KEY (order_id)  REFERENCES orders(order_id);
ALTER TABLE order_items
  ADD CONSTRAINT fk_oi__product FOREIGN KEY (product_id) REFERENCES products(product_id);
ALTER TABLE order_items
  ADD CONSTRAINT fk_oi__seller  FOREIGN KEY (seller_id)  REFERENCES sellers(seller_id);
