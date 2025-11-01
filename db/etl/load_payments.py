"""
Usage: python db/etl/load_payments.py data/raw/olist_order_payments_dataset.csv
Parametrik INSERT kullan; executemany ile batch ekle.
"""
def load_payments(csv_path: str):
    pass

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python db/etl/load_payments.py <csv_path>")
        sys.exit(1)
    load_payments(sys.argv[1])
