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
