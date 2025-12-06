"use strict";

const API_BASE = "http://127.0.0.1:5001";

function setCustomersError(message) {
    const el = document.getElementById("customers-results");
    if (!el) return;
    if (!message) {
        return;
    }
    el.innerHTML = `<p style="color:red">${message}</p>`;
}

function renderCustomersByState(rows) {
    const container = document.getElementById("customers-results");
    if (!container) return;

    if (!rows || rows.length === 0) {
        container.innerHTML = "<p>No customers found for this state.</p>";
        return;
    }

    let html = "<table><thead><tr>";
    html += "<th>customer_id</th><th>customer_city</th><th>customer_state</th>";
    html += "</tr></thead><tbody>";

    for (const row of rows) {
        html += `<tr>
            <td>${row.customer_id ?? ""}</td>
            <td>${row.customer_city ?? ""}</td>
            <td>${row.customer_state ?? ""}</td>
        </tr>`;
    }

    html += "</tbody></table>";
    container.innerHTML = html;
}

function renderTopCities(rows) {
    const container = document.getElementById("customers-results");
    if (!container) return;

    if (!rows || rows.length === 0) {
        container.innerHTML = "<p>No cities found.</p>";
        return;
    }

    let html = "<table><thead><tr>";
    html += "<th>customer_city</th><th>customer_count</th>";
    html += "</tr></thead><tbody>";

    for (const row of rows) {
        html += `<tr>
            <td>${row.customer_city ?? ""}</td>
            <td>${row.customer_count ?? 0}</td>
        </tr>`;
    }

    html += "</tbody></table>";
    container.innerHTML = html;
}

async function loadCustomersByState() {
    const stateInput = document.getElementById("customers-state");
    const state = (stateInput?.value || "").trim();
    const resultsDiv = document.getElementById("customers-results");

    if (!state) {
        setCustomersError("State is required (e.g. SP).");
        return;
    }

    try {
        const url = `${API_BASE}/customers/by-state?state=${encodeURIComponent(state)}`;
        const res = await fetch(url);
        if (!res.ok) {
            throw new Error(`HTTP ${res.status}`);
        }
        const data = await res.json();
        // backend: beklenen format: [{customer_id, customer_city, customer_state}, ...]
        renderCustomersByState(data);
    } catch (err) {
        console.error("Error loading customers by state:", err);
        setCustomersError("Error loading customers.");
    }
}

async function loadTopCities() {
    const limitInput = document.getElementById("customers-limit");
    let limit = Number(limitInput?.value || 5);

    if (!Number.isFinite(limit) || limit < 1 || limit > 50) {
        setCustomersError("Limit must be between 1 and 50.");
        return;
    }

    try {
        const url = `${API_BASE}/customers/top-cities?limit=${encodeURIComponent(limit)}`;
        const res = await fetch(url);

        if (!res.ok) {
            let msg = "Error loading top cities.";
            try {
                const body = await res.json();
                if (body && body.error) msg = body.error;
            } catch (_) {}
            throw new Error(msg);
        }

        const data = await res.json();
        // backend: [{customer_city, customer_count}, ...]
        renderTopCities(data);
    } catch (err) {
        console.error("Error loading top cities:", err);
        setCustomersError("Error loading top cities.");
    }
}

// Geo Analytics Functions

function showLoading(elementId) {
    const el = document.getElementById(elementId);
    if (el) {
        el.innerHTML = "<p>Loading...</p>";
    }
}

function showError(elementId, message) {
    const el = document.getElementById(elementId);
    if (el) {
        el.innerHTML = `<p style="color:red">${message}</p>`;
    }
}

function renderTable(elementId, rows, columns) {
    const container = document.getElementById(elementId);
    if (!container) return;

    if (!rows || rows.length === 0) {
        container.innerHTML = "<p>No results found.</p>";
        return;
    }

    let html = "<table><thead><tr>";
    for (const col of columns) {
        html += `<th>${col}</th>`;
    }
    html += "</tr></thead><tbody>";

    for (const row of rows) {
        html += "<tr>";
        for (const col of columns) {
            html += `<td>${row[col] ?? ""}</td>`;
        }
        html += "</tr>";
    }

    html += "</tbody></table>";
    container.innerHTML = html;
}

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
        showError("customers-by-city-results", "State is required.");
        return;
    }
    if (!city) {
        showError("customers-by-city-results", "City is required.");
        return;
    }
    if (!Number.isFinite(limit) || limit < 1 || limit > 50) {
        showError("customers-by-city-results", "Limit must be between 1 and 50.");
        return;
    }

    showLoading("customers-by-city-results");

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
        renderTable("customers-by-city-results", data, ["customer_id", "city", "state"]);
    } catch (err) {
        console.error("Error loading customers by city:", err);
        showError("customers-by-city-results", err.message || "Error loading customers by city.");
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
        showError("geo-top-states-results", "Limit must be between 1 and 27.");
        return;
    }

    showLoading("geo-top-states-results");

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
        renderTable("geo-top-states-results", items, ["state", "customer_count"]);
    } catch (err) {
        console.error("Error loading top states:", err);
        showError("geo-top-states-results", err.message || "Error loading top states.");
    }
}

function handleGeoTopStatesDemo() {
    const limitInput = document.getElementById("geo-top-states-limit");

    if (limitInput) limitInput.value = "10";

    handleGeoTopStatesSubmit();
}
