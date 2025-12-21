# Presentation Slide Outline

**Course:** BLG212E Database Management Systems  
**Team:** The Queryous Five  
**Presentation Time:** 10-15 minutes

---

## Slide Structure (15 Slides)

### Part 1: Introduction (2 slides)

#### Slide 1: Title & Team

**Content:**
- Project title: "Olist Analytics Platform"
- Subtitle: "MySQL-Backed E-Commerce Analytics Dashboard"
- Team name: The Queryous Five
- Course: BLG212E Fall 2024

**Visual:**
- Team logo (if any)
- Course logo
- Project screenshot (homepage)

**Speaker Notes:**
- Introduce team members
- Brief project overview (1 sentence)

---

#### Slide 2: Project Overview

**Content:**
- What: MySQL analytics dashboard for Brazilian e-commerce data
- Why: Learn complex queries, normalization, performance optimization
- How: Flask REST API + vanilla JavaScript + MySQL

**Bullets:**
- 100,000+ orders
- 9 normalized tables
- 26 REST endpoints
- 4 complex analytics queries

**Visual:**
- Architecture diagram (Frontend → Backend → Database)

**Speaker Notes:**
- Explain motivation (real-world dataset, complex queries)
- Mention 2-year dataset from Olist marketplace

---

### Part 2: Database Design (4 slides)

#### Slide 3: ER Diagram (High-Level)

**Content:**
- Show complete ER diagram with 9 entities
- Highlight key relationships:
  - customers 1:N orders
  - orders 1:N order_items (weak entity)
  - products 1:N order_items
  - sellers 1:N order_items

**Bullets:**
- 9 entities
- 8 relationships
- Cardinality: 1:1, 1:N
- Participation: total/partial

**Visual:**
- ER diagram (Chen notation) from `docs/presentation/assets/er_diagram.drawio`

**Speaker Notes:**
- Explain weak entity (order_items depends on orders)
- Mention optional relationships (e.g., orders 1:1 reviews is optional)

---

#### Slide 4: ER to Relational Mapping

**Content:**
- Show mapping rules applied:
  1. Entities → Tables
  2. Weak entities → Composite PKs
  3. 1:N relationships → FK in "N" side
  4. 1:1 relationships → FK in either side
  5. M:N relationships → Junction table (not in our schema)

**Table:**
| ER Element | Table | Primary Key | Foreign Key(s) |
|------------|-------|-------------|----------------|
| customers | customers | customer_id | - |
| orders | orders | order_id | customer_id |
| order_items | order_items | (order_id, order_item_id) | order_id, product_id, seller_id |

**Visual:**
- Mapping diagram from `docs/presentation/assets/er_to_relational.drawio`

**Speaker Notes:**
- Emphasize composite PK for weak entity
- Mention FKs enforce referential integrity (optional in our setup)

---

#### Slide 5: Normalization

**Content:**
- Show before/after example (denormalized → 3NF)
- Starting point: One big "Orders" table with all data
- Problem: Update anomalies, data redundancy
- Solution: Decompose into 5 tables

**Bullets:**
- Before: 1 table with 50+ columns
- After: 5 tables (orders, order_items, products, sellers, customers)
- Result: 3NF/BCNF compliant

**Visual:**
- Before/after diagram from `docs/presentation/assets/normalization_before_after.drawio`
- Show functional dependencies (FD arrows)

**Speaker Notes:**
- Explain one FD example: order_id → customer_id, order_status
- Mention 1NF → 2NF → 3NF steps (detailed in docs/sprint_c/NORMALIZATION.md)

---

#### Slide 6: Schema Summary

**Content:**
- List all 9 tables with row counts
- Show table relationships (simplified ER)

**Table:**
| Table | Rows | Description |
|-------|------|-------------|
| customers | 99,441 | Customer profiles |
| orders | 99,441 | Order metadata |
| order_items | 112,650 | Items in orders (weak) |
| products | 32,951 | Product catalog |
| sellers | 3,095 | Seller profiles |
| order_payments | ~103K | Payment transactions |
| order_reviews | ~99K | Customer reviews |
| categories | 71 | Product categories |
| geolocation | 1M+ | Zip code geolocation |

**Visual:**
- Table icons with row counts

**Speaker Notes:**
- Total: ~1.4M rows
- Normalized schema (no redundancy)

---

### Part 3: Dataset & ETL (2 slides)

#### Slide 7: Dataset Overview

**Content:**
- Source: Olist Brazilian E-Commerce (Kaggle)
- Coverage: 2016-2018 (2 years)
- Size: 100,000+ orders, 32,951 products

**Bullets:**
- Real commercial data (anonymized)
- 9 CSV files
- Geographic: All 27 Brazilian states
- Top categories: bed_bath_table, health_beauty, sports_leisure

**Visual:**
- Map of Brazil with concentration (SP, RJ)
- Pie chart of payment types (credit_card 74%, boleto 19%)

**Speaker Notes:**
- Explain Olist marketplace model (connects sellers to customers)
- Mention data quality issues (missing reviews, NULL dates)

---

#### Slide 8: ETL Pipeline

**Content:**
- 9 ETL scripts in dependency order
- Execution: categories → customers → products → sellers → orders → order_items → payments → reviews → geolocation

**Bullets:**
- Automated pipeline (run_etl_all.ps1)
- Data cleaning: NULL handling, type conversions
- Validation: FK integrity checked
- Duration: ~2-5 minutes

**Visual:**
- ETL flow diagram (CSV → Python scripts → MySQL)

**Speaker Notes:**
- Explain dependency order (e.g., order_items requires orders, products, sellers)
- Mention data cleaning (NULL categories → "Unknown")

---

### Part 4: Features & Complex Queries (4 slides)

#### Slide 9: Application Features

**Content:**
- Frontend: 6 dashboard sections
- Backend: 26 REST endpoints
- Demo: Live dashboard walkthrough

**Bullets:**
1. Customers (by state, top cities)
2. Orders (recent, stats, by customer)
3. Products (catalog, categories, stats)
4. Payments (type breakdown)
5. Reviews (recent, score distribution)
6. **Analytics** (complex queries)

**Visual:**
- Dashboard screenshot with all 6 cards

**Speaker Notes:**
- Click through each section (use "demo values" buttons)
- Focus on Analytics section (most complex)

---

#### Slide 10: Complex Query 1 - Revenue by Category

**Content:**
- **Endpoint:** `/analytics/revenue-by-category`
- **SQL Complexity:** 3-table JOIN + GROUP BY + 5 aggregates

**SQL Snippet:**
```sql
SELECT
    COALESCE(p.product_category_name, 'Unknown') AS category_name,
    COUNT(*) AS items_sold,
    COUNT(DISTINCT oi.order_id) AS distinct_orders,
    ROUND(SUM(oi.price + oi.freight_value), 2) AS total_revenue,
    ROUND(AVG(oi.price), 2) AS avg_item_price
FROM order_items oi
JOIN products p ON p.product_id = oi.product_id
JOIN orders o ON o.order_id = oi.order_id
WHERE o.order_status = 'delivered'
GROUP BY p.product_category_name
ORDER BY total_revenue DESC LIMIT 10;
```

**Bullets:**
- 3 tables: order_items, products, orders
- 5 aggregates: COUNT, COUNT DISTINCT, SUM, AVG
- NULL handling: COALESCE

**Visual:**
- Screenshot of revenue table from frontend

**Speaker Notes:**
- Explain multi-table JOIN (why 3 tables needed)
- Show result: top 10 categories by revenue

---

#### Slide 11: Complex Query 2 - Review vs Delivery

**Content:**
- **Endpoint:** `/analytics/review-vs-delivery`
- **SQL Complexity:** 4-table JOIN + LEFT JOIN + TIMESTAMPDIFF + HAVING

**SQL Snippet:**
```sql
SELECT
    s.seller_id, s.seller_city, s.seller_state,
    COUNT(DISTINCT r.review_id) AS review_count,
    ROUND(AVG(r.review_score), 2) AS avg_review_score,
    ROUND(AVG(TIMESTAMPDIFF(DAY, o.order_purchase_timestamp, 
                            o.order_delivered_customer_date)), 1) AS avg_delivery_days
FROM order_items oi
JOIN sellers s ON s.seller_id = oi.seller_id
JOIN orders o ON o.order_id = oi.order_id
LEFT JOIN order_reviews r ON r.order_id = o.order_id
WHERE o.order_status = 'delivered'
  AND o.order_delivered_customer_date IS NOT NULL
GROUP BY s.seller_id, s.seller_city, s.seller_state
HAVING COUNT(DISTINCT r.review_id) >= 50
ORDER BY avg_review_score DESC, avg_delivery_days ASC LIMIT 20;
```

**Bullets:**
- **Most complex query** in project
- 4 tables: order_items, sellers, orders, order_reviews
- LEFT JOIN (not all orders have reviews)
- TIMESTAMPDIFF (date arithmetic)
- HAVING (post-aggregation filter)

**Visual:**
- Screenshot of review vs delivery table

**Speaker Notes:**
- Explain why LEFT JOIN (optional reviews)
- Show result: sellers with high scores + fast delivery

---

#### Slide 12: Query Optimization (Performance)

**Content:**
- Problem: Slow queries without indexes
- Solution: 8 performance indexes
- Result: 10-21x speedup

**Table:**
| Query | Before (ms) | After (ms) | Speedup |
|-------|------------|-----------|---------|
| Revenue by Category | 980 | 82 | **12x** |
| Top Sellers | 1200 | 80 | **15x** |
| Review vs Delivery | 2500 | 120 | **21x** |
| Order Funnel | 450 | 45 | **10x** |

**Bullets:**
- 8 indexes (~20 MB overhead)
- Index types: Single-column, composite
- Target: order_items, orders, reviews

**Visual:**
- EXPLAIN output comparison (before/after)
- Bar chart of speedup

**Speaker Notes:**
- Explain index design (covered in docs/sprint_c/PERFORMANCE.md)
- Show EXPLAIN output (key column shows index used)

---

#### Slide 13: SQL Concepts Demonstrated

**Content:**
- Summary of SQL techniques used in project

**Table:**
| SQL Feature | Usage | Example |
|-------------|-------|---------|
| Multi-table JOINs | 3-4 tables | Revenue, Sellers, Reviews |
| LEFT JOIN | Optional relationships | Reviews (not all orders) |
| Aggregate Functions | COUNT, SUM, AVG | All analytics queries |
| GROUP BY | Single/multi-column | By category, seller |
| HAVING | Post-aggregation filter | min_reviews >= 50 |
| TIMESTAMPDIFF | Date arithmetic | Delivery time calculation |
| COALESCE | NULL handling | Unknown categories |
| Subqueries | (none in final) | Considered but optimized out |

**Visual:**
- Icon grid or checklist

**Speaker Notes:**
- Emphasize variety of SQL techniques
- Mention LEFT JOIN vs INNER JOIN choice

---

### Part 5: Testing & Conclusion (3 slides)

#### Slide 14: Testing & CI/CD

**Content:**
- Automated testing: pytest (9 tests, 100% pass rate)
- CI/CD: GitHub Actions (runs on every push)
- Monkeypatching: No real DB needed for tests

**Bullets:**
- 9 tests covering all analytics endpoints
- Tests: schema validation, error handling, edge cases
- CI: Python 3.11, pip install, pytest
- Status: ✅ All tests passing

**Visual:**
- GitHub Actions workflow screenshot (green checks)
- Pytest output: `9 passed in 0.70s`

**Speaker Notes:**
- Explain monkeypatch strategy (mock DB connection)
- Show CI badge in README

---

#### Slide 15: Conclusion & Q&A

**Content:**
- Summary of achievements
- Learning outcomes
- Repository & documentation

**Achievements:**
- ✅ Normalized schema (3NF/BCNF)
- ✅ Complex multi-table queries
- ✅ Performance optimization (10-21x speedup)
- ✅ Automated testing + CI/CD
- ✅ Full-stack implementation

**Learning Outcomes:**
- ER modeling & relational design
- SQL query optimization
- Database normalization
- REST API development
- Full-stack integration

**Repository:**
- GitHub: https://github.com/The-Queryous-Five/database-project
- Documentation: `/docs` folder
- Live demo: http://127.0.0.1:5000

**Speaker Notes:**
- Thank audience
- Open floor for questions
- Mention documentation is comprehensive (if they want details)

---

## Slide Count Summary

| Section | Slides | Duration |
|---------|--------|----------|
| Introduction | 2 | 2 min |
| Database Design | 4 | 4 min |
| Dataset & ETL | 2 | 2 min |
| Features & Queries | 4 | 5 min |
| Testing & Conclusion | 3 | 2 min |
| **Total** | **15** | **15 min** |

---

## Presentation Tips

### Timing (15 minutes total)

- **5 people × 3 minutes each** = 15 minutes
- Or: **2 minutes intro + 10 minutes technical + 3 minutes demo/Q&A**

### Speaker Assignment

See [SPEAKER_SPLIT_5P.md](SPEAKER_SPLIT_5P.md) for detailed split.

### Visual Design

- **Use consistent theme** (ITU colors or professional template)
- **Limit text:** 3-5 bullets per slide max
- **Use screenshots:** Show actual dashboard, not just code
- **Code snippets:** Syntax highlighting, keep < 10 lines

### Demo Strategy

- **Have backup screenshots** in case live demo fails
- **Use "demo values" buttons** (don't type manually)
- **Show 2-3 key features only** (not all 26 endpoints)

---

## Screenshot Checklist

See [SHOTLIST.md](SHOTLIST.md) for complete list.

**Priority screenshots:**
- Dashboard homepage (all 6 cards)
- Revenue by Category table (Slide 10)
- Review vs Delivery table (Slide 11)
- EXPLAIN output before/after (Slide 12)
- GitHub Actions workflow (Slide 14)

---

## Backup Slides (Optional)

If time permits or for Q&A:

- **Backup 1:** Detailed ER diagram (all attributes)
- **Backup 2:** Normalization steps (1NF → 2NF → 3NF)
- **Backup 3:** ETL pipeline code walkthrough
- **Backup 4:** Frontend architecture
- **Backup 5:** Additional complex queries

---

## Q&A Preparation

### Expected Questions

**Q1:** Why not enforce FK constraints?  
**A:** ETL flexibility - enforcing FKs would require strict insertion order. We validate referential integrity in ETL scripts instead. (But optional FKs provided in `sprint_c_constraints_indexes.sql`)

**Q2:** Why use LEFT JOIN for reviews?  
**A:** Not all orders have reviews (~10% missing). LEFT JOIN preserves sellers without reviews in result.

**Q3:** How did you optimize queries?  
**A:** Added 8 indexes on join/filter columns. Analyzed with EXPLAIN. Achieved 10-21x speedup. (Show EXPLAIN output)

**Q4:** What if database fails?  
**A:** Health endpoint reports DB status. Frontend shows error message. Tests use mocks (no real DB needed).

**Q5:** Why MySQL not PostgreSQL?  
**A:** Project requirements (Windows + MySQL). But we also have PostgreSQL DDL scripts in `/db/ddl/`.

---

**For complete documentation, see `/docs/final/` and `/docs/sprint_c/`**
