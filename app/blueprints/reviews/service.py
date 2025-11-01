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
