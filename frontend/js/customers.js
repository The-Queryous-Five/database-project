"use strict";

const API_BASE = window.API_BASE_URL || 'http://127.0.0.1:5000';

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

// ============ GEO ANALYTICS FUNCTIONS ============

async function handleCustomersByCitySubmit() {
    const stateInput = document.getElementById("customers-by-city-state");
    const cityInput = document.getElementById("customers-by-city-city");
    const limitInput = document.getElementById("customers-by-city-limit");
    const resultsDiv = document.getElementById("customers-by-city-results");

    const state = (stateInput?.value || "").trim();
    const city = (cityInput?.value || "").trim();
    let limit = Number(limitInput?.value || 10);

    // Validation
    if (!state) {
        showError(resultsDiv, "State is required.");
        return;
    }
    if (!city) {
        showError(resultsDiv, "City is required.");
        return;
    }
    if (!Number.isFinite(limit) || limit < 1 || limit > 50) {
        showError(resultsDiv, "Limit must be between 1 and 50.");
        return;
    }

    showLoading(resultsDiv);

    try {
        const url = `${API_BASE}/customers/by-city?state=${encodeURIComponent(state)}&city=${encodeURIComponent(city)}&limit=${encodeURIComponent(limit)}`;
        const res = await fetch(url);

        if (!res.ok) {
            let errorMsg = "Error loading customers by city.";
            try {
                const body = await res.json();
                if (body && body.error) errorMsg = body.error;
            } catch (_) {}
            throw new Error(errorMsg);
        }

        const data = await res.json();
        
        const columns = [
            { key: 'customer_id', label: 'Customer ID' },
            { key: 'city', label: 'City' },
            { key: 'state', label: 'State' }
        ];
        
        renderTable(resultsDiv, columns, data);
    } catch (err) {
        console.error("Error loading customers by city:", err);
        showError(resultsDiv, err.message || "Error loading customers by city.");
    }
}

function handleCustomersByCityDemo() {
    const stateInput = document.getElementById("customers-by-city-state");
    const cityInput = document.getElementById("customers-by-city-city");
    const limitInput = document.getElementById("customers-by-city-limit");

    if (stateInput) stateInput.value = "SP";
    if (cityInput) cityInput.value = "sao_paulo";
    if (limitInput) limitInput.value = "10";

    handleCustomersByCitySubmit();
}

async function handleGeoTopStatesSubmit() {
    const limitInput = document.getElementById("geo-top-states-limit");
    const resultsDiv = document.getElementById("geo-top-states-results");

    let limit = Number(limitInput?.value || 10);

    // Validation
    if (!Number.isFinite(limit) || limit < 1 || limit > 27) {
        showError(resultsDiv, "Limit must be between 1 and 27.");
        return;
    }

    showLoading(resultsDiv);

    try {
        const url = `${API_BASE}/geo/top-states?limit=${encodeURIComponent(limit)}`;
        const res = await fetch(url);

        if (!res.ok) {
            let errorMsg = "Error loading top states.";
            try {
                const body = await res.json();
                if (body && body.error) errorMsg = body.error;
            } catch (_) {}
            throw new Error(errorMsg);
        }

        const data = await res.json();
        // Backend returns {items: [...]}
        const items = data.items || data;
        
        const columns = [
            { key: 'state', label: 'State' },
            { key: 'customer_count', label: 'Customer Count' }
        ];
        
        renderTable(resultsDiv, columns, items);
    } catch (err) {
        console.error("Error loading top states:", err);
        showError(resultsDiv, err.message || "Error loading top states.");
    }
}

function handleGeoTopStatesDemo() {
    const limitInput = document.getElementById("geo-top-states-limit");

    if (limitInput) limitInput.value = "10";

    handleGeoTopStatesSubmit();
}
