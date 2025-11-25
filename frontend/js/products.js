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

// Get products by category
async function loadProductsByCategory() {
  setMsg('');
  const idEl = document.getElementById('products-category-id');
  const limEl = document.getElementById('products-limit');
  const categoryId = String(idEl?.value || '').trim();
  const limit = Number(limEl?.value || 10);
  
  if (!categoryId) { 
    setMsg('Please enter category_id', true); 
    return; 
  }

  const params = new URLSearchParams({ category_id: categoryId, limit: limit });
  const url = `${BASE_URL}/products/by-category?${params.toString()}`;
  
  try {
    const resp = await fetch(url);
    
    if (resp.status === 400 || resp.status === 422) {
      const errorData = await resp.json();
      setMsg(errorData.error || 'Validation error', true);
      return;
    }
    
    if (!resp.ok) {
      const text = await resp.text();
      setMsg(`Request failed (${resp.status}): ${text}`, true);
      return;
    }
    
    const data = await resp.json();
    
    if (data.products && data.products.length > 0) {
      renderTable('products-results', data.products);
      setMsg(`Found ${data.row_count} products in category ${data.category_id}`);
    } else {
      document.getElementById('products-results').innerHTML = '<p>No products found for this category.</p>';
    }
  } catch (e) {
    console.error(e);
    setMsg('Network error - is the Flask API running?', true);
  }
}

// Show top categories
async function loadTopCategories() {
  setMsg('');
  const limEl = document.getElementById('products-limit');
  const limit = Number(limEl?.value || 10);

  const params = new URLSearchParams({ limit: limit });
  const url = `${BASE_URL}/products/top-categories?${params.toString()}`;
  
  try {
    const resp = await fetch(url);
    
    if (resp.status === 400 || resp.status === 422) {
      const errorData = await resp.json();
      setMsg(errorData.error || 'Validation error', true);
      return;
    }
    
    if (!resp.ok) {
      const text = await resp.text();
      setMsg(`Request failed (${resp.status}): ${text}`, true);
      return;
    }
    
    const data = await resp.json();
    
    if (data.categories && data.categories.length > 0) {
      renderTable('products-results', data.categories);
      setMsg(`Showing top ${data.categories.length} categories`);
    } else {
      document.getElementById('products-results').innerHTML = '<p>No categories found.</p>';
    }
  } catch (e) {
    console.error(e);
    setMsg('Network error - is the Flask API running?', true);
  }
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
