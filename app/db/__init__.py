"""
Database module initialization.
Exports db object with get_conn() method for compatibility with existing code.
"""
from .db import get_conn

class DB:
    """Database connection wrapper."""
    def get_conn(self):
        return get_conn()

db = DB()

