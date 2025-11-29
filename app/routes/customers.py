from flask import Blueprint, request, jsonify
from app.db import db
from psycopg import OperationalError  # DB hatasını yakalamak için

bp_customers = Blueprint("customers", __name__)
bp_geo = Blueprint("geo", __name__)

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


@bp_customers.get("/customers/by-city")
def customers_by_city():
    """Get customers by state and city from geo_zip table."""
    state = request.args.get("state")
    city = request.args.get("city")
    limit = request.args.get("limit", default=10, type=int)
    
    # Validation
    if not state:
        return jsonify({"error": "Missing required parameter: state"}), 400
    if not city:
        return jsonify({"error": "Missing required parameter: city"}), 400
    
    # State validation: 2 uppercase letters
    state = state.strip().upper()
    if len(state) != 2 or not state.isalpha():
        return jsonify({"error": "state must be 2 uppercase letters"}), 422
    
    # City validation: not empty
    city = city.strip()
    if not city:
        return jsonify({"error": "city cannot be empty"}), 422
    
    # Limit validation: 1-50
    if limit < 1 or limit > 50:
        return jsonify({"error": "limit must be between 1 and 50"}), 422
    
    # SQL query: join customers with geo_zip
    sql = """
    SELECT
        c.customer_id,
        g.geolocation_city AS city,
        g.geolocation_state AS state
    FROM customers c
    JOIN geo_zip g
      ON c.customer_zip_code_prefix = g.geolocation_zip_code_prefix
    WHERE g.geolocation_state = %s
      AND g.geolocation_city = %s
    LIMIT %s
    """
    
    try:
        with db.get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (state, city, limit))
                cols = [d[0] for d in cur.description]
                rows = cur.fetchall()
        
        result = [dict(zip(cols, row)) for row in rows]
        return jsonify(result)
    except OperationalError as e:
        return jsonify({"error": "database not available (by-city)"}), 503
    except Exception as e:
        return jsonify({"error": f"database error: {str(e)}"}), 503


@bp_geo.get("/geo/top-states")
def geo_top_states():
    """Get top states by customer count."""
    limit = request.args.get("limit", default=10, type=int)
    
    # Limit validation: 1-27 (Brazil has 27 states)
    if limit < 1 or limit > 27:
        return jsonify({"error": "limit must be between 1 and 27"}), 422
    
    # SQL query: join customers with geo_zip and group by state
    sql = """
    SELECT
        g.geolocation_state AS state,
        COUNT(*) AS customer_count
    FROM customers c
    JOIN geo_zip g
      ON c.customer_zip_code_prefix = g.geolocation_zip_code_prefix
    GROUP BY g.geolocation_state
    ORDER BY customer_count DESC
    LIMIT %s
    """
    
    try:
        with db.get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (limit,))
                cols = [d[0] for d in cur.description]
                rows = cur.fetchall()
        
        result = [dict(zip(cols, row)) for row in rows]
        return jsonify({"items": result})
    except OperationalError as e:
        return jsonify({"error": "database not available (top-states)"}), 503
    except Exception as e:
        return jsonify({"error": f"database error: {str(e)}"}), 503
