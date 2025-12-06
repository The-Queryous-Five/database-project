import os, csv, sys
from app.db.db import get_conn
from typing import Iterable, List, Tuple

DRY = os.getenv("DRY_RUN", "0") in ("1","true","True")
EXPECTED_COLS = {"customer_id","customer_unique_id","customer_zip_code_prefix","customer_city","customer_state"}
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

def read_head(path, n=3):
    with open(path, "r", encoding="utf-8-sig") as f:
        r = csv.DictReader(f); cols=set(r.fieldnames or []); missing = EXPECTED_COLS - cols
        if missing: print(f"[WARN] Missing columns: {missing}")
        head=[]
        for i,row in enumerate(r):
            if i>=n: break
            head.append(row)
        return cols, head
def count_rows(path):
    with open(path, "r", encoding="utf-8-sig") as f: return sum(1 for _ in f)-1

def load_customers(csv_path: str):
    sql = (
        "INSERT IGNORE INTO customers(customer_id, customer_unique_id, customer_zip_code_prefix, customer_city, customer_state) "
        "VALUES (%s,%s,%s,%s,%s)"
    )
    with open(csv_path, newline='', encoding='utf-8-sig') as f, get_conn() as conn, conn.cursor() as cur:
        reader = csv.DictReader(f)
        def to_int(x):
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

def main():
    if len(sys.argv)<2: print("Usage: python db/etl/load_customers.py <csv_path>"); sys.exit(1)
    path=sys.argv[1]
    
    if DRY:
        total=count_rows(path); cols,head=read_head(path)
        print("[DRY_RUN] customers CSV path:", path)
        print("[DRY_RUN] total_rows:", total)
        print("[DRY_RUN] columns:", sorted(list(cols)))
        print("[DRY_RUN] head:")
        for i,row in enumerate(head,1):
            keys=list(row.keys())[:6]; print(f"  {i}. ", {k: row[k] for k in keys})
        print("[INFO] Set DRY_RUN=0 to actually load to database.")
    else:
        load_customers(path)

if __name__=="__main__": main()
