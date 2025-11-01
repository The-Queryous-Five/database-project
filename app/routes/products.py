from flask import Blueprint, request, jsonify

products_bp = Blueprint("products", __name__)

@products_bp.get("/products/sample")
def products_sample():
    q = request.args.get("n")
    try:
        n = int(q)
    except (TypeError, ValueError):
        return jsonify(error="n must be integer in [1,100]"), 422
    if not (1 <= n <= 100):
        return jsonify(error="n must be between 1 and 100"), 422

    items = [{"product_id": i, "name": f"placeholder_{i}"} for i in range(1, n+1)]
    return jsonify(items=items)
