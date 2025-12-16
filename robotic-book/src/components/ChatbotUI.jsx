// robotic-book/src/components/ChatbotUI.jsx
import React, { useState } from 'react';
import styles from './ChatbotUI.module.css'; // Assuming you'll create a CSS module

const ChatbotUI = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');

  const toggleChatbot = () => {
    setIsOpen(!isOpen);
  };

  const handleSendMessage = async () => {
    if (input.trim() === '') return;

    const userMessage = { text: input, sender: 'user' };
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
        text: data.status === 'error' ? data.answer || 'Sorry, something went wrong.' : data.answer,
        sources: data.sources || [],
        sender: 'bot'
      };
      setMessages((prevMessages) => [...prevMessages, botMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage = { text: 'Sorry, something went wrong.', sender: 'bot' };
      setMessages((prevMessages) => [...prevMessages, errorMessage]);
    }

    // Comment out the simulated response code:
    /*
    // Simulate API call to backend
    const simulatedBackendResponse = `This is a simulated response to your query: "${input}".`;
    const botMessage = { text: simulatedBackendResponse, sender: 'bot' };
    setTimeout(() => {
      setMessages((prevMessages) => [...prevMessages, botMessage]);
    }, 1000);
    */
  };

  return (
    <div className={styles.chatbotContainer}>
      <button className={styles.chatbotToggle} onClick={toggleChatbot}>
        {isOpen ? 'Close Chat' : 'Open Chat'}
      </button>

      {isOpen && (
        <div className={styles.chatWindow}>
          <div className={styles.messagesContainer}>
            {messages.map((msg, index) => (
              <div key={index} className={`${styles.message} ${styles[msg.sender]}`}>
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
              placeholder="Ask me about the book..."
              className={styles.chatInput}
            />
            <button onClick={handleSendMessage} className={styles.sendButton}>
              Send
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default ChatbotUI;
