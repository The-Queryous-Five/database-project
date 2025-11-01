from app.db.db import get_conn

def last_orders(from_date=None, to_date=None):
    """Get last 20 orders, optionally filtered by date range."""
    sql = """
    SELECT order_id, customer_id, order_status, order_purchase_timestamp
    FROM orders 
    WHERE 1=1
    """
    params = []
    
    if from_date:
        sql += " AND order_purchase_timestamp >= %s"
        params.append(from_date)
    
    if to_date:
        sql += " AND order_purchase_timestamp <= %s"
        params.append(to_date)
    
    sql += " ORDER BY order_purchase_timestamp DESC LIMIT 20"
    
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(sql, params or None)
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, r)) for r in cur.fetchall()]
