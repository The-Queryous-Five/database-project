"use strict";

/**
 * Reviews Module - Frontend UI for review statistics
 * Week 4 Task: Display review stats filtered by score range (1-5)
 */

const API_BASE_URL = window.API_BASE_URL;

/**
 * Load review statistics based on min_score and max_score
 * Validates input before making API request
 */
async function loadReviewStats() {
    const minScoreInput = document.getElementById("reviews-min-score");
    const maxScoreInput = document.getElementById("reviews-max-score");
    const errorDiv = document.getElementById("reviews-error");
    const resultsDiv = document.getElementById("reviews-results");
    
    // Clear previous results and errors
    errorDiv.textContent = "";
    resultsDiv.innerHTML = "";
    
    // Get and validate inputs
    const minScore = parseInt(minScoreInput.value);
    const maxScore = parseInt(maxScoreInput.value);
    
    // Validation: check if values are valid numbers
    if (isNaN(minScore) || isNaN(maxScore)) {
        errorDiv.textContent = "⚠️ Min and Max scores must be valid numbers";
        return;
    }
    
    // Validation: check range (1-5)
    if (minScore < 1 || minScore > 5) {
        errorDiv.textContent = "⚠️ Min score must be between 1 and 5";
        return;
    }
    
    if (maxScore < 1 || maxScore > 5) {
        errorDiv.textContent = "⚠️ Max score must be between 1 and 5";
        return;
    }
    
    // Validation: min should not be greater than max
    if (minScore > maxScore) {
        errorDiv.textContent = "⚠️ Min score cannot be greater than Max score";
        return;
    }
    
    try {
        // Show loading state
        resultsDiv.innerHTML = "<p>Loading...</p>";
        
        // Build URL with URLSearchParams
        const params = new URLSearchParams({
            min_score: minScore,
            max_score: maxScore
        });
        const url = `${API_BASE_URL}/reviews/stats?${params.toString()}`;
        const response = await fetch(url);
        
        if (response.status === 400 || response.status === 422) {
            const errorData = await response.json();
            errorDiv.textContent = errorData.error || "Validation error";
            resultsDiv.innerHTML = "";
            return;
        }
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Build stats table with backend response format (total_reviews, average_score, stats)
        let html = `<div class="stats-summary">`;
        html += `<h4>📊 Review Statistics</h4>`;
        html += `<p><strong>Score Range:</strong> ${data.min_score} - ${data.max_score}</p>`;
        html += `<p><strong>Total Reviews:</strong> ${data.total_reviews.toLocaleString()}</p>`;
        html += `<p><strong>Average Score:</strong> ${data.average_score !== null ? data.average_score.toFixed(2) : 'N/A'}</p>`;
        html += `</div>`;
        
        if (data.stats && data.stats.length > 0) {
            html += `<table><thead><tr><th>Review Score</th><th>Review Count</th></tr></thead><tbody>`;
            for (const stat of data.stats) {
                html += `<tr><td>${stat.review_score}</td><td>${stat.review_count.toLocaleString()}</td></tr>`;
            }
            html += `</tbody></table>`;
        } else {
            html += `<p>No reviews found in this score range.</p>`;
        }
        
        resultsDiv.innerHTML = html;
        
    } catch (error) {
        console.error("Error loading review stats:", error);
        errorDiv.textContent = `❌ Network error - is the Flask API running?`;
        resultsDiv.innerHTML = "";
    }
}

document.addEventListener("DOMContentLoaded", () => {
    // Demo button handler
    const demoBtn = document.getElementById("reviews-demo-btn");
    if (demoBtn) {
        demoBtn.addEventListener("click", () => {
            const minScoreInput = document.getElementById("reviews-min-score");
            const maxScoreInput = document.getElementById("reviews-max-score");
            
            if (minScoreInput) minScoreInput.value = "4";
            if (maxScoreInput) maxScoreInput.value = "5";
            
            // Auto-trigger the query
            loadReviewStats();
        });
    }
    
    console.log("reviews.js loaded - Review stats UI ready");
});
