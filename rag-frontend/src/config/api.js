/**
 * API Configuration
 */
const API_CONFIG = {
  // API base URL - can be overridden by environment variable
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  
  // API endpoints
  endpoints: {
    askQuestion: '/askQuestion',
    health: '/health'
  },
  
  // Request timeout (ms)
  timeout: 30000
};

export default API_CONFIG;

