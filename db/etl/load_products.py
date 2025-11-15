import os, sys, pandas as pd

def main(path):
    df = pd.read_csv(path)
    print(f"[products] rows={len(df)}, cols={list(df.columns)}")
    print(df.head(3).to_string(index=False))

    # Bazı hızlı istatistikler (varsa)
    for col in ['name','category_id','category_name','product_category_name']:
        if col in df.columns:
            print(f"[products] null {col}: {df[col].isna().sum()}")

    # Hafta 2 görevi: missing category logu
    DRY = 1 if os.getenv("DRY_RUN") else 0
    if 'category_id' in df.columns:
        missing = int(df['category_id'].isna().sum())
        basis = 'category_id'
    elif 'product_category_name' in df.columns:
        # Olist ürünlerinde category_id yok; proxy olarak isim kolonundaki NaN sayılır
        missing = int(df['product_category_name'].isna().sum())
        basis = 'product_category_name'
    else:
        missing = 0
        basis = 'n/a'
    print(f"[products] missing category (basis={basis}) = {missing} rows (DRY_RUN={DRY})")

if __name__ == "__main__":
    csv_path = sys.argv[1] if len(sys.argv) > 1 else "data/raw/products.csv"
    if not os.getenv("DRY_RUN"):
        print("DRY_RUN=1 olmadan bu script sadece önizleme/log üretir.")
    main(csv_path)
