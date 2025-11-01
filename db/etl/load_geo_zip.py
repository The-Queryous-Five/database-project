"""
Usage: python db/etl/load_geo_zip.py data/raw/olist_geolocation_dataset.csv
Parametrik INSERT kullan; executemany ile batch ekle.
"""
from app.db.db import get_conn
import csv
from typing import Iterable, List, Tuple, Set

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


def load_geo_zip(csv_path: str):  # olist_geolocation_dataset.csv
    """Deduplicate by first seen zip and insert into geo_zip."""
    sql = (
        "INSERT INTO geo_zip(geolocation_zip_code_prefix, geolocation_lat, geolocation_lng, geolocation_city, geolocation_state) "
        "VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING"
    )
    seen: Set[int] = set()
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        def gen_rows():
            for row in reader:
                try:
                    z = row.get('geolocation_zip_code_prefix')
                    if z is None or z == '':
                        continue
                    z_int = int(z)
                except ValueError:
                    continue
                if z_int in seen:
                    continue
                seen.add(z_int)
                lat = row.get('geolocation_lat')
                lng = row.get('geolocation_lng')
                city = row.get('geolocation_city')
                state = row.get('geolocation_state')
                lat_f = float(lat) if lat not in (None, '') else None
                lng_f = float(lng) if lng not in (None, '') else None
                city_s = city.strip() if city else None
                state_s = state.strip() if state else None
                yield (z_int, lat_f, lng_f, city_s, state_s)
        with get_conn() as conn, conn.cursor() as cur:
            total = 0
            for batch in _iter_batches(gen_rows()):
                cur.executemany(sql, batch)
                total += len(batch)
            print(f"geo_zip loaded: {total}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python db/etl/load_geo_zip.py <csv_path>")
        sys.exit(1)
    load_geo_zip(sys.argv[1])
