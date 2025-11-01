"""
Usage: python db/etl/load_categories.py data/raw/product_category_name_translation.csv
Parametrik INSERT kullan; executemany ile batch ekle.
"""
def load_categories(csv_path: str):
    # TODO: INSERT INTO categories(category_name, category_name_english)
    pass

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python db/etl/load_categories.py <csv_path>")
        sys.exit(1)
    load_categories(sys.argv[1])
