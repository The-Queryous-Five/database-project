import psycopg2
from app.config import DB_CFG
def get_conn():
    return psycopg2.connect(**DB_CFG)
