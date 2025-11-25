"use strict";

const API_BASE_ORDERS = "http://127.0.0.1:5000";

// ============ HELPER FUNCTIONS ============

function showLoadingOrders(container) {
    if (!container) return;
    container.innerHTML = '<p class="info-message">Loading...</p>';
}

function showErrorOrders(container, message) {
    if (!container) return;
    container.innerHTML = `<p class="error-message">${message}</p>`;
}

function clearErrorOrders(container) {
    if (!container) return;
    container.innerHTML = '';
}

function renderTableOrders(container, columns, rows) {
    if (!container) return;
    
    if (!rows || rows.length === 0) {
        container.innerHTML = '<p>No orders found.</p>';
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

async function loadOrdersByCustomer() {
    const resultsDiv = document.getElementById('orders-results');
    const customerIdInput = document.getElementById('orders-customer-id');
    const limitInput = document.getElementById('orders-limit');

    clearErrorOrders(resultsDiv);

    const customerId = customerIdInput?.value.trim();
    const limit = limitInput?.value || '5';

    if (!customerId) {
        showErrorOrders(resultsDiv, "Please enter a Customer ID!");
        return;
    }

    showLoadingOrders(resultsDiv);

    try {
        const url = `${API_BASE_ORDERS}/orders/by-customer/${encodeURIComponent(customerId)}?limit=${encodeURIComponent(limit)}`;
        const response = await fetch(url);

        if (!response.ok) {
            const errData = await response.json().catch(() => ({}));
            throw new Error(errData.error || `Error: ${response.status}`);
        }

        const data = await response.json();

        const columns = [
            { key: 'order_id', label: 'Order ID' },
            { key: 'order_status', label: 'Status' },
            { key: 'order_purchase_timestamp', label: 'Purchase Date' }
        ];

        renderTableOrders(resultsDiv, columns, data);

    } catch (error) {
        console.error("Error details:", error);
        showErrorOrders(resultsDiv, `Error: ${error.message}`);
    }
}

// ============ DEMO FUNCTIONS ============

document.addEventListener("DOMContentLoaded", () => {
    const demoBtn = document.getElementById("orders-demo-btn");
    if (demoBtn) {
        demoBtn.addEventListener("click", () => {
            const customerIdInput = document.getElementById("orders-customer-id");
            const limitInput = document.getElementById("orders-limit");
            
            // Use a placeholder customer ID (user should replace with real one)
            if (customerIdInput) customerIdInput.value = "PASTE_VALID_CUSTOMER_ID_HERE";
            if (limitInput) limitInput.value = "5";
            
            alert("Please replace the placeholder customer ID with a real one from your database, then click 'Get orders by customer'");
        });
    }
});