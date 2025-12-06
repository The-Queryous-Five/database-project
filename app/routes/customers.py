from flask import Blueprint, request, jsonify
from app.db import db
from psycopg import OperationalError
import logging

logger = logging.getLogger(__name__)

bp_customers = Blueprint("customers", __name__)


@bp_customers.get("/customers/by-state/<string:state>")
def customers_by_state(state):
    """Get customers by state code with optional limit."""
    limit_str = request.args.get("limit", "10")
    
    # Validate state
    if not state or not state.strip():
        return jsonify({"error": "State code cannot be empty"}), 400
    
    if len(state) > 2:
        return jsonify({"error": "State code must be 2 characters"}), 400
    
    # Validate limit
    try:
        limit = int(limit_str)
        if not (1 <= limit <= 100):
            return jsonify({"error": "limit must be between 1 and 100"}), 400
    except ValueError:
        return jsonify({"error": "limit must be a valid integer"}), 400
    
    try:
        sql = """
        SELECT 
            customer_id,
            customer_city,
            customer_state
        FROM customers
        WHERE UPPER(customer_state) = UPPER(%s)
        ORDER BY customer_city
        LIMIT %s
        """
        
        with db.get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (state, limit))
                rows = cur.fetchall()
        
        customers = [
            {
                "customer_id": row[0],
                "customer_city": row[1],
                "customer_state": row[2]
            }
            for row in rows
        ]
        
        return jsonify(customers), 200
    
    except Exception as e:
        logger.error(f"Error fetching customers by state: {e}")
        return jsonify({"error": "Database error occurred"}), 500


def get_top_cities(limit: int = 5):
    sql = """
    SELECT customer_city,
           COUNT(*) AS customer_count
    FROM customers
    GROUP BY customer_city
    ORDER BY customer_count DESC
    LIMIT %s
    """
    with db.get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (limit,))
            rows = cur.fetchall()

    return [
        {"customer_city": row[0], "customer_count": row[1]}
        for row in rows
    ]


@bp_customers.get("/customers/top-cities")
def customers_top_cities():
    limit = request.args.get("limit", default=5, type=int)

    if limit < 1 or limit > 50:
        return jsonify({"error": "limit must be between 1 and 50"}), 422

    try:
        rows = get_top_cities(limit)
        return jsonify(rows)
    except OperationalError:
        return jsonify({"error": "database not available (top-cities)"}), 503
