"use strict";

/**
 * Render payments by type result in the container
 * @param {HTMLElement} container - The container element to render results in
 * @param {Object} data - The payment data object
 * @param {string} data.payment_type - The payment type
 * @param {number} data.payment_count - Number of payments
 * @param {number} data.total_value - Total value of payments
 */
function renderPaymentsByTypeResult(container, data) {
    container.innerHTML = `
        <p>Type: <strong>${data.payment_type}</strong></p>
        <p>Count: ${data.payment_count}</p>
        <p>Total value: ${data.total_value.toFixed(2)}</p>
    `;
}

/**
 * Handle the "Get payments by type" button click
 */
async function onPaymentsByTypeClick() {
    const errorDiv = document.querySelector("#payments-error");
    const resultsDiv = document.querySelector("#payments-results");
    const input = document.querySelector("#payment-type-input");

    // Clear previous results and errors
    errorDiv.textContent = "";
    resultsDiv.innerHTML = "";

    // Get and validate input
    const paymentType = input.value.trim();
    if (!paymentType) {
        errorDiv.textContent = "payment_type is required";
        return;
    }

    try {
        // Make API request
        const url = `http://localhost:5000/payments/by-type?payment_type=${encodeURIComponent(paymentType)}`;
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
        errorDiv.textContent = "Network error - is the Flask API running?";
        console.error("Payment API error:", error);
    }
}

// Initialize when DOM is ready
document.addEventListener("DOMContentLoaded", () => {
    const button = document.querySelector("#payments-by-type-btn");
    const input = document.querySelector("#payment-type-input");
    const resultsDiv = document.querySelector("#payments-results");
    const errorDiv = document.querySelector("#payments-error");

    // Check if all required elements exist
    if (!button || !input || !resultsDiv || !errorDiv) {
        console.error("Payments UI elements not found");
        return;
    }

    // Attach event listener
    button.addEventListener("click", onPaymentsByTypeClick);
    console.log("payments.js loaded - ready to fetch payment data");
});
