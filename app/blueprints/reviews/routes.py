from flask import request, jsonify
from app.blueprints.reviews import bp
from .service import reviews_sample, recent_reviews

@bp.get("/sample")
def sample():
    """
    GET /reviews/sample?n=10
    Returns n sample reviews (1-100). Default is 10.
    """
    n_str = request.args.get("n", "10")
    try:
        n = int(n_str)
        if n < 1 or n > 100:
            return jsonify({"error": "n must be between 1 and 100"}), 422
    except ValueError:
        return jsonify({"error": "n must be an integer"}), 422
    return jsonify(reviews_sample(n))

@bp.get("/recent")
def recent():
    """
    GET /reviews/recent
    Returns the 20 most recent reviews ordered by creation date.
    """
    return jsonify(recent_reviews())
