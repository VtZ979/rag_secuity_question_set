/**
 * API Configuration
 */
const API_CONFIG = {
  // API base URL - 统一使用 /api (通过 Vite proxy 或 Nginx proxy)
  // 可以通过环境变量 VITE_API_URL 覆盖
  baseURL: import.meta.env.VITE_API_URL || '/api',
  
  // API endpoints
  endpoints: {
    askQuestion: '/askQuestion',
    health: '/health'
  },
  
  // Request timeout (ms) - 增加超时时间，因为 LLM 响应可能较慢
  timeout: 60000
};

export default API_CONFIG;

