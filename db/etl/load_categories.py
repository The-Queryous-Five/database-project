"""
Usage: python db/etl/load_categories.py data/raw/product_category_name_translation.csv
Parametrik INSERT kullan; executemany ile batch ekle.
DRY_RUN=1 ile DB'siz veri önizleme.
"""
from db.etl.etl_utils import get_env_bool, iter_batches, dry_insert_preview
import csv
from typing import Iterable, List, Tuple

BATCH_SIZE = 5000


def load_categories(csv_path: str):  # product_category_name_translation.csv
    """Load categories into categories(category_name, category_name_english).
    Uses parametrized executemany in batches with ON CONFLICT DO NOTHING.
    """
    DRY_RUN = get_env_bool("DRY_RUN")
    
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        def gen_rows():
            for row in reader:
                name = (row.get('product_category_name') or '').strip() or None
                name_en = (row.get('product_category_name_english') or '').strip() or None
                if not name:
                    continue
                yield (name, name_en)
        
        all_rows = list(gen_rows())
        
        if DRY_RUN:
            dry_insert_preview("categories", all_rows, len(all_rows))
            return
        
        # Real DB insert
        from app.db.db import get_conn
        sql = (
            "INSERT INTO categories(category_name, category_name_english) "
            "VALUES (%s, %s) ON CONFLICT (category_name) DO NOTHING"
        )
        with get_conn() as conn, conn.cursor() as cur:
            total = 0
            for batch in iter_batches(all_rows, BATCH_SIZE):
                cur.executemany(sql, batch)
                total += len(batch)
            print(f"categories loaded: {total}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python db/etl/load_categories.py <csv_path>")
        print("Set DRY_RUN=1 for data preview without DB")
        sys.exit(1)
    load_categories(sys.argv[1])
