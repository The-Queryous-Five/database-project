"""
Usage: python db/etl/load_products.py data/raw/olist_products_dataset.csv
Parametrik INSERT kullan; executemany ile batch ekle.
"""
from app.db.db import get_conn
import csv
from typing import Dict, Iterable, List, Tuple, Optional

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


def _load_category_map(conn) -> Dict[str, int]:
    with conn.cursor() as cur:
        cur.execute("SELECT category_name, category_id FROM categories")
        return {name: cid for (name, cid) in cur.fetchall() if name}


def load_products(csv_path: str):  # olist_products_dataset.csv
    sql = (
        "INSERT INTO products("
        "product_id, product_weight_g, product_length_cm, product_height_cm, product_width_cm, "
        "product_photos_qty, product_category_name, category_id) "
        "VALUES (%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT (product_id) DO NOTHING"
    )
    with get_conn() as conn:
        cat_map = _load_category_map(conn)
        with open(csv_path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            def to_int(x: Optional[str]) -> Optional[int]:
                try:
                    return int(x) if x not in (None, '') else None
                except ValueError:
                    return None
            def gen_rows():
                for row in reader:
                    pid = (row.get('product_id') or '').strip()
                    if not pid:
                        continue
                    cat_name = (row.get('product_category_name') or '').strip() or None
                    cid = cat_map.get(cat_name) if cat_name else None
                    w = to_int(row.get('product_weight_g'))
                    l = to_int(row.get('product_length_cm'))
                    h = to_int(row.get('product_height_cm'))
                    wcm = to_int(row.get('product_width_cm'))
                    photos = to_int(row.get('product_photos_qty'))
                    yield (pid, w, l, h, wcm, photos, cat_name, cid)
            with conn.cursor() as cur:
                total = 0
                for batch in _iter_batches(gen_rows()):
                    cur.executemany(sql, batch)
                    total += len(batch)
                print(f"products loaded: {total}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python db/etl/load_products.py <csv_path>")
        sys.exit(1)
    load_products(sys.argv[1])

def load_products(csv_path: str):
    # TODO: products + category_id eşleme (categories ile join)
    pass

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python db/etl/load_products.py <csv_path>")
        sys.exit(1)
    load_products(sys.argv[1])
