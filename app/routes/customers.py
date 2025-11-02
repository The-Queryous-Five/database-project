from flask import Blueprint, request, jsonify
bp_customers = Blueprint("customers", __name__)
@bp_customers.get("/customers/by-state")
def customers_by_state():
    state = request.args.get("state")
    if not state:
        return jsonify({"error": "Missing required parameter: state"}), 400
    return jsonify({"state": state, "total_customers": 0})
