"""
Usage: python db/etl/load_orders.py data/raw/olist_orders_dataset.csv
Parametrik INSERT kullan; executemany ile batch ekle.
"""
def load_orders(csv_path: str):
    pass

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python db/etl/load_orders.py <csv_path>")
        sys.exit(1)
    load_orders(sys.argv[1])
