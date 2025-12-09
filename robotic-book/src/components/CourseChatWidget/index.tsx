// robotic-book/src/components/CourseChatWidget/index.tsx

import React, { useState, useRef, useEffect } from 'react';
import styles from './styles.module.css';
import type { Message, WidgetState } from './types';

const API_BASE_URL = process.env.NODE_ENV === 'production'
  ? 'https://api.example.com/api/v1'  // Replace with actual production URL
  : 'http://localhost:8000/api/v1';

// T014: Helper function to generate unique message IDs
function generateId(): string {
  return `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
}

// T015: Helper function to extract current page context
function extractPageContext() {
  return {
    title: typeof document !== 'undefined' ? document.title : '',
    pathname: typeof window !== 'undefined' ? window.location.pathname : '/',
  };
}

export default function CourseChatWidget() {
  // T013: Component state
  const [state, setState] = useState<WidgetState>({
    isOpen: false,
    messages: [],
    inputValue: '',
    isLoading: false,
    errorMessage: null,
  });

  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  // T020: Auto-scroll to latest message
  useEffect(() => {
    if (state.isOpen) {
      messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }
  }, [state.messages, state.isOpen]);

  // T021: Focus input when widget opens
  useEffect(() => {
    if (state.isOpen) {
      inputRef.current?.focus();
    }
  }, [state.isOpen]);

  // T016: Toggle button handler
  const toggleWidget = () => {
    setState(prev => ({ ...prev, isOpen: !prev.isOpen }));
  };

  // T019: Send message function with mock response (MVP - no API call yet)
  const sendMessage = async () => {
    if (!state.inputValue.trim() || state.isLoading) return;

    const userMessage: Message = {
      id: generateId(),
      text: state.inputValue.trim(),
      sender: 'user',
      timestamp: Date.now(),
      status: 'pending',
    };

    setState(prev => ({
      ...prev,
      messages: [...prev.messages, userMessage],
      inputValue: '',
      isLoading: true,
      errorMessage: null,
    }));

    // Mock response for MVP (Phase 3)
    // API integration will be added in Phase 4 (US2)
    setTimeout(() => {
      const botMessage: Message = {
        id: generateId(),
        text: `This is a mock response to: "${userMessage.text}". The AI backend will be integrated in Phase 4.`,
        sender: 'bot',
        timestamp: Date.now(),
      };

      setState(prev => ({
        ...prev,
        messages: prev.messages.map(msg =>
          msg.id === userMessage.id ? { ...msg, status: 'sent' } : msg
        ).concat(botMessage),
        isLoading: false,
      }));
    }, 1000);
  };

  // T022: Keyboard support (Enter to send, Escape to close)
  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    } else if (e.key === 'Escape') {
      setState(prev => ({ ...prev, isOpen: false }));
    }
  };

  return (
    <div className={styles.container}>
      {/* T016: Toggle button (icon) */}
      {!state.isOpen && (
        <button
          className={styles.toggleButton}
          onClick={toggleWidget}
          aria-label="Open course chat assistant"
        >
          💬
        </button>
      )}

      {/* T017-T018: Chat panel structure and message rendering */}
      {state.isOpen && (
        <div className={styles.panel} role="dialog" aria-label="Course chat assistant">
          {/* Header */}
          <div className={styles.header}>
            <h3>Course Assistant</h3>
            <button
              className={styles.closeButton}
              onClick={toggleWidget}
              aria-label="Close chat"
            >
              ✕
            </button>
          </div>

          {/* Messages container */}
          <div className={styles.messagesContainer}>
            {state.messages.map(msg => (
              <div
                key={msg.id}
                className={`${styles.message} ${styles[msg.sender]}`}
              >
                {msg.text}
              </div>
            ))}
            {state.isLoading && (
              <div className={styles.loadingIndicator}>...</div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Input container */}
          <div className={styles.inputContainer}>
            <input
              ref={inputRef}
              type="text"
              value={state.inputValue}
              onChange={e => setState(prev => ({ ...prev, inputValue: e.target.value }))}
              onKeyDown={handleKeyPress}
              placeholder="Ask about this page..."
              className={styles.input}
              disabled={state.isLoading}
            />
            <button
              onClick={sendMessage}
              disabled={!state.inputValue.trim() || state.isLoading}
              className={styles.sendButton}
            >
              Send
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
