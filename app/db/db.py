from app.config import DB_CFG
import logging

logger = logging.getLogger(__name__)

def get_conn():
    """Get database connection based on DB_VENDOR."""
    vendor = DB_CFG.get("vendor", "postgres")
    
    if vendor == "postgres":
        try:
            import psycopg
            conn_params = {
                "host": DB_CFG["host"],
                "port": DB_CFG["port"],
                "dbname": DB_CFG["dbname"],
                "user": DB_CFG["user"],
                "password": DB_CFG["password"]
            }
            return psycopg.connect(**conn_params)
        except ImportError:
            logger.error("psycopg not installed. Run: pip install 'psycopg[binary]==3.2.3'")
            raise
    
    elif vendor == "mysql":
        try:
            import mysql.connector
            conn_params = {
                "host": DB_CFG["host"],
                "port": DB_CFG["port"],
                "database": DB_CFG["dbname"],
                "user": DB_CFG["user"],
                "password": DB_CFG["password"]
            }
            return mysql.connector.connect(**conn_params)
        except ImportError:
            logger.error("mysql-connector-python not installed. Run: pip install mysql-connector-python==9.0.0")
            raise
    
    else:
        raise ValueError(f"Unsupported DB_VENDOR: {vendor}. Use 'postgres' or 'mysql'.")
