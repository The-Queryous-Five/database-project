#!/bin/bash
# Run all ETL scripts in the correct order
# Usage: ./scripts/run_all_etls.sh

echo "======================================"
echo "Running All ETL Scripts"
echo "======================================"
echo ""

export PYTHONPATH=.

ETL_SCRIPTS=(
    "db/etl/load_categories.py data/raw/product_category_name_translation.csv"
    "db/etl/load_geo_zip.py data/raw/olist_geolocation_dataset.csv"
    "db/etl/load_products.py data/raw/olist_products_dataset.csv"
    "db/etl/load_customers.py data/raw/olist_customers_dataset.csv"
    "db/etl/load_sellers.py data/raw/olist_sellers_dataset.csv"
    "db/etl/load_orders.py data/raw/olist_orders_dataset.csv"
    "db/etl/load_order_items.py data/raw/olist_order_items_dataset.csv"
    "db/etl/load_payments.py data/raw/olist_order_payments_dataset.csv"
    "db/etl/load_reviews.py data/raw/olist_order_reviews_dataset.csv"
)

for etl in "${ETL_SCRIPTS[@]}"; do
    echo "Running: venv/bin/python $etl"
    venv/bin/python $etl
    if [ $? -eq 0 ]; then
        echo "✓ Completed successfully"
    else
        echo "✗ Failed"
        exit 1
    fi
    echo ""
done

echo "======================================"
echo "✓ All ETL scripts completed!"
echo "======================================"

# Verify data
echo ""
echo "Verifying loaded data..."
mysql -u root olist <<EOF
SELECT 'categories' as table_name, COUNT(*) as count FROM categories
UNION ALL SELECT 'geo_zip', COUNT(*) FROM geo_zip
UNION ALL SELECT 'products', COUNT(*) FROM products
UNION ALL SELECT 'customers', COUNT(*) FROM customers
UNION ALL SELECT 'sellers', COUNT(*) FROM sellers
UNION ALL SELECT 'orders', COUNT(*) FROM orders
UNION ALL SELECT 'order_items', COUNT(*) FROM order_items
UNION ALL SELECT 'order_payments', COUNT(*) FROM order_payments
UNION ALL SELECT 'order_reviews', COUNT(*) FROM order_reviews;
EOF
