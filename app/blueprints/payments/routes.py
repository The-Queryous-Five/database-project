from flask import request, jsonify
from app.blueprints.payments import bp
from .service import payment_mix, payment_by_installments

@bp.get("/mix")
def mix():
    return jsonify(payment_mix())

@bp.get("/by-installments")
def by_installments():
    m_str = request.args.get("min", "1")
    try:
        m = int(m_str)
        if m < 1:
            return jsonify({"error": "min must be >= 1"}), 422
    except ValueError:
        return jsonify({"error": "min must be an integer"}), 422
    return jsonify(payment_by_installments(m))
