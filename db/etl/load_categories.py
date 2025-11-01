import os, sys, pandas as pd

def main(path):
    df = pd.read_csv(path)
    print(f"[categories] rows={len(df)}, cols={list(df.columns)}")
    print(df.head(3).to_string(index=False))
    if 'category_id' in df.columns:
        print(f"[categories] duplicate category_id: {df['category_id'].duplicated().sum()}")

if __name__ == "__main__":
    csv_path = sys.argv[1] if len(sys.argv) > 1 else "data/raw/categories.csv"
    if not os.getenv("DRY_RUN"):
        print("DRY_RUN=1 olmadan bu script sadece önizleme yapar.")
    main(csv_path)
