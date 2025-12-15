/**
 * Products tab – uses /products/by-category and /products/top-categories
 */

const PRODUCTS_API_BASE_URL = typeof API_BASE_URL !== 'undefined'
  ? API_BASE_URL
  : 'http://127.0.0.1:5000';

function setProductsMsg(text, isError = false) {
  const el = document.getElementById('products-msg');
  if (!el) return;
  el.textContent = text || '';
  el.style.color = isError ? 'red' : '#333';
}

function renderProductsTable(rows) {
  const container = document.getElementById('products-results');
  if (!container) return;

  if (!rows || rows.length === 0) {
    container.innerHTML = '<p>No data.</p>';
    return;
  }

  const columns = Object.keys(rows[0]);

  const thead = '<tr>' + columns.map(c => `<th>${c}</th>`).join('') + '</tr>';
  const tbody = rows.map(row =>
    '<tr>' +
      columns.map(c => `<td>${row[c] ?? ''}</td>`).join('') +
    '</tr>'
  ).join('');

  container.innerHTML = `
    <table>
      <thead>${thead}</thead>
      <tbody>${tbody}</tbody>
    </table>
  `;
}

async function loadProductsByCategory() {
  setProductsMsg('');
  const idInput = document.getElementById('products-category-id');
  const limitInput = document.getElementById('products-limit');

  if (!idInput || !limitInput) return;

  const categoryId = idInput.value.trim();
  const limit = limitInput.value.trim() || '10';

  if (!categoryId) {
    setProductsMsg('Category ID gerekli.', true);
    return;
  }

  try {
    const url = `${PRODUCTS_API_BASE_URL}/products/by-category/${encodeURIComponent(categoryId)}?limit=${encodeURIComponent(limit)}`;
    const resp = await fetch(url);

    if (!resp.ok) {
      setProductsMsg(`Backend error (${resp.status}).`, true);
      return;
    }

    const data = await resp.json();
    const rows = data.items || [];
    renderProductsTable(rows);
  } catch (err) {
    console.error(err);
    setProductsMsg('Network error - is the Flask API running?', true);
  }
}

async function loadTopCategories() {
  setProductsMsg('');

  try {
    const url = `${PRODUCTS_API_BASE_URL}/products/top-categories`;
    const resp = await fetch(url);

    if (!resp.ok) {
      setProductsMsg(`Backend error (${resp.status}).`, true);
      return;
    }

    const data = await resp.json();
    const rows = data.items || [];
    renderProductsTable(rows);
  } catch (err) {
    console.error(err);
    setProductsMsg('Network error - is the Flask API running?', true);
  }
}

document.addEventListener('DOMContentLoaded', () => {
  const btnByCat = document.getElementById('btn-products-by-category');
  const btnTop = document.getElementById('btn-top-categories');

  if (btnByCat) btnByCat.addEventListener('click', loadProductsByCategory);
  if (btnTop) btnTop.addEventListener('click', loadTopCategories);
});
