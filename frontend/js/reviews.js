"use strict";

/**
 * Reviews Module - Frontend UI for review statistics
 * Week 4 Task: Display review stats filtered by score range (1-5)
 */

const API_BASE_URL = "http://localhost:5000";

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
        
        // Make API request
        const url = `${API_BASE_URL}/reviews/stats?min_score=${minScore}&max_score=${maxScore}`;
        const response = await fetch(url);
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Display results in a nice summary box
        resultsDiv.innerHTML = `
            <div class="stats-summary">
                <h4>📊 Review Statistics</h4>
                <div class="stats-grid">
                    <div class="stat-item">
                        <span class="stat-label">Score Range:</span>
                        <span class="stat-value">${data.min_score} - ${data.max_score}</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-label">Average Score:</span>
                        <span class="stat-value">${data.avg_score ? data.avg_score.toFixed(2) : 'N/A'}</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-label">Review Count:</span>
                        <span class="stat-value">${data.review_count.toLocaleString()}</span>
                    </div>
                </div>
                <p class="stats-info">
                    Reviews with scores between ${data.min_score} and ${data.max_score}: 
                    <strong>Average ${data.avg_score ? data.avg_score.toFixed(2) : 'N/A'}</strong>, 
                    <strong>${data.review_count.toLocaleString()} reviews</strong>
                </p>
            </div>
        `;
        
    } catch (error) {
        console.error("Error loading review stats:", error);
        errorDiv.textContent = `❌ Error loading review stats: ${error.message}`;
        resultsDiv.innerHTML = "";
    }
}

document.addEventListener("DOMContentLoaded", () => {
    console.log("reviews.js loaded - Review stats UI ready");
});
