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
        return {"ok": True}
    
    @app.get("/demo")
    def demo():
        """Demo page explaining features and raw SQL usage."""
        from flask import render_template
        return render_template("demo.html")
    
    return app

app = create_app()
