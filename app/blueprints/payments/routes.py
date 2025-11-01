from flask import request, jsonify
from app.blueprints.payments import bp
from .service import payment_mix, payment_by_installments
@bp.get("/mix")
def mix():
    return jsonify(payment_mix())
@bp.get("/by-installments")
def by_installments():
    m = int(request.args.get("min", 1))
    return jsonify(payment_by_installments(m))
