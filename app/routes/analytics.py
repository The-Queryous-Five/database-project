from flask import Blueprint, render_template
from app.db import db
import logging

logger = logging.getLogger(__name__)

bp_analytics = Blueprint("analytics", __name__)


@bp_analytics.get("/analytics/sales-by-state")
def sales_by_state():
    """Complex query page: 4+ tables, JOINs, GROUP BY, aggregates."""
    try:
        # Raw SQL query using cursor.execute - NO ORM
        # Uses 4 tables: customers, orders, order_items, order_payments
        sql = """
        SELECT
            c.customer_state,
            COUNT(DISTINCT o.order_id) AS total_orders,
            COUNT(oi.order_item_id) AS total_items,
            SUM(p.payment_value) AS total_payment_value,
            AVG(p.payment_value) AS avg_payment_value
        FROM customers c
        JOIN orders o ON o.customer_id = c.customer_id
        JOIN order_items oi ON oi.order_id = o.order_id
        JOIN order_payments p ON p.order_id = o.order_id
        GROUP BY c.customer_state
        ORDER BY total_payment_value DESC
        LIMIT 20
        """
        
        with db.get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                cols = [d[0] for d in cur.description]
                rows = cur.fetchall()
        
        # Convert rows to dictionaries for template
        results = [dict(zip(cols, row)) for row in rows]
        
        return render_template("analytics/sales_by_state.html", results=results)
    
    except Exception as e:
        logger.error(f"Error fetching sales by state: {e}")
        return render_template("analytics/sales_by_state.html", results=[], error=str(e)), 500


@bp_analytics.get("/analytics/high-value-customers")
def high_value_customers():
    """Nested/subquery page: customers with total payment above average."""
    try:
        # Raw SQL query with nested subquery using cursor.execute - NO ORM
        sql = """
        SELECT
            c.customer_id,
            c.customer_city,
            c.customer_state,
            t.total_spent
        FROM customers c
        JOIN (
            SELECT o.customer_id, SUM(p.payment_value) AS total_spent
            FROM orders o
            JOIN order_payments p ON p.order_id = o.order_id
            GROUP BY o.customer_id
        ) t ON t.customer_id = c.customer_id
        WHERE t.total_spent > (
            SELECT AVG(total_spent) FROM (
                SELECT o.customer_id, SUM(p.payment_value) AS total_spent
                FROM orders o
                JOIN order_payments p ON p.order_id = o.order_id
                GROUP BY o.customer_id
            ) x
        )
        ORDER BY t.total_spent DESC
        LIMIT 50
        """
        
        with db.get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                cols = [d[0] for d in cur.description]
                rows = cur.fetchall()
        
        # Convert rows to dictionaries for template
        results = [dict(zip(cols, row)) for row in rows]
        
        return render_template("analytics/high_value_customers.html", results=results)
    
    except Exception as e:
        logger.error(f"Error fetching high value customers: {e}")
        return render_template("analytics/high_value_customers.html", results=[], error=str(e)), 500
