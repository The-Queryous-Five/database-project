# MySQL Fresh Installation Guide for macOS

## Option 1: Install via Homebrew (Recommended - Easiest)

### Step 1: Install Homebrew (if not installed)
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### Step 2: Uninstall old MySQL
```bash
./scripts/uninstall_mysql.sh
```

### Step 3: Install MySQL via Homebrew
```bash
brew install mysql
```

### Step 4: Start MySQL
```bash
brew services start mysql
```

### Step 5: Secure Installation (set password)
```bash
mysql_secure_installation
```
Follow the prompts:
- Set root password: **newpass123** (or your choice)
- Remove anonymous users: **Y**
- Disallow root login remotely: **Y**
- Remove test database: **Y**
- Reload privilege tables: **Y**

### Step 6: Test Connection
```bash
mysql -u root -p
# Enter your password: newpass123
```

### Step 7: Create olist database
```bash
mysql -u root -p -e "CREATE DATABASE olist;"
```

### Step 8: Update .env file
```
DB_VENDOR=mysql
DB_HOST=localhost
DB_PORT=3306
DB_NAME=olist
DB_USER=root
DB_PASS=newpass123
```

---

## Option 2: Download from MySQL.com

### Step 1: Uninstall old MySQL
```bash
./scripts/uninstall_mysql.sh
```

### Step 2: Download MySQL
Visit: https://dev.mysql.com/downloads/mysql/
- Select macOS
- Download DMG Archive
- Choose your processor (Apple Silicon or Intel)

### Step 3: Install
- Open the downloaded DMG file
- Run the installer
- **IMPORTANT:** Note down the temporary password shown at the end!

### Step 4: Start MySQL
- Open System Settings
- Go to MySQL preference pane
- Click "Start MySQL Server"

### Step 5: Reset Password
```bash
mysql -u root -p
# Enter the temporary password from installation

# Then run:
ALTER USER 'root'@'localhost' IDENTIFIED BY 'newpass123';
FLUSH PRIVILEGES;
EXIT;
```

### Step 6: Create olist database
```bash
mysql -u root -pnewpass123 -e "CREATE DATABASE olist;"
```

---

## After Installation - Continue with Project Setup

```bash
# 1. Apply DDL
./scripts/apply_ddl_mysql.sh olist root newpass123

# 2. Run ETL (load data)
venv/bin/python db/etl/load_categories.py data/raw/product_category_name_translation.csv
venv/bin/python db/etl/load_geo_zip.py data/raw/olist_geolocation_dataset.csv
venv/bin/python db/etl/load_products.py data/raw/olist_products_dataset.csv
venv/bin/python db/etl/load_customers.py data/raw/olist_customers_dataset.csv
venv/bin/python db/etl/load_sellers.py data/raw/olist_sellers_dataset.csv
venv/bin/python db/etl/load_orders.py data/raw/olist_orders_dataset.csv
venv/bin/python db/etl/load_order_items.py data/raw/olist_order_items_dataset.csv
venv/bin/python db/etl/load_payments.py data/raw/olist_order_payments_dataset.csv
venv/bin/python db/etl/load_reviews.py data/raw/olist_order_reviews_dataset.csv

# 3. Start Flask app
venv/bin/python -m flask --app app/app.py --debug run

# 4. Test
curl http://127.0.0.1:5000/health
```

---

## Quick Commands Reference

```bash
# Start MySQL (Homebrew)
brew services start mysql

# Start MySQL (DMG install)
sudo /usr/local/mysql/support-files/mysql.server start

# Stop MySQL (Homebrew)
brew services stop mysql

# Stop MySQL (DMG install)
sudo /usr/local/mysql/support-files/mysql.server stop

# Check MySQL status
brew services list | grep mysql
# OR
sudo /usr/local/mysql/support-files/mysql.server status

# Connect to MySQL
mysql -u root -p
```
