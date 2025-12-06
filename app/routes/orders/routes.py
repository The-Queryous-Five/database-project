from flask import Blueprint, request, jsonify
from app.db import db
import logging

# Az önce yazdığımız service fonksiyonunu import ediyoruz
from .service import get_orders_by_customer 

logger = logging.getLogger(__name__)

# 'orders' adında yeni bir Blueprint (Flask modülü) oluşturuyoruz
orders_bp = Blueprint('orders', __name__, url_prefix='/orders')

#
# Burası senin Hafta 3 görevin olan yeni endpoint:
#
@orders_bp.route('/by-customer/<string:customer_id>', methods=['GET'])
def list_orders_by_customer(customer_id):
    """
    Belirli bir müşterinin siparişlerini listeler.
    GET /orders/by-customer/1234567890?limit=10
    """
    
    # --- Validasyon (Görev 2) ---
    limit_str = request.args.get('limit', '10') # limit'i al, yoksa 10 say

    try:
        limit = int(limit_str)
        if not (1 <= limit <= 50):
            return jsonify({"error": "limit must be between 1 and 50"}), 422
    except ValueError:
        return jsonify({"error": "limit must be a valid integer"}), 422
    # --- Validasyon Sonu ---

    # Servis fonksiyonunu çağır
    orders = get_orders_by_customer(customer_id, limit)
    
    # Sonucu JSON olarak dön
    return jsonify(orders), 200


@orders_bp.get("/stats")
def get_order_stats():
    """
    Get order statistics including total orders, items, and averages.
    GET /orders/stats
    """
    try:
        sql = """
        SELECT 
            COUNT(DISTINCT o.order_id) as total_orders,
            COUNT(oi.order_id) as total_items,
            AVG(items_per_order) as avg_items_per_order
        FROM orders o
        LEFT JOIN (
            SELECT order_id, COUNT(*) as items_per_order
            FROM order_items
            GROUP BY order_id
        ) oi ON o.order_id = oi.order_id
        """
        
        with db.get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                row = cur.fetchone()
                
                if row:
                    return jsonify({
                        "total_orders": int(row[0]) if row[0] else 0,
                        "total_items": int(row[1]) if row[1] else 0,
                        "avg_items_per_order": float(row[2]) if row[2] else 0.0,
                        "total_revenue": 0  # Can be calculated from order_payments if needed
                    }), 200
                else:
                    return jsonify({"error": "No data available"}), 404
                    
    except Exception as e:
        logger.error(f"Error fetching order stats: {e}")
        return jsonify({"error": "Failed to fetch order statistics"}), 500


@orders_bp.get("/recent")
def get_recent_orders():
    """
    Get recent orders with optional limit.
    GET /orders/recent?limit=20
    """
    limit_str = request.args.get('limit', '20')
    
    try:
        limit = int(limit_str)
        if not (1 <= limit <= 100):
            return jsonify({"error": "limit must be between 1 and 100"}), 422
    except ValueError:
        return jsonify({"error": "limit must be a valid integer"}), 422
    
    try:
        sql = """
        SELECT 
            order_id,
            customer_id,
            order_status,
            order_purchase_timestamp,
            order_estimated_delivery_date
        FROM orders
        ORDER BY order_purchase_timestamp DESC
        LIMIT %s
        """
        
        with db.get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (limit,))
                rows = cur.fetchall()
                
                orders = []
                for row in rows:
                    orders.append({
                        "order_id": row[0],
                        "customer_id": row[1],
                        "order_status": row[2],
                        "order_purchase_timestamp": row[3].isoformat() if row[3] else None,
                        "order_delivered_customer_date": None,  # Not available in schema
                        "order_estimated_delivery_date": row[4].isoformat() if row[4] else None
                    })
                
                return jsonify(orders), 200
                    
    except Exception as e:
        logger.error(f"Error fetching recent orders: {e}")
        return jsonify({"error": "Failed to fetch recent orders"}), 500

#
# NOT: Bu 'orders_bp'nin ana app/app.py dosyasında register edilmesi gerekir.
# Eğer edilmediyse, app/app.py'a gidip
# from app.routes.orders.routes import orders_bp
# ...
# app.register_blueprint(orders_bp)
# satırlarını eklemeniz gerekebilir.
#