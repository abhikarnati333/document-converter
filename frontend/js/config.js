/**
 * Application Configuration
 * Environment-specific settings
 */

const CONFIG = {
    // API Base URL - update this based on your environment
    API_BASE_URL: window.location.hostname === 'localhost' 
        ? 'http://localhost:8000'
        : (import.meta.env?.VITE_API_BASE_URL || 'http://localhost:8000')
};

// Make config globally available
window.CONFIG = CONFIG;
