# 🚀 Quick Start Guide - Olist Analytics Platform (Windows)

**BLG212E Database Management Systems Project**

Get the demo running in 5 minutes with just a few commands!

---

## 📋 Prerequisites

### Required Software

1. **Python 3.8+**
   - Download: https://www.python.org/downloads/
   - ✅ Check: `python --version`

2. **MySQL 8.0+**
   - Download: https://dev.mysql.com/downloads/installer/
   - Install MySQL Server during setup
   - ✅ Check: MySQL service running in Services panel
   - 💡 Remember your root password!

3. **Git** (optional, for cloning)
   - Download: https://git-scm.com/download/win

---

## 🛠️ One-Time Setup

### Step 1: Clone Repository & Create Virtual Environment

```powershell
# Clone the repo
git clone https://github.com/The-Queryous-Five/database-project.git
cd database-project

# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**Execution Policy Error?** Run this first:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

### Step 2: Configure Database Connection

Create `.env` file:

```powershell
Copy-Item .env.example .env
notepad .env
```

Edit these lines (replace with your actual password):

```env
DB_VENDOR=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=olist
DB_USER=root
DB_PASS=your_actual_mysql_password_here

FLASK_ENV=development
FLASK_APP=app/app.py
```

**💡 Important:** Use your real MySQL password, not "changeme" or "root"!

---

### Step 3: Setup Database & Load Data

Run these commands in order:

```powershell
# 1. Create the database
.\scripts\mysql-create-db.ps1

# 2. Apply schema (create tables)
.\scripts\apply_ddl_mysql.ps1

# 3. Load data from CSV files
.\scripts\run_etl_all.ps1

# 4. Verify everything is working
.\scripts\check-health.ps1
```

Each script will show ✓ or ✗ for success/failure. If any fails, fix the issue before continuing.

---

## 🎯 Running the Demo

**One-command startup:**

```powershell
.\scripts\start-demo.ps1
```

This will:
1. ✅ Activate virtual environment
2. ✅ Start Flask backend on http://127.0.0.1:5000
3. ✅ Open frontend in your browser

**To stop:** Press `Ctrl+C` in the PowerShell terminal

---

## 🎯 Using the Demo

The frontend opens automatically at `frontend/index.html` in your browser.

### Available Features

Click the demo buttons to test each feature:

1. **Customers** 
   - Query by state (e.g., SP)
   - Top cities by customer count
   - "Use demo values" button for quick testing

2. **Orders**
   - Search by customer ID
   - View recent orders
   - Order statistics

3. **Products**
   - Top categories
   - Products by category
   - Sample products

4. **Payments**
   - Payment statistics by type
   - Payment distributions

5. **Reviews**
   - Recent reviews
   - Review statistics

6. **Analytics (Sprint B)** 🔥 **NEW!**
   - Revenue by Category (multi-table JOIN + GROUP BY)
   - Top Sellers (DISTINCT counting + geographic analysis)
   - Review vs Delivery (HAVING + date math)
   - Order Funnel (conditional aggregation)
   - **Click "🚀 Use demo values" for instant results**

All API calls go to `http://127.0.0.1:5000` (configured in `frontend/js/config.js`)

---

## 🔧 Troubleshooting

### MySQL CLI Not Found

**Error:** `mysql command not found in PATH!`

**Solution:** Add MySQL to your PATH:
```powershell
$env:PATH += ";C:\Program Files\MySQL\MySQL Server 8.0\bin"
```

Or find your installation directory:
- `C:\Program Files\MySQL\MySQL Server 8.0\bin`
- `C:\Program Files\MySQL\MySQL Server 9.0\bin`

### Wrong Password

**Error:** `Access denied for user 'root'@'localhost'`

**Solution:** Check your `.env` file and ensure `DB_PASS` matches your MySQL root password.

### Port 5000 Already in Use

**Error:** `Address already in use`

**Solution:** Find and kill the process using port 5000:
```powershell
# Find process
netstat -ano | findstr :5000

# Kill it (replace PID with actual process ID)
taskkill /PID <PID> /F
```

### Database Connection Failed

**Error:** `Can't connect to MySQL server`

**Solution:** 
1. Verify MySQL service is running (Services panel)
2. Check `.env` has correct `DB_HOST` and `DB_PORT`
3. Run health check: `.\scripts\check-health.ps1`

### Virtual Environment Issues

**Error:** `.\venv\Scripts\Activate.ps1 cannot be loaded`

**Solution:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## 📁 Project Structure

```
database-project/
├── app/              # Flask application
│   ├── app.py        # Main Flask app
│   ├── routes/       # API endpoints
│   └── db/           # Database connection
├── frontend/         # HTML/CSS/JS frontend
│   ├── index.html    # Main demo page
│   └── js/           # Frontend modules
├── db/
│   ├── ddl_mysql/    # MySQL schema files
│   └── etl/          # Data loading scripts
├── scripts/          # Windows PowerShell scripts
│   ├── start-demo.ps1        # One-command demo start
│   ├── mysql-create-db.ps1   # Create database
│   ├── apply_ddl_mysql.ps1   # Apply schema
│   ├── run_etl_all.ps1       # Load all data
│   └── check-health.ps1      # Health check
├── data/raw/         # CSV source files
├── .env              # Your config (create from .env.example)
└── requirements.txt  # Python dependencies
```

---

## 🚦 Next Steps

After the demo is running:

1. **Explore the API** - Check [API_ENDPOINTS.md](API_ENDPOINTS.md)
2. **Run Tests** - See [TESTING.md](TESTING.md)  
3. **View Documentation** - Read [README.md](README.md)

---

## 🆘 Still Having Issues?

1. Run health check: `.\scripts\check-health.ps1`
2. Check Flask routes: `$env:FLASK_APP="app/app.py"; flask routes`
3. View backend logs in the PowerShell terminal
4. Check [DATABASE_CONFIG.md](docs/DATABASE_CONFIG.md) for detailed setup

---

**Ready for demo day? Just run:** `.\scripts\start-demo.ps1` ✨

---

## 📂 Additional Documentation

- **API Reference**: [API_ENDPOINTS.md](API_ENDPOINTS.md)
- **Testing Guide**: [TESTING.md](TESTING.md)
- **Full Documentation**: [README.md](README.md)
- **Database Details**: [docs/DATABASE_CONFIG.md](docs/DATABASE_CONFIG.md)

---

## 🎓 Development Tips

### Making Changes

1. **Backend** (Python): Edit files in `app/`, restart Flask
2. **Frontend** (HTML/CSS/JS): Edit files in `frontend/`, refresh browser (F5)  
3. **Database**: Modify DDL in `db/ddl_mysql/`, reapply with `apply_ddl_mysql.ps1`

### Quick API Test

```powershell
# Test an endpoint directly
Invoke-WebRequest http://127.0.0.1:5000/health
```

---

Made with ❤️ by The Queryous Five - BLG212E Fall 2024

### Team Repository
https://github.com/The-Queryous-Five/database-project

### Common Issues
- Check `.env` file exists and has correct MySQL credentials
- Ensure MySQL service is running
- Verify virtual environment is activated
- Check port 5000 is available

### Debug Mode
Run Flask with debug output:
```powershell
$env:FLASK_DEBUG="1"
flask run --host 127.0.0.1 --port 5000
```

---

## ✅ Quick Verification Checklist

Before demo:

- [ ] MySQL service running
- [ ] Database `olist` exists
- [ ] Virtual environment activated
- [ ] `.env` file configured
- [ ] DDL applied (tables created)
- [ ] ETL completed (data loaded)
- [ ] Health check passes: `python -m tools.test_db_connection`
- [ ] Backend starts: `flask run`
- [ ] Frontend opens in browser
- [ ] Demo buttons work

---

**Ready to demo! 🎉**

For detailed API documentation, see `API_ENDPOINTS.md`.
