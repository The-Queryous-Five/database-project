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


def get_insert_ignore_sql(table: str, columns: str, placeholders: str, conflict_column: str = None) -> str:
    """
    Generate INSERT IGNORE/ON CONFLICT SQL based on DB vendor.
    
    Args:
        table: Table name
        columns: Column names (e.g., "col1, col2")
        placeholders: Value placeholders (e.g., "%s, %s")
        conflict_column: Column(s) for conflict resolution (optional)
    
    Returns:
        SQL string appropriate for the current DB vendor
    """
    from app.config import DB_CFG
    vendor = DB_CFG.get("vendor", "postgres")
    
    if vendor == "mysql":
        return f"INSERT IGNORE INTO {table}({columns}) VALUES ({placeholders})"
    else:  # postgres
        if conflict_column:
            return f"INSERT INTO {table}({columns}) VALUES ({placeholders}) ON CONFLICT ({conflict_column}) DO NOTHING"
        else:
            return f"INSERT INTO {table}({columns}) VALUES ({placeholders})"


def read_csv_in_batches(csv_path: str, batch_size: int = 5000) -> Iterable[List[dict]]:
    """
    Read CSV file in batches.
    Yields batches of dictionaries.
    Uses utf-8-sig to handle BOM if present.
    """
    with open(csv_path, newline='', encoding='utf-8-sig') as f:
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
