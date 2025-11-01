from flask import Flask, jsonify
from app.db.db import get_conn
def create_app():
    app = Flask(__name__)
    from app.blueprints.customers.routes import bp as customers_bp
    from app.blueprints.orders.routes    import bp as orders_bp
    from app.blueprints.products.routes  import bp as products_bp
    from app.blueprints.payments.routes  import bp as payments_bp
    from app.blueprints.reviews.routes   import bp as reviews_bp
    app.register_blueprint(customers_bp, url_prefix="/customers")
    app.register_blueprint(orders_bp,    url_prefix="/orders")
    app.register_blueprint(products_bp,  url_prefix="/products")
    app.register_blueprint(payments_bp,  url_prefix="/payments")
    app.register_blueprint(reviews_bp,   url_prefix="/reviews")
    @app.get("/health")
    def health():
        try:
            with get_conn() as _:
                return jsonify({"ok": True})
        except Exception as e:
            return jsonify({"ok": False, "err": str(e)}), 500
    return app
app = create_app()
