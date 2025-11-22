"use strict";

const API_BASE = "http://127.0.0.1:5000";

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
