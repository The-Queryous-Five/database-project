from flask import request, jsonify
from app.blueprints.reviews import bp
from .service import reviews_sample, recent_reviews, get_review_stats

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

@bp.get("/stats")
def stats():
    """
    GET /reviews/stats?min_score=1&max_score=5
    Returns average score and review count for reviews within the score range.
    
    Query params:
        min_score: Minimum review score (1-5, default: 1)
        max_score: Maximum review score (1-5, default: 5)
    
    Returns:
        {
            "min_score": int,
            "max_score": int,
            "avg_score": float,
            "review_count": int
        }
    """
    min_score_str = request.args.get("min_score", "1")
    max_score_str = request.args.get("max_score", "5")
    
    # Validate min_score
    try:
        min_score = int(min_score_str)
    except ValueError:
        return jsonify({"error": "min_score must be an integer"}), 422
    
    # Validate max_score
    try:
        max_score = int(max_score_str)
    except ValueError:
        return jsonify({"error": "max_score must be an integer"}), 422
    
    # Validate range 1-5
    if min_score < 1 or min_score > 5:
        return jsonify({"error": "min_score must be between 1 and 5"}), 422
    
    if max_score < 1 or max_score > 5:
        return jsonify({"error": "max_score must be between 1 and 5"}), 422
    
    # Validate min <= max
    if min_score > max_score:
        return jsonify({"error": "min_score cannot be greater than max_score"}), 422
    
    result = get_review_stats(min_score, max_score)
    
    return jsonify({
        "min_score": min_score,
        "max_score": max_score,
        "avg_score": result["avg_score"],
        "review_count": result["review_count"]
    })
