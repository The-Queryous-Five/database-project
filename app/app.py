from flask import Flask, jsonify, request, session
from flask_cors import CORS
from app.routes.customers import bp_customers
from app.routes.products import products_bp
from app.routes.orders.routes import orders_bp
from app.routes.payments import bp_payments
from app.routes.reviews import bp_reviews
from app.db.db import get_conn
import uuid
from datetime import datetime

def create_app():
    app = Flask(__name__)
    
    # Secret key for session management
    app.secret_key = 'olist-dashboard-secret-key-2025'
    
    # Enable CORS for all routes with credentials support
    CORS(app, supports_credentials=True)
    
    app.register_blueprint(orders_bp)
    app.register_blueprint(bp_customers)
    app.register_blueprint(products_bp)
    app.register_blueprint(bp_payments)
    app.register_blueprint(bp_reviews)

    @app.get("/health")
    def health():
        return {"ok": True}
    
    @app.get("/stats")
    def dashboard_stats():
        """
        Get overall statistics for the dashboard.
        Returns counts for customers, orders, products, and reviews.
        """
        try:
            with get_conn() as conn:
                with conn.cursor() as cur:
                    # Get all stats in one query for efficiency
                    sql = """
                    SELECT 
                        (SELECT COUNT(*) FROM customers) as total_customers,
                        (SELECT COUNT(*) FROM orders) as total_orders,
                        (SELECT COUNT(*) FROM products) as total_products,
                        (SELECT COUNT(*) FROM order_reviews) as total_reviews
                    """
                    cur.execute(sql)
                    row = cur.fetchone()
                    
                    if row:
                        return jsonify({
                            "customers": int(row[0]) if row[0] else 0,
                            "orders": int(row[1]) if row[1] else 0,
                            "products": int(row[2]) if row[2] else 0,
                            "reviews": int(row[3]) if row[3] else 0
                        }), 200
                    else:
                        return jsonify({"error": "No data available"}), 404
        except Exception as e:
            print(f"Error fetching dashboard stats: {e}")
            return jsonify({"error": "Failed to fetch dashboard statistics"}), 500
    
    @app.get("/analytics/sales-trend")
    def analytics_sales_trend():
        """
        Get monthly sales trend data.
        Returns revenue grouped by month for the last 12 months.
        """
        try:
            with get_conn() as conn:
                with conn.cursor() as cur:
                    sql = """
                    SELECT 
                        DATE_FORMAT(o.order_purchase_timestamp, '%Y-%m') as month,
                        COUNT(DISTINCT o.order_id) as order_count,
                        COALESCE(SUM(p.payment_value), 0) as revenue
                    FROM orders o
                    LEFT JOIN order_payments p ON o.order_id = p.order_id
                    WHERE o.order_purchase_timestamp IS NOT NULL
                    GROUP BY DATE_FORMAT(o.order_purchase_timestamp, '%Y-%m')
                    ORDER BY month DESC
                    LIMIT 12
                    """
                    cur.execute(sql)
                    rows = cur.fetchall()
                    
                    # Reverse to get oldest to newest
                    data = []
                    for row in reversed(rows):
                        data.append({
                            "month": row[0],
                            "orders": int(row[1]) if row[1] else 0,
                            "revenue": float(row[2]) if row[2] else 0.0
                        })
                    
                    return jsonify(data), 200
        except Exception as e:
            print(f"Error fetching sales trend: {e}")
            return jsonify({"error": "Failed to fetch sales trend"}), 500
    
    @app.get("/analytics/satisfaction")
    def analytics_satisfaction():
        """
        Get customer satisfaction metrics from reviews.
        """
        try:
            with get_conn() as conn:
                with conn.cursor() as cur:
                    sql = """
                    SELECT 
                        AVG(review_score) as avg_score,
                        COUNT(CASE WHEN review_score >= 4 THEN 1 END) * 100.0 / COUNT(*) as positive_pct,
                        COUNT(CASE WHEN review_score = 3 THEN 1 END) * 100.0 / COUNT(*) as neutral_pct,
                        COUNT(CASE WHEN review_score <= 2 THEN 1 END) * 100.0 / COUNT(*) as negative_pct,
                        COUNT(*) as total_reviews
                    FROM order_reviews
                    WHERE review_score IS NOT NULL
                    """
                    cur.execute(sql)
                    row = cur.fetchone()
                    
                    if row:
                        return jsonify({
                            "avg_score": round(float(row[0]), 2) if row[0] else 0,
                            "positive_pct": round(float(row[1]), 1) if row[1] else 0,
                            "neutral_pct": round(float(row[2]), 1) if row[2] else 0,
                            "negative_pct": round(float(row[3]), 1) if row[3] else 0,
                            "total_reviews": int(row[4]) if row[4] else 0
                        }), 200
                    else:
                        return jsonify({"error": "No data available"}), 404
        except Exception as e:
            print(f"Error fetching satisfaction data: {e}")
            return jsonify({"error": "Failed to fetch satisfaction data"}), 500
    
    # ============================================================
    # COMPLEX SQL QUERIES (ZOR SQL SORGULARI)
    # ============================================================
    
    @app.get("/queries/nested")
    def query_nested():
        """
        NESTED QUERY (Alt Sorgu):
        Ortalama sipariş değerinin üzerinde ödeme yapan siparişleri getirir.
        """
        try:
            with get_conn() as conn:
                with conn.cursor() as cur:
                    sql = """
                    SELECT 
                        o.order_id,
                        o.order_status,
                        p.payment_value,
                        c.customer_city,
                        c.customer_state
                    FROM orders o
                    JOIN order_payments p ON o.order_id = p.order_id
                    JOIN customers c ON o.customer_id = c.customer_id
                    WHERE p.payment_value > (
                        SELECT AVG(payment_value) FROM order_payments
                    )
                    ORDER BY p.payment_value DESC
                    LIMIT 20
                    """
                    cur.execute(sql)
                    rows = cur.fetchall()
                    
                    # Get average for display
                    cur.execute("SELECT AVG(payment_value) FROM order_payments")
                    avg_row = cur.fetchone()
                    avg_value = float(avg_row[0]) if avg_row[0] else 0
                    
                    data = []
                    for row in rows:
                        data.append({
                            "order_id": row[0],
                            "order_status": row[1],
                            "payment_value": float(row[2]) if row[2] else 0,
                            "customer_city": row[3],
                            "customer_state": row[4]
                        })
                    
                    return jsonify({
                        "query_name": "Nested Query (Alt Sorgu)",
                        "description": "Ortalama sipariş değerinin ($" + f"{avg_value:.2f}" + ") üzerinde ödeme yapan siparişler",
                        "sql": """SELECT o.order_id, o.order_status, p.payment_value, c.customer_city
FROM orders o
JOIN order_payments p ON o.order_id = p.order_id
JOIN customers c ON o.customer_id = c.customer_id
WHERE p.payment_value > (SELECT AVG(payment_value) FROM order_payments)
ORDER BY p.payment_value DESC LIMIT 20""",
                        "avg_payment": avg_value,
                        "results": data
                    }), 200
        except Exception as e:
            print(f"Error in nested query: {e}")
            return jsonify({"error": f"Query failed: {str(e)}"}), 500
    
    @app.get("/queries/multi-join")
    def query_multi_join():
        """
        4+ TABLE JOIN:
        Orders, Customers, Order_Items, Products, Sellers tablolarını birleştirir.
        """
        try:
            with get_conn() as conn:
                with conn.cursor() as cur:
                    sql = """
                    SELECT 
                        o.order_id,
                        c.customer_city,
                        c.customer_state,
                        p.product_id,
                        p.product_category_name,
                        s.seller_city,
                        s.seller_state,
                        oi.price,
                        oi.freight_value
                    FROM orders o
                    JOIN customers c ON o.customer_id = c.customer_id
                    JOIN order_items oi ON o.order_id = oi.order_id
                    JOIN products p ON oi.product_id = p.product_id
                    JOIN sellers s ON oi.seller_id = s.seller_id
                    ORDER BY o.order_purchase_timestamp DESC
                    LIMIT 20
                    """
                    cur.execute(sql)
                    rows = cur.fetchall()
                    
                    data = []
                    for row in rows:
                        data.append({
                            "order_id": row[0],
                            "customer_city": row[1],
                            "customer_state": row[2],
                            "product_id": row[3][:8] + "..." if row[3] else None,
                            "category": row[4],
                            "seller_city": row[5],
                            "seller_state": row[6],
                            "price": float(row[7]) if row[7] else 0,
                            "freight": float(row[8]) if row[8] else 0
                        })
                    
                    return jsonify({
                        "query_name": "4+ Table JOIN",
                        "description": "5 tablo birleşimi: Orders, Customers, Order_Items, Products, Sellers",
                        "tables_used": ["orders", "customers", "order_items", "products", "sellers"],
                        "sql": """SELECT o.order_id, c.customer_city, c.customer_state,
       p.product_id, p.product_category_name,
       s.seller_city, s.seller_state, oi.price, oi.freight_value
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
JOIN sellers s ON oi.seller_id = s.seller_id
LIMIT 20""",
                        "results": data
                    }), 200
        except Exception as e:
            print(f"Error in multi-join query: {e}")
            return jsonify({"error": f"Query failed: {str(e)}"}), 500
    
    @app.get("/queries/group-by")
    def query_group_by():
        """
        GROUP BY:
        Kategoriye göre sipariş sayısı ve toplam gelir.
        """
        try:
            with get_conn() as conn:
                with conn.cursor() as cur:
                    sql = """
                    SELECT 
                        COALESCE(p.product_category_name, 'Uncategorized') as category,
                        COUNT(DISTINCT o.order_id) as order_count,
                        COUNT(oi.order_item_id) as item_count,
                        SUM(oi.price) as total_revenue,
                        AVG(oi.price) as avg_price
                    FROM order_items oi
                    JOIN orders o ON oi.order_id = o.order_id
                    JOIN products p ON oi.product_id = p.product_id
                    GROUP BY p.product_category_name
                    ORDER BY total_revenue DESC
                    LIMIT 15
                    """
                    cur.execute(sql)
                    rows = cur.fetchall()
                    
                    data = []
                    for row in rows:
                        data.append({
                            "category": row[0],
                            "order_count": int(row[1]) if row[1] else 0,
                            "item_count": int(row[2]) if row[2] else 0,
                            "total_revenue": float(row[3]) if row[3] else 0,
                            "avg_price": float(row[4]) if row[4] else 0
                        })
                    
                    return jsonify({
                        "query_name": "GROUP BY Query",
                        "description": "Ürün kategorisine göre sipariş sayısı ve toplam gelir",
                        "sql": """SELECT p.product_category_name as category,
       COUNT(DISTINCT o.order_id) as order_count,
       COUNT(oi.order_item_id) as item_count,
       SUM(oi.price) as total_revenue,
       AVG(oi.price) as avg_price
FROM order_items oi
JOIN orders o ON oi.order_id = o.order_id
JOIN products p ON oi.product_id = p.product_id
GROUP BY p.product_category_name
ORDER BY total_revenue DESC""",
                        "results": data
                    }), 200
        except Exception as e:
            print(f"Error in group by query: {e}")
            return jsonify({"error": f"Query failed: {str(e)}"}), 500
    
    @app.get("/queries/outer-join")
    def query_outer_join():
        """
        OUTER JOIN (LEFT JOIN):
        Tüm müşterileri ve varsa siparişlerini gösterir (siparişi olmayan müşteriler dahil).
        """
        try:
            with get_conn() as conn:
                with conn.cursor() as cur:
                    sql = """
                    SELECT 
                        c.customer_id,
                        c.customer_city,
                        c.customer_state,
                        COUNT(o.order_id) as order_count,
                        COALESCE(SUM(p.payment_value), 0) as total_spent
                    FROM customers c
                    LEFT JOIN orders o ON c.customer_id = o.customer_id
                    LEFT JOIN order_payments p ON o.order_id = p.order_id
                    GROUP BY c.customer_id, c.customer_city, c.customer_state
                    HAVING order_count = 0 OR order_count > 0
                    ORDER BY order_count ASC, c.customer_city
                    LIMIT 25
                    """
                    cur.execute(sql)
                    rows = cur.fetchall()
                    
                    data = []
                    no_order_count = 0
                    for row in rows:
                        order_count = int(row[3]) if row[3] else 0
                        if order_count == 0:
                            no_order_count += 1
                        data.append({
                            "customer_id": row[0][:8] + "..." if row[0] else None,
                            "customer_city": row[1],
                            "customer_state": row[2],
                            "order_count": order_count,
                            "total_spent": float(row[4]) if row[4] else 0,
                            "has_orders": order_count > 0
                        })
                    
                    return jsonify({
                        "query_name": "LEFT OUTER JOIN",
                        "description": "Tüm müşteriler ve sipariş bilgileri (siparişi olmayan müşteriler dahil)",
                        "sql": """SELECT c.customer_id, c.customer_city, c.customer_state,
       COUNT(o.order_id) as order_count,
       COALESCE(SUM(p.payment_value), 0) as total_spent
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
LEFT JOIN order_payments p ON o.order_id = p.order_id
GROUP BY c.customer_id, c.customer_city, c.customer_state
ORDER BY order_count ASC""",
                        "customers_without_orders": no_order_count,
                        "results": data
                    }), 200
        except Exception as e:
            print(f"Error in outer join query: {e}")
            return jsonify({"error": f"Query failed: {str(e)}"}), 500
    
    @app.get("/queries/all")
    def get_all_queries():
        """
        Tüm zor sorguların listesini döndürür.
        """
        return jsonify({
            "queries": [
                {
                    "id": "nested",
                    "name": "Nested Query (Alt Sorgu)",
                    "description": "Ortalama değerin üzerindeki siparişleri bulmak için alt sorgu kullanır",
                    "endpoint": "/queries/nested"
                },
                {
                    "id": "multi-join",
                    "name": "4+ Table JOIN",
                    "description": "5 tabloyu birleştirerek detaylı sipariş bilgisi getirir",
                    "endpoint": "/queries/multi-join"
                },
                {
                    "id": "group-by",
                    "name": "GROUP BY Query",
                    "description": "Kategoriye göre gruplama ve aggregation işlemleri",
                    "endpoint": "/queries/group-by"
                },
                {
                    "id": "outer-join",
                    "name": "LEFT OUTER JOIN",
                    "description": "Siparişi olmayan müşterileri de göstermek için LEFT JOIN kullanır",
                    "endpoint": "/queries/outer-join"
                }
            ]
        }), 200
    
    @app.get("/schema")
    def get_schema():
        """
        Database şemasını döndürür (PK/FK ilişkileri ile).
        """
        return jsonify({
            "tables": [
                {
                    "name": "customers",
                    "description": "Müşteri bilgileri",
                    "columns": ["customer_id (PK)", "customer_unique_id", "customer_zip_code_prefix", "customer_city", "customer_state"],
                    "pk": "customer_id",
                    "fk": []
                },
                {
                    "name": "orders",
                    "description": "Sipariş bilgileri",
                    "columns": ["order_id (PK)", "customer_id (FK)", "order_status", "order_purchase_timestamp", "order_estimated_delivery_date"],
                    "pk": "order_id",
                    "fk": [{"column": "customer_id", "references": "customers(customer_id)"}]
                },
                {
                    "name": "order_items",
                    "description": "Sipariş ürün detayları (bridge table)",
                    "columns": ["order_id (PK, FK)", "order_item_id (PK)", "product_id (FK)", "seller_id (FK)", "price", "freight_value"],
                    "pk": "order_id + order_item_id",
                    "fk": [
                        {"column": "order_id", "references": "orders(order_id)"},
                        {"column": "product_id", "references": "products(product_id)"},
                        {"column": "seller_id", "references": "sellers(seller_id)"}
                    ]
                },
                {
                    "name": "order_payments",
                    "description": "Ödeme bilgileri",
                    "columns": ["order_id (PK, FK)", "payment_sequential (PK)", "payment_type", "payment_installments", "payment_value"],
                    "pk": "order_id + payment_sequential",
                    "fk": [{"column": "order_id", "references": "orders(order_id)"}]
                },
                {
                    "name": "order_reviews",
                    "description": "Müşteri değerlendirmeleri",
                    "columns": ["review_id (PK)", "order_id", "customer_id (FK)", "review_score", "review_comment_message"],
                    "pk": "review_id",
                    "fk": [{"column": "customer_id", "references": "customers(customer_id)"}]
                },
                {
                    "name": "products",
                    "description": "Ürün bilgileri",
                    "columns": ["product_id (PK)", "product_category_name", "product_weight_g", "product_length_cm", "product_height_cm", "product_width_cm"],
                    "pk": "product_id",
                    "fk": []
                },
                {
                    "name": "sellers",
                    "description": "Satıcı bilgileri",
                    "columns": ["seller_id (PK)", "seller_zip_code_prefix", "seller_city", "seller_state"],
                    "pk": "seller_id",
                    "fk": []
                }
            ],
            "relationships": [
                "customers (1) ─── (N) orders",
                "orders (1) ─── (N) order_items",
                "orders (1) ─── (N) order_payments",
                "products (1) ─── (N) order_items",
                "sellers (1) ─── (N) order_items",
                "customers (1) ─── (N) order_reviews"
            ]
        }), 200
    
    # ============================================================
    # SESSION / AUTH ENDPOINTS
    # ============================================================
    
    # Simple in-memory user store (for demo purposes)
    users_db = {
        "admin": {"password": "admin123", "name": "Admin User", "role": "admin"},
        "demo": {"password": "demo123", "name": "Demo User", "role": "user"},
    }
    
    @app.post("/auth/login")
    def login():
        """
        Login endpoint - creates a session.
        POST /auth/login
        Body: { username, password }
        """
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Request body is required"}), 400
        
        username = data.get('username', '').strip()
        password = data.get('password', '')
        
        if not username:
            return jsonify({"error": "Username is required"}), 400
        if not password:
            return jsonify({"error": "Password is required"}), 400
        
        user = users_db.get(username)
        if user and user['password'] == password:
            session['user'] = {
                'username': username,
                'name': user['name'],
                'role': user['role'],
                'logged_in_at': datetime.now().isoformat()
            }
            return jsonify({
                "message": "Login successful",
                "user": {
                    "username": username,
                    "name": user['name'],
                    "role": user['role']
                }
            }), 200
        else:
            return jsonify({"error": "Invalid username or password"}), 401
    
    @app.post("/auth/logout")
    def logout():
        """
        Logout endpoint - destroys session.
        POST /auth/logout
        """
        session.pop('user', None)
        return jsonify({"message": "Logged out successfully"}), 200
    
    @app.get("/auth/me")
    def get_current_user():
        """
        Get current logged-in user.
        GET /auth/me
        """
        user = session.get('user')
        if user:
            return jsonify({
                "logged_in": True,
                "user": user
            }), 200
        else:
            return jsonify({
                "logged_in": False,
                "user": None
            }), 200
    
    # ============================================================
    # REVIEWS CRUD ENDPOINTS
    # ============================================================
    
    @app.get("/reviews/stats")
    def get_review_stats():
        """Get review statistics."""
        try:
            with get_conn() as conn:
                with conn.cursor() as cur:
                    sql = """
                    SELECT 
                        COUNT(*) as total_reviews,
                        AVG(review_score) as avg_score
                    FROM order_reviews
                    WHERE review_score IS NOT NULL
                    """
                    cur.execute(sql)
                    row = cur.fetchone()
                    
                    # Get score distribution
                    cur.execute("""
                        SELECT review_score, COUNT(*) as count
                        FROM order_reviews
                        WHERE review_score IS NOT NULL
                        GROUP BY review_score
                        ORDER BY review_score DESC
                    """)
                    dist_rows = cur.fetchall()
                    
                    distribution = [{"score": int(r[0]), "count": int(r[1])} for r in dist_rows]
                    
                    return jsonify({
                        "total_reviews": int(row[0]) if row[0] else 0,
                        "avg_score": float(row[1]) if row[1] else 0,
                        "score_distribution": distribution
                    }), 200
        except Exception as e:
            print(f"Error fetching review stats: {e}")
            return jsonify({"error": str(e)}), 500
    
    @app.get("/reviews/recent")
    def get_recent_reviews():
        """Get recent reviews with optional filters."""
        limit = request.args.get('limit', 20, type=int)
        score_filter = request.args.get('score', type=int)
        
        try:
            with get_conn() as conn:
                with conn.cursor() as cur:
                    sql = """
                    SELECT 
                        review_id,
                        order_id,
                        review_score,
                        review_comment_message,
                        review_creation_date
                    FROM order_reviews
                    WHERE review_score IS NOT NULL
                    """
                    params = []
                    
                    if score_filter:
                        sql += " AND review_score = %s"
                        params.append(score_filter)
                    
                    sql += " ORDER BY review_creation_date DESC LIMIT %s"
                    params.append(limit)
                    
                    cur.execute(sql, params)
                    rows = cur.fetchall()
                    
                    reviews = []
                    for row in rows:
                        reviews.append({
                            "review_id": row[0],
                            "order_id": row[1],
                            "review_score": int(row[2]) if row[2] else 0,
                            "review_comment_title": "",
                            "review_comment_message": row[3] or "",
                            "review_creation_date": row[4].isoformat() if row[4] else None
                        })
                    
                    return jsonify(reviews), 200
        except Exception as e:
            print(f"Error fetching recent reviews: {e}")
            return jsonify({"error": str(e)}), 500
    
    @app.post("/reviews/")
    def create_review():
        """
        CREATE: Add a new review.
        POST /reviews/
        Body: { order_id, review_score, review_comment_message }
        """
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Request body is required"}), 400
        
        order_id = data.get('order_id')
        review_score = data.get('review_score')
        review_comment = data.get('review_comment_message', '')
        
        # Validation
        if not order_id:
            return jsonify({"error": "Order ID is required"}), 400
        if not review_score or not (1 <= int(review_score) <= 5):
            return jsonify({"error": "Review score must be between 1 and 5"}), 400
        
        try:
            with get_conn() as conn:
                with conn.cursor() as cur:
                    # Check order exists
                    cur.execute("SELECT customer_id FROM orders WHERE order_id = %s", (order_id,))
                    order = cur.fetchone()
                    if not order:
                        return jsonify({"error": "Order not found"}), 404
                    
                    customer_id = order[0]
                    review_id = str(uuid.uuid4()).replace('-', '')[:32]
                    
                    sql = """
                    INSERT INTO order_reviews (review_id, order_id, customer_id, review_score, review_comment_message, review_creation_date)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """
                    cur.execute(sql, (review_id, order_id, customer_id, int(review_score), review_comment, datetime.now()))
                    conn.commit()
                    
                    return jsonify({
                        "message": "Review created successfully",
                        "review_id": review_id
                    }), 201
        except Exception as e:
            print(f"Error creating review: {e}")
            return jsonify({"error": str(e)}), 500
    
    @app.put("/reviews/<string:review_id>")
    def update_review(review_id):
        """
        UPDATE: Modify an existing review.
        PUT /reviews/<review_id>
        Body: { review_score, review_comment_message }
        """
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Request body is required"}), 400
        
        try:
            with get_conn() as conn:
                with conn.cursor() as cur:
                    # Check review exists
                    cur.execute("SELECT review_id FROM order_reviews WHERE review_id = %s", (review_id,))
                    if not cur.fetchone():
                        return jsonify({"error": "Review not found"}), 404
                    
                    update_parts = []
                    params = []
                    
                    if 'review_score' in data:
                        score = int(data['review_score'])
                        if not (1 <= score <= 5):
                            return jsonify({"error": "Review score must be between 1 and 5"}), 400
                        update_parts.append("review_score = %s")
                        params.append(score)
                    
                    if 'review_comment_message' in data:
                        update_parts.append("review_comment_message = %s")
                        params.append(data['review_comment_message'])
                    
                    if update_parts:
                        params.append(review_id)
                        sql = f"UPDATE order_reviews SET {', '.join(update_parts)} WHERE review_id = %s"
                        cur.execute(sql, params)
                        conn.commit()
                    
                    return jsonify({"message": "Review updated successfully"}), 200
        except Exception as e:
            print(f"Error updating review: {e}")
            return jsonify({"error": str(e)}), 500
    
    @app.delete("/reviews/<string:review_id>")
    def delete_review(review_id):
        """
        DELETE: Remove a review.
        DELETE /reviews/<review_id>
        """
        try:
            with get_conn() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT review_id FROM order_reviews WHERE review_id = %s", (review_id,))
                    if not cur.fetchone():
                        return jsonify({"error": "Review not found"}), 404
                    
                    cur.execute("DELETE FROM order_reviews WHERE review_id = %s", (review_id,))
                    conn.commit()
                    
                    return jsonify({"message": "Review deleted successfully"}), 200
        except Exception as e:
            print(f"Error deleting review: {e}")
            return jsonify({"error": str(e)}), 500
    
    @app.get("/reviews/orders-without-review")
    def get_orders_without_review():
        """Get orders that don't have a review yet (for dropdown)."""
        try:
            with get_conn() as conn:
                with conn.cursor() as cur:
                    sql = """
                    SELECT o.order_id, o.order_purchase_timestamp, c.customer_city
                    FROM orders o
                    LEFT JOIN order_reviews r ON o.order_id = r.order_id
                    JOIN customers c ON o.customer_id = c.customer_id
                    WHERE r.review_id IS NULL
                    AND o.order_status = 'delivered'
                    ORDER BY o.order_purchase_timestamp DESC
                    LIMIT 50
                    """
                    cur.execute(sql)
                    rows = cur.fetchall()
                    
                    orders = []
                    for row in rows:
                        orders.append({
                            "order_id": row[0],
                            "order_date": row[1].strftime('%Y-%m-%d') if row[1] else '',
                            "customer_city": row[2],
                            "label": f"{row[0][:8]}... - {row[2]} ({row[1].strftime('%Y-%m-%d') if row[1] else 'N/A'})"
                        })
                    
                    return jsonify(orders), 200
        except Exception as e:
            print(f"Error fetching orders: {e}")
            return jsonify({"error": str(e)}), 500
    
    return app

app = create_app()
