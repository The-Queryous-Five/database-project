import os
from dotenv import load_dotenv
import logging

load_dotenv()

logger = logging.getLogger(__name__)

# Database vendor selection
DB_VENDOR = os.getenv("DB_VENDOR", "postgres").lower()

if DB_VENDOR not in ["postgres", "mysql"]:
    logger.warning(f"Invalid DB_VENDOR '{DB_VENDOR}', defaulting to 'postgres'. Valid options: 'postgres' or 'mysql'")
    DB_VENDOR = "postgres"

# Database configuration with consistent DB_* environment variable names
DB_CFG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "5432" if DB_VENDOR == "postgres" else "3306")),
    "dbname": os.getenv("DB_NAME", "olist"),
    "user": os.getenv("DB_USER", "postgres" if DB_VENDOR == "postgres" else "root"),
    "password": os.getenv("DB_PASS", ""),
    "vendor": DB_VENDOR
}

# Warn if using default/empty password
if not DB_CFG["password"]:
    logger.warning("DB_PASS not set or empty. Database connection may fail. Please set DB_PASS in your .env file.")

DEBUG = os.getenv("FLASK_ENV", "development") == "development"
