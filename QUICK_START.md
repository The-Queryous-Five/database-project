# 🚀 Quick Start Guide - Olist Analytics Platform

## ✅ Both Servers Are Running!

### 🎯 Access Your Application

**Frontend (Next.js Dashboard):**
- 🌐 URL: **http://localhost:3000**
- 📱 Beautiful modern UI with glassmorphism design
- 🎨 Dark gradient background with smooth animations

**Backend (Flask API):**
- 🔧 URL: **http://localhost:5001**
- 📊 Health check: http://localhost:5001/health
- 🔗 CORS enabled for frontend communication

---

## 📊 Current Status

| Service | Status | Port | URL |
|---------|--------|------|-----|
| **Next.js Frontend** | ✅ Running | 3000 | http://localhost:3000 |
| **Flask Backend** | ✅ Running | 5001 | http://localhost:5001 |
| **MySQL Database** | ✅ Running | 3306 | localhost:3306 |

---

## 🎨 Available Pages

Navigate through the sidebar to access:

1. **📊 Dashboard** (`/`) - Overview with statistics
2. **👥 Customers** (`/customers`) - Customer analytics and search
3. **📦 Orders** (`/orders`) - Order management (coming soon)
4. **🏷️ Products** (`/products`) - Product catalog (coming soon)
5. **💳 Payments** (`/payments`) - Payment analytics (coming soon)
6. **⭐ Reviews** (`/reviews`) - Review statistics (coming soon)
7. **📈 Analytics** (`/analytics`) - Advanced analytics (coming soon)

---

## 🔧 How to Restart Servers

### Option 1: Quick Restart (if servers are running)
```bash
# The servers should already be running!
# Just refresh your browser at http://localhost:3000
```

### Option 2: Manual Start

**Terminal 1 - Flask Backend:**
```bash
cd /Users/yusakaraaslan/Desktop/dersler\ 2025\ güz/db/proje/database-project
source venv/bin/activate
export PYTHONPATH="$(pwd):$PYTHONPATH"
flask --app app/app.py run --port 5001
```

**Terminal 2 - Next.js Frontend:**
```bash
cd /Users/yusakaraaslan/Desktop/dersler\ 2025\ güz/db/proje/database-project/olist-dashboard
npm run dev
```

### Option 3: Use the startup script
```bash
cd /Users/yusakaraaslan/Desktop/dersler\ 2025\ güz/db/proje/database-project
./start-servers.sh
```

---

## 🧪 Test the API

```bash
# Health check
curl http://localhost:5001/health

# Get top cities
curl "http://localhost:5001/customers/top-cities?limit=5"

# Search customers by state
curl "http://localhost:5001/customers/by-state/SP?limit=10"
```

---

## 📱 Features Currently Working

### ✅ Dashboard Page
- 4 animated stat cards showing:
  - 👥 Total Customers: 99,163
  - 📦 Total Orders: 99,441
  - 🏷️ Products: 32,951
  - ⭐ Reviews: 98,410
- Quick action links
- System status indicators

### ✅ Customers Page
- 🔍 Search by state
- 📊 Top cities ranking
- 📋 Beautiful data tables
- ⚡ Real-time API integration
- 🎨 Loading states and error handling

---

## 🎨 Design Features

- ✨ Glassmorphism sidebar
- 🌈 Gradient backgrounds
- 🎭 Smooth hover animations
- 📱 Fully responsive
- 🎯 Professional typography
- ⚡ Fast page transitions

---

## 🛠️ Tech Stack

```
Frontend:
├── Next.js 16 (App Router)
├── TypeScript
├── Tailwind CSS
├── Lucide React (icons)
└── Axios (HTTP client)

Backend:
├── Flask 3.0.3
├── Flask-CORS
├── MySQL Connector
└── Python 3.9

Database:
└── MySQL 9.5.0
    ├── 9 tables
    └── 1.3M+ rows
```

---

## 📊 Database Tables

| Table | Rows | Status |
|-------|------|--------|
| categories | 71 | ✅ Loaded |
| customers | 99,163 | ✅ Loaded |
| sellers | 3,088 | ✅ Loaded |
| geo_zip | 19,015 | ✅ Loaded |
| products | 32,951 | ✅ Loaded |
| orders | 99,441 | ✅ Loaded |
| order_items | 112,650 | ✅ Loaded |
| order_payments | 103,886 | ✅ Loaded |
| order_reviews | 98,410 | ✅ Loaded |

---

## 🔥 Hot Tips

1. **Auto-refresh**: Next.js has hot reload - just save your changes!
2. **API Errors**: Check Flask logs if API calls fail
3. **Port conflicts**: Kill processes on ports 3000 or 5001 if needed
4. **Database**: MySQL must be running (`brew services list`)

---

## 🚨 Troubleshooting

### Next.js won't start
```bash
cd olist-dashboard
rm -rf .next
npm run dev
```

### Flask won't start
```bash
# Check if port 5001 is in use
lsof -i :5001
# Kill the process if needed
kill -9 <PID>
```

### API calls failing
1. Check Flask is running: `curl http://localhost:5001/health`
2. Check CORS is enabled in `app/app.py`
3. Verify `.env` file has correct database settings

---

## 🎉 You're All Set!

**Your professional analytics dashboard is running!**

👉 **Open your browser:** http://localhost:3000

Enjoy exploring your beautiful Olist Analytics Platform! 🌟

---

<div align="center">
  <strong>Made with ❤️ for Database Systems Course 2025</strong>
</div>
