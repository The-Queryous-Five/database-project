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
7. Test DB connection: python -m tools.test_db_connection
8. Start Flask: flask run

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
    host = DB_CFG["host"]
    port = DB_CFG["port"]
    dbname = DB_CFG["dbname"]
    user = DB_CFG["user"]
    password = DB_CFG["password"]
    
    if vendor == "postgres":
        try:
            import psycopg
            
            logger.info(
                f"Attempting PostgreSQL connection: user={user}, host={host}, port={port}, database={dbname}"
            )
            
            conn_params = {
                "host": host,
                "port": port,
                "dbname": dbname,
                "user": user,
                "password": password
            }
            
            conn = psycopg.connect(**conn_params)
            logger.debug(f"PostgreSQL connection successful")
            return conn
            
        except ImportError as e:
            error_msg = "psycopg library not installed. Run: pip install 'psycopg[binary]>=3.0'"
            logger.error(error_msg)
            raise ImportError(error_msg) from e
            
        except Exception as e:
            error_msg = (
                f"PostgreSQL connection failed - vendor={vendor}, host={host}, port={port}, "
                f"database={dbname}, user={user}. Error: {type(e).__name__}: {str(e)}"
            )
            logger.error(error_msg)
            raise ConnectionError(error_msg) from e
    
    elif vendor == "mysql":
        try:
            import mysql.connector
            
            logger.info(
                f"Attempting MySQL connection: user={user}, host={host}, port={port}, database={dbname}"
            )
            
            conn_params = {
                "host": host,
                "port": port,
                "database": dbname,
                "user": user,
                "password": password
            }
            
            conn = mysql.connector.connect(**conn_params)
            logger.debug(f"MySQL connection successful")
            return conn
            
        except ImportError as e:
            error_msg = "mysql-connector-python library not installed. Run: pip install mysql-connector-python"
            logger.error(error_msg)
            raise ImportError(error_msg) from e
            
        except Exception as e:
            error_msg = (
                f"MySQL connection failed - vendor={vendor}, host={host}, port={port}, "
                f"database={dbname}, user={user}. Error: {type(e).__name__}: {str(e)}"
            )
            logger.error(error_msg)
            raise ConnectionError(error_msg) from e
    
    else:
        error_msg = f"Unsupported DB_VENDOR: '{vendor}'. Must be 'postgres' or 'mysql'."
        logger.error(error_msg)
        raise ValueError(error_msg)
