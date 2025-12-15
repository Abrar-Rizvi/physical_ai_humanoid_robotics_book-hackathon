// Unit tests for ChatInterface component
import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import ChatInterface from '../ChatInterface';

// Mock the API service
jest.mock('../../services/api', () => ({
  sendQuery: jest.fn(),
  checkHealth: jest.fn(),
}));

// Mock the text selection utility
jest.mock('../../utils/textSelection', () => ({
  getSelectedTextWithMetadata: jest.fn(() => null),
}));

// Mock the session service
jest.mock('../../services/session', () => ({
  createNewSession: jest.fn(() => ({ id: 'session-123', messages: [] })),
  getCurrentSession: jest.fn(() => ({ id: 'session-123', messages: [] })),
  addMessageToCurrentSession: jest.fn(),
  updateSessionMetadata: jest.fn(),
  getAllSessions: jest.fn(() => []),
}));

describe('ChatInterface Component', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('renders toggle button initially', () => {
    render(<ChatInterface />);

    // Check that the toggle button is present
    const toggleButton = screen.getByLabelText(/Open chat/i);
    expect(toggleButton).toBeInTheDocument();
    expect(toggleButton).toHaveTextContent('💬');
  });

  test('opens chat window when toggle button is clicked', () => {
    render(<ChatInterface />);

    // Click the toggle button
    const toggleButton = screen.getByLabelText(/Open chat/i);
    fireEvent.click(toggleButton);

    // Check that the chat window is now visible
    expect(screen.getByLabelText(/Chat Interface/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Type your message/i)).toBeInTheDocument();
  });

  test('closes chat window when close button is clicked', () => {
    render(<ChatInterface />);

    // Open the chat first
    const toggleButton = screen.getByLabelText(/Open chat/i);
    fireEvent.click(toggleButton);

    // Then close it
    const closeButton = screen.getByLabelText(/Close chat/i);
    fireEvent.click(closeButton);

    // Check that the chat window is no longer visible
    expect(screen.queryByLabelText(/Chat Interface/i)).not.toBeInTheDocument();
  });

  test('allows typing in the input field', () => {
    render(<ChatInterface />);

    // Open the chat
    const toggleButton = screen.getByLabelText(/Open chat/i);
    fireEvent.click(toggleButton);

    // Find the input field and type in it
    const inputField = screen.getByLabelText(/Type your message/i);
    fireEvent.change(inputField, { target: { value: 'Hello, world!' } });

    // Verify the input field has the correct value
    expect(inputField.value).toBe('Hello, world!');
  });

  test('disables send button when input is empty', () => {
    render(<ChatInterface />);

    // Open the chat
    const toggleButton = screen.getByLabelText(/Open chat/i);
    fireEvent.click(toggleButton);

    // Find the send button
    const sendButton = screen.getByLabelText(/Send message/i);

    // Initially, the button should be disabled because input is empty
    expect(sendButton).toBeDisabled();

    // Type something
    const inputField = screen.getByLabelText(/Type your message/i);
    fireEvent.change(inputField, { target: { value: 'Hello' } });

    // Now the button should be enabled
    expect(sendButton).not.toBeDisabled();
  });

  test('shows welcome message when no messages exist', () => {
    render(<ChatInterface />);

    // Open the chat
    const toggleButton = screen.getByLabelText(/Open chat/i);
    fireEvent.click(toggleButton);

    // Check for welcome message
    expect(screen.getByText(/Ask me anything about the book content!/i)).toBeInTheDocument();
  });

  test('handles Enter key to send message', async () => {
    const { sendQuery } = require('../../services/api');
    sendQuery.mockResolvedValue({
      response: 'Test response',
      sources: [],
      session_id: 'session-123',
    });

    render(<ChatInterface />);

    // Open the chat
    const toggleButton = screen.getByLabelText(/Open chat/i);
    fireEvent.click(toggleButton);

    // Type a message
    const inputField = screen.getByLabelText(/Type your message/i);
    fireEvent.change(inputField, { target: { value: 'Test question' } });

    // Simulate pressing Enter
    fireEvent.keyPress(inputField, { key: 'Enter', code: 'Enter', char: 'Enter', shiftKey: false });

    // Wait for the API call to complete
    await waitFor(() => {
      expect(sendQuery).toHaveBeenCalled();
    });
  });

  test('shows loading state when sending message', async () => {
    const { sendQuery } = require('../../services/api');
    // Mock a delayed response to see the loading state
    sendQuery.mockImplementation(() => new Promise(resolve => {
      setTimeout(() => resolve({
        response: 'Test response',
        sources: [],
        session_id: 'session-123',
      }), 100);
    }));

    render(<ChatInterface />);

    // Open the chat
    const toggleButton = screen.getByLabelText(/Open chat/i);
    fireEvent.click(toggleButton);

    // Type a message
    const inputField = screen.getByLabelText(/Type your message/i);
    fireEvent.change(inputField, { target: { value: 'Test question' } });

    // Click send button
    const sendButton = screen.getByLabelText(/Send message/i);
    fireEvent.click(sendButton);

    // Verify loading state appears
    expect(screen.getByText('Sending...')).toBeInTheDocument();
    expect(sendButton).toBeDisabled();
  });

  test('displays error message when API call fails', async () => {
    const { sendQuery } = require('../../services/api');
    sendQuery.mockRejectedValue(new Error('API Error'));

    render(<ChatInterface />);

    // Open the chat
    const toggleButton = screen.getByLabelText(/Open chat/i);
    fireEvent.click(toggleButton);

    // Type a message
    const inputField = screen.getByLabelText(/Type your message/i);
    fireEvent.change(inputField, { target: { value: 'Test question' } });

    // Click send button
    const sendButton = screen.getByLabelText(/Send message/i);
    fireEvent.click(sendButton);

    // Wait for the error to be displayed
    await waitFor(() => {
      expect(screen.getByText(/Error: API Error/)).toBeInTheDocument();
    });
  });
});