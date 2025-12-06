"""
Usage: python db/etl/load_reviews.py data/raw/olist_order_reviews_dataset.csv
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


def load_reviews(csv_path: str):  # olist_order_reviews_dataset.csv
    """
    Loads reviews without customer_id (NULL), then updates from orders table,
    checks orphans, and tightens NOT NULL if safe.
    """
    insert_sql = (
        "INSERT IGNORE INTO order_reviews(review_id, order_id, review_score, review_comment_message, review_creation_date) "
        "VALUES (%s,%s,%s,%s,%s)"
    )
    with open(csv_path, newline='', encoding='utf-8-sig') as f, get_conn() as conn, conn.cursor() as cur:
        reader = csv.DictReader(f)
        def to_int(x: Optional[str]):
            try:
                return int(x) if x not in (None, '') else None
            except ValueError:
                return None
        def gen_rows():
            for row in reader:
                rid = (row.get('review_id') or '').strip()
                if not rid:
                    continue
                oid = (row.get('order_id') or '').strip() or None
                score = to_int(row.get('review_score'))
                msg = row.get('review_comment_message')
                if msg is not None:
                    msg = msg.strip() or None
                cdate = (row.get('review_creation_date') or '').strip() or None
                yield (rid, oid, score, msg, cdate)
        total = 0
        for batch in _iter_batches(gen_rows()):
            cur.executemany(insert_sql, batch)
            total += len(batch)
        print(f"order_reviews loaded: {total}")

        # Update customer_id from orders after load
        print("Updating order_reviews.customer_id from orders...")
        cur.execute(
            """
            UPDATE order_reviews r
            JOIN orders o ON r.order_id = o.order_id
            SET r.customer_id = o.customer_id
            WHERE r.customer_id IS NULL
            """
        )
        # Orphan check (customer_id still NULL?)
        cur.execute("SELECT COUNT(*) FROM order_reviews WHERE customer_id IS NULL")
        (orphans,) = cur.fetchone()
        print(f"order_reviews.customer_id NULL count: {orphans}")
        if orphans == 0:
            print("Tightening NOT NULL on order_reviews.customer_id...")
            cur.execute("ALTER TABLE order_reviews MODIFY customer_id VARCHAR(255) NOT NULL")
        else:
            print("Skipping NOT NULL alter due to remaining NULLs.")


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python db/etl/load_reviews.py <csv_path>")
        sys.exit(1)
    load_reviews(sys.argv[1])
