from flask import Flask
from app.routes.customers import bp_customers
def create_app():
    app = Flask(__name__)
    app.register_blueprint(bp_customers)
    @app.get("/health")
    def health(): return {"ok": True}
    return app
app = create_app()
