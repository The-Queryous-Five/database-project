"""
Usage: python db/etl/load_reviews.py data/raw/olist_order_reviews_dataset.csv
Parametrik INSERT kullan; executemany ile batch ekle.
"""
def load_reviews(csv_path: str):
    # Yükleme sonrası: UPDATE ile reviews.customer_id = orders.customer_id
    pass

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python db/etl/load_reviews.py <csv_path>")
        sys.exit(1)
    load_reviews(sys.argv[1])
