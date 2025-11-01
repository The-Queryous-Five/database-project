"""
Usage: python db/etl/load_order_items.py data/raw/olist_order_items_dataset.csv
Parametrik INSERT kullan; executemany ile batch ekle.
"""
def load_order_items(csv_path: str):
    pass

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python db/etl/load_order_items.py <csv_path>")
        sys.exit(1)
    load_order_items(sys.argv[1])
