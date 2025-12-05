/**
 * API Service for communicating with backend
 */
import axios from 'axios';
import API_CONFIG from '../config/api.js';

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_CONFIG.baseURL,
  timeout: API_CONFIG.timeout,
  headers: {
    'Content-Type': 'application/json'
  }
});

/**
 * Search for security knowledge
 * @param {string} query - Search query
 * @returns {Promise<Object>} Response data
 */
export const searchKnowledge = async (query) => {
  try {
    const response = await apiClient.post(
      API_CONFIG.endpoints.askQuestion,
      { question: query }
    );
    return response.data;
  } catch (error) {
    console.error('API Error:', error);
    throw new Error(
      error.response?.data?.message || 
      'Failed to search knowledge base. Please try again.'
    );
  }
};

/**
 * Check API health
 * @returns {Promise<Object>} Health status
 */
export const checkHealth = async () => {
  try {
    const response = await apiClient.get(API_CONFIG.endpoints.health);
    return response.data;
  } catch (error) {
    console.error('Health check failed:', error);
    throw error;
  }
};

