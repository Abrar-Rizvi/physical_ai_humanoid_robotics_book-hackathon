// ChatInterface component for RAG Chatbot
// Implements the basic chat UI with constitution-compliant positioning
import React, { useState, useEffect, useRef } from 'react';
import { sendQuery } from '../services/api';
import { getSelectedTextWithMetadata } from '../utils/textSelection';
import {
  createNewSession,
  getCurrentSession,
  addMessageToCurrentSession,
  updateSessionMetadata
} from '../services/session';
import { ChatMessage } from '../types/chat';

import './ChatInterface.css'; // Import the CSS file

const ChatInterface = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [session, setSession] = useState(null);

  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  // Initialize the chat session
  useEffect(() => {
    const currentSession = getCurrentSession();
    if (currentSession) {
      setSession(currentSession);
      setMessages(currentSession.messages || []);
    } else {
      const newSession = createNewSession();
      setSession(newSession);
      setMessages([]);
    }
  }, []);

  // Scroll to bottom of messages
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  // Validate input according to data-model.md rules
  const validateInput = (query, context) => {
    // Query validation: 1-2000 characters
    if (!query || query.trim().length < 1) {
      throw new Error('Query cannot be empty');
    }
    if (query.length > 2000) {
      throw new Error('Query exceeds maximum length of 2000 characters');
    }

    // Context validation: if provided, 1-5000 characters
    if (context && context.length > 0) {
      if (context.length > 5000) {
        throw new Error('Selected text context exceeds maximum length of 5000 characters');
      }
    }

    // Basic XSS prevention - sanitize inputs
    // Note: For production, consider using a more robust sanitization library
    const sanitizeInput = (input) => {
      if (typeof input !== 'string') return input;
      return input.replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, '')
                 .replace(/javascript:/gi, '')
                 .replace(/on\w+\s*=/gi, '');
    };

    return {
      query: sanitizeInput(query),
      context: context ? sanitizeInput(context) : null
    };
  };

  // Logging utility function
  const logEvent = (event, details) => {
    // In a real application, this might send logs to an external service
    console.log(`[ChatInterface] ${event}`, {
      timestamp: new Date().toISOString(),
      sessionId: session?.id,
      ...details
    });
  };

  // Handle sending a message
  const handleSend = async () => {
    if (!inputValue.trim() || isLoading) return;

    try {
      setIsLoading(true);
      setError(null);

      // Log the start of the query
      logEvent('query_start', { queryLength: inputValue.length });

      // Get any selected text context with metadata
      const selectedTextData = getSelectedTextWithMetadata();

      // Validate inputs according to data-model.md rules
      const validatedInputs = validateInput(inputValue, selectedTextData?.text || null);

      // Create user message
      const userMessage = {
        id: `msg_${Date.now()}`,
        role: 'user',
        content: validatedInputs.query,
        timestamp: new Date().toISOString()
      };

      // Add user message to state
      const updatedMessages = [...messages, userMessage];
      setMessages(updatedMessages);

      // Prepare query data
      const queryData = {
        query: validatedInputs.query,
        context: validatedInputs.context || undefined,
        session_id: session?.id,
        metadata: {
          page_url: window.location.href,
          timestamp: new Date().toISOString(),
          user_agent: navigator.userAgent,
          selected_text_metadata: selectedTextData || undefined
        }
      };

      // Send query to backend
      const response = await sendQuery(queryData);

      // Log successful response
      logEvent('query_success', {
        responseLength: response.response.length,
        sourceCount: response.sources?.length || 0
      });

      // Create assistant message
      const assistantMessage = {
        id: `msg_${Date.now() + 1}`,
        role: 'assistant',
        content: response.response,
        sources: response.sources,
        timestamp: new Date().toISOString()
      };

      // Update messages state
      const finalMessages = [...updatedMessages, assistantMessage];
      setMessages(finalMessages);

      // Update session with new messages
      if (session) {
        const updatedSession = {
          ...session,
          messages: finalMessages,
          last_activity: new Date().toISOString()
        };
        setSession(updatedSession);
        addMessageToCurrentSession(userMessage);
        addMessageToCurrentSession(assistantMessage);
      }

      // Clear input
      setInputValue('');

    } catch (err) {
      setError(err.message);
      logEvent('query_error', { error: err.message });
      console.error('Error sending message:', err);
    } finally {
      setIsLoading(false);
      logEvent('query_complete');
    }
  };

  // Handle key press (Enter to send)
  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  // Toggle chat window open/close
  const toggleChat = () => {
    setIsOpen(!isOpen);
    if (!isOpen) {
      // Focus input when opening
      setTimeout(() => inputRef.current?.focus(), 100);
    }
  };

  // Close chat window
  const closeChat = () => {
    setIsOpen(false);
  };

  return (
    <div className="chat-interface" role="complementary" aria-label="Book Assistant Chat">
      {/* Chat Window */}
      {isOpen && (
        <div
          className="chat-window"
          role="dialog"
          aria-modal="true"
          aria-label="Chat Interface"
          onKeyDown={(e) => {
            // Close chat with Escape key
            if (e.key === 'Escape') {
              closeChat();
            }
          }}
        >
          <div className="chat-header" role="banner">
            <span className="chat-title">Book Assistant</span>
            <button
              className="chat-close-btn"
              onClick={closeChat}
              aria-label="Close chat"
              onKeyDown={(e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                  closeChat();
                }
              }}
            >
              ×
            </button>
          </div>

          <div
            className="chat-messages"
            role="log"
            aria-live="polite"
            aria-relevant="additions"
          >
            {messages.length === 0 ? (
              <div className="chat-welcome" role="status" aria-live="polite">
                <p>Ask me anything about the book content!</p>
                <p>I can help explain concepts and provide information based on the book.</p>
              </div>
            ) : (
              messages.map((message) => (
                <div
                  key={message.id}
                  className={`chat-message ${message.role === 'user' ? 'user-message' : 'assistant-message'}`}
                  role="listitem"
                  aria-label={`${message.role === 'user' ? 'Your message' : 'Assistant response'}: ${message.content.substring(0, 50)}...`}
                >
                  <div className="message-content">
                    {message.content}
                  </div>
                  {message.sources && message.sources.length > 0 && (
                    <div className="message-sources">
                      <details>
                        <summary aria-label="Toggle sources visibility">
                          Sources:
                        </summary>
                        <ul aria-label="Sources for this response">
                          {message.sources.map((source, idx) => (
                            <li key={idx}>
                              <a
                                href={source.url}
                                target="_blank"
                                rel="noopener noreferrer"
                                aria-label={`Source: ${source.title}`}
                              >
                                {source.title}
                              </a>
                            </li>
                          ))}
                        </ul>
                      </details>
                    </div>
                  )}
                </div>
              ))
            )}
            {isLoading && (
              <div className="chat-message assistant-message" role="status" aria-live="polite">
                <div className="message-content">
                  <em>Thinking...</em>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} aria-hidden="true" />
          </div>

          {error && (
            <div className="chat-error" role="alert" aria-live="assertive">
              Error: {error}
            </div>
          )}

          <div className="chat-input-area" role="form" aria-label="Message composition">
            <textarea
              ref={inputRef}
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask a question about the book..."
              className="chat-input"
              rows="2"
              disabled={isLoading}
              aria-label="Type your message"
              aria-required="true"
              onKeyDown={(e) => {
                // Navigate with arrow keys if needed
                if (e.key === 'Escape') {
                  closeChat();
                }
              }}
            />
            <button
              onClick={handleSend}
              className="chat-send-btn"
              disabled={!inputValue.trim() || isLoading}
              aria-label="Send message"
              aria-disabled={isLoading || !inputValue.trim()}
            >
              {isLoading ? 'Sending...' : 'Send'}
            </button>
          </div>
        </div>
      )}

      {/* Chat Toggle Button */}
      <button
        className={`chat-toggle-btn ${isOpen ? 'open' : ''}`}
        onClick={toggleChat}
        aria-label={isOpen ? "Close chat" : "Open chat"}
        aria-expanded={isOpen}
        aria-controls="chat-window"
        onKeyDown={(e) => {
          if (e.key === 'Enter' || e.key === ' ') {
            toggleChat();
          } else if (e.key === 'Escape' && isOpen) {
            closeChat();
          }
        }}
      >
        💬
      </button>
    </div>
  );
};

export default ChatInterface;