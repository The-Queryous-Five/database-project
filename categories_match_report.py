import os, sys, pandas as pd, pathlib

cats_path  = sys.argv[1] if len(sys.argv)>1 else "data/raw/categories.csv"
prods_path = sys.argv[2] if len(sys.argv)>2 else "data/raw/products.csv"
out_md     = pathlib.Path("reports/categories_match_report.md")

cats  = pd.read_csv(cats_path)
prods = pd.read_csv(prods_path)

def norm(s): return str(s).strip().lower()

has_name = 'category_name' in prods.columns
id_col   = 'category_id' if 'category_id' in cats.columns else 'id'
name_col = 'category_name' if 'category_name' in cats.columns else 'name'

cats['_key']  = cats[name_col].map(norm)
prods['_key'] = prods['category_name'].map(norm) if has_name else ""

m = prods.merge(cats[['_key', id_col]], on='_key', how='left')

matched   = m[id_col].notna().sum()
total     = len(m)
unmatched = total - matched
rate      = 0 if total==0 else round(100*matched/total,2)
unq_unm   = sorted(set(m.loc[m[id_col].isna(),'_key']) - {''})

md = f"""# Categories ↔ Products Eşleşme Raporu

- Toplam ürün satırı: **{total}**
- Eşleşen ürün: **{matched}**
- **Eşleşmeyen** ürün: **{unmatched}**
- Eşleşme oranı: **{rate}%**

## Eşleşmeyen kategori adları (ilk 20)
{os.linesep.join(f"- {x}" for x in unq_unm[:20]) if unq_unm else "- (yok)"}
"""
out_md.parent.mkdir(parents=True, exist_ok=True)
out_md.write_text(md, encoding="utf-8")
print(md)
