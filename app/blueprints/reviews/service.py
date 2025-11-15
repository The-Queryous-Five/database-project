from app.db.db import get_conn

def reviews_sample(n=10):
    """
    Get a sample of n reviews from the order_reviews table.
    Returns all review fields including review_id, order_id, customer_id, 
    review_score, review_comment_message, and review_creation_date.
    """
    sql = "SELECT review_id, order_id, customer_id, review_score, review_comment_message, review_creation_date FROM order_reviews LIMIT %s"
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(sql, (n,))
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, r)) for r in cur.fetchall()]

def recent_reviews():
    """
    Get the 20 most recent reviews ordered by review_creation_date.
    Returns review_id, customer_id, review_score, and review_creation_date.
    """
    sql = """
    SELECT review_id, customer_id, review_score, review_creation_date
    FROM order_reviews ORDER BY review_creation_date DESC LIMIT 20
    """
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(sql)
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, r)) for r in cur.fetchall()]

def get_review_stats(min_score: int = 1, max_score: int = 5):
    """
    Return average score and count for reviews with scores between min_score and max_score.
    
    Args:
        min_score: Minimum review score (1-5)
        max_score: Maximum review score (1-5)
    
    Returns:
        dict: Contains avg_score and review_count
    """
    sql = """
    SELECT AVG(review_score) AS avg_score,
           COUNT(*)          AS review_count
    FROM order_reviews
    WHERE review_score BETWEEN %s AND %s
    """
    try:
        with get_conn() as conn, conn.cursor() as cur:
            cur.execute(sql, (min_score, max_score))
            result = cur.fetchone()
            if result:
                return {
                    "avg_score": float(result[0]) if result[0] is not None else 0.0,
                    "review_count": int(result[1])
                }
            return {"avg_score": 0.0, "review_count": 0}
    except Exception:
        # Fallback if DB not available
        return {"avg_score": 0.0, "review_count": 0}
