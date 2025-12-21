# Project Overview - Olist Analytics Platform

**BLG212E Database Management Systems - Fall 2024**  
**Team:** The Queryous Five

---

## What Is This Application?

A **MySQL-backed analytics dashboard** for exploring Brazilian e-commerce data from Olist.

**Core Components:**
- **Frontend:** Static HTML/CSS/JavaScript (vanilla ES6+, no frameworks)
- **Backend:** Flask 3.0.3 REST API (Python 3.8+)
- **Database:** MySQL 8.0+ with normalized schema (3NF/BCNF)

---

## Motivation & Goals

### Why This Project?

1. **Real-world dataset:** 100K+ orders from actual e-commerce marketplace
2. **Complex query challenges:** Multi-table JOINs, aggregations, time-series analysis
3. **Clean database design:** Normalized schema with proper relationships
4. **Full-stack learning:** ETL pipeline, REST API, frontend integration

### Project Objectives

- ✅ Design normalized database schema (ER → Relational mapping)
- ✅ Implement ETL pipeline from CSV to MySQL
- ✅ Build REST API with complex analytical queries
- ✅ Create interactive frontend dashboard
- ✅ Optimize query performance with indexes
- ✅ Establish testing and CI/CD pipeline

---

## Architecture

```
┌─────────────────────┐
│   Frontend (HTML)   │  ← User Interface (static files)
│   + JavaScript      │     • Dashboard cards
│                     │     • API calls (fetch)
└──────────┬──────────┘
           │ HTTP
           ↓
┌─────────────────────┐
│   Flask Backend     │  ← REST API (Python)
│   (app/routes/)     │     • 26 endpoints
│                     │     • Blueprint architecture
└──────────┬──────────┘
           │ SQL
           ↓
┌─────────────────────┐
│   MySQL Database    │  ← Data Layer
│   (9 tables)        │     • Normalized schema
│                     │     • Performance indexes
└─────────────────────┘
```

---

## Key Features

### Data Management
- 9 normalized tables: customers, orders, order_items, products, sellers, payments, reviews, categories, geolocation
- 100,000+ orders, 32,951 products, 99,441 customers
- Automated ETL pipeline with dependency resolution

### Analytics Capabilities
- Revenue by product category (multi-table aggregation)
- Top sellers by revenue and order count
- Review scores vs. delivery time correlation
- Order funnel analysis by status

### Technical Excellence
- Comprehensive ER diagram with cardinality/participation
- Normalization proof (unnormalized → 3NF/BCNF)
- Performance optimization (8 indexes, 10-21x speedup)
- Automated testing (pytest) and CI/CD (GitHub Actions)

---

## Technology Stack

**Backend:**
- Python 3.8+
- Flask 3.0.3 (web framework)
- python-dotenv 1.0.0 (configuration)
- mysqlclient 2.2.5 (database driver)

**Database:**
- MySQL 8.0+ (relational database)
- InnoDB storage engine
- UTF-8 character encoding

**Frontend:**
- Vanilla JavaScript (ES6+)
- HTML5 + CSS3
- No external frameworks

**Development:**
- pytest 8.3.4 (testing)
- GitHub Actions (CI/CD)
- PowerShell automation scripts

---

## Project Structure

```
database-project/
├── app/                # Flask application
│   ├── routes/         # API endpoints
│   ├── blueprints/     # Blueprint modules
│   └── db/             # Database connection
├── data/raw/           # CSV source files
├── db/                 # Database scripts
│   ├── ddl/            # PostgreSQL schema
│   ├── ddl_mysql/      # MySQL schema + indexes
│   └── etl/            # ETL scripts (9 files)
├── docs/               # Documentation
│   ├── final/          # Submission docs
│   ├── presentation/   # Presentation assets
│   └── sprint_c/       # Database theory docs
├── frontend/           # Static web files
│   ├── index.html      # Main dashboard
│   ├── css/            # Stylesheets
│   └── js/             # Client-side logic
├── scripts/            # Automation scripts
│   ├── start-demo.ps1  # One-command startup
│   └── run_etl_all.ps1 # Full data pipeline
└── tests/              # Pytest test suite
```

---

## Academic Context

**Course:** BLG212E Database Management Systems  
**Institution:** Istanbul Technical University  
**Semester:** Fall 2024  
**Instructor:** [Course Instructor Name]

**Learning Outcomes Demonstrated:**
- ER modeling and relational design
- SQL query optimization
- Database normalization (1NF → 2NF → 3NF → BCNF)
- Index design and performance tuning
- CRUD operations and transaction management
- RESTful API design
- Full-stack integration

---

## Repository

**GitHub:** https://github.com/The-Queryous-Five/database-project  
**Documentation:** See `/docs` folder for detailed guides

---

## Quick Start

See [QUICK_START.md](../../QUICK_START.md) for 5-minute Windows setup guide.

**One-command demo:**
```powershell
.\scripts\start-demo.ps1
```

Opens at: http://127.0.0.1:5000

---

**For detailed feature descriptions, see [FEATURES.md](FEATURES.md)**  
**For dataset information, see [DATASET.md](DATASET.md)**
