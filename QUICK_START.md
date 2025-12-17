# 🚀 Quick Start Guide - Olist Analytics Platform

> **Goal**: Get the demo running in **10 minutes or less**

## Prerequisites

- MySQL 9.5+ installed and running
- Python 3.9+ with `venv`
- Node.js 18+ with npm
- Git (with LFS if cloning fresh)

---

## 1️⃣ Setup (One Time Only)

### Clone & Install Dependencies (5 min)

```bash
# Navigate to project
cd /Users/yusakaraaslan/Desktop/dersler\ 2025\ güz/db/proje/database-project

# Python setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Frontend setup
cd olist-dashboard
npm install
cd ..
```

### Database Setup (2 min)

```bash
# Start MySQL (if not running)
brew services start mysql

# Database should already be created with data
# If not: mysql -u root -e "CREATE DATABASE olist;"
# Then run: ./scripts/load_all_data.sh
```

---

## 2️⃣ Run the Demo (2 min)

### Terminal 1 - Start Flask Backend

```bash
cd /Users/yusakaraaslan/Desktop/dersler\ 2025\ güz/db/proje/database-project
source venv/bin/activate
export PYTHONPATH="$(pwd):$PYTHONPATH"
flask --app app/app.py run --port 5001
```

**Expected output**: `Running on http://127.0.0.1:5001`

### Terminal 2 - Start Next.js Frontend

```bash
cd /Users/yusakaraaslan/Desktop/dersler\ 2025\ güz/db/proje/database-project/olist-dashboard
npm run dev
```

**Expected output**: `Ready on http://localhost:3000`

---

## 3️⃣ Test the Demo (1 min)

### Health Check

```bash
curl http://localhost:5001/health
# Expected: {"message": "Server is healthy", "status": "OK"}
```

### Open Dashboard

**Browser**: http://localhost:3000

**Test flow**:
1. Dashboard shows 4 stat cards (customers, orders, products, reviews)
2. Click "Customers" → Search by state (e.g., "SP")
3. Click "Orders" → View recent orders and stats
4. Click "Products" → Browse products, filter by category
5. Click "Payments" → See payment type breakdown
6. Click "Reviews" → Filter by star rating

---

## 🎯 What You Should See

| Page | Features |
|------|----------|
| **Dashboard** | 4 stat cards, navigation links |
| **Customers** | State search, top cities table |
| **Orders** | Recent orders, order stats, search by ID/customer/status |
| **Products** | Product list, category filter, stats |
| **Payments** | Payment breakdown by type, stats |
| **Reviews** | Review cards, star rating filter, stats |
| **Analytics** | Charts with time range and metric filters |

---

## 🚨 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| Flask won't start | `lsof -i :5001` → `kill -9 <PID>` |
| Next.js won't start | `cd olist-dashboard && rm -rf .next && npm run dev` |
| API calls fail | Check Flask is running: `curl http://localhost:5001/health` |
| MySQL not running | `brew services start mysql` |
| Port conflict | Kill process: `lsof -i :3000` or `lsof -i :5001` |

---

## 📊 Database Info

- **Database**: `olist` (MySQL 9.5.0)
- **Tables**: 9 tables with 1,368,465 total rows
- **Connection**: `localhost:3306` (root, no password)

---

## 📚 More Documentation

- **API Endpoints**: See `API_ENDPOINTS.md`
- **Frontend Guide**: See `FRONTEND_README.md`
- **Schema & Queries**: See `SCHEMA_FIXES.md` and `NESTED_QUERIES.md`

---

<div align="center">
  <strong>✅ Demo ready in 10 minutes!</strong>
</div>
