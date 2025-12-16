// robotic-book/src/components/ChatbotUI.jsx
import React, { useState } from 'react';
import { MessageCircle, X } from 'lucide-react';
import styles from './ChatbotUI.module.css';

const ChatbotUI = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');

  const toggleChatbot = () => {
    setIsOpen(!isOpen);
  };

  const handleSendMessage = async () => {
    if (input.trim() === '') return;

    const userMessage = {
      id: Date.now().toString(),
      text: input,
      sender: 'user',
      timestamp: new Date()
    };
    setMessages((prevMessages) => [...prevMessages, userMessage]);
    setInput('');

    // In a real application, you would make an actual API call:
    try {
      const response = await fetch('http://127.0.0.1:8000/query', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: input,
          context: "", // Context from selected text could be added here
          session_id: 'session-' + Date.now(), // Generate a simple session ID
        }),
      });
      const data = await response.json();
      const botMessage = {
        id: (Date.now() + 1).toString(),
        text: data.status === 'error' ? data.answer || 'Sorry, something went wrong.' : data.answer,
        sources: data.sources || [],
        sender: 'assistant',
        timestamp: new Date()
      };
      setMessages((prevMessages) => [...prevMessages, botMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage = {
        id: (Date.now() + 1).toString(),
        text: 'Sorry, something went wrong.',
        sender: 'assistant',
        timestamp: new Date()
      };
      setMessages((prevMessages) => [...prevMessages, errorMessage]);
    }
  };

  return (
    <div className={styles.chatbotContainer}>
      {!isOpen ? (
        // Floating Chatbot Button (Closed State)
        <button
          className={styles.floatingButton}
          onClick={toggleChatbot}
          aria-label="Open AI Companion chat"
        >
          <MessageCircle
            size={24}
            color="white"
            strokeWidth={2}
            className={styles.chatIcon}
          />
        </button>
      ) : (
        // Chat Window (Open State)
        <div className={styles.chatWindow}>
          {/* Header Section */}
          <div className={styles.header}>
            <div className={styles.headerContent}>
              <div className={styles.statusContainer}>
                <span className={styles.onlineDot}></span>
                <div>
                  <div className={styles.title}>AI Companion</div>
                  <div className={styles.subtitle}>Online • Powered by RAG</div>
                </div>
              </div>
              <button
                className={styles.closeButton}
                onClick={toggleChatbot}
                aria-label="Close chat"
              >
                <X size={20} color="white" />
              </button>
            </div>
          </div>

          {/* Messages Container */}
          <div className={styles.messagesContainer}>
            {messages.map((msg, index) => (
              <div
                key={msg.id}
                className={`${styles.message} ${msg.sender === 'user' ? styles.userMessage : styles.assistantMessage}`}
              >
                <div className={styles.messageText}>{msg.text}</div>
                {msg.sources && msg.sources.length > 0 && (
                  <div className={styles.sourcesContainer}>
                    <details className={styles.sourcesDetails}>
                      <summary className={styles.sourcesSummary}>
                        Sources:
                      </summary>
                      <ul className={styles.sourcesList}>
                        {msg.sources.map((source, idx) => {
                          // Handle different possible source formats
                          let title = 'Source';
                          let url = null;
                          let content = null;

                          if (typeof source === 'string') {
                            // If source is just a string
                            title = source.length > 50 ? source.substring(0, 50) + '...' : source;
                            content = source;
                          } else if (typeof source === 'object' && source !== null) {
                            // If source is an object, try to extract meaningful fields
                            title = source.title || source.page_title || source.metadata?.title || source.metadata?.source || `Source ${idx + 1}`;
                            url = source.url || source.metadata?.url || source.metadata?.source_url || null;
                            content = source.content || source.content_snippet || source.text || null;
                          } else {
                            // Fallback for any other type
                            title = `Source ${idx + 1}`;
                          }

                          return (
                            <li key={idx} className={styles.sourceItem}>
                              {url ? (
                                <a
                                  href={url}
                                  target="_blank"
                                  rel="noopener noreferrer"
                                  className={styles.sourceLink}
                                >
                                  {title}
                                </a>
                              ) : (
                                <span className={styles.sourceText}>
                                  {title}
                                  {content && (
                                    <div className={styles.sourceContentPreview}>
                                      {content.length > 100 ? content.substring(0, 100) + '...' : content}
                                    </div>
                                  )}
                                </span>
                              )}
                            </li>
                          );
                        })}
                      </ul>
                    </details>
                  </div>
                )}
              </div>
            ))}
          </div>

          {/* Input Area */}
          <div className={styles.inputContainer}>
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={(e) => {
                if (e.key === 'Enter') {
                  handleSendMessage();
                }
              }}
              placeholder="Type a message..."
              className={styles.chatInput}
            />
            <button
              onClick={handleSendMessage}
              className={styles.sendButton}
              aria-label="Send message"
            >
              Send
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default ChatbotUI;
