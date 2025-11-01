# Olist DB App (Flask + PostgreSQL, dbapi2, NO ORM)
- 5 main tablo ve ek tablolarla REST uçları.
- Kurulum:
  1) Python 3.11+ ve PostgreSQL 16 kurulu.
  2) PowerShell: `python -m venv venv`
     ardından: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process` → `Y`
     `.\venv\Scripts\Activate.ps1`
  3) `pip install -r requirements.txt`
  4) `.env` dosyanı `.env.example`'dan kopyala ve doldur.
  5) DDL'leri sırayla uygula: 000 → 010 → 020 → 030 → 040
  6) ETL sırası: categories → geo_zip → products → customers/sellers → orders → order_items → payments → reviews
  7) Çalıştır: `flask --app app/app.py --debug run`
- Sağlık: `GET /health`
