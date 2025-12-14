from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from app.db import db
from psycopg import OperationalError
import logging

logger = logging.getLogger(__name__)

bp_customers = Blueprint("customers", __name__)
bp_geo = Blueprint("geo", __name__)


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


@bp_customers.get("/customers/ui")
def customers_ui():
    """Render customers list UI page with raw SQL query."""
    try:
        # Raw SQL query using cursor.execute - NO ORM
        sql = """
        SELECT 
            customer_id,
            customer_unique_id,
            customer_city,
            customer_state
        FROM customers
        ORDER BY customer_state, customer_city
        LIMIT 200
        """
        
        with db.get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                cols = [d[0] for d in cur.description]
                rows = cur.fetchall()
        
        # Convert rows to dictionaries for template
        customers = [dict(zip(cols, row)) for row in rows]
        
        return render_template("customers/list.html", customers=customers)
    
    except Exception as e:
        logger.error(f"Error fetching customers for UI: {e}")
        # Return template with empty list on error
        return render_template("customers/list.html", customers=[]), 500


@bp_customers.get("/customers/create")
def customers_create_get():
    """Render customer creation form."""
    return render_template("customers/create.html")


@bp_customers.post("/customers/create")
def customers_create_post():
    """Handle customer creation with raw SQL INSERT."""
    customer_id = request.form.get("customer_id", "").strip()
    customer_unique_id = request.form.get("customer_unique_id", "").strip()
    customer_zip_code_prefix = request.form.get("customer_zip_code_prefix", "").strip()
    customer_city = request.form.get("customer_city", "").strip()
    customer_state = request.form.get("customer_state", "").strip()
    
    # Validate required fields
    if not customer_id or not customer_unique_id:
        return render_template("customers/create.html", 
                             error="Customer ID and Unique ID are required fields.")
    
    try:
        # Convert zip code prefix to int if provided
        zip_code = None
        if customer_zip_code_prefix:
            try:
                zip_code = int(customer_zip_code_prefix)
            except ValueError:
                return render_template("customers/create.html",
                                     error="Zip code prefix must be a valid number.")
        
        # Raw SQL INSERT using cursor.execute - NO ORM
        sql = """
        INSERT INTO customers (customer_id, customer_unique_id, customer_zip_code_prefix, customer_city, customer_state)
        VALUES (%s, %s, %s, %s, %s)
        """
        
        with db.get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (customer_id, customer_unique_id, zip_code, customer_city or None, customer_state or None))
                conn.commit()
        
        return redirect(url_for("customers.customers_ui"))
    
    except Exception as e:
        logger.error(f"Error creating customer: {e}")
        error_msg = f"Error creating customer: {str(e)}"
        return render_template("customers/create.html", error=error_msg)


@bp_customers.get("/customers/<customer_id>/edit")
def customers_edit_get(customer_id):
    """Render customer edit form with current values."""
    try:
        # Raw SQL SELECT using cursor.execute - NO ORM
        sql = """
        SELECT customer_id, customer_unique_id, customer_zip_code_prefix, customer_city, customer_state
        FROM customers
        WHERE customer_id = %s
        """
        
        with db.get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (customer_id,))
                row = cur.fetchone()
        
        if not row:
            return render_template("customers/edit.html", 
                                 error=f"Customer with ID '{customer_id}' not found."), 404
        
        cols = ["customer_id", "customer_unique_id", "customer_zip_code_prefix", "customer_city", "customer_state"]
        customer = dict(zip(cols, row))
        
        return render_template("customers/edit.html", customer=customer)
    
    except Exception as e:
        logger.error(f"Error fetching customer for edit: {e}")
        return render_template("customers/edit.html", 
                             error=f"Error loading customer: {str(e)}"), 500


@bp_customers.post("/customers/<customer_id>/edit")
def customers_edit_post(customer_id):
    """Handle customer update with raw SQL UPDATE."""
    customer_unique_id = request.form.get("customer_unique_id", "").strip()
    customer_zip_code_prefix = request.form.get("customer_zip_code_prefix", "").strip()
    customer_city = request.form.get("customer_city", "").strip()
    customer_state = request.form.get("customer_state", "").strip()
    
    # Validate required fields
    if not customer_unique_id:
        return render_template("customers/edit.html",
                             customer={"customer_id": customer_id},
                             error="Customer Unique ID is required.")
    
    try:
        # Convert zip code prefix to int if provided
        zip_code = None
        if customer_zip_code_prefix:
            try:
                zip_code = int(customer_zip_code_prefix)
            except ValueError:
                return render_template("customers/edit.html",
                                     customer={"customer_id": customer_id},
                                     error="Zip code prefix must be a valid number.")
        
        # Raw SQL UPDATE using cursor.execute - NO ORM
        sql = """
        UPDATE customers
        SET customer_unique_id = %s,
            customer_zip_code_prefix = %s,
            customer_city = %s,
            customer_state = %s
        WHERE customer_id = %s
        """
        
        with db.get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (customer_unique_id, zip_code, customer_city or None, customer_state or None, customer_id))
                if cur.rowcount == 0:
                    return render_template("customers/edit.html",
                                         customer={"customer_id": customer_id},
                                         error=f"Customer with ID '{customer_id}' not found."), 404
                conn.commit()
        
        return redirect(url_for("customers.customers_ui"))
    
    except Exception as e:
        logger.error(f"Error updating customer: {e}")
        error_msg = f"Error updating customer: {str(e)}"
        return render_template("customers/edit.html",
                             customer={"customer_id": customer_id},
                             error=error_msg), 500


@bp_customers.post("/customers/<customer_id>/delete")
def customers_delete(customer_id):
    """Handle customer deletion with raw SQL DELETE."""
    try:
        # Raw SQL DELETE using cursor.execute - NO ORM
        sql = "DELETE FROM customers WHERE customer_id = %s"
        
        with db.get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (customer_id,))
                conn.commit()
        
        return redirect(url_for("customers.customers_ui"))
    
    except Exception as e:
        logger.error(f"Error deleting customer: {e}")
        # On error, redirect back to list (could also flash a message)
        return redirect(url_for("customers.customers_ui"))
