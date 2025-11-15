from flask import request, jsonify
from app.blueprints.payments import bp
from .service import payment_mix, payment_by_installments, get_payments_by_type

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

@bp.get("/by-type")
def by_type():
    payment_type = request.args.get("payment_type")
    
    if not payment_type:
        return jsonify({"error": "payment_type is required"}), 400
    
    if not payment_type.strip():
        return jsonify({"error": "payment_type must be non-empty"}), 422
    
    try:
        result = get_payments_by_type(payment_type)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": "internal error"}), 500
