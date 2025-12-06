import os, sys, pandas as pd
from app.db.db import get_conn
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

def load_products(csv_path: str):
    df = pd.read_csv(csv_path, encoding='utf-8-sig')
    print(f"[products] rows={len(df)}, cols={list(df.columns)}")
    print(df.head(3).to_string(index=False))

    # Bazı hızlı istatistikler (varsa)
    for col in ['name','category_id','category_name','product_category_name']:
        if col in df.columns:
            print(f"[products] null {col}: {df[col].isna().sum()}")

    # Load to database
    sql = (
        "INSERT IGNORE INTO products(product_id, product_weight_g, product_length_cm, product_height_cm, product_width_cm, product_photos_qty, product_category_name, category_id) "
        "VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
    )
    
    with get_conn() as conn, conn.cursor() as cur:
        def gen_rows():
            for _, row in df.iterrows():
                pid = str(row.get('product_id', '')).strip()
                if not pid or pd.isna(pid):
                    continue
                
                # Try to get category_id - might need mapping from product_category_name
                cat_name = row.get('product_category_name')
                cat_id = None
                if pd.notna(cat_name):
                    # Look up category_id from categories table
                    cur.execute(
                        "SELECT category_id FROM categories WHERE category_name = %s LIMIT 1",
                        (str(cat_name).strip(),)
                    )
                    result = cur.fetchone()
                    if result:
                        cat_id = result[0]
                
                weight = int(row['product_weight_g']) if 'product_weight_g' in df.columns and pd.notna(row.get('product_weight_g')) else None
                length = int(row['product_length_cm']) if 'product_length_cm' in df.columns and pd.notna(row.get('product_length_cm')) else None
                height = int(row['product_height_cm']) if 'product_height_cm' in df.columns and pd.notna(row.get('product_height_cm')) else None
                width = int(row['product_width_cm']) if 'product_width_cm' in df.columns and pd.notna(row.get('product_width_cm')) else None
                photos = int(row['product_photos_qty']) if 'product_photos_qty' in df.columns and pd.notna(row.get('product_photos_qty')) else None
                cat_name_str = str(cat_name).strip() if pd.notna(cat_name) else None
                
                yield (pid, weight, length, height, width, photos, cat_name_str, cat_id)
        
        total = 0
        for batch in _iter_batches(gen_rows()):
            cur.executemany(sql, batch)
            total += len(batch)
        print(f"products loaded: {total}")
        
        # Check missing categories
        cur.execute("SELECT COUNT(*) FROM products WHERE category_id IS NULL")
        (missing,) = cur.fetchone()
        print(f"[products] missing category_id = {missing} rows")

def main(path):
    DRY = os.getenv("DRY_RUN", "0") in ("1","true","True")
    
    if DRY:
        df = pd.read_csv(path, encoding='utf-8-sig')
        print(f"[DRY_RUN] [products] rows={len(df)}, cols={list(df.columns)}")
        print(df.head(3).to_string(index=False))
        print("[INFO] Set DRY_RUN=0 to actually load to database.")
    else:
        load_products(path)

if __name__ == "__main__":
    csv_path = sys.argv[1] if len(sys.argv) > 1 else "data/raw/products.csv"
    main(csv_path)
