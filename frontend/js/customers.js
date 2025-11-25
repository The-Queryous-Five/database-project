"use strict";

const API_BASE = "http://127.0.0.1:5000";

// ============ HELPER FUNCTIONS ============

function showLoading(container) {
    if (!container) return;
    container.innerHTML = '<p class="info-message">Loading...</p>';
}

function clearLoading(container) {
    if (!container) return;
    // Loading will be replaced by results or error
}

function showError(container, message) {
    if (!container) return;
    container.innerHTML = `<p class="error-message">${message}</p>`;
}

function clearError(container) {
    if (!container) return;
    container.innerHTML = '';
}

function renderTable(container, columns, rows) {
    if (!container) return;
    
    if (!rows || rows.length === 0) {
        container.innerHTML = '<p>No data found.</p>';
        return;
    }
    
    let html = '<table><thead><tr>';
    columns.forEach(col => {
        html += `<th>${col.label}</th>`;
    });
    html += '</tr></thead><tbody>';
    
    rows.forEach(row => {
        html += '<tr>';
        columns.forEach(col => {
            html += `<td>${row[col.key] ?? ''}</td>`;
        });
        html += '</tr>';
    });
    
    html += '</tbody></table>';
    container.innerHTML = html;
}

// ============ API FUNCTIONS ============

async function loadCustomersByState() {
    const stateInput = document.getElementById("customers-state");
    const resultsDiv = document.getElementById("customers-results");
    
    clearError(resultsDiv);
    
    const state = (stateInput?.value || "").trim();

    if (!state) {
        showError(resultsDiv, "State is required (e.g. SP).");
        return;
    }

    showLoading(resultsDiv);

    try {
        const url = `${API_BASE}/customers/by-state?state=${encodeURIComponent(state)}`;
        const res = await fetch(url);
        
        if (!res.ok) {
            const errorData = await res.json().catch(() => ({}));
            throw new Error(errorData.error || `HTTP ${res.status}`);
        }
        
        const data = await res.json();
        
        const columns = [
            { key: 'customer_id', label: 'Customer ID' },
            { key: 'customer_city', label: 'City' },
            { key: 'customer_state', label: 'State' }
        ];
        
        renderTable(resultsDiv, columns, data);
    } catch (err) {
        console.error("Error loading customers by state:", err);
        showError(resultsDiv, "Error loading customers.");
    }
}

async function loadTopCities() {
    const limitInput = document.getElementById("customers-limit");
    const resultsDiv = document.getElementById("customers-results");
    
    clearError(resultsDiv);
    
    let limit = Number(limitInput?.value || 5);

    if (!Number.isFinite(limit) || limit < 1 || limit > 50) {
        showError(resultsDiv, "Limit must be between 1 and 50.");
        return;
    }

    showLoading(resultsDiv);

    try {
        const url = `${API_BASE}/customers/top-cities?limit=${encodeURIComponent(limit)}`;
        const res = await fetch(url);

        if (!res.ok) {
            const errorData = await res.json().catch(() => ({}));
            throw new Error(errorData.error || `HTTP ${res.status}`);
        }

        const data = await res.json();
        
        const columns = [
            { key: 'customer_city', label: 'City' },
            { key: 'customer_count', label: 'Customer Count' }
        ];
        
        renderTable(resultsDiv, columns, data);
    } catch (err) {
        console.error("Error loading top cities:", err);
        showError(resultsDiv, "Error loading top cities.");
    }
}

// ============ DEMO FUNCTIONS ============

document.addEventListener("DOMContentLoaded", () => {
    const demoBtn = document.getElementById("customers-demo-btn");
    if (demoBtn) {
        demoBtn.addEventListener("click", () => {
            const stateInput = document.getElementById("customers-state");
            const limitInput = document.getElementById("customers-limit");
            
            if (stateInput) stateInput.value = "SP";
            if (limitInput) limitInput.value = "10";
            
            // Auto-trigger the query
            loadTopCities();
        });
    }
});
