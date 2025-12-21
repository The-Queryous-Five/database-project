"use strict";

const API_BASE = window.API_BASE_URL || 'http://127.0.0.1:5000';

/**
 * Render payments by type result in the container
 */
function renderPaymentsByTypeResult(container, data) {
    if (!data.payments || data.payments.length === 0) {
        container.innerHTML = `<p>No payments found for type: <strong>${data.payment_type}</strong></p>`;
        return;
    }
    
    let html = `<p>Payment Type: <strong>${data.payment_type}</strong></p>`;
    html += `<p>Total Results: ${data.row_count}</p>`;
    html += `<table><thead><tr>`;
    html += `<th>Order ID</th><th>Sequential</th><th>Installments</th><th>Value</th>`;
    html += `</tr></thead><tbody>`;
    
    for (const payment of data.payments) {
        html += `<tr>`;
        html += `<td>${payment.order_id || ''}</td>`;
        html += `<td>${payment.payment_sequential ?? ''}</td>`;
        html += `<td>${payment.payment_installments ?? ''}</td>`;
        html += `<td>${payment.payment_value ? payment.payment_value.toFixed(2) : 'N/A'}</td>`;
        html += `</tr>`;
    }
    
    html += `</tbody></table>`;
    container.innerHTML = html;
}

/**
 * Handle the "Get payments by type" button click
 */
async function onPaymentsByTypeClick() {
    const errorDiv = document.querySelector("#payments-error");
    const resultsDiv = document.querySelector("#payments-results");
    const typeInput = document.querySelector("#payment-type-input");
    const limitInput = document.querySelector("#payments-limit");

    // Clear previous results and errors
    errorDiv.textContent = "";
    resultsDiv.innerHTML = "";

    // Get and validate input
    const paymentType = typeInput.value.trim();
    if (!paymentType) {
        errorDiv.textContent = "payment_type is required";
        return;
    }

    const limit = limitInput?.value ? parseInt(limitInput.value) : 20;

    try {
        // Build URL with URLSearchParams
        const params = new URLSearchParams({ 
            payment_type: paymentType,
            limit: limit
        });
        const url = `${API_BASE}/payments/by-type?${params.toString()}`;
        const response = await fetch(url);

        if (response.status === 400 || response.status === 422) {
            // Handle validation errors
            const errorData = await response.json();
            errorDiv.textContent = errorData.error || "Validation error";
            return;
        }

        if (response.status === 200) {
            // Handle success
            const data = await response.json();
            renderPaymentsByTypeResult(resultsDiv, data);
            return;
        }

        // Handle unexpected status codes
        errorDiv.textContent = "Unexpected error: " + response.status;
    } catch (error) {
        // Handle network errors
        const errorMsg = window.handleFetchError ? window.handleFetchError(error, null) : "Network error";
        errorDiv.textContent = errorMsg;
        console.error("Payment API error:", error);
    }
}

// Initialize when DOM is ready
document.addEventListener("DOMContentLoaded", () => {
    const button = document.querySelector("#payments-by-type-btn");
    const typeInput = document.querySelector("#payment-type-input");
    const resultsDiv = document.querySelector("#payments-results");
    const errorDiv = document.querySelector("#payments-error");

    // Check if all required elements exist
    if (!button || !typeInput || !resultsDiv || !errorDiv) {
        console.error("Payments UI elements not found");
        return;
    }

    // Attach event listener
    button.addEventListener("click", onPaymentsByTypeClick);
    
    // Demo button handler
    const demoBtn = document.getElementById("payments-demo-btn");
    if (demoBtn) {
        demoBtn.addEventListener("click", () => {
            if (typeInput) typeInput.value = "credit_card";
            
            // Auto-trigger the query
            onPaymentsByTypeClick();
        });
    }
    
    console.log("payments.js loaded - ready to fetch payment data");
});
