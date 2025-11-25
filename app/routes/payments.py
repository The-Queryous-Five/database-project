from flask import Blueprint, request, jsonify
from app.db import db
import logging

logger = logging.getLogger(__name__)

bp_payments = Blueprint("payments", __name__, url_prefix="/payments")


@bp_payments.get("/by-type")
def payments_by_type():
    """Get payments filtered by payment_type with optional limit."""
    payment_type = request.args.get("payment_type")
    limit_str = request.args.get("limit", "20")
    
    # Validate payment_type
    if not payment_type:
        return jsonify({"error": "Missing required parameter: payment_type"}), 400
    
    if not payment_type.strip():
        return jsonify({"error": "payment_type cannot be empty"}), 400
    
    if len(payment_type) > 50:
        return jsonify({"error": "payment_type must not exceed 50 characters"}), 400
    
    # Validate limit
    try:
        limit = int(limit_str)
        if not (1 <= limit <= 200):
            return jsonify({"error": "limit must be between 1 and 200"}), 400
    except ValueError:
        return jsonify({"error": "limit must be a valid integer"}), 400
    
    try:
        sql = """
        SELECT 
            order_id,
            payment_sequential,
            payment_type,
            payment_installments,
            payment_value
        FROM order_payments
        WHERE payment_type = %s
        ORDER BY order_id, payment_sequential
        LIMIT %s
        """
        
        with db.get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (payment_type, limit))
                rows = cur.fetchall()
        
        payments = [
            {
                "order_id": row[0],
                "payment_sequential": row[1],
                "payment_type": row[2],
                "payment_installments": row[3],
                "payment_value": float(row[4]) if row[4] is not None else None
            }
            for row in rows
        ]
        
        return jsonify({
            "payment_type": payment_type,
            "limit": limit,
            "row_count": len(payments),
            "payments": payments
        })
    
    except Exception as e:
        logger.error(f"Error fetching payments by type: {e}")
        return jsonify({"error": "Database error occurred"}), 500
