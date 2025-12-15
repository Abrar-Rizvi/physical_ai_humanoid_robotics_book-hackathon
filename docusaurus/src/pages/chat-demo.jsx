import React from 'react';
import ChatInterface from '../components/ChatInterface';

const ChatDemoPage = () => {
  return (
    <div style={{ padding: '2rem' }}>
      <h1>Humanoid Robotics Book - Interactive Assistant</h1>
      <p>
        This page demonstrates the integration of the RAG Chatbot with the book content.
        The floating chat icon at the bottom-right of the screen allows you to ask questions
        about the content on this page or any other page in the documentation.
      </p>

      <div style={{ margin: '2rem 0', padding: '1rem', backgroundColor: '#f0f8ff', borderRadius: '4px' }}>
        <h2>Sample Content</h2>
        <p>
          Humanoid robotics is an interdisciplinary branch of robotics that focuses on the design,
          construction, and operation of robots that resemble humans in appearance and behavior.
          These robots typically have a head, torso, two arms, and two legs, and are designed
          to interact with human environments and perform tasks in human-like ways.
        </p>
        <p>
          The development of humanoid robots involves expertise from various fields including
          mechanical engineering, electrical engineering, computer science, and cognitive science.
          One of the key challenges in humanoid robotics is creating robots that can walk and
          maintain balance, which requires sophisticated control systems and sensors.
        </p>
      </div>

      <div style={{ margin: '2rem 0' }}>
        <h3>How it Works</h3>
        <ul>
          <li>Select any text on this page and ask questions about it</li>
          <li>The chatbot will provide answers based on the book content</li>
          <li>Responses include source attribution for transparency</li>
          <li>Conversations are maintained across page navigation</li>
        </ul>
      </div>

      {/* The ChatInterface component is automatically positioned at bottom-right */}
      <ChatInterface />
    </div>
  );
};

export default ChatDemoPage;