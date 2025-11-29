"""
Quick script to create olist database in MySQL and apply DDL scripts.
Run with: python -m tools.setup_mysql
Or specify password as argument: python -m tools.setup_mysql yourpassword
"""
import os
import sys
import mysql.connector
from pathlib import Path

# Connection params
HOST = "127.0.0.1"
PORT = 3306
USER = "root"
PASSWORD = sys.argv[1] if len(sys.argv) > 1 else "root"
DB_NAME = "olist"

print(f"Attempting to connect with: host={HOST}, port={PORT}, user={USER}, password={'*' * len(PASSWORD)}")

def create_database():
    """Create the olist database if it doesn't exist."""
    print(f"Connecting to MySQL at {HOST}:{PORT}...")
    conn = mysql.connector.connect(
        host=HOST,
        port=PORT,
        user=USER,
        password=PASSWORD
    )
    cursor = conn.cursor()
    
    print(f"Creating database '{DB_NAME}' if it doesn't exist...")
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    print(f"✓ Database '{DB_NAME}' ready")
    
    cursor.close()
    conn.close()

def apply_ddl():
    """Apply DDL scripts in order."""
    print(f"\nConnecting to database '{DB_NAME}'...")
    conn = mysql.connector.connect(
        host=HOST,
        port=PORT,
        user=USER,
        password=PASSWORD,
        database=DB_NAME
    )
    cursor = conn.cursor()
    
    # DDL scripts in order
    ddl_dir = Path("db/ddl_mysql")
    scripts = [
        "000_base.sql",
        "010_categories.sql",
        "020_geo_zip.sql",
        "030_fk_v2_1.sql",
        "040_indexes.sql"
    ]
    
    for script_name in scripts:
        script_path = ddl_dir / script_name
        if not script_path.exists():
            print(f"⚠ Warning: {script_path} not found, skipping...")
            continue
            
        print(f"Applying {script_name}...")
        sql_content = script_path.read_text(encoding='utf-8')
        
        # Split by semicolon and execute each statement
        statements = [s.strip() for s in sql_content.split(';') if s.strip()]
        for statement in statements:
            try:
                cursor.execute(statement)
            except mysql.connector.Error as e:
                print(f"  Warning: {e}")
        
        conn.commit()
        print(f"  ✓ {script_name} applied")
    
    cursor.close()
    conn.close()
    print("\n✓ All DDL scripts applied successfully!")

if __name__ == "__main__":
    try:
        create_database()
        apply_ddl()
        print("\n" + "="*70)
        print("MySQL setup complete!")
        print("="*70)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)
