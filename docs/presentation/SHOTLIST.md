# Screenshot Shotlist

**For:** BLG212E Database Management Systems Presentation  
**Date:** December 21, 2024

---

## Purpose

This document lists **all screenshots needed** for the presentation slides and documentation.

---

## Screenshot Targets (Priority Order)

### HIGH PRIORITY (Must Have)

#### 1. Dashboard Homepage
- **Location:** Frontend `index.html` loaded in browser
- **Shows:** All 6 cards visible (Customers, Orders, Products, Payments, Reviews, Analytics)
- **For Slide:** 9 (Application Features)
- **Capture:** Full browser window at 1920x1080
- **Status:** ⬜

---

#### 2. Revenue by Category (Analytics)
- **Location:** Frontend → Analytics section → Revenue by Category card
- **Action:** Click "Run Query" button
- **Shows:** Table with top 10 categories, columns: category_name, items_sold, distinct_orders, total_revenue, avg_item_price
- **For Slide:** 10 (Complex Query 1)
- **Capture:** Just the result table, crop to card
- **Status:** ⬜

---

#### 3. Review vs Delivery (Analytics)
- **Location:** Frontend → Analytics section → Review vs Delivery card
- **Action:** Click "Run Query" button
- **Shows:** Table with sellers, columns: seller_id, seller_city, seller_state, review_count, avg_review_score, avg_delivery_days
- **For Slide:** 11 (Complex Query 2 - Most Complex)
- **Capture:** Full table with at least 10 rows visible
- **Status:** ⬜

---

#### 4. GitHub Actions Workflow
- **Location:** https://github.com/The-Queryous-Five/database-project/actions
- **Shows:** Green checkmarks for CI workflow, "All checks passed"
- **For Slide:** 14 (Testing & CI/CD)
- **Capture:** Workflow run list with green status
- **Status:** ⬜

---

#### 5. Pytest Output
- **Location:** Terminal after running `pytest -v`
- **Shows:** `9 passed in 0.70s` or similar
- **For Slide:** 14 (Testing & CI/CD)
- **Capture:** Terminal window with green "PASSED" text
- **Status:** ⬜

---

### MEDIUM PRIORITY (Nice to Have)

#### 6. Top Sellers (Analytics)
- **Location:** Frontend → Analytics section → Top Sellers card
- **Shows:** Table with seller_id, location, revenue, order_count
- **For Slide:** Optional backup slide
- **Capture:** Result table
- **Status:** ⬜

---

#### 7. Order Funnel (Analytics)
- **Location:** Frontend → Analytics section → Order Funnel card
- **Shows:** Table with order_status, order_count, avg_delivery_days
- **For Slide:** Optional backup slide
- **Capture:** Result table
- **Status:** ⬜

---

#### 8. Customers by State
- **Location:** Frontend → Customers section
- **Action:** Enter "SP" in state field, click "Query by State"
- **Shows:** Table with customer records from São Paulo
- **For Slide:** Demo walkthrough
- **Capture:** Result table with 10-20 rows
- **Status:** ⬜

---

#### 9. Health Endpoint JSON
- **Location:** Browser at http://127.0.0.1:5000/health
- **Shows:** JSON response with "status": "healthy", database connection details
- **For Slide:** System health verification
- **Capture:** Browser window with formatted JSON
- **Status:** ⬜

---

#### 10. EXPLAIN Output (Before Indexes)
- **Location:** Terminal or MySQL Workbench
- **Action:** Run `EXPLAIN SELECT ... FROM order_items JOIN ...` (revenue query)
- **Shows:** Execution plan with type=ALL (table scan), key=NULL
- **For Slide:** 12 (Query Optimization - Before)
- **Capture:** EXPLAIN table output
- **Status:** ⬜

---

#### 11. EXPLAIN Output (After Indexes)
- **Location:** Terminal or MySQL Workbench
- **Action:** Run same query after applying `sprint_c_constraints_indexes.sql`
- **Shows:** Execution plan with type=ref, key=idx_order_items_order
- **For Slide:** 12 (Query Optimization - After)
- **Capture:** EXPLAIN table output
- **Status:** ⬜

---

### LOW PRIORITY (Optional)

#### 12. ER Diagram (Hand-drawn or Draw.io)
- **Location:** Draw.io file or photo of whiteboard
- **Shows:** 9 entities, 8 relationships, cardinality labels
- **For Slide:** 3 (ER Diagram)
- **Note:** Can create in Draw.io during presentation prep
- **Status:** ⬜

---

#### 13. Products Catalog
- **Location:** Frontend → Products section
- **Shows:** Product listing with dimensions, categories
- **For Slide:** Demo walkthrough
- **Status:** ⬜

---

#### 14. Payment Statistics
- **Location:** Frontend → Payments section
- **Shows:** Payment type breakdown (credit_card, boleto, etc.)
- **For Slide:** Demo walkthrough
- **Status:** ⬜

---

#### 15. Review Score Distribution
- **Location:** Frontend → Reviews section
- **Shows:** Review stats with score distribution (1-5 stars)
- **For Slide:** Demo walkthrough
- **Status:** ⬜

---

## Capture Instructions

### Tools

**Windows Snipping Tool:**
```powershell
# Launch with Win + Shift + S
# Or: snipping tool from Start menu
```

**Browser DevTools (for JSON):**
- F12 → Network tab → View response
- Or: Install JSON Formatter extension

**Terminal Screenshots:**
- Use Windows Terminal (better colors)
- Increase font size: Ctrl + Scroll
- Copy output to file: `command > output.txt`

---

### Settings

- **Resolution:** 1920x1080 (100% zoom)
- **Browser:** Chrome or Edge
- **Theme:** Light mode (better for projector)
- **Crop:** Remove browser chrome (URL bar, bookmarks)
- **Format:** PNG (better quality than JPG)

---

### Naming Convention

Save screenshots as:

```
01_dashboard_homepage.png
02_analytics_revenue_by_category.png
03_analytics_review_vs_delivery.png
04_github_actions_workflow.png
05_pytest_output.png
06_analytics_top_sellers.png
07_analytics_order_funnel.png
08_customers_by_state_SP.png
09_health_endpoint_json.png
10_explain_before_indexes.png
11_explain_after_indexes.png
12_er_diagram.png
13_products_catalog.png
14_payment_statistics.png
15_review_score_distribution.png
```

---

## Screenshot Checklist

Use this table to track progress:

| # | Screenshot | Priority | Status | Assigned To | Notes |
|---|-----------|----------|--------|-------------|-------|
| 1 | Dashboard Homepage | HIGH | ⬜ | | Slide 9 |
| 2 | Revenue by Category | HIGH | ⬜ | | Slide 10 |
| 3 | Review vs Delivery | HIGH | ⬜ | | Slide 11 |
| 4 | GitHub Actions | HIGH | ⬜ | | Slide 14 |
| 5 | Pytest Output | HIGH | ⬜ | | Slide 14 |
| 6 | Top Sellers | MEDIUM | ⬜ | | Backup |
| 7 | Order Funnel | MEDIUM | ⬜ | | Backup |
| 8 | Customers by State | MEDIUM | ⬜ | | Demo |
| 9 | Health JSON | MEDIUM | ⬜ | | Demo |
| 10 | EXPLAIN Before | MEDIUM | ⬜ | | Slide 12 |
| 11 | EXPLAIN After | MEDIUM | ⬜ | | Slide 12 |
| 12 | ER Diagram | LOW | ⬜ | | Slide 3 |
| 13 | Products Catalog | LOW | ⬜ | | Demo |
| 14 | Payment Stats | LOW | ⬜ | | Demo |
| 15 | Review Distribution | LOW | ⬜ | | Demo |

**Total:** 15 screenshots (5 HIGH, 6 MEDIUM, 4 LOW)

---

## Pre-Capture Setup

### Step 1: Start Demo

```powershell
# Navigate to repo
cd D:\database-project

# Activate venv
.\venv\Scripts\Activate.ps1

# Start backend
.\scripts\start-demo.ps1
```

**Verify:** Backend running at http://127.0.0.1:5000

---

### Step 2: Open Frontend

- Browser opens automatically
- If not: Open `frontend/index.html` in Chrome

---

### Step 3: Wait for Data Load

- Each card should populate with data
- No "Failed to load" errors
- If errors: Check backend logs

---

### Step 4: Start Capturing

- Follow shotlist order (HIGH → MEDIUM → LOW)
- Save to `docs/presentation/screenshots/` folder
- Use naming convention above

---

## EXPLAIN Capture (Advanced)

### Option 1: PowerShell Script

```powershell
# Run EXPLAIN helper script
.\scripts\explain_analytics.ps1
```

**Screenshot:** Capture terminal output

---

### Option 2: MySQL Workbench

1. Connect to localhost:3306 (olist database)
2. Open new query tab
3. Paste query from `app/routes/analytics.py`
4. Add `EXPLAIN` prefix
5. Execute (Ctrl+Enter)
6. Screenshot result grid

**Example:**
```sql
EXPLAIN
SELECT
    COALESCE(p.product_category_name, 'Unknown') AS category_name,
    COUNT(*) AS items_sold,
    -- ... rest of query
FROM order_items oi
JOIN products p ON p.product_id = oi.product_id
JOIN orders o ON o.order_id = oi.order_id
WHERE o.order_status = 'delivered'
GROUP BY p.product_category_name
ORDER BY total_revenue DESC
LIMIT 10;
```

---

### Option 3: curl + jq (JSON formatted)

```powershell
# Install jq first: choco install jq
curl http://127.0.0.1:5000/health | jq .
```

**Screenshot:** Formatted JSON output

---

## Post-Capture Tasks

1. **Review screenshots:** Check clarity, no sensitive data visible
2. **Crop if needed:** Remove unnecessary UI elements
3. **Add annotations:** Red arrows/boxes to highlight key data (optional)
4. **Organize:** Move to `docs/presentation/screenshots/`
5. **Backup:** Copy to Google Drive or cloud storage

---

## Slide Integration

After capturing screenshots:

1. Insert into PowerPoint/Google Slides
2. Crop to fit slide layout
3. Add captions (e.g., "Revenue by Category - Multi-table JOIN")
4. Ensure text is readable at presentation resolution

---

## Backup Plan

If live demo fails during presentation:

1. **Use screenshots** instead of live demo
2. **Walk through code** in `app/routes/analytics.py`
3. **Show test output** from pytest

**Prepare:** Print screenshots as handouts (optional)

---

## Quality Checklist

Before finalizing screenshots:

- [ ] All HIGH priority screenshots captured
- [ ] Images are clear and readable
- [ ] No personal data visible (passwords, tokens)
- [ ] Consistent resolution (1920x1080)
- [ ] Proper naming convention
- [ ] Organized in folder
- [ ] Backed up to cloud

---

**For slide content, see [SLIDE_OUTLINE.md](SLIDE_OUTLINE.md)**  
**For speaker assignments, see [SPEAKER_SPLIT_5P.md](SPEAKER_SPLIT_5P.md)**
