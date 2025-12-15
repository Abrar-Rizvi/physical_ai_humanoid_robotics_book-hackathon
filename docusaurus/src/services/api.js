// API service for RAG Chatbot communication
// Implements HTTP client wrapper for API communication per task T007
import axios from 'axios';

// Create an axios instance with base configuration
const apiClient = axios.create({
  baseURL: process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000',
  timeout: 30000, // 30 second timeout
  headers: {
    'Content-Type': 'application/json',
  },
});

// Function to send a query to the RAG backend with enhanced error handling
export const sendQuery = async (queryData, timeoutMs = 30000) => {
  try {
    // Set timeout for this specific request if different from default
    const config = timeoutMs !== 30000 ? { timeout: timeoutMs } : {};
    const response = await apiClient.post('/query', queryData, config);
    return response.data;
  } catch (error) {
    // Handle different types of errors
    if (error.code === 'ECONNABORTED' || error.message.includes('timeout')) {
      // Request timeout
      throw new Error('Request timeout: The server took too long to respond. Please try again.');
    } else if (error.response) {
      // Server responded with error status
      const status = error.response.status;
      const errorData = error.response.data;

      if (status >= 500) {
        // Server error
        throw new Error(`Server error (${status}): The service is temporarily unavailable. Please try again later.`);
      } else if (status === 429) {
        // Rate limit
        throw new Error('Rate limit exceeded: Please wait before sending another request.');
      } else if (status === 400) {
        // Bad request
        throw new Error(`Invalid request: ${errorData?.error || 'Please check your input and try again.'}`);
      } else {
        // Other client/server errors
        throw new Error(`Request failed (${status}): ${errorData?.error || 'An error occurred'}`);
      }
    } else if (error.request) {
      // Request was made but no response received (network error)
      throw new Error('Network error: Unable to reach the backend service. Please check your connection.');
    } else {
      // Something else happened
      throw new Error(`Request error: ${error.message}`);
    }
  }
};

// Health check function to verify backend connectivity with enhanced error handling
export const checkHealth = async () => {
  try {
    const response = await apiClient.get('/health');
    return response.data;
  } catch (error) {
    if (error.code === 'ECONNABORTED' || error.message.includes('timeout')) {
      // Request timeout
      throw new Error('Health check timeout: The service is not responding.');
    } else if (error.response) {
      // Server responded with error status
      throw new Error(`Health check failed (${error.response.status}): Service may be unavailable.`);
    } else if (error.request) {
      // Request was made but no response received (network error)
      throw new Error('Health check failed: Cannot connect to the service. Please check your network connection.');
    } else {
      // Something else happened
      throw new Error(`Health check error: ${error.message}`);
    }
  }
};

// Export the apiClient for direct use if needed
export default apiClient;