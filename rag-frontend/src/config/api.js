/**
 * API Configuration
 */
const API_CONFIG = {
  // API base URL - can be overridden by environment variable
  // Production: use /api (via Nginx proxy)
  // Development: use http://localhost:8000
  baseURL: import.meta.env.VITE_API_URL || 
    (import.meta.env.PROD ? '/api' : 'http://localhost:8000'),
  
  // API endpoints
  endpoints: {
    askQuestion: '/askQuestion',
    health: '/health'
  },
  
  // Request timeout (ms)
  timeout: 30000
};

export default API_CONFIG;

