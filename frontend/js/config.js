// API Configuration
// Single source of truth for backend API base URL
window.API_BASE_URL = "http://127.0.0.1:5000";

// Shared error handling helper
window.handleFetchError = function(error, response) {
    // Network error (TypeError) - API not reachable
    if (error instanceof TypeError) {
        return "⚠️ API not reachable. Did you start Flask on 127.0.0.1:5000? Run: .\\scripts\\start-demo.ps1";
    }
    
    // HTTP 503 - DB connection failed
    if (response && response.status === 503) {
        return "⚠️ API is running but DB connection failed. Check .env (DB_VENDOR/DB_PASS) and run: .\\scripts\\check-health.ps1";
    }
    
    // HTTP 400/422 - Validation error
    if (response && (response.status === 400 || response.status === 422)) {
        return error.message || "Validation error. Please check your input.";
    }
    
    // Other errors
    return error.message || "An unexpected error occurred.";
};
