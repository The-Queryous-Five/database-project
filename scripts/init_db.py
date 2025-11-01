"""
Helper script to create the database and apply DDL without psql CLI.
Usage: python scripts/init_db.py
"""
import psycopg
from psycopg import sql
import os
from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv("DB_NAME", "olist")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "postgres")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "5432"))

DDL_FILES = [
    "db/ddl/000_base.sql",
    "db/ddl/010_categories.sql",
    "db/ddl/020_geo_zip.sql",
    "db/ddl/030_fk_v2_1.sql",
    "db/ddl/040_indexes.sql",
]


def create_database():
    """Create the olist database if it doesn't exist."""
    conn = psycopg.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASS,
        dbname="postgres",  # connect to default db
        autocommit=True
    )
    cur = conn.cursor()
    # Check if DB exists
    cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (DB_NAME,))
    exists = cur.fetchone()
    if not exists:
        cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(DB_NAME)))
        print(f"Database '{DB_NAME}' created.")
    else:
        print(f"Database '{DB_NAME}' already exists.")
    cur.close()
    conn.close()


def apply_ddl():
    """Apply DDL files in order."""
    conn = psycopg.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASS,
        dbname=DB_NAME
    )
    cur = conn.cursor()
    for ddl_file in DDL_FILES:
        print(f"Applying {ddl_file}...")
        with open(ddl_file, 'r', encoding='utf-8') as f:
            sql_script = f.read()
        cur.execute(sql_script)
        conn.commit()
        print(f"  ✓ {ddl_file} applied.")
    cur.close()
    conn.close()
    print("All DDL files applied successfully.")


if __name__ == "__main__":
    create_database()
    apply_ddl()
