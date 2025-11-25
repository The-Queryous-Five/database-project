# PR: Vendor Switch + DRY_RUN + MySQL DDL

## 🎯 Amaç

Bu PR, projeyi **DB-bağımsız geliştirme**ye hazırlıyor:
- PostgreSQL **ve** MySQL desteği (dbapi2, ORM yok)
- ETL dosyalarını **DRY_RUN** moduyla DB kurmadan test edebilme
- API endpoint'lerine **input validation** (400/422 hata kodları)
- Orphan FK kontrolü için hazır SQL scriptleri

---

## ✅ Kontrol Listesi

### Dokümantasyon
- [x] **`docs/proposal_v2.md`** güncel:
  - PostgreSQL + MySQL dbapi2 desteği
  - **≥5 FK** kısıtı (Orders→Customers, Payments→Orders, Reviews→Customers, Products→Categories, Customers→Geo_Zip)
  - 5 main tablo + bridge tanımı

### Vendor Switch
- [x] **`app/config.py`**: `DB_VENDOR` env var (postgres/mysql)
- [x] **`app/db/db.py`**: Vendor-aware `get_conn()` (psycopg vs mysql.connector)
- [x] **`requirements.txt`**: psycopg[binary]==3.2.3 (mysql-connector-python commented)

### MySQL DDL
- [x] **`db/ddl_mysql/`**: 5 DDL dosyası (000-040)
  - PK VARCHAR, DECIMAL, DATETIME, AUTO_INCREMENT
  - FK'ler ve indexler
- [x] **`scripts/apply_ddl_mysql.ps1`**: MySQL DDL runner

### Scripts
- [x] **`scripts/apply_ddl.ps1`**: PostgreSQL DDL runner
- [x] **`scripts/check_orphans_postgres.sql`**: FK orphan checks (::int casting)
- [x] **`scripts/check_orphans_mysql.sql`**: MySQL orphan checks (IF() syntax)
- [x] **`scripts/init_db.py`**: Python-based DB creation without psql CLI

### ETL DRY_RUN
- [x] **`db/etl/etl_utils.py`**: DRY_RUN helpers (`get_env_bool`, `dry_insert_preview`, `iter_batches`)
- [x] **`db/etl/load_categories.py`**: DRY_RUN mode implemented
- [x] **`db/etl/load_products.py`**: DRY_RUN mode implemented
- [ ] Kalan 7 ETL dosyası (customers, sellers, orders, order_items, payments, reviews, geo_zip) — sonraki PR'larda eklenecek

### API Validations
- [x] **`/customers/by-state?state=`**: state zorunlu, yoksa **400**
- [x] **`/products/sample?n=`**: n ∈ [1, 100], dışında **422**
- [x] **`/payments/by-installments?min=`**: min ≥ 1, aksi **422**
- [x] **`/orders/last?from=&to=`**: ISO tarih doğrulama, geçersizse **422**
- [x] **`/reviews/recent?min_score=`**: min_score validation (blueprint'te mevcut)

### Gizlilik & LFS
- [x] **`.gitignore`**: `.env` excluded (credentials güvende)
- [x] **`.gitattributes`**: `data/raw/*.csv filter=lfs` (ekip: `git lfs install`)

---

## 🧪 Kanıt: DRY_RUN Çıktıları

### 1) Categories ETL (0 rows - dosya boş veya format hatası)
```
$env:DRY_RUN=1
python db/etl/load_categories.py data/raw/product_category_name_translation.csv

[DRY_RUN] Table: categories
[DRY_RUN] Total rows to insert: 0
[DRY_RUN] Sample (first 3 rows):
```

### 2) Products ETL (32,951 rows)
```
$env:DRY_RUN=1
python db/etl/load_products.py data/raw/olist_products_dataset.csv

[DRY_RUN] Table: products
[DRY_RUN] Total rows to insert: 32951
[DRY_RUN] Sample (first 3 rows):
  1. ('1e9e8ef04dbcff4541ed26657ea517e5', 225, 16, 10, 14, 1, 'perfumaria', None)
  2. ('3aa071139cb16b67ca9e5dea641aaa2f', 1000, 30, 18, 20, 1, 'artes', None)
  3. ('96bd76ec8810374ed1b65e291975717f', 154, 18, 9, 15, 1, 'esporte_lazer', None)

[DRY_RUN] Note: category_id mapping requires DB; shown as None
```

---

## 🧪 Kanıt: API Validations (Test with `docs/api_examples.http`)

### 400 - Bad Request (missing required parameter)
```http
GET http://localhost:5000/customers/by-state?state=
→ 400 {"error": "state parameter required and must be non-empty"}
```

### 422 - Validation Error (out of range)
```http
GET http://localhost:5000/products/sample?n=150
→ 422 {"error": "n must be an integer between 1 and 100"}
```

### 422 - Date Format Error
```http
GET http://localhost:5000/orders/last?from=2024-13-01
→ 422 {"error": "Invalid date format for from. Use ISO: YYYY-MM-DD"}
```

---

## 🔧 FK Kuralı (≥5)

1. **Orders.customer_id → Customers.customer_id**
2. **Order_Payments.order_id → Orders.order_id**
3. **Order_Reviews.customer_id → Customers.customer_id** *(Orders'tan farklı hedef)*
4. **Products.category_id → Categories.category_id**
5. **Customers.customer_zip_code_prefix → Geo_Zip.geolocation_zip_code_prefix**
6. *(Bonus)* Sellers.seller_zip_code_prefix → Geo_Zip.geolocation_zip_code_prefix

---

## 📋 Sonraki Adımlar

- [ ] Merge sonrası **Issues** aç ve ekibe dağıt (CODEOWNERS'a göre)
- [ ] Her üye kendi modülü için DRY_RUN + validation PR'ı açsın
- [ ] DB kurulumu (PostgreSQL veya MySQL) yapılınca gerçek ETL testleri
- [ ] Orphan check scriptleriyle FK bütünlüğünü doğrula

---

## 🙋 Reviewer'a Notlar

- **q1:** CODEOWNERS'taki kullanıcı adları placeholder (@mehmet, @ozan, vb.). Gerçek GitHub handle'larınızı bildirin.
- **q2:** Branch protection'ı PR merge'ünden **önce** mi sonra mı açalım?
- **q3:** Categories ETL 0 satır gösteriyor (CSV dosyası boş olabilir) - bu beklenmeyen bir durum.

---

**Commit:** `04b1e8b` (22 files changed, 550 insertions(+), 79 deletions(-))  
**Branch:** `chore/vendor-switch-and-dryrun`
