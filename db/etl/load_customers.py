"""
Usage: python db/etl/load_customers.py data/raw/olist_customers_dataset.csv
Parametrik INSERT kullan; executemany ile batch ekle.
"""
def load_customers(csv_path: str):
    pass

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python db/etl/load_customers.py <csv_path>")
        sys.exit(1)
    load_customers(sys.argv[1])
