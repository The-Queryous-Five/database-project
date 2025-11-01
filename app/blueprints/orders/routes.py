from flask import request, jsonify
from app.blueprints.orders import bp
from .service import last_orders
from datetime import datetime

@bp.get("/last")
def last():
    from_date = request.args.get("from")
    to_date = request.args.get("to")
    
    # Optional date range validation
    if from_date:
        try:
            datetime.fromisoformat(from_date.replace('Z', '+00:00'))
        except ValueError:
            return jsonify({"error": "from must be valid ISO date format"}), 422
    
    if to_date:
        try:
            datetime.fromisoformat(to_date.replace('Z', '+00:00'))
        except ValueError:
            return jsonify({"error": "to must be valid ISO date format"}), 422
    
    return jsonify(last_orders(from_date, to_date))
