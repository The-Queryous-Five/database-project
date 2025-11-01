import os, sys, csv, unicodedata, pandas as pd, pathlib

cats_path  = sys.argv[1] if len(sys.argv)>1 else "data/raw/product_category_name_translation.csv"
prods_path = sys.argv[2] if len(sys.argv)>2 else "data/raw/olist_products_dataset.csv"
out_md     = pathlib.Path("reports/categories_match_report.md")

def read_csv_smart(path):
    last_err = None
    for enc in ("utf-8", "utf-8-sig", "latin-1"):
        try:
            with open(path, "r", encoding=enc, newline="") as f:
                sample = f.read(4096)
                f.seek(0)
                try:
                    dialect = csv.Sniffer().sniff(sample)
                    sep = dialect.delimiter
                except Exception:
                    sep = None
            df = pd.read_csv(path, sep=sep, engine="python", encoding=enc, dtype=str)
            # kolon adlarını normalize et (BOM temizliği dahil)
            df.columns = [
                str(c).lstrip("\ufeff").strip().lower().replace(" ", "_").replace("-", "_")
                for c in df.columns
            ]
            return df
        except Exception as e:
            last_err = e
    raise SystemExit(f"CSV okunamadı: {path} ({last_err})")

def deaccent(s):
    if s is None: return ""
    s = str(s)
    s = unicodedata.normalize("NFKD", s).encode("ascii","ignore").decode("ascii")
    return s

def norm(s):
    s = deaccent(s).strip().lower()
    for ch in ["-", "_", "/"]:
        s = s.replace(ch, " ")
    s = " ".join(s.split())
    return s

cats  = read_csv_smart(cats_path)
prods = read_csv_smart(prods_path)

# ---- kolon tespiti (esnek) ----
# categories (çeviri) tarafında PT veya EN isim olabilir
cat_name_candidates = [
    "product_category_name",          # olist PT
    "category_name",
]
cat_name_col = next((c for c in cat_name_candidates if c in cats.columns), None)

cat_en_candidates = [
    "product_category_name_english",  # olist EN
    "category_name_english",
]
cat_en_col = next((c for c in cat_en_candidates if c in cats.columns), None)

if cat_name_col is None and cat_en_col is None:
    raise SystemExit("[cats] kategori adı kolonu bulunamadı (ne PT ne EN).")

# products tarafında kategori adı
prods_cat_candidates = [
    "product_category_name", "category_name", "product_category"
]
prods_cat_col = next((c for c in prods_cat_candidates if c in prods.columns), None)
if prods_cat_col is None:
    raise SystemExit("[products] product_category_name kolonu yok.")

# eşleşme anahtarı: PT isim üzerinden
cats["_key_pt"]  = cats[cat_name_col].map(norm) if cat_name_col else ""
prods["_key_pt"] = prods[prods_cat_col].map(norm)

use_pt = cat_name_col is not None

if use_pt:
    cats_key = cats[["_key_pt"]].copy()
    # referans kolon: EN varsa onu yazalım, yoksa PT'yi
    cats_key["ref"] = cats[cat_en_col] if cat_en_col in cats.columns else cats[cat_name_col]
    prods_m = prods.merge(cats_key.rename(columns={"_key_pt":"_key"}), left_on="_key_pt", right_on="_key", how="left")
    matched = prods_m["ref"].notna().sum()
    total   = len(prods_m)
    unq_unm = sorted(set(prods_m.loc[prods_m["ref"].isna(), "_key_pt"]) - {""})
else:
    matched = 0
    total   = len(prods)
    unq_unm = sorted(set(prods["_key_pt"]) - {""})

rate = 0 if total==0 else round(100*matched/total, 2)

md = f"""# Categories ↔ Products Eşleşme Raporu (Olist)

- Toplam ürün satırı: **{total}**
- Eşleşen ürün: **{matched}**
- **Eşleşmeyen** ürün: **{total - matched}**
- Eşleşme oranı: **{rate}%**
- Not: {'PT kolon bulundu ve onunla eşleştirildi.' if use_pt else 'Çeviri CSV’de PT kolon bulunamadı; eşleşme yapılamadı (0%).'}

## Eşleşmeyen kategori adları (ilk 20)
{os.linesep.join(f"- {x}" for x in unq_unm[:20]) if unq_unm else "- (yok)"}
"""
out_md.parent.mkdir(parents=True, exist_ok=True)
out_md.write_text(md, encoding="utf-8")
print(md)
