"""
Usage: python db/etl/load_orders.py data/raw/olist_orders_dataset.csv
Parametrik INSERT kullan; executemany ile batch ekle.
"""
from app.db.db import get_conn
import csv
from typing import Iterable, List, Tuple

BATCH_SIZE = 5000


def _iter_batches(rows: Iterable[Tuple], batch_size: int = BATCH_SIZE):
    batch: List[Tuple] = []
    for r in rows:
        batch.append(r)
        if len(batch) >= batch_size:
            yield batch
            batch = []
    if batch:
        yield batch


def load_orders(csv_path: str):  # olist_orders_dataset.csv
    sql = (
        "INSERT INTO orders(order_id, customer_id, order_status, order_purchase_timestamp, order_estimated_delivery_date) "
        "VALUES (%s,%s,%s,%s,%s) ON CONFLICT (order_id) DO NOTHING"
    )
    with open(csv_path, newline='', encoding='utf-8') as f, get_conn() as conn, conn.cursor() as cur:
        reader = csv.DictReader(f)
        def gen_rows():
            for row in reader:
                oid = (row.get('order_id') or '').strip()
                if not oid:
                    continue
                cid = (row.get('customer_id') or '').strip() or None
                status = (row.get('order_status') or '').strip() or None
                ts = (row.get('order_purchase_timestamp') or '').strip() or None
                est = (row.get('order_estimated_delivery_date') or '').strip() or None
                yield (oid, cid, status, ts, est)
        total = 0
        for batch in _iter_batches(gen_rows()):
            cur.executemany(sql, batch)
            total += len(batch)
        print(f"orders loaded: {total}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python db/etl/load_orders.py <csv_path>")
        sys.exit(1)
    load_orders(sys.argv[1])
