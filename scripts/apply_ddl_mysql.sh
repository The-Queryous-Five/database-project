#!/bin/bash
# Apply MySQL DDL files for olist database
# Usage: ./apply_ddl_mysql.sh [database] [user] [password]

DB_NAME=${1:-olist}
DB_USER=${2:-root}
DB_PASS=${3:-""}

echo "Applying MySQL DDL to database: $DB_NAME"
echo "User: $DB_USER"
echo ""

# Create database
echo "Creating database if not exists..."
if [ -z "$DB_PASS" ]; then
    mysql -u $DB_USER -e "CREATE DATABASE IF NOT EXISTS $DB_NAME;"
else
    mysql -u $DB_USER -p$DB_PASS -e "CREATE DATABASE IF NOT EXISTS $DB_NAME;"
fi

if [ $? -ne 0 ]; then
    echo "Failed to create database. Please check your MySQL credentials."
    exit 1
fi

# Apply DDL files in order
DDL_FILES=(
    "db/ddl_mysql/000_base.sql"
    "db/ddl_mysql/010_categories.sql"
    "db/ddl_mysql/020_geo_zip.sql"
    "db/ddl_mysql/030_fk_v2_1.sql"
    "db/ddl_mysql/040_indexes.sql"
)

for ddl_file in "${DDL_FILES[@]}"; do
    echo "Applying $ddl_file..."
    if [ -z "$DB_PASS" ]; then
        mysql -u $DB_USER $DB_NAME < $ddl_file
    else
        mysql -u $DB_USER -p$DB_PASS $DB_NAME < $ddl_file
    fi
    
    if [ $? -eq 0 ]; then
        echo "✓ $ddl_file applied successfully"
    else
        echo "✗ Failed to apply $ddl_file"
        exit 1
    fi
done

echo ""
echo "✓ All MySQL DDL files applied successfully!"
echo ""
echo "Verifying tables..."
if [ -z "$DB_PASS" ]; then
    mysql -u $DB_USER $DB_NAME -e "SHOW TABLES;"
else
    mysql -u $DB_USER -p$DB_PASS $DB_NAME -e "SHOW TABLES;"
fi
