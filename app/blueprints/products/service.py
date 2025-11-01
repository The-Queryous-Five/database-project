from app.db.db import get_conn
def products_sample(n=10):
    sql = "SELECT product_id, category_id, product_weight_g, product_photos_qty FROM products LIMIT %s"
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(sql, (n,))
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, r)) for r in cur.fetchall()]
