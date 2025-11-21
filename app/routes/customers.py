from flask import Blueprint, request, jsonify
from app.db import db
from psycopg import OperationalError  # DB hatasını yakalamak için

bp_customers = Blueprint("customers", __name__)

@bp_customers.get("/customers/by-state")
def customers_by_state():
    state = request.args.get("state")
    if not state:
        return jsonify({"error": "Missing required parameter: state"}), 400

    # Şimdilik dummy cevap (Week 1’deki gibi)
    return jsonify({"state": state, "total_customers": 0})


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
        # Postgres ayakta değilse buraya düşer
        return jsonify({"error": "database not available (top-cities)"}), 503
