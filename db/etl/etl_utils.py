"""
ETL utility functions for dry-run mode and batch processing.
"""
import csv
import os
from typing import Iterable, List, Tuple, Any


def get_env_bool(key: str, default: bool = False) -> bool:
    """Get boolean from environment variable."""
    val = os.getenv(key, "").strip().lower()
    if val in ("1", "true", "yes", "on"):
        return True
    if val in ("0", "false", "no", "off", ""):
        return default
    return default


def read_csv_in_batches(csv_path: str, batch_size: int = 5000) -> Iterable[List[dict]]:
    """
    Read CSV file in batches.
    Yields batches of dictionaries.
    """
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        batch: List[dict] = []
        for row in reader:
            batch.append(row)
            if len(batch) >= batch_size:
                yield batch
                batch = []
        if batch:
            yield batch


def dry_insert_preview(table: str, rows: List[Tuple], total_count: int):
    """
    Print preview of data for dry-run mode.
    Shows first 3 rows and total count.
    """
    print(f"\n[DRY_RUN] Table: {table}")
    print(f"[DRY_RUN] Total rows to insert: {total_count}")
    print(f"[DRY_RUN] Sample (first 3 rows):")
    for i, row in enumerate(rows[:3], 1):
        print(f"  {i}. {row}")
    print()


def iter_batches(rows: Iterable[Tuple], batch_size: int = 5000) -> Iterable[List[Tuple]]:
    """
    Batch generator for tuple rows.
    """
    batch: List[Tuple] = []
    for r in rows:
        batch.append(r)
        if len(batch) >= batch_size:
            yield batch
            batch = []
    if batch:
        yield batch
