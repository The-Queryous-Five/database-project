from app.db.db import get_conn

def reviews_sample(n=10):
    sql = "SELECT review_id, order_id, customer_id, review_score, review_comment_message, review_creation_date FROM order_reviews LIMIT %s"
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(sql, (n,))
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, r)) for r in cur.fetchall()]

def recent_reviews():
    sql = """
    SELECT review_id, customer_id, review_score, review_creation_date
    FROM order_reviews ORDER BY review_creation_date DESC LIMIT 20
    """
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(sql)
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, r)) for r in cur.fetchall()]
