"""
Usage: python db/etl/load_customers.py data/raw/olist_customers_dataset.csv
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


def load_customers(csv_path: str):  # olist_customers_dataset.csv
    sql = (
        "INSERT INTO customers(customer_id, customer_unique_id, customer_zip_code_prefix, customer_city, customer_state) "
        "VALUES (%s,%s,%s,%s,%s) ON CONFLICT (customer_id) DO NOTHING"
    )
    with open(csv_path, newline='', encoding='utf-8') as f, get_conn() as conn, conn.cursor() as cur:
        reader = csv.DictReader(f)
        def to_int(x: Optional[str]):
            try:
                return int(x) if x not in (None, '') else None
            except ValueError:
                return None
        def gen_rows():
            for row in reader:
                cid = (row.get('customer_id') or '').strip()
                if not cid:
                    continue
                uid = (row.get('customer_unique_id') or '').strip() or None
                zipi = to_int(row.get('customer_zip_code_prefix'))
                city = (row.get('customer_city') or '').strip() or None
                state = (row.get('customer_state') or '').strip() or None
                yield (cid, uid, zipi, city, state)
        total = 0
        for batch in _iter_batches(gen_rows()):
            cur.executemany(sql, batch)
            total += len(batch)
        print(f"customers loaded: {total}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python db/etl/load_customers.py <csv_path>")
        sys.exit(1)
    load_customers(sys.argv[1])
