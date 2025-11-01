import os, sys, pandas as pd

def main(path):
    df = pd.read_csv(path)
    print(f"[products] rows={len(df)}, cols={list(df.columns)}")
    print(df.head(3).to_string(index=False))
    for col in ['name','category_id','category_name']:
        if col in df.columns:
            print(f"[products] null {col}: {df[col].isna().sum()}")

if __name__ == "__main__":
    csv_path = sys.argv[1] if len(sys.argv) > 1 else "data/raw/products.csv"
    if not os.getenv("DRY_RUN"):
        print("DRY_RUN=1 olmadan bu script sadece önizleme yapar.")
    main(csv_path)
