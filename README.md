# Olist Analytics Platform

**BLG212E Database Management Systems - Fall 2024**  
**Team:** The Queryous Five

[![CI Status](https://github.com/The-Queryous-Five/database-project/actions/workflows/ci.yml/badge.svg)](https://github.com/The-Queryous-Five/database-project/actions)

---

## Overview

MySQL-backed analytics dashboard for exploring Brazilian e-commerce data from Olist marketplace. Features normalized database design (3NF/BCNF), complex multi-table queries, performance optimization with indexes, and automated testing with CI/CD.

**Tech Stack:** Flask 3.0.3 + MySQL 8.0+ + Vanilla JavaScript

---

## Quick Start (Windows)

**5-minute setup:**

```powershell
# 1. Setup virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

# 2. Configure database (edit .env)
Copy-Item .env.example .env
notepad .env  # Add your MySQL password

# 3. Setup database
.\scripts\mysql-create-db.ps1
.\scripts\apply_ddl_mysql.ps1
.\scripts\run_etl_all.ps1

# 4. Start demo
.\scripts\start-demo.ps1
```

Opens at: **http://127.0.0.1:5000**

**For detailed setup, see [QUICK_START.md](QUICK_START.md)**

---

## Documentation

### Final Deliverables (Sprint D)
- **[OVERVIEW.md](docs/final/OVERVIEW.md)** - Project overview, architecture, tech stack
- **[DATASET.md](docs/final/DATASET.md)** - Dataset description, size, ETL pipeline
- **[FEATURES.md](docs/final/FEATURES.md)** - Feature catalog with screenshot checklist
- **[COMPLEX_QUERIES.md](docs/final/COMPLEX_QUERIES.md)** - SQL query analysis, complexity breakdown
- **[TESTING.md](docs/final/TESTING.md)** - Testing strategy, pytest coverage, CI/CD
- **[DEMO_RUNBOOK_WINDOWS.md](docs/final/DEMO_RUNBOOK_WINDOWS.md)** - Complete demo day guide

### Database Theory (Sprint C)
- **[ER_DIAGRAM_GUIDE.md](docs/sprint_c/ER_DIAGRAM_GUIDE.md)** - Complete ER diagram with 9 entities
- **[ER_TO_RELATIONAL_MAPPING.md](docs/sprint_c/ER_TO_RELATIONAL_MAPPING.md)** - ER → Relational mapping rules
- **[NORMALIZATION.md](docs/sprint_c/NORMALIZATION.md)** - Normalization proof (0NF → 3NF/BCNF)
- **[PERFORMANCE.md](docs/sprint_c/PERFORMANCE.md)** - Index design, EXPLAIN analysis, 10-21x speedup

---

## Project Statistics

- **Database:** 9 normalized tables, ~1.4M rows
- **Orders:** 100,000+ orders from 2016-2018
- **Products:** 32,951 products across 71 categories
- **Customers:** 99,441 customers across 27 Brazilian states
- **API Endpoints:** 26 REST endpoints (4 complex analytics queries)
- **Tests:** 9 pytest tests, 100% pass rate
- **Performance:** 10-21x speedup with 8 indexes

---

## Features

### Data Sections
1. **Customers** - Query by state, top cities
2. **Orders** - Recent orders, order statistics, customer orders
3. **Products** - Catalog, categories, product stats
4. **Payments** - Payment type breakdown
5. **Reviews** - Recent reviews, score distribution

### Analytics (Complex Queries)
1. **Revenue by Category** - 3-table JOIN, 5 aggregates, GROUP BY
2. **Top Sellers** - Multi-table JOIN, seller performance analysis
3. **Review vs Delivery** - 4-table JOIN, LEFT JOIN, TIMESTAMPDIFF, HAVING (most complex)
4. **Order Funnel** - Status distribution, date arithmetic

---

## Testing & CI/CD

**Automated Testing:**
- 9 pytest tests covering all endpoints
- Monkeypatched database (no real MySQL needed)
- Schema validation, error handling, edge cases

**CI/CD Pipeline:**
- GitHub Actions workflow on push/PR
- Python 3.11, syntax check, pytest
- Status: ✅ All tests passing

**Run tests locally:**
```powershell
.\venv\Scripts\python.exe -m pytest -v
```

---

## Advanced Features

### Performance Optimization (Sprint C)

Apply 8 performance indexes:
```powershell
mysql -u root -p olist < db\ddl_mysql\sprint_c_constraints_indexes.sql
```

**Run EXPLAIN analysis:**
```powershell
.\scripts\explain_analytics.ps1
```

**Results:** 10-21x query speedup, ~20 MB overhead

---

## Repository Structure

```
database-project/
├── app/                 # Flask application
│   ├── routes/          # API endpoints (26 endpoints)
│   └── db/              # Database connection
├── data/raw/            # CSV source files (9 files)
├── db/
│   ├── ddl_mysql/       # MySQL schema + indexes
│   └── etl/             # ETL scripts (9 scripts)
├── docs/
│   ├── final/           # Final deliverables
│   ├── sprint_c/        # Database theory docs
│   └── presentation/    # Presentation assets
├── frontend/            # HTML/CSS/JS dashboard
├── scripts/             # Automation scripts
├── tests/               # Pytest test suite
└── .github/workflows/   # CI/CD configuration
```

---

## Team & Course

**Course:** BLG212E Database Management Systems  
**Institution:** Istanbul Technical University  
**Semester:** Fall 2024  
**Team:** The Queryous Five

**Repository:** https://github.com/The-Queryous-Five/database-project

---

## Additional Notes

- **LFS:** Run `git lfs install` once per team member
- **MySQL vs PostgreSQL:** Both DDL scripts available in `/db/ddl/` and `/db/ddl_mysql/`

---

## Troubleshooting

**Common issues:**
- MySQL service not running → Open Services panel (Win+R → `services.msc`)
- Wrong password in `.env` → Check MySQL Workbench credentials
- Port 5000 blocked → Use `netstat -ano | findstr :5000` to find blocking process
- ETL fails → Check CSV files exist in `data/raw/`

**For detailed troubleshooting, see [DEMO_RUNBOOK_WINDOWS.md](docs/final/DEMO_RUNBOOK_WINDOWS.md)**
