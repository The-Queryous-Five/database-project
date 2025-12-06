"""
Usage: python db/etl/load_payments.py data/raw/olist_order_payments_dataset.csv
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


def load_payments(csv_path: str):  # olist_order_payments_dataset.csv
    sql = (
        "INSERT IGNORE INTO order_payments(order_id, payment_sequential, payment_type, payment_installments, payment_value) "
        "VALUES (%s,%s,%s,%s,%s)"
    )
    with open(csv_path, newline='', encoding='utf-8-sig') as f, get_conn() as conn, conn.cursor() as cur:
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
                seq = to_int(row.get('payment_sequential'))
                ptype = (row.get('payment_type') or '').strip() or None
                inst = to_int(row.get('payment_installments'))
                val = to_float(row.get('payment_value'))
                if seq is None:
                    continue
                yield (oid, seq, ptype, inst, val)
        total = 0
        for batch in _iter_batches(gen_rows()):
            cur.executemany(sql, batch)
            total += len(batch)
        print(f"order_payments loaded: {total}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python db/etl/load_payments.py <csv_path>")
        sys.exit(1)
    load_payments(sys.argv[1])
