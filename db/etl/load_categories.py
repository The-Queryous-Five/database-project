"""
Usage: python db/etl/load_categories.py data/raw/product_category_name_translation.csv
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


def load_categories(csv_path: str):  # product_category_name_translation.csv
    """Load categories into categories(category_name, category_name_english).
    Uses parametrized executemany in batches with ON CONFLICT DO NOTHING.
    """
    sql = (
        "INSERT INTO categories(category_name, category_name_english) "
        "VALUES (%s, %s) ON CONFLICT (category_name) DO NOTHING"
    )
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        def gen_rows():
            for row in reader:
                name = (row.get('product_category_name') or '').strip() or None
                name_en = (row.get('product_category_name_english') or '').strip() or None
                if not name:
                    continue
                yield (name, name_en)
        with get_conn() as conn, conn.cursor() as cur:
            total = 0
            for batch in _iter_batches(gen_rows()):
                cur.executemany(sql, batch)
                total += len(batch)
            print(f"categories loaded: {total}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python db/etl/load_categories.py <csv_path>")
        sys.exit(1)
    load_categories(sys.argv[1])
