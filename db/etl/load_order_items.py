"""
Usage: python db/etl/load_order_items.py data/raw/olist_order_items_dataset.csv
Parametrik INSERT kullan; executemany ile batch ekle.
"""
from app.db.db import get_conn
import csv
from typing import Iterable, List, Tuple, Optional

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


def load_order_items(csv_path: str):  # olist_order_items_dataset.csv
    sql = (
        "INSERT INTO order_items(order_id, order_item_id, product_id, seller_id, shipping_limit_date, price, freight_value) "
        "VALUES (%s,%s,%s,%s,%s,%s,%s) ON CONFLICT (order_id, order_item_id) DO NOTHING"
    )
    with open(csv_path, newline='', encoding='utf-8') as f, get_conn() as conn, conn.cursor() as cur:
        reader = csv.DictReader(f)
        def to_int(x: Optional[str]):
            try:
                return int(x) if x not in (None, '') else None
            except ValueError:
                return None
        def to_float(x: Optional[str]):
            try:
                return float(x) if x not in (None, '') else None
            except ValueError:
                return None
        def gen_rows():
            for row in reader:
                oid = (row.get('order_id') or '').strip()
                if not oid:
                    continue
                item_id = to_int(row.get('order_item_id'))
                pid = (row.get('product_id') or '').strip() or None
                sid = (row.get('seller_id') or '').strip() or None
                ship = (row.get('shipping_limit_date') or '').strip() or None
                price = to_float(row.get('price'))
                freight = to_float(row.get('freight_value'))
                if item_id is None:
                    continue
                yield (oid, item_id, pid, sid, ship, price, freight)
        total = 0
        for batch in _iter_batches(gen_rows()):
            cur.executemany(sql, batch)
            total += len(batch)
        print(f"order_items loaded: {total}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python db/etl/load_order_items.py <csv_path>")
        sys.exit(1)
    load_order_items(sys.argv[1])
