/* Main JavaScript for AI Resume Screener */

// Global configuration
const API_BASE = "/api";

// Utility Functions
function showAlert(message, type = "danger") {
  const alertHTML = `
        <div class="alert alert-${type} alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;

  const container = document.querySelector(".main-content") || document.body;
  const alertElement = document.createElement("div");
  alertElement.innerHTML = alertHTML;
  container.insertBefore(alertElement.firstElementChild, container.firstChild);
}

function formatDate(dateString) {
  const date = new Date(dateString);
  return date.toLocaleDateString("en-US", {
    year: "numeric",
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

function roundScore(score, decimals = 1) {
  return Math.round(score * Math.pow(10, decimals)) / Math.pow(10, decimals);
}

// API Helper Functions
async function apiCall(endpoint, options = {}) {
  try {
    const url = `${API_BASE}${endpoint}`;
    const response = await fetch(url, options);

    if (!response.ok) {
      const data = await response.json();
      throw new Error(data.error || `HTTP ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error(`API Error on ${endpoint}:`, error);
    throw error;
  }
}

// DOM Ready
document.addEventListener("DOMContentLoaded", function () {
  // Initialize tooltips if Bootstrap is available
  if (typeof bootstrap !== "undefined") {
    document
      .querySelectorAll('[data-bs-toggle="tooltip"]')
      .forEach((tooltipTriggerEl) => {
        new bootstrap.Tooltip(tooltipTriggerEl);
      });
  }
});

// Chart utility function for future use
function createChart(ctx, config) {
  if (typeof Chart !== "undefined") {
    return new Chart(ctx, config);
  }
  console.warn("Chart.js not loaded");
  return null;
}
