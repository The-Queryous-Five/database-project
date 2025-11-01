from flask import request, jsonify
from app.blueprints.customers import bp
from .service import customers_by_state

@bp.get("/by-state")
def by_state():
    state = request.args.get("state")
    if not state or not state.strip():
        return jsonify({"error": "state parameter is required"}), 400
    return jsonify(customers_by_state(state.strip()))
