// frontend/js/orders.js

/**
 * Bu fonksiyon index.html'deki "Siparişleri Getir" butonuna tıklandığında çalışır.
 * Backend API: GET /orders/by-customer/<customer_id>?limit=<limit>
 */
async function loadOrdersByCustomer() {
    // HTML'den gerekli elementleri seçelim
    const resultsDiv = document.getElementById('orders-results');
    const customerIdInput = document.getElementById('orders-customer-id');
    const limitInput = document.getElementById('orders-limit');

    // Değerleri alalım
    const customerId = customerIdInput.value.trim();
    const limit = limitInput.value;

    // 1. Validasyon (Basit kontrol)
    if (!customerId) {
        alert("Lütfen bir Customer ID girin!");
        return;
    }

    // Yükleniyor mesajı göster
    resultsDiv.innerHTML = '<p style="color: gray;">Veriler yükleniyor...</p>';

    try {
        // 2. API İsteği (Backend'in 5001 portunda çalıştığını varsayıyoruz)
        const url = `http://127.0.0.1:5001/orders/by-customer/${customerId}?limit=${limit}`;
        console.log("İstek atılıyor:", url); // Hata ayıklama için log

        const response = await fetch(url);

        // Backend hata döndürdüyse (örneğin 422 veya 404)
        if (!response.ok) {
            const errData = await response.json();
            throw new Error(errData.error || `Bir hata oluştu: ${response.status}`);
        }

        const data = await response.json();

        // 3. Gelen Veriyi Tabloya Çevirme
        if (data.length === 0) {
            resultsDiv.innerHTML = '<p>Bu müşteriye ait sipariş bulunamadı.</p>';
            return;
        }

        // Tablo başlığı
        let html = `
            <div style="overflow-x: auto;">
                <table border="1" cellpadding="8" style="border-collapse: collapse; width: 100%; border-color: #ddd; font-family: Arial, sans-serif;">
                    <thead>
                        <tr style="background-color: #f2f2f2; text-align: left;">
                            <th>Order ID</th>
                            <th>Status</th>
                            <th>Purchase Date</th>
                        </tr>
                    </thead>
                    <tbody>
        `;

        // Satırları döngüyle ekle
        data.forEach(order => {
            html += `
                <tr>
                    <td>${order.order_id}</td>
                    <td>
                        <span style="padding: 4px 8px; border-radius: 4px; background-color: #e8f5e9; color: #2e7d32;">
                            ${order.order_status}
                        </span>
                    </td>
                    <td>${order.order_purchase_timestamp}</td>
                </tr>
            `;
        });

        html += '</tbody></table></div>';
        
        // Sonucu ekrana bas
        resultsDiv.innerHTML = html;

    } catch (error) {
        console.error("Hata detayı:", error);
        resultsDiv.innerHTML = `<p style="color: red; font-weight: bold;">Hata: ${error.message}</p>`;
    }
}