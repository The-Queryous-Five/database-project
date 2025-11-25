"""
Database Connection Health Check Utility

This script tests database connectivity using the same configuration as the Flask app.
It helps diagnose connection issues before running the application.

Usage:
    1. Activate your virtual environment (if using one)
    2. Ensure .env file exists in the project root with correct DB_* variables
    3. Run from project root:
       python -m tools.test_db_connection

Exit codes:
    0 - Connection successful
    1 - Connection failed

The script will print detailed information about:
- Database vendor (postgres/mysql)
- Connection parameters (host, port, database, user)
- Success or failure with error details
"""

import sys
import os

# Add project root to path so we can import app modules
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

def test_connection():
    """
    Test database connection and print diagnostic information.
    
    Returns:
        bool: True if connection successful, False otherwise
    """
    try:
        # Import after adding to path
        from app.db.db import get_conn
        from app.config import DB_CFG
        
        vendor = DB_CFG.get("vendor", "unknown")
        host = DB_CFG.get("host", "unknown")
        port = DB_CFG.get("port", "unknown")
        dbname = DB_CFG.get("dbname", "unknown")
        user = DB_CFG.get("user", "unknown")
        
        print("=" * 70)
        print("DATABASE CONNECTION TEST")
        print("=" * 70)
        print(f"Vendor:   {vendor}")
        print(f"Host:     {host}")
        print(f"Port:     {port}")
        print(f"Database: {dbname}")
        print(f"User:     {user}")
        print("-" * 70)
        print("Attempting connection...")
        print()
        
        # Try to connect
        conn = get_conn()
        
        # If we get here, connection succeeded
        print("✓ Connection successful!")
        print()
        
        # Try a simple query to verify the connection works
        if vendor == "postgres":
            with conn.cursor() as cur:
                cur.execute("SELECT version();")
                version = cur.fetchone()[0]
                print(f"PostgreSQL version: {version}")
        elif vendor == "mysql":
            cursor = conn.cursor()
            cursor.execute("SELECT VERSION();")
            version = cursor.fetchone()[0]
            cursor.close()
            print(f"MySQL version: {version}")
        
        # Close connection
        conn.close()
        print()
        print("=" * 70)
        print("✓ Database connection test PASSED")
        print("=" * 70)
        return True
        
    except ImportError as e:
        print(f"✗ Import Error: {e}")
        print()
        print("Make sure the required database driver is installed:")
        if "psycopg" in str(e):
            print("  pip install 'psycopg[binary]>=3.0'")
        elif "mysql" in str(e):
            print("  pip install mysql-connector-python")
        print()
        print("=" * 70)
        print("✗ Database connection test FAILED")
        print("=" * 70)
        return False
        
    except ConnectionError as e:
        print(f"✗ Connection Error: {e}")
        print()
        print("Common causes:")
        print("  - Database server is not running")
        print("  - Incorrect host or port in .env")
        print("  - Database does not exist")
        print("  - Invalid credentials (username/password)")
        print("  - Firewall blocking the connection")
        print()
        print("Troubleshooting steps:")
        print(f"  1. Verify {vendor} server is running")
        print(f"  2. Check .env file has correct DB_HOST, DB_PORT, DB_NAME")
        print(f"  3. Verify DB_USER and DB_PASS are correct")
        print(f"  4. Create database if needed: CREATE DATABASE {dbname};")
        print()
        print("=" * 70)
        print("✗ Database connection test FAILED")
        print("=" * 70)
        return False
        
    except ValueError as e:
        print(f"✗ Configuration Error: {e}")
        print()
        print("Check your .env file:")
        print("  - DB_VENDOR must be 'postgres' or 'mysql'")
        print("  - All required DB_* variables must be set")
        print()
        print("=" * 70)
        print("✗ Database connection test FAILED")
        print("=" * 70)
        return False
        
    except Exception as e:
        print(f"✗ Unexpected Error: {type(e).__name__}: {e}")
        print()
        print("=" * 70)
        print("✗ Database connection test FAILED")
        print("=" * 70)
        return False

def main():
    """Main entry point for the health check script."""
    success = test_connection()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
