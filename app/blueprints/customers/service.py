from app.db.db import get_conn
def customers_by_state(state):
    sql = "SELECT customer_id, customer_city, customer_state FROM customers WHERE customer_state = %s LIMIT 50"
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(sql, (state,))
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, r)) for r in cur.fetchall()]
