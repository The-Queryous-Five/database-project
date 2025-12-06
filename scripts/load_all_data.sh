#!/bin/bash

# Script to load all CSV data into MySQL database
# Must be run from project root directory

set -e  # Exit on error

PROJECT_ROOT="/Users/yusakaraaslan/Desktop/dersler 2025 güz/db/proje/database-project"
cd "$PROJECT_ROOT"

# Set PYTHONPATH so modules can be imported
export PYTHONPATH="$PROJECT_ROOT:$PYTHONPATH"

# Activate virtual environment
source venv/bin/activate

echo "========================================="
echo "Loading all data into MySQL database"
echo "========================================="

# 1. Load categories (already loaded, but safe to re-run with INSERT IGNORE)
echo ""
echo "1. Loading categories..."
python db/etl/load_categories.py data/raw/product_category_name_translation.csv

# 2. Load customers (no dependencies)
echo ""
echo "2. Loading customers..."
python db/etl/load_customers.py data/raw/olist_customers_dataset.csv

# 3. Load sellers (no dependencies)
echo ""
echo "3. Loading sellers..."
python db/etl/load_sellers.py data/raw/olist_sellers_dataset.csv

# 4. Load geo_zip (no dependencies)
echo ""
echo "4. Loading geo_zip..."
python db/etl/load_geo_zip.py data/raw/olist_geolocation_dataset.csv

# 5. Load products (depends on categories)
echo ""
echo "5. Loading products..."
python db/etl/load_products.py data/raw/olist_products_dataset.csv

# 6. Load orders (depends on customers)
echo ""
echo "6. Loading orders..."
python db/etl/load_orders.py data/raw/olist_orders_dataset.csv

# 7. Load order_items (depends on orders, products, sellers)
echo ""
echo "7. Loading order_items..."
python db/etl/load_order_items.py data/raw/olist_order_items_dataset.csv

# 8. Load order_payments (depends on orders)
echo ""
echo "8. Loading order_payments..."
python db/etl/load_payments.py data/raw/olist_order_payments_dataset.csv

# 9. Load order_reviews (depends on orders, will update customer_id from orders)
echo ""
echo "9. Loading order_reviews..."
python db/etl/load_reviews.py data/raw/olist_order_reviews_dataset.csv

echo ""
echo "========================================="
echo "All data loaded successfully!"
echo "========================================="
