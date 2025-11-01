from flask import jsonify
from app.blueprints.orders import bp
from .service import last_orders
@bp.get("/last")
def last():
    return jsonify(last_orders())
