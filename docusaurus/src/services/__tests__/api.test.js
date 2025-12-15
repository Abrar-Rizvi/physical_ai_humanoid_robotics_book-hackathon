// Unit tests for API service
import axios from 'axios';
import { sendQuery, checkHealth } from '../api';

// Mock axios
jest.mock('axios');
const mockedAxios = axios;

describe('API Service', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('sendQuery', () => {
    test('successfully sends a query and returns response', async () => {
      const mockResponse = {
        response: 'Test response',
        sources: [{ id: 'source-1', title: 'Test Source', content: 'Test content' }],
        session_id: 'session-123',
        metadata: { processing_time: 1000 }
      };

      mockedAxios.post.mockResolvedValue({ data: mockResponse });

      const queryData = {
        query: 'Test question',
        context: 'Test context',
        session_id: 'session-123'
      };

      const result = await sendQuery(queryData);

      expect(mockedAxios.post).toHaveBeenCalledWith('/query', queryData);
      expect(result).toEqual(mockResponse);
    });

    test('handles 5xx server errors', async () => {
      const mockError = {
        response: {
          status: 500,
          data: { error: 'Internal server error' }
        }
      };
      mockedAxios.post.mockRejectedValue(mockError);

      const queryData = {
        query: 'Test question',
        context: 'Test context',
        session_id: 'session-123'
      };

      await expect(sendQuery(queryData))
        .rejects
        .toThrow('Server error (500): The service is temporarily unavailable. Please try again later.');
    });

    test('handles 429 rate limit errors', async () => {
      const mockError = {
        response: {
          status: 429,
          data: { error: 'Rate limit exceeded' }
        }
      };
      mockedAxios.post.mockRejectedValue(mockError);

      const queryData = {
        query: 'Test question',
        context: 'Test context',
        session_id: 'session-123'
      };

      await expect(sendQuery(queryData))
        .rejects
        .toThrow('Rate limit exceeded: Please wait before sending another request.');
    });

    test('handles 400 bad request errors', async () => {
      const mockError = {
        response: {
          status: 400,
          data: { error: 'Invalid query format' }
        }
      };
      mockedAxios.post.mockRejectedValue(mockError);

      const queryData = {
        query: 'Test question',
        context: 'Test context',
        session_id: 'session-123'
      };

      await expect(sendQuery(queryData))
        .rejects
        .toThrow('Invalid request: Invalid query format');
    });

    test('handles network errors', async () => {
      const mockError = {
        request: {}
      };
      mockedAxios.post.mockRejectedValue(mockError);

      const queryData = {
        query: 'Test question',
        context: 'Test context',
        session_id: 'session-123'
      };

      await expect(sendQuery(queryData))
        .rejects
        .toThrow('Network error: Unable to reach the backend service. Please check your connection.');
    });

    test('handles timeout errors', async () => {
      const mockError = {
        code: 'ECONNABORTED',
        message: 'timeout of 30000ms exceeded'
      };
      mockedAxios.post.mockRejectedValue(mockError);

      const queryData = {
        query: 'Test question',
        context: 'Test context',
        session_id: 'session-123'
      };

      await expect(sendQuery(queryData))
        .rejects
        .toThrow('Request timeout: The server took too long to respond. Please try again.');
    });
  });

  describe('checkHealth', () => {
    test('successfully checks health and returns response', async () => {
      const mockResponse = {
        status: 'healthy',
        services: { qdrant: 'healthy', openai: 'healthy' }
      };

      mockedAxios.get.mockResolvedValue({ data: mockResponse });

      const result = await checkHealth();

      expect(mockedAxios.get).toHaveBeenCalledWith('/health');
      expect(result).toEqual(mockResponse);
    });

    test('handles health check errors', async () => {
      const mockError = {
        response: {
          status: 503,
          data: { error: 'Service unavailable' }
        }
      };
      mockedAxios.get.mockRejectedValue(mockError);

      await expect(checkHealth())
        .rejects
        .toThrow('Health check failed (503): Service may be unavailable.');
    });
  });
});