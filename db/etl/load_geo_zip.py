import os, csv, sys
DRY = os.getenv("DRY_RUN", "0") in ("1","true","True")
EXPECTED_COLS = {"geolocation_zip_code_prefix","geolocation_lat","geolocation_lng","geolocation_city","geolocation_state"}
def read_head(path, n=3):
    with open(path, "r", encoding="utf-8") as f:
        r = csv.DictReader(f); cols = set(r.fieldnames or []); missing = EXPECTED_COLS - cols
        if missing: print(f"[WARN] Missing columns: {missing}")
        head=[]; 
        for i,row in enumerate(r):
            if i>=n: break
            head.append(row)
        return cols, head
def count_rows(path):
    with open(path, "r", encoding="utf-8") as f: return sum(1 for _ in f)-1
def main():
    if len(sys.argv)<2: print("Usage: python db/etl/load_geo_zip.py <csv_path>"); sys.exit(1)
    path=sys.argv[1]; total=count_rows(path); cols,head=read_head(path)
    print("[DRY_RUN] geo_zip CSV path:", path)
    print("[DRY_RUN] total_rows:", total)
    print("[DRY_RUN] columns:", sorted(list(cols)))
    print("[DRY_RUN] head:")
    for i,row in enumerate(head,1):
        keys=list(row.keys())[:6]; print(f"  {i}. ", {k: row[k] for k in keys})
    if not DRY: print("[INFO] DRY_RUN=0 olsaydı burada DB'ye yazacaktık.")
if __name__=="__main__": main()
