import os
from app.db.db import get_conn # Veritabanı bağlantısı için
from psycopg.rows import dict_row # Sonuçları dictionary olarak almak için

def get_orders_by_customer(customer_id: str, limit: int = 10):
    """
    Belirli bir müşterinin son siparişlerini döner.
    Hata durumunda (DB kapalıysa) None döner.
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
    
    try:
        with get_conn() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(sql, (customer_id, limit))
                orders = cur.fetchall()
                return orders
    except Exception as e:
        print(f"[ERROR] get_orders_by_customer db hatası: {e}")
        # Hata durumunda [] yerine None dönüyoruz ki route 503 verebilsin
        return None

def get_sample_customer_ids(limit: int = 5):
    """
    Demo için rastgele/örnek müşteri ID'leri döner.
    """
    # Demo için en son sipariş verenleri çekelim ki veri güncel görünsün
    sql = """
    SELECT DISTINCT customer_id 
    FROM orders 
    LIMIT %s
    """
    
    try:
        with get_conn() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(sql, (limit,))
                results = cur.fetchall()
                # Gelen [{'customer_id': 'xyz'}, ...] listesini ['xyz', ...] haline getiriyoruz
                return [row['customer_id'] for row in results]
    except Exception as e:
        print(f"[ERROR] get_sample_customer_ids db hatası: {e}")
        
        # Eğer DRY_RUN açıksa veya DB yoksa demo patlamasın diye MOCK veri dön
        if os.environ.get('DRY_RUN') == '1':
             return ["871766c5855e863f6eccc05f988b23cb (MOCK DATA)"]
        
        return None