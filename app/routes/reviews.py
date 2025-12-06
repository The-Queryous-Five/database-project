from flask import Blueprint, request, jsonify
from app.db import db
import logging

logger = logging.getLogger(__name__)

bp_reviews = Blueprint("reviews", __name__, url_prefix="/reviews")


@bp_reviews.get("/stats")
def reviews_stats():
    """Get review statistics including score distribution and averages."""
    # Make parameters optional for dashboard use
    min_score_str = request.args.get("min_score", "1")
    max_score_str = request.args.get("max_score", "5")
    
    # Validate min_score
    try:
        min_score = int(min_score_str)
        if not (1 <= min_score <= 5):
            return jsonify({"error": "min_score must be between 1 and 5"}), 400
    except ValueError:
        return jsonify({"error": "min_score must be a valid integer"}), 400
    
    # Validate max_score
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
        # Get overall stats
        overall_sql = """
        SELECT 
            COUNT(*) as total_reviews,
            AVG(review_score) as avg_score
        FROM order_reviews
        """
        
        # Get score distribution
        dist_sql = """
        SELECT 
            review_score,
            COUNT(*) AS count
        FROM order_reviews
        WHERE review_score BETWEEN %s AND %s
        GROUP BY review_score
        ORDER BY review_score
        """
        
        with db.get_conn() as conn:
            with conn.cursor() as cur:
                # Get overall stats
                cur.execute(overall_sql)
                overall_row = cur.fetchone()
                
                # Get distribution
                cur.execute(dist_sql, (min_score, max_score))
                dist_rows = cur.fetchall()
        
        score_distribution = []
        for row in dist_rows:
            score_distribution.append({
                "score": int(row[0]),
                "count": int(row[1])
            })
        
        return jsonify({
            "total_reviews": int(overall_row[0]) if overall_row[0] else 0,
            "avg_score": float(overall_row[1]) if overall_row[1] else 0.0,
            "score_distribution": score_distribution
        }), 200
    
    except Exception as e:
        logger.error(f"Error fetching review stats: {e}")
        return jsonify({"error": "Database error occurred"}), 500


@bp_reviews.get("/recent")
def get_recent_reviews():
    """
    Get recent reviews with optional limit.
    GET /reviews/recent?limit=20
    """
    limit_str = request.args.get('limit', '20')
    
    try:
        limit = int(limit_str)
        if not (1 <= limit <= 100):
            return jsonify({"error": "limit must be between 1 and 100"}), 422
    except ValueError:
        return jsonify({"error": "limit must be a valid integer"}), 422
    
    try:
        sql = """
        SELECT 
            review_id,
            order_id,
            review_score,
            review_comment_message,
            review_creation_date
        FROM order_reviews
        ORDER BY review_creation_date DESC
        LIMIT %s
        """
        
        with db.get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (limit,))
                rows = cur.fetchall()
                
                reviews = []
                for row in rows:
                    reviews.append({
                        "review_id": row[0],
                        "order_id": row[1],
                        "review_score": int(row[2]) if row[2] else 0,
                        "review_comment_title": None,  # Not available in schema
                        "review_comment_message": row[3],
                        "review_creation_date": row[4].isoformat() if row[4] else None,
                        "review_answer_timestamp": None  # Not available in schema
                    })
                
                return jsonify(reviews), 200
                    
    except Exception as e:
        logger.error(f"Error fetching recent reviews: {e}")
        return jsonify({"error": "Failed to fetch recent reviews"}), 500
