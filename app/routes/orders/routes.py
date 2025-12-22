from flask import Blueprint, request, jsonify
from app.db import db
import logging
import uuid
from datetime import datetime

# Az önce yazdığımız service fonksiyonunu import ediyoruz
from .service import get_orders_by_customer 

logger = logging.getLogger(__name__)

# 'orders' adında yeni bir Blueprint (Flask modülü) oluşturuyoruz
orders_bp = Blueprint('orders', __name__, url_prefix='/orders')


# ============================================================
# CRUD OPERATIONS FOR ORDERS
# ============================================================

@orders_bp.post("/")
def create_order():
    """
    CREATE: Yeni bir sipariş oluşturur.
    POST /orders/
    Body: { customer_id, order_status, payment_type, payment_value }
    """
    try:
        data = request.get_json()
        
        # Validation
        if not data:
            return jsonify({"error": "Request body is required"}), 400
        
        customer_id = data.get('customer_id')
        order_status = data.get('order_status', 'processing')
        payment_type = data.get('payment_type', 'credit_card')
        payment_value = data.get('payment_value', 0)
        
        if not customer_id:
            return jsonify({"error": "customer_id is required"}), 400
        
        if not payment_value or float(payment_value) <= 0:
            return jsonify({"error": "payment_value must be greater than 0"}), 400
        
        # Generate new order ID
        order_id = str(uuid.uuid4()).replace('-', '')[:32]
        purchase_timestamp = datetime.now()
        
        with db.get_conn() as conn:
            with conn.cursor() as cur:
                # Verify customer exists
                cur.execute("SELECT customer_id FROM customers WHERE customer_id = %s", (customer_id,))
                if not cur.fetchone():
                    return jsonify({"error": "Customer not found"}), 404
                
                # Insert order
                sql_order = """
                INSERT INTO orders (order_id, customer_id, order_status, order_purchase_timestamp)
                VALUES (%s, %s, %s, %s)
                """
                cur.execute(sql_order, (order_id, customer_id, order_status, purchase_timestamp))
                
                # Insert payment
                sql_payment = """
                INSERT INTO order_payments (order_id, payment_sequential, payment_type, payment_installments, payment_value)
                VALUES (%s, 1, %s, 1, %s)
                """
                cur.execute(sql_payment, (order_id, payment_type, float(payment_value)))
                
                conn.commit()
                
                return jsonify({
                    "message": "Order created successfully",
                    "order_id": order_id,
                    "customer_id": customer_id,
                    "order_status": order_status,
                    "payment_type": payment_type,
                    "payment_value": float(payment_value)
                }), 201
                
    except Exception as e:
        logger.error(f"Error creating order: {e}")
        return jsonify({"error": f"Failed to create order: {str(e)}"}), 500


@orders_bp.get("/<string:order_id>")
def get_order(order_id):
    """
    READ: Tek bir siparişi ID ile getirir.
    GET /orders/<order_id>
    """
    try:
        sql = """
        SELECT 
            o.order_id,
            o.customer_id,
            o.order_status,
            o.order_purchase_timestamp,
            o.order_estimated_delivery_date,
            c.customer_city,
            c.customer_state,
            p.payment_type,
            p.payment_value
        FROM orders o
        LEFT JOIN customers c ON o.customer_id = c.customer_id
        LEFT JOIN order_payments p ON o.order_id = p.order_id AND p.payment_sequential = 1
        WHERE o.order_id = %s
        """
        
        with db.get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (order_id,))
                row = cur.fetchone()
                
                if row:
                    return jsonify({
                        "order_id": row[0],
                        "customer_id": row[1],
                        "order_status": row[2],
                        "order_purchase_timestamp": row[3].isoformat() if row[3] else None,
                        "order_estimated_delivery_date": row[4].isoformat() if row[4] else None,
                        "customer_city": row[5],
                        "customer_state": row[6],
                        "payment_type": row[7],
                        "payment_value": float(row[8]) if row[8] else 0
                    }), 200
                else:
                    return jsonify({"error": "Order not found"}), 404
                    
    except Exception as e:
        logger.error(f"Error fetching order: {e}")
        return jsonify({"error": "Failed to fetch order"}), 500


@orders_bp.put("/<string:order_id>")
def update_order(order_id):
    """
    UPDATE: Mevcut bir siparişi günceller.
    PUT /orders/<order_id>
    Body: { order_status, payment_type, payment_value }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Request body is required"}), 400
        
        order_status = data.get('order_status')
        payment_type = data.get('payment_type')
        payment_value = data.get('payment_value')
        
        with db.get_conn() as conn:
            with conn.cursor() as cur:
                # Check if order exists
                cur.execute("SELECT order_id FROM orders WHERE order_id = %s", (order_id,))
                if not cur.fetchone():
                    return jsonify({"error": "Order not found"}), 404
                
                # Update order status
                if order_status:
                    sql_order = "UPDATE orders SET order_status = %s WHERE order_id = %s"
                    cur.execute(sql_order, (order_status, order_id))
                
                # Update payment
                if payment_type or payment_value:
                    update_parts = []
                    params = []
                    
                    if payment_type:
                        update_parts.append("payment_type = %s")
                        params.append(payment_type)
                    
                    if payment_value:
                        update_parts.append("payment_value = %s")
                        params.append(float(payment_value))
                    
                    if update_parts:
                        params.append(order_id)
                        sql_payment = f"UPDATE order_payments SET {', '.join(update_parts)} WHERE order_id = %s AND payment_sequential = 1"
                        cur.execute(sql_payment, params)
                
                conn.commit()
                
                return jsonify({
                    "message": "Order updated successfully",
                    "order_id": order_id
                }), 200
                
    except Exception as e:
        logger.error(f"Error updating order: {e}")
        return jsonify({"error": f"Failed to update order: {str(e)}"}), 500


@orders_bp.delete("/<string:order_id>")
def delete_order(order_id):
    """
    DELETE: Bir siparişi siler.
    DELETE /orders/<order_id>
    """
    try:
        with db.get_conn() as conn:
            with conn.cursor() as cur:
                # Check if order exists
                cur.execute("SELECT order_id FROM orders WHERE order_id = %s", (order_id,))
                if not cur.fetchone():
                    return jsonify({"error": "Order not found"}), 404
                
                # Delete related records first (FK constraints)
                cur.execute("DELETE FROM order_payments WHERE order_id = %s", (order_id,))
                cur.execute("DELETE FROM order_reviews WHERE order_id = %s", (order_id,))
                cur.execute("DELETE FROM order_items WHERE order_id = %s", (order_id,))
                
                # Delete order
                cur.execute("DELETE FROM orders WHERE order_id = %s", (order_id,))
                
                conn.commit()
                
                return jsonify({
                    "message": "Order deleted successfully",
                    "order_id": order_id
                }), 200
                
    except Exception as e:
        logger.error(f"Error deleting order: {e}")
        return jsonify({"error": f"Failed to delete order: {str(e)}"}), 500


@orders_bp.get("/customers/list")
def get_customers_for_dropdown():
    """
    Get list of customers for dropdown selection.
    GET /orders/customers/list
    """
    try:
        sql = """
        SELECT DISTINCT customer_id, customer_city, customer_state 
        FROM customers 
        ORDER BY customer_city 
        LIMIT 100
        """
        
        with db.get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                rows = cur.fetchall()
                
                customers = []
                for row in rows:
                    customers.append({
                        "customer_id": row[0],
                        "customer_city": row[1],
                        "customer_state": row[2],
                        "label": f"{row[1]}, {row[2]} ({row[0][:8]}...)"
                    })
                
                return jsonify(customers), 200
                
    except Exception as e:
        logger.error(f"Error fetching customers: {e}")
        return jsonify({"error": "Failed to fetch customers"}), 500

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
            AVG(items_per_order) as avg_items_per_order,
            COALESCE(SUM(p.payment_value), 0) as total_revenue
        FROM orders o
        LEFT JOIN (
            SELECT order_id, COUNT(*) as items_per_order
            FROM order_items
            GROUP BY order_id
        ) oi ON o.order_id = oi.order_id
        LEFT JOIN order_payments p ON o.order_id = p.order_id
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
                        "total_revenue": float(row[3]) if row[3] else 0.0
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