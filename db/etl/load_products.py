"""
Usage: python db/etl/load_products.py data/raw/olist_products_dataset.csv
Parametrik INSERT kullan; executemany ile batch ekle.
"""
def load_products(csv_path: str):
    # TODO: products + category_id eşleme (categories ile join)
    pass

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python db/etl/load_products.py <csv_path>")
        sys.exit(1)
    load_products(sys.argv[1])
