"""
Usage: python db/etl/load_sellers.py data/raw/olist_sellers_dataset.csv
Parametrik INSERT kullan; executemany ile batch ekle.
"""
def load_sellers(csv_path: str):
    pass

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python db/etl/load_sellers.py <csv_path>")
        sys.exit(1)
    load_sellers(sys.argv[1])
