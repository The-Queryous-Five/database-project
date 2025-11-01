from app.db.db import get_conn
def last_orders():
    sql = """
    SELECT order_id, customer_id, order_status, order_purchase_timestamp
    FROM orders ORDER BY order_purchase_timestamp DESC LIMIT 20
    """
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(sql)
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, r)) for r in cur.fetchall()]
