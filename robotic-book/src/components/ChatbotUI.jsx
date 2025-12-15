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
                {msg.text}
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
