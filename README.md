# Olist DB App (Flask + PostgreSQL/MySQL, dbapi2, NO ORM)
- 5 main tablo ve ek tablolarla REST uçları.
- Kurulum:
  1) Python 3.11+ ve PostgreSQL 16 veya MySQL 8+ kurulu.
  2) PowerShell: `python -m venv venv`
     ardından: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process` → `Y`
     `.\venv\Scripts\Activate.ps1`
  3) `pip install -r requirements.txt`
  4) `.env` dosyanı `.env.example`'dan kopyala ve doldur.
  5) DDL'leri sırayla uygula: 000 → 010 → 020 → 030 → 040
  6) ETL sırası: categories → geo_zip → products → customers/sellers → orders → order_items → payments → reviews
  7) Çalıştır: `flask --app app/app.py --debug run`
- Sağlık: `GET /health`

- LFS notu: tüm ekip bir kez `git lfs install` çalıştırsın.

## Database Setup / DRY_RUN
Henüz MySQL/PostgreSQL kurulu değilse ETL'ler **DRY_RUN=1** ile çalıştırılabilir.

**Örnek komut:**
```powershell
$env:DRY_RUN=1
python db/etl/load_products.py data/raw/olist_products_dataset.csv
```

**DRY_RUN modunda:**
- Veritabanına yazılmaz
- Sadece satır sayısı ve örnek satırlar (ilk 3) loglanır
- DB bağlantısı gerekmez

Bu mod, ETL scriptlerini test etmek ve veri kalitesini kontrol etmek için kullanılır.

## MySQL ile Çalışma
1) `.env` dosyasında:
   ```
   DB_VENDOR=mysql
   DB_PORT=3306
   DB_USER=root
   DB_PASS=<your_password>
   ```
2) MySQL paketini yükle: `pip install mysql-connector-python==9.0.0`
3) DDL uygula: `.\scripts\apply_ddl_mysql.ps1`
4) ETL çalıştır (aynı script)

## ETL DRY_RUN Modu (DB'siz veri önizleme)
```powershell
$env:DRY_RUN=1
python db/etl/load_categories.py data/raw/product_category_name_translation.csv
# Her dosya için ilk 3 satır örnek ve toplam satır sayısını gösterir
```

## Orphan Check (FK doğrulama)
PostgreSQL:
```powershell
psql -U postgres -d olist -f scripts/check_orphans_postgres.sql
```
MySQL:
```powershell
mysql -u root -p olist < scripts/check_orphans_mysql.sql
```
