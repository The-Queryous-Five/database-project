// Analytics Module - Sprint B
// Complex SQL query showcase for database project demo

const API_BASE_ANALYTICS = window.API_BASE_URL + "/analytics";


// ===================== Revenue by Category =====================
async function loadRevenueByCategory() {
    const limit = document.getElementById("revenue-limit").value;
    const resultsDiv = document.getElementById("revenue-results");
    
    resultsDiv.innerHTML = "<p>Loading...</p>";
    
    try {
        const response = await fetch(`${API_BASE_ANALYTICS}/revenue-by-category?limit=${limit}`);
        
        if (!response.ok) {
            const errorData = await response.json();
            resultsDiv.innerHTML = window.handleFetchError(null, response, errorData);
            return;
        }
        
        const result = await response.json();
        
        if (!result.ok || !result.data || result.data.length === 0) {
            resultsDiv.innerHTML = "<p class='info-message'>No data found.</p>";
            return;
        }
        
        // Build table
        let html = `<p class='info-message'>Showing top ${result.params.limit} categories by revenue</p>`;
        html += "<table><thead><tr>";
        html += "<th>Category</th><th>Items Sold</th><th>Orders</th><th>Revenue</th><th>Avg Price</th>";
        html += "</tr></thead><tbody>";
        
        result.data.forEach(row => {
            html += "<tr>";
            html += `<td>${row.category_name || 'N/A'}</td>`;
            html += `<td>${row.items_sold || 0}</td>`;
            html += `<td>${row.distinct_orders || 0}</td>`;
            html += `<td>R$ ${(row.total_revenue || 0).toFixed(2)}</td>`;
            html += `<td>R$ ${(row.avg_item_price || 0).toFixed(2)}</td>`;
            html += "</tr>";
        });
        
        html += "</tbody></table>";
        resultsDiv.innerHTML = html;
        
    } catch (error) {
        resultsDiv.innerHTML = window.handleFetchError(error, null);
    }
}

function demoRevenueByCategory() {
    document.getElementById("revenue-limit").value = 10;
    loadRevenueByCategory();
}


// ===================== Top Sellers =====================
async function loadTopSellers() {
    const limit = document.getElementById("sellers-limit").value;
    const resultsDiv = document.getElementById("sellers-results");
    
    resultsDiv.innerHTML = "<p>Loading...</p>";
    
    try {
        const response = await fetch(`${API_BASE_ANALYTICS}/top-sellers?limit=${limit}`);
        
        if (!response.ok) {
            const errorData = await response.json();
            resultsDiv.innerHTML = window.handleFetchError(null, response, errorData);
            return;
        }
        
        const result = await response.json();
        
        if (!result.ok || !result.data || result.data.length === 0) {
            resultsDiv.innerHTML = "<p class='info-message'>No data found.</p>";
            return;
        }
        
        // Build table
        let html = `<p class='info-message'>Top ${result.params.limit} sellers by revenue</p>`;
        html += "<table><thead><tr>";
        html += "<th>Seller ID</th><th>City</th><th>State</th><th>Orders</th><th>Items</th><th>Revenue</th><th>Avg Price</th>";
        html += "</tr></thead><tbody>";
        
        result.data.forEach(row => {
            html += "<tr>";
            html += `<td>${row.seller_id.substring(0, 8)}...</td>`;
            html += `<td>${row.seller_city || 'N/A'}</td>`;
            html += `<td>${row.seller_state || 'N/A'}</td>`;
            html += `<td>${row.order_count || 0}</td>`;
            html += `<td>${row.items_sold || 0}</td>`;
            html += `<td>R$ ${(row.total_revenue || 0).toFixed(2)}</td>`;
            html += `<td>R$ ${(row.avg_item_price || 0).toFixed(2)}</td>`;
            html += "</tr>";
        });
        
        html += "</tbody></table>";
        resultsDiv.innerHTML = html;
        
    } catch (error) {
        resultsDiv.innerHTML = window.handleFetchError(error, null);
    }
}

function demoTopSellers() {
    document.getElementById("sellers-limit").value = 10;
    loadTopSellers();
}


// ===================== Review vs Delivery =====================
async function loadReviewVsDelivery() {
    const minReviews = document.getElementById("min-reviews").value;
    const resultsDiv = document.getElementById("review-delivery-results");
    
    resultsDiv.innerHTML = "<p>Loading...</p>";
    
    try {
        const response = await fetch(`${API_BASE_ANALYTICS}/review-vs-delivery?min_reviews=${minReviews}`);
        
        if (!response.ok) {
            const errorData = await response.json();
            resultsDiv.innerHTML = window.handleFetchError(null, response, errorData);
            return;
        }
        
        const result = await response.json();
        
        if (!result.ok || !result.data || result.data.length === 0) {
            resultsDiv.innerHTML = "<p class='info-message'>No data found. Try lowering min_reviews.</p>";
            return;
        }
        
        // Build table
        let html = `<p class='info-message'>Sellers with ${result.params.min_reviews}+ reviews (sorted by score + delivery time)</p>`;
        html += "<table><thead><tr>";
        html += "<th>Seller ID</th><th>City</th><th>State</th><th>Reviews</th><th>Avg Score</th><th>Avg Delivery Days</th>";
        html += "</tr></thead><tbody>";
        
        result.data.forEach(row => {
            html += "<tr>";
            html += `<td>${row.seller_id.substring(0, 8)}...</td>`;
            html += `<td>${row.seller_city || 'N/A'}</td>`;
            html += `<td>${row.seller_state || 'N/A'}</td>`;
            html += `<td>${row.review_count || 0}</td>`;
            html += `<td>${(row.avg_review_score || 0).toFixed(2)} ⭐</td>`;
            html += `<td>${(row.avg_delivery_days || 0).toFixed(1)} days</td>`;
            html += "</tr>";
        });
        
        html += "</tbody></table>";
        resultsDiv.innerHTML = html;
        
    } catch (error) {
        resultsDiv.innerHTML = window.handleFetchError(error, null);
    }
}

function demoReviewVsDelivery() {
    document.getElementById("min-reviews").value = 50;
    loadReviewVsDelivery();
}


// ===================== Order Funnel =====================
async function loadOrderFunnel() {
    const resultsDiv = document.getElementById("funnel-results");
    
    resultsDiv.innerHTML = "<p>Loading...</p>";
    
    try {
        const response = await fetch(`${API_BASE_ANALYTICS}/order-funnel`);
        
        if (!response.ok) {
            const errorData = await response.json();
            resultsDiv.innerHTML = window.handleFetchError(null, response, errorData);
            return;
        }
        
        const result = await response.json();
        
        if (!result.ok || !result.data || result.data.length === 0) {
            resultsDiv.innerHTML = "<p class='info-message'>No data found.</p>";
            return;
        }
        
        // Build table
        let html = "<p class='info-message'>Order counts by status with avg processing times</p>";
        html += "<table><thead><tr>";
        html += "<th>Order Status</th><th>Count</th><th>Avg Delivery Days</th><th>Avg Approval Days</th>";
        html += "</tr></thead><tbody>";
        
        result.data.forEach(row => {
            html += "<tr>";
            html += `<td><strong>${row.order_status || 'unknown'}</strong></td>`;
            html += `<td>${row.order_count || 0}</td>`;
            html += `<td>${row.avg_delivery_days !== null ? row.avg_delivery_days.toFixed(1) : 'N/A'}</td>`;
            html += `<td>${row.avg_approval_days !== null ? row.avg_approval_days.toFixed(1) : 'N/A'}</td>`;
            html += "</tr>";
        });
        
        html += "</tbody></table>";
        resultsDiv.innerHTML = html;
        
    } catch (error) {
        resultsDiv.innerHTML = window.handleFetchError(error, null);
    }
}

function demoOrderFunnel() {
    loadOrderFunnel();
}


console.log("Analytics module loaded - Sprint B");
