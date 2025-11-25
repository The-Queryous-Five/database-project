from flask import Blueprint, request, jsonify
from app.db import db
import logging

logger = logging.getLogger(__name__)

bp_reviews = Blueprint("reviews", __name__, url_prefix="/reviews")


@bp_reviews.get("/stats")
def reviews_stats():
    """Get review statistics filtered by score range."""
    min_score_str = request.args.get("min_score")
    max_score_str = request.args.get("max_score")
    
    # Validate min_score
    if not min_score_str:
        return jsonify({"error": "Missing required parameter: min_score"}), 400
    
    try:
        min_score = int(min_score_str)
        if not (1 <= min_score <= 5):
            return jsonify({"error": "min_score must be between 1 and 5"}), 400
    except ValueError:
        return jsonify({"error": "min_score must be a valid integer"}), 400
    
    # Validate max_score
    if not max_score_str:
        return jsonify({"error": "Missing required parameter: max_score"}), 400
    
    try:
        max_score = int(max_score_str)
        if not (1 <= max_score <= 5):
            return jsonify({"error": "max_score must be between 1 and 5"}), 400
    except ValueError:
        return jsonify({"error": "max_score must be a valid integer"}), 400
    
    # Validate range
    if max_score < min_score:
        return jsonify({"error": "max_score must be greater than or equal to min_score"}), 400
    
    try:
        sql = """
        SELECT 
            review_score,
            COUNT(*) AS review_count
        FROM order_reviews
        WHERE review_score BETWEEN %s AND %s
        GROUP BY review_score
        ORDER BY review_score
        """
        
        with db.get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (min_score, max_score))
                rows = cur.fetchall()
        
        stats = [
            {
                "review_score": row[0],
                "review_count": row[1]
            }
            for row in rows
        ]
        
        # Calculate totals
        total_reviews = sum(item["review_count"] for item in stats)
        
        if total_reviews > 0:
            weighted_sum = sum(item["review_score"] * item["review_count"] for item in stats)
            average_score = weighted_sum / total_reviews
        else:
            average_score = None
        
        return jsonify({
            "min_score": min_score,
            "max_score": max_score,
            "total_reviews": total_reviews,
            "average_score": round(average_score, 2) if average_score is not None else None,
            "stats": stats
        })
    
    except Exception as e:
        logger.error(f"Error fetching review stats: {e}")
        return jsonify({"error": "Database error occurred"}), 500
