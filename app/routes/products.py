from flask import Blueprint, request, jsonify
from app.db import db
import logging

logger = logging.getLogger(__name__)

products_bp = Blueprint("products", __name__, url_prefix="/products")

@products_bp.get("/sample")
def products_sample():
    q = request.args.get("n")
    try:
        n = int(q)
    except (TypeError, ValueError):
        return jsonify(error="n must be integer in [1,100]"), 422
    if not (1 <= n <= 100):
        return jsonify(error="n must be between 1 and 100"), 422

    items = [{"product_id": i, "name": f"placeholder_{i}"} for i in range(1, n+1)]
    return jsonify(items=items)


@products_bp.get("/by-category")
def products_by_category():
    """Get products filtered by category_id with optional limit."""
    category_id_str = request.args.get("category_id")
    limit_str = request.args.get("limit", "10")
    
    # Validate category_id
    if not category_id_str:
        return jsonify({"error": "Missing required parameter: category_id"}), 400
    
    try:
        category_id = int(category_id_str)
        if category_id <= 0:
            return jsonify({"error": "category_id must be a positive integer"}), 400
    except ValueError:
        return jsonify({"error": "category_id must be a valid integer"}), 400
    
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
            p.product_id,
            p.category_id,
            c.category_name,
            c.category_name_english,
            p.product_weight_g,
            p.product_length_cm
        FROM products p
        JOIN categories c ON p.category_id = c.category_id
        WHERE p.category_id = %s
        ORDER BY p.product_id
        LIMIT %s
        """
        
        with db.get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (category_id, limit))
                rows = cur.fetchall()
        
        products = [
            {
                "product_id": row[0],
                "category_id": row[1],
                "category_name": row[2],
                "category_name_english": row[3],
                "product_weight_g": row[4],
                "product_length_cm": row[5]
            }
            for row in rows
        ]
        
        return jsonify({
            "category_id": category_id,
            "limit": limit,
            "row_count": len(products),
            "products": products
        })
    
    except Exception as e:
        logger.error(f"Error fetching products by category: {e}")
        return jsonify({"error": "Database error occurred"}), 500


@products_bp.get("/top-categories")
def products_top_categories():
    """Get top categories by product count."""
    limit_str = request.args.get("limit", "10")
    
    # Validate limit
    try:
        limit = int(limit_str)
        if not (1 <= limit <= 50):
            return jsonify({"error": "limit must be between 1 and 50"}), 400
    except ValueError:
        return jsonify({"error": "limit must be a valid integer"}), 400
    
    try:
        sql = """
        SELECT 
            c.category_id,
            c.category_name,
            COUNT(p.product_id) AS product_count
        FROM categories c
        LEFT JOIN products p ON c.category_id = p.category_id
        GROUP BY c.category_id, c.category_name
        ORDER BY product_count DESC
        LIMIT %s
        """
        
        with db.get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (limit,))
                rows = cur.fetchall()
        
        categories = [
            {
                "category_id": row[0],
                "category_name": row[1],
                "product_count": row[2]
            }
            for row in rows
        ]
        
        return jsonify({
            "limit": limit,
            "categories": categories
        })
    
    except Exception as e:
        logger.error(f"Error fetching top categories: {e}")
        return jsonify({"error": "Database error occurred"}), 500
