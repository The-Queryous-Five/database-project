"""
Usage: python db/etl/load_products.py data/raw/olist_products_dataset.csv
Parametrik INSERT kullan; executemany ile batch ekle.
DRY_RUN=1 ile DB'siz veri önizleme.
"""
from db.etl.etl_utils import get_env_bool, iter_batches, dry_insert_preview
import csv
from typing import Optional

BATCH_SIZE = 5000


def load_products(csv_path: str):  # olist_products_dataset.csv
    DRY_RUN = get_env_bool("DRY_RUN")

    def to_int(x: Optional[str]) -> Optional[int]:
        try:
            return int(x) if x not in (None, '') else None
        except ValueError:
            return None

    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        def gen_rows():
            for row in reader:
                pid = (row.get('product_id') or '').strip()
                if not pid:
                    continue
                cat_name = (row.get('product_category_name') or '').strip() or None
                w = to_int(row.get('product_weight_g'))
                l = to_int(row.get('product_length_cm'))
                h = to_int(row.get('product_height_cm'))
                wcm = to_int(row.get('product_width_cm'))
                photos = to_int(row.get('product_photos_qty'))
                yield (pid, w, l, h, wcm, photos, cat_name, None)  # category_id=None in dry-run

        all_rows = list(gen_rows())

        if DRY_RUN:
            dry_insert_preview("products", all_rows, len(all_rows))
            print("[DRY_RUN] Note: category_id mapping requires DB; shown as None")
            return

        # Real DB insert with category_id mapping
        from app.db.db import get_conn
        sql = (
            "INSERT INTO products("
            "product_id, product_weight_g, product_length_cm, product_height_cm, product_width_cm, "
            "product_photos_qty, product_category_name, category_id) "
            "VALUES (%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT (product_id) DO NOTHING"
        )
        with get_conn() as conn:
            # Load category map
            with conn.cursor() as cur:
                cur.execute("SELECT category_name, category_id FROM categories")
                cat_map = {name: cid for (name, cid) in cur.fetchall() if name}

            # Re-process rows with category_id
            def gen_rows_with_cat():
                with open(csv_path, newline='', encoding='utf-8') as f2:
                    reader2 = csv.DictReader(f2)
                    for row in reader2:
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
                for batch in iter_batches(gen_rows_with_cat(), BATCH_SIZE):
                    cur.executemany(sql, batch)
                    total += len(batch)
                print(f"products loaded: {total}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python db/etl/load_products.py <csv_path>")
        print("Set DRY_RUN=1 for data preview without DB")
        sys.exit(1)
    load_products(sys.argv[1])
