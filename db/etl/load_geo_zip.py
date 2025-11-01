"""
Usage: python db/etl/load_geo_zip.py data/raw/olist_geolocation_dataset.csv
Parametrik INSERT kullan; executemany ile batch ekle.
"""
def load_geo_zip(csv_path: str):
    # TODO: aynı zip tekilleştirme: "ilk kayıt" (alternatif: lat/lng ortalaması)
    pass

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python db/etl/load_geo_zip.py <csv_path>")
        sys.exit(1)
    load_geo_zip(sys.argv[1])
