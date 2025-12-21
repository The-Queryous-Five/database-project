# Demo Day Runbook - Windows + MySQL

**Last Updated:** December 21, 2024  
**Platform:** Windows 10/11  
**Database:** MySQL 8.0+

---

## Quick Start (For Impatient Demos)

```powershell
# Activate environment
.\venv\Scripts\Activate.ps1

# Start demo (one command)
.\scripts\start-demo.ps1
```

Opens at: **http://127.0.0.1:5000**

**That's it!** (If you've already done setup once)

---

## Full Setup (First Time Only)

### Prerequisites

Install these **before** demo day:

1. **Python 3.8+**
   - Download: https://www.python.org/downloads/
   - Verify: `python --version`

2. **MySQL 8.0+**
   - Download: https://dev.mysql.com/downloads/installer/
   - Install "MySQL Server" during setup
   - **Remember your root password!**
   - Verify: Open Services → MySQL80 is running

3. **Git** (for cloning)
   - Download: https://git-scm.com/download/win

---

## Step 0: Configure Database Connection

### Create `.env` File

**Important:** `.env` is NOT in the repository (it's in `.gitignore` for security).

```powershell
# Copy template
Copy-Item .env.example .env

# Edit with Notepad
notepad .env
```

### Edit `.env` Contents

**Replace `your_actual_mysql_password_here` with your real MySQL root password:**

```env
# Database Configuration
DB_VENDOR=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=olist
DB_USER=root
DB_PASS=your_actual_mysql_password_here

# Flask Configuration
FLASK_ENV=development
FLASK_APP=app/app.py
FLASK_RUN_HOST=127.0.0.1
FLASK_RUN_PORT=5000
```

**Save and close Notepad.**

### Important Notes

- **Workbench users:** If you connect to MySQL via MySQL Workbench, use the **same username and password** in `.env`
- **Security:** NEVER commit `.env` to Git (it's already in `.gitignore`)
- **Testing:** You can test connection with:
  ```powershell
  python -m tools.test_db_connection
  ```

---

## Step 1: Virtual Environment Setup

**One-time setup** (do this before first demo):

```powershell
# Create virtual environment
python -m venv venv

# Activate it
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### Troubleshooting: Execution Policy Error

If you see `cannot be loaded because running scripts is disabled`:

```powershell
# Run this ONCE as Administrator
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then try `.\venv\Scripts\Activate.ps1` again.

---

## Step 2: Database Setup Pipeline

**Run these commands in order** (one-time setup):

### 2.1 Create Database

```powershell
.\scripts\mysql-create-db.ps1
```

**Expected Output:**
```
✓ Creating MySQL database 'olist'...
✓ Database created successfully!
```

**If it fails:**
- Check MySQL service is running (Services panel)
- Verify `.env` has correct password
- Try manually: `mysql -u root -p` and enter password

---

### 2.2 Apply Schema (Create Tables)

```powershell
.\scripts\apply_ddl_mysql.ps1
```

**Expected Output:**
```
✓ Applying DDL scripts to MySQL...
✓ 000_base.sql applied
✓ 010_categories.sql applied
✓ 020_geo_zip.sql applied
✓ 030_fk_v2_1.sql applied
✓ 040_indexes.sql applied
✓ Schema applied successfully!
```

**What this does:** Creates 9 tables (customers, orders, products, etc.)

---

### 2.3 Load Data from CSV Files

```powershell
.\scripts\run_etl_all.ps1
```

**Expected Output:**
```
✓ Running ETL pipeline...
✓ 1/9: categories loaded (71 rows)
✓ 2/9: customers loaded (99441 rows)
✓ 3/9: products loaded (32951 rows)
✓ 4/9: sellers loaded (3095 rows)
✓ 5/9: orders loaded (99441 rows)
✓ 6/9: order_items loaded (112650 rows)
✓ 7/9: order_payments loaded (103886 rows)
✓ 8/9: order_reviews loaded (99224 rows)
✓ 9/9: geolocation loaded (1000163 rows)
✓ ETL pipeline completed!
```

**Duration:** ~2-5 minutes (depends on your disk speed)

**What this does:** Loads ~1.4M rows from CSV files into MySQL

---

### 2.4 Verify Everything Works

```powershell
.\scripts\check-health.ps1
```

**Expected Output:**
```json
{
  "status": "healthy",
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

**If you see "healthy":** ✅ Setup complete!

---

## Step 3: Start Demo

### One-Command Startup

```powershell
.\scripts\start-demo.ps1
```

**What this does:**
1. Activates virtual environment
2. Starts Flask backend on http://127.0.0.1:5000
3. Opens frontend in your default browser

**Expected Output:**
```
✓ Starting Olist Analytics Demo...
✓ Virtual environment activated
✓ Flask starting on http://127.0.0.1:5000
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
```

**Browser opens automatically** showing the dashboard at `frontend/index.html`

---

## Step 4: Verify Endpoints

### Quick Endpoint Test

**In a new PowerShell window:**

```powershell
# Test health endpoint
Invoke-WebRequest http://127.0.0.1:5000/health

# Test analytics endpoint
Invoke-WebRequest http://127.0.0.1:5000/analytics/revenue-by-category
```

**Or open in browser:**
- http://127.0.0.1:5000/health
- http://127.0.0.1:5000/products/stats
- http://127.0.0.1:5000/analytics/revenue-by-category

---

## Step 5: Use the Dashboard

### Frontend Features

The dashboard has **6 sections:**

1. **Customers**
   - Query by state (try "SP")
   - Top cities by customer count
   - Click "Use demo values" for quick testing

2. **Orders**
   - Recent orders
   - Order statistics
   - Orders by customer ID

3. **Products**
   - Product catalog
   - Top categories
   - Product stats

4. **Payments**
   - Payment statistics by type
   - Payment distributions

5. **Reviews**
   - Recent customer reviews
   - Review score distribution

6. **Analytics** (Complex Queries)
   - Revenue by Category
   - Top Sellers
   - Review vs Delivery Time
   - Order Funnel

### Demo Flow Suggestion

**For a 5-minute demo:**

1. Show **Health endpoint** (prove DB connected)
2. Show **Customers by State** (simple query)
3. Show **Analytics → Revenue by Category** (complex query with 3-table JOIN)
4. Show **Analytics → Review vs Delivery** (most complex: 4-table JOIN + TIMESTAMPDIFF)

---

## Stopping the Demo

**To stop Flask:**

Press `Ctrl+C` in the PowerShell terminal where Flask is running.

**To stop MySQL** (if needed):

```powershell
# Stop MySQL service
net stop MySQL80
```

**To restart MySQL:**

```powershell
# Start MySQL service
net start MySQL80
```

---

## Troubleshooting

### Issue 1: "Access Denied" Error

**Symptom:** `Access denied for user 'root'@'localhost'`

**Fix:**
1. Check `.env` has correct password
2. Try connecting manually: `mysql -u root -p`
3. If password forgotten, reset MySQL root password:
   ```powershell
   .\scripts\reset_mysql_password.sh
   ```

---

### Issue 2: MySQL Service Not Running

**Symptom:** `Can't connect to MySQL server on '127.0.0.1'`

**Fix:**
1. Open **Services** panel (Win+R → `services.msc`)
2. Find **MySQL80** service
3. Right-click → Start
4. Retry connection

---

### Issue 3: Port 5000 Already in Use

**Symptom:** `Address already in use: 127.0.0.1:5000`

**Fix:**
1. Kill process using port 5000:
   ```powershell
   # Find process
   netstat -ano | findstr :5000
   
   # Kill process (replace PID)
   taskkill /F /PID <PID>
   ```
2. Or use different port:
   ```powershell
   $env:FLASK_RUN_PORT="5001"
   flask run
   ```

---

### Issue 4: Database Not Loaded

**Symptom:** Dashboard shows "0 products" or empty tables

**Fix:**
1. Re-run ETL pipeline:
   ```powershell
   .\scripts\run_etl_all.ps1
   ```
2. Check for errors in ETL output
3. Verify CSV files exist in `data/raw/`

---

### Issue 5: "Failed to Load Data" in Frontend

**Symptom:** Frontend shows error message in cards

**Fix:**
1. Check Flask is running (http://127.0.0.1:5000/health should return JSON)
2. Open browser console (F12) to see error messages
3. Verify backend URL in `frontend/js/config.js` or each JS file

---

### Issue 6: Virtual Environment Not Activated

**Symptom:** `ModuleNotFoundError: No module named 'flask'`

**Fix:**
```powershell
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Verify activation (should show "(venv)" prefix)
# Re-run command
```

---

## Quick Recovery Commands

If something goes wrong during demo:

### Reset Everything

```powershell
# 1. Drop and recreate database
mysql -u root -p -e "DROP DATABASE IF EXISTS olist; CREATE DATABASE olist CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# 2. Re-apply schema
.\scripts\apply_ddl_mysql.ps1

# 3. Re-load data
.\scripts\run_etl_all.ps1

# 4. Restart demo
.\scripts\start-demo.ps1
```

**Duration:** ~5 minutes

---

### Verify Setup Checklist

Before starting demo, verify:

- [ ] MySQL service running
- [ ] `.env` file exists with correct credentials
- [ ] Virtual environment activated
- [ ] Database `olist` exists
- [ ] Tables created (9 tables)
- [ ] Data loaded (~1.4M rows)
- [ ] Health check passes
- [ ] Port 5000 available

**Quick check script:**
```powershell
.\scripts\check-health.ps1
```

---

## Advanced: Optional Performance Indexes

**For advanced demos** (shows query optimization):

```powershell
# Apply Sprint C performance indexes
mysql -u root -p olist < db\ddl_mysql\sprint_c_constraints_indexes.sql

# Run EXPLAIN analysis
.\scripts\explain_analytics.ps1
```

**What this does:**
- Adds 8 indexes (~20 MB overhead)
- Improves analytics queries by 10-21x
- Shows EXPLAIN output for all 4 analytics queries

**Use case:** If professor asks "How did you optimize queries?"

---

## API Documentation

**Full API docs:** See `API_ENDPOINTS.md`

**Quick reference:**

| Endpoint | Description |
|----------|-------------|
| `/health` | System health check |
| `/customers/by-state?state=SP` | Customers in state |
| `/customers/top-cities` | Top cities by customer count |
| `/orders/stats` | Order statistics |
| `/orders/recent?limit=20` | Recent orders |
| `/products/stats` | Product statistics |
| `/products?limit=50` | Product catalog |
| `/payments/stats` | Payment breakdown |
| `/reviews/recent?limit=20` | Recent reviews |
| `/analytics/revenue-by-category` | Revenue by category (complex) |
| `/analytics/top-sellers` | Top sellers (complex) |
| `/analytics/review-vs-delivery` | Review vs delivery (most complex) |
| `/analytics/order-funnel` | Order funnel (complex) |

---

## Database Theory Docs (For Q&A)

If professor asks about database design:

**Quick links:**
- **ER Diagram:** `docs/sprint_c/ER_DIAGRAM_GUIDE.md`
- **Normalization:** `docs/sprint_c/NORMALIZATION.md`
- **Performance:** `docs/sprint_c/PERFORMANCE.md`
- **ER → Relational:** `docs/sprint_c/ER_TO_RELATIONAL_MAPPING.md`

---

## Demo Day Tips

### Before You Start

1. **Close unnecessary apps** (to free up memory)
2. **Disable notifications** (Windows Focus Assist)
3. **Increase terminal font size** (for visibility)
4. **Test demo once** the night before

### During Demo

1. **Start with health endpoint** (proves everything works)
2. **Use "demo values" buttons** (don't type manually)
3. **Have backup screenshots** (in case of network issues)
4. **Know 1-2 complex queries by heart** (for Q&A)

### If Demo Fails

1. **Show screenshots** (have them ready)
2. **Walk through code** (show SQL queries in `app/routes/analytics.py`)
3. **Explain architecture** (use `OVERVIEW.md`)
4. **Show test results** (run pytest live)

---

## Contact Info (If You Get Stuck)

**GitHub Repository:**  
https://github.com/The-Queryous-Five/database-project

**Documentation:**  
See `/docs` folder for all guides

**Quick Start:**  
See `QUICK_START.md` for condensed version

---

## Final Checklist (Print This!)

**30 minutes before demo:**

- [ ] MySQL service running
- [ ] `.env` configured correctly
- [ ] Virtual environment activated
- [ ] Database loaded (run `check-health.ps1`)
- [ ] Flask starts without errors
- [ ] Frontend loads in browser
- [ ] All 6 dashboard sections working
- [ ] Analytics queries return data
- [ ] Screenshots ready (backup)
- [ ] Docs open in browser tabs

**If all checked:** ✅ **You're ready to demo!**

---

**Good luck! 🎉**
