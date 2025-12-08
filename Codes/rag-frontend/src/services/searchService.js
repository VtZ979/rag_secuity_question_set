import axios from 'axios'

// Get API URL from environment variable or use default
// For VPS deployment, set VITE_API_URL in .env.production
// Example: VITE_API_URL=http://your-vps-ip:8001
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8001'

export const searchKnowledge = async (query) => {
    try {
      
    //   if (process.env.NODE_ENV === 'development') {
    //     // 模拟网络延迟
    //     await new Promise(resolve => setTimeout(resolve, 1000))
    //     return mockData
    //   }
      
      const response = await axios.post(
        `${API_BASE_URL}/askQuestion`,
        { question: query },
        { headers: { 'Content-Type': 'application/json' } }
      );
      console.log('query success:', response.data)
      return response.data
    } catch (error) {
      console.error('query fail:', error)
      throw error
    }
  }