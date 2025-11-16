from app.db.db import get_conn # Veritabanı bağlantısı için
from psycopg.rows import dict_row # Sonuçları dictionary olarak almak için (JSON için ideal)

def get_orders_by_customer(customer_id: str, limit: int = 10):
    """
    Belirli bir müşterinin son siparişlerini döner.
    """
    sql = """
    SELECT o.order_id,
           o.order_status,
           o.order_purchase_timestamp
    FROM orders o
    WHERE o.customer_id = %s
    ORDER BY o.order_purchase_timestamp DESC
    LIMIT %s
    """
    
    # Plana göre DB'si hazır olmayan SQL'i yazıp bırakabilir.
    # Ama idealde çalıştırmayı denemek için tam kod budur:
    try:
        with get_conn() as conn, conn.cursor(row_factory=dict_row) as cur:
            cur.execute(sql, (customer_id, limit))
            orders = cur.fetchall()
            return orders
    except Exception as e:
        print(f"Error fetching orders by customer: {e}")
        # Hata durumunda boş bir liste veya hata mesajı dönebilirsin
        return [] # Şimdilik boş liste dönelim