"""
Database Connection Module

This module provides database connectivity for both PostgreSQL and MySQL.

Development Setup:
1. Copy .env.example to .env in the project root
2. Set DB_VENDOR to 'postgres' or 'mysql'
3. Configure the corresponding DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASS
4. Ensure your database server is running
5. Apply DDL scripts: db/ddl/ (Postgres) or db/ddl_mysql/ (MySQL)
6. Run ETL scripts from db/etl/ to load data
7. Start Flask: flask run

The get_conn() function automatically uses the correct driver based on DB_VENDOR.
"""

from app.config import DB_CFG
import logging

logger = logging.getLogger(__name__)

def get_conn():
    """
    Get database connection based on DB_VENDOR environment variable.
    
    Returns:
        Connection object (psycopg.Connection or mysql.connector.Connection)
        
    Raises:
        ImportError: If the required database driver is not installed
        ValueError: If DB_VENDOR is not 'postgres' or 'mysql'
        Exception: For connection errors (authentication, network, etc.)
    """
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
            logger.info(f"Connecting to PostgreSQL: {conn_params['user']}@{conn_params['host']}:{conn_params['port']}/{conn_params['dbname']}")
            return psycopg.connect(**conn_params)
        except ImportError:
            logger.error("psycopg not installed. Run: pip install 'psycopg[binary]==3.2.3'")
            raise
        except Exception as e:
            logger.error(f"PostgreSQL connection failed: {e}")
            raise
    
    elif vendor == "mysql":
        try:
            import mysql.connector
            conn_params = {
                "host": DB_CFG["host"],
                "port": DB_CFG["port"],
                "database": DB_CFG["dbname"],
                "user": DB_CFG["user"],
                "password": DB_CFG["password"],
                "autocommit": True  # Enable autocommit for MySQL
            }
            logger.info(f"Connecting to MySQL: {conn_params['user']}@{conn_params['host']}:{conn_params['port']}/{conn_params['database']}")
            return mysql.connector.connect(**conn_params)
        except ImportError:
            logger.error("mysql-connector-python not installed. Run: pip install mysql-connector-python==9.0.0")
            raise
        except Exception as e:
            logger.error(f"MySQL connection failed: {e}")
            raise
    
    else:
        error_msg = f"Unsupported DB_VENDOR: {vendor}. Use 'postgres' or 'mysql'."
        logger.error(error_msg)
        raise ValueError(error_msg)
