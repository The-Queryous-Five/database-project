from flask import Flask

from flask_cors import CORS
from app.routes.customers import bp_customers, bp_geo

from app.routes.products import products_bp
from app.routes.orders.routes import orders_bp
from app.routes.payments import bp_payments
from app.routes.reviews import bp_reviews
from app.routes.analytics import bp_analytics

def create_app():
    app = Flask(__name__)
    
    # Enable CORS for all routes
    CORS(app)
    
    app.register_blueprint(orders_bp)
    app.register_blueprint(bp_customers)
    app.register_blueprint(bp_geo)
    app.register_blueprint(products_bp)
    app.register_blueprint(bp_payments)
    app.register_blueprint(bp_reviews)
    app.register_blueprint(bp_analytics)

    @app.get("/health")
    def health():
        """
        Enhanced health check endpoint with database status.
        Returns API status, database connection state, and table counts.
        """
        from app.db.db import get_conn
        from app.config import DB_CFG
        
        response = {
            "api_status": "ok",
            "db_vendor": DB_CFG.get("vendor"),
            "db_host": DB_CFG.get("host"),
            "db_port": DB_CFG.get("port"),
            "db_name": DB_CFG.get("dbname"),
            "db_connected": False,
            "table_counts": {},
            "errors": []
        }
        
        # Try to connect to database and get table counts
        try:
            conn = get_conn()
            response["db_connected"] = True
            
            # Query table counts
            tables = ["customers", "orders", "order_items", "products", "payments", "reviews"]
            
            if DB_CFG.get("vendor") == "mysql":
                cursor = conn.cursor()
                for table in tables:
                    try:
                        cursor.execute(f"SELECT COUNT(*) FROM {table}")
                        count = cursor.fetchone()[0]
                        response["table_counts"][table] = count
                    except Exception as e:
                        response["table_counts"][table] = f"error: {str(e)}"
                cursor.close()
            else:  # postgres
                with conn.cursor() as cur:
                    for table in tables:
                        try:
                            cur.execute(f"SELECT COUNT(*) FROM {table}")
                            count = cur.fetchone()[0]
                            response["table_counts"][table] = count
                        except Exception as e:
                            response["table_counts"][table] = f"error: {str(e)}"
            
            conn.close()
            return response, 200
            
        except ImportError as e:
            response["errors"].append(f"Database driver not installed: {str(e)}")
            return response, 503
        except ConnectionError as e:
            response["errors"].append(f"Database connection failed: {str(e)}")
            return response, 503
        except Exception as e:
            response["errors"].append(f"Unexpected error: {type(e).__name__}: {str(e)}")
            return response, 503
    
    @app.get("/demo")
    def demo():
        """Demo page explaining features and raw SQL usage."""
        from flask import render_template
        return render_template("demo.html")
    
    return app

app = create_app()
