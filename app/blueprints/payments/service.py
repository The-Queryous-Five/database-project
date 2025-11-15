from app.db.db import get_conn
def _rows(sql, params=None):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(sql, params or ())
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, r)) for r in cur.fetchall()]
def payment_mix():
    return _rows("""
        SELECT payment_type, COUNT(*) n, ROUND(SUM(payment_value)::numeric,2) total
        FROM order_payments GROUP BY payment_type ORDER BY total DESC
    """)
def payment_by_installments(m):
    return _rows("""
        SELECT payment_type, payment_installments, COUNT(*) n,
               ROUND(SUM(payment_value)::numeric,2) total
        FROM order_payments
        WHERE payment_installments >= %s
        GROUP BY payment_type, payment_installments
        ORDER BY payment_installments, total DESC
    """, (m,))

def get_payments_by_type(payment_type: str):
    """
    Return count and total payment_value for a given payment_type.
    Works both on PostgreSQL and MySQL via db.get_conn().
    """
    sql = """
    SELECT payment_type,
           COUNT(*) AS payment_count,
           SUM(payment_value) AS total_value
    FROM order_payments
    WHERE payment_type = %s
    GROUP BY payment_type
    """
    conn = None
    cursor = None
    try:
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute(sql, (payment_type,))
        row = cursor.fetchone()
        
        if not row:
            return {
                "payment_type": payment_type,
                "payment_count": 0,
                "total_value": 0.0,
            }
        
        return {
            "payment_type": row[0],
            "payment_count": int(row[1]),
            "total_value": float(row[2] or 0),
        }
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
