from flask import Flask
from app.routes.customers import bp_customers
from app.routes.products import products_bp
from app.routes.orders.routes import orders_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(orders_bp)
    app.register_blueprint(bp_customers)
    app.register_blueprint(products_bp)

    @app.get("/health")
    def health():
        return {"ok": True}
    return app

app = create_app()
