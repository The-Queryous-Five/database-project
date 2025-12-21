"use strict";

// Ömer'in config.js'i varsa onu kullan, yoksa default 5000 portunu al
const API_BASE_ORDERS = window.API_BASE_URL || 'http://127.0.0.1:5000';

// ============ HELPER FUNCTIONS ============

function showLoadingOrders(container) {
    if (!container) return;
    container.innerHTML = '<p class="info-message" style="color: gray;">Veriler yükleniyor...</p>';
}

function showErrorOrders(container, message) {
    if (!container) return;
    container.innerHTML = `<p class="error-message" style="color: red; font-weight: bold;">${message}</p>`;
}

function clearErrorOrders(container) {
    if (!container) return;
    container.innerHTML = '';
}

function renderTableOrders(container, columns, rows) {
    if (!container) return;
    
    if (!rows || rows.length === 0) {
        container.innerHTML = '<p>Bu müşteriye ait sipariş bulunamadı.</p>';
        return;
    }
    
    let html = '<div style="overflow-x: auto;"><table border="1" cellpadding="8" style="border-collapse: collapse; width: 100%; border-color: #ddd;"><thead><tr style="background-color: #f2f2f2;">';
    columns.forEach(col => {
        html += `<th>${col.label}</th>`;
    });
    html += '</tr></thead><tbody>';
    
    rows.forEach(row => {
        html += '<tr>';
        columns.forEach(col => {
            // Durum sütunu için renklendirme (opsiyonel görsel güzellik)
            let cellData = row[col.key] ?? '';
            if (col.key === 'order_status') {
                cellData = `<span style="padding: 4px 8px; border-radius: 4px; background-color: #e8f5e9; color: #2e7d32;">${cellData}</span>`;
            }
            html += `<td>${cellData}</td>`;
        });
        html += '</tr>';
    });
    
    html += '</tbody></table></div>';
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
        showErrorOrders(resultsDiv, "Lütfen bir Customer ID girin!");
        return;
    }

    showLoadingOrders(resultsDiv);

    try {
        // 2. API İsteği (Backend'den sipariş verilerini getir)
        const url = `${API_BASE_ORDERS}/orders/by-customer/${encodeURIComponent(customerId)}?limit=${encodeURIComponent(limit)}`;
        console.log("Fetching orders:", url);
        
        const response = await fetch(url);

        // Backend 503 (DB unavailable) dönerse
        if (response.status === 503) {
            throw new Error("Veritabanı bağlantısı yok (503 Service Unavailable).");
        }

        if (!response.ok) {
            const errData = await response.json().catch(() => ({}));
            throw new Error(errData.error || `Hata: ${response.status}`);
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
        const errorMsg = window.handleFetchError ? window.handleFetchError(error, { status: error.message?.includes('503') ? 503 : null }) : error.message;
        showErrorOrders(resultsDiv, errorMsg || `Hata: ${error.message}`);
    }
}

// ============ DEMO / SAMPLE ID FUNCTION ============

async function fetchSampleCustomer() {
    const customerIdInput = document.getElementById("orders-customer-id");
    
    if (customerIdInput) {
        customerIdInput.placeholder = "ID aranıyor...";
        customerIdInput.value = ""; // Önce temizle
    }

    try {
        // Backend'deki yeni endpoint'e istek at
        const response = await fetch(`${API_BASE_ORDERS}/orders/sample-customer`);
        
        if (response.status === 503) {
            alert("Veritabanı bağlantısı kurulamadı (503).");
            return;
        }

        const data = await response.json();

        if (data.sample_ids && data.sample_ids.length > 0) {
            // İlk gelen ID'yi kutuya yaz
            if (customerIdInput) {
                customerIdInput.value = data.sample_ids[0];
                // İstersen otomatik aramayı tetikleyebilirsin:
                // loadOrdersByCustomer(); 
            }
            console.log("Sample IDs fetched:", data.sample_ids);
        } else {
            alert("Örnek veri bulunamadı.");
        }

    } catch (error) {
        console.error("Sample fetch error:", error);
        if (customerIdInput) customerIdInput.placeholder = "Hata oluştu";
        alert("Demo ID getirilemedi: " + error.message);
    }
}

// ============ INITIALIZATION ============

document.addEventListener("DOMContentLoaded", () => {
    // 1. Eğer HTML'de 'orders-demo-btn' ID'li bir buton varsa ona bağla
    const existingDemoBtn = document.getElementById("orders-demo-btn");
    
    if (existingDemoBtn) {
        existingDemoBtn.addEventListener("click", fetchSampleCustomer);
    } else {
        // 2. Yoksa (ki muhtemelen yok), biz JS ile dinamik olarak ekleyelim
        const inputGroup = document.querySelector('#orders-section .input-group');
        if (inputGroup) {
            const newBtn = document.createElement('button');
            newBtn.id = 'orders-demo-btn-dynamic';
            newBtn.innerText = '🎲 Demo ID Getir';
            newBtn.style.marginLeft = '10px';
            newBtn.style.backgroundColor = '#ff9800'; // Turuncu
            newBtn.style.color = 'white';
            newBtn.style.border = 'none';
            newBtn.style.padding = '5px 10px';
            newBtn.style.cursor = 'pointer';
            
            newBtn.addEventListener("click", fetchSampleCustomer);
            inputGroup.appendChild(newBtn);
        }
    }
});