import os
from dotenv import load_dotenv
load_dotenv()
DB_CFG = {
    "host": os.getenv("DB_HOST","localhost"),
    "port": int(os.getenv("DB_PORT","5432")),
    "dbname": os.getenv("DB_NAME","olist"),
    "user": os.getenv("DB_USER","postgres"),
    "password": os.getenv("DB_PASS","postgres"),
}
DEBUG = os.getenv("FLASK_ENV","development") == "development"
