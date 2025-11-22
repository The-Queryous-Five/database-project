const BASE_URL = 'http://127.0.0.1:5000';

function setMsg(text, isError=false) {
  const el = document.getElementById('products-msg');
  if (!el) return;
  el.textContent = text || '';
  el.style.color = isError ? 'crimson' : 'inherit';
}

function renderTable(containerId, rows) {
  const host = document.getElementById(containerId);
  if (!host) return;
  if (!rows || rows.length === 0) { host.innerHTML = '<p>No data.</p>'; return; }
  const cols = Object.keys(rows[0]);
  const thead = '<thead><tr>' + cols.map(c=>`<th>${c}</th>`).join('') + '</tr></thead>';
  const tbody = '<tbody>' + rows.map(r=>(
    '<tr>' + cols.map(c=>`<td>${r[c] ?? ''}</td>`).join('') + '</tr>'
  )).join('') + '</tbody>';
  host.innerHTML = `<table>${thead}${tbody}</table>`;
}

// ÇALIŞAN BUTON: Get products by category
async function loadProductsByCategory() {
  setMsg('');
  const idEl = document.getElementById('products-category-id');
  const limEl = document.getElementById('products-limit');
  const categoryId = String(idEl?.value || '').trim();
  const limit = Number(limEl?.value || 10);
  if (!categoryId) { setMsg('Please enter category_id', true); return; }

  const url = `${BASE_URL}/products/by-category/${encodeURIComponent(categoryId)}?limit=${encodeURIComponent(limit)}`;
  try {
    const resp = await fetch(url);
    if (!resp.ok) {
      // Backend endpoint yoksa /products/sample ile fallback yap
      if (resp.status === 404) {
        const sample = await fetch(`${BASE_URL}/products/sample?n=${encodeURIComponent(limit)}`);
        if (sample.ok) {
          const data = await sample.json();
          renderTable('products-results', data.items || data || []);
          setMsg('Using /products/sample fallback (by-category not implemented)');
          return;
        }
      }
      const text = await resp.text();
      setMsg(`Request failed (${resp.status}): ${text}`, true);
      return;
    }
    const data = await resp.json();
    renderTable('products-results', data.items || data || []);
  } catch (e) {
    console.error(e);
    setMsg('Error loading products', true);
  }
}

// ŞİMDİLİK SADECE TODO MESAJI: Show top categories
function loadTopCategories() {
  setMsg('Top categories endpoint is not implemented yet (TODO – uses Week 2 SQL).');
  const demo = [
    { category: 'perfumaria', product_count: 1234 },
    { category: 'esporte_lazer', product_count: 987 },
    { category: 'moveis_decoracao', product_count: 850 },
  ];
  renderTable('products-results', demo);
}

// UI'yı Products section'a enjekte et
document.addEventListener('DOMContentLoaded', () => {
  const sec = document.getElementById('products-section');
  if (!sec) return;

  if (!document.getElementById('products-category-id')) {
    sec.insertAdjacentHTML('beforeend', `
      <div class="controls">
        <label>Category ID:
          <input id="products-category-id" type="number" placeholder="e.g. 21">
        </label>
        <label>Limit:
          <input id="products-limit" type="number" value="10" min="1" max="100">
        </label>
        <button id="btn-products-by-category">Get products by category</button>
        <button id="btn-top-categories">Show top categories</button>
      </div>
      <div id="products-msg" class="msg"></div>
      <div id="products-results" class="results"></div>
    `);
  }

  document.getElementById('btn-products-by-category')?.addEventListener('click', loadProductsByCategory);
  document.getElementById('btn-top-categories')?.addEventListener('click', loadTopCategories);
});
