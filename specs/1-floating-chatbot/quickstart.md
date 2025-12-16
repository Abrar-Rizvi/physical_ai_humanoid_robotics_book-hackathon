# Quickstart Guide: Floating Chatbot UI Component

**Feature**: Floating Chatbot UI Component
**Date**: 2025-12-17

## Overview
This guide provides instructions for setting up and using the floating chatbot UI component in your Docusaurus project.

## Prerequisites
- Node.js >= 20.0
- Docusaurus 2 (v3.9.2)
- React 19
- Modern browser (Chrome, Firefox, Safari, Edge)

## Installation

### 1. Install Dependencies
```bash
npm install lucide-react  # For icons
# The component uses standard React hooks, no additional dependencies needed
```

### 2. Add Component Files
Create the following files in your Docusaurus project:

```
src/
└── components/
    └── FloatingChatbot/
        ├── FloatingChatbot.jsx
        ├── ChatWindow.jsx
        ├── MessageBubble.jsx
        └── FloatingChatbot.module.css
```

## Basic Usage

### 1. Import and Use Component
```jsx
import React, { useState } from 'react';
import FloatingChatbot from './components/FloatingChatbot';

function Layout() {
  const [isChatOpen, setIsChatOpen] = useState(false);
  const [messages, setMessages] = useState([]);

  const handleSendMessage = async (messageText) => {
    // Add user message to state
    const userMessage = {
      id: Date.now().toString(),
      content: messageText,
      sender: 'user',
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);

    // Send to backend and get response
    try {
      const response = await fetch('/api/chat/send', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: messageText,
          sessionId: 'current-session-id'
        })
      });

      const data = await response.json();
      setMessages(prev => [...prev, data]);
    } catch (error) {
      console.error('Failed to send message:', error);
    }
  };

  return (
    <div>
      {/* Your existing layout content */}
      <FloatingChatbot
        isOpen={isChatOpen}
        onToggle={() => setIsChatOpen(!isChatOpen)}
        title="AI Partner"
        subtitle="Online • Powered by RAG"
        isOnline={true}
        messages={messages}
        onSendMessage={handleSendMessage}
      />
    </div>
  );
}
```

### 2. Add to Docusaurus Layout
In your `src/theme/Layout/index.js` or appropriate layout file:

```jsx
import React, { useState } from 'react';
import OriginalLayout from '@theme-original/Layout';
import FloatingChatbot from '@site/src/components/FloatingChatbot';

export default function Layout(props) {
  const [isChatOpen, setIsChatOpen] = useState(false);
  const [messages, setMessages] = useState([]);

  const handleSendMessage = async (messageText) => {
    // Implementation as above
  };

  return (
    <>
      <OriginalLayout {...props}>
        {props.children}
      </OriginalLayout>
      <FloatingChatbot
        isOpen={isChatOpen}
        onToggle={() => setIsChatOpen(!isChatOpen)}
        title="AI Partner"
        subtitle="Online • Powered by RAG"
        isOnline={true}
        messages={messages}
        onSendMessage={handleSendMessage}
      />
    </>
  );
}
```

## Configuration Options

The component accepts the following props:

| Prop | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `isOpen` | boolean | Yes | - | Controls open/closed state |
| `onToggle` | function | Yes | - | Callback when state changes |
| `title` | string | No | "AI Partner" | Header title text |
| `subtitle` | string | No | "Online • Powered by RAG" | Header subtitle text |
| `isOnline` | boolean | No | true | Online status indicator |
| `messages` | array | No | [] | Array of message objects |
| `onSendMessage` | function | No | () => {} | Callback for sending messages |

## Styling

The component uses CSS modules for styling. You can customize the appearance by modifying the CSS file:

```css
/* FloatingChatbot.module.css */
.floatingButton {
  background-color: #2563eb; /* Primary blue */
  border: 2px solid white;
  /* Additional customizations */
}

.chatWindow {
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
  /* Additional customizations */
}
```

## API Integration

The chatbot connects to a backend service that should implement the API contracts defined in `contracts/chat-api.yaml`. Update the API endpoints in your component to match your backend configuration.

## Environment Configuration

Set the API endpoint in your environment:

```bash
# .env
REACT_APP_CHAT_API_URL=https://your-backend.com/api
```

## Development

### Running Locally
```bash
cd your-docusaurus-project
npm start
```

### Testing
The component includes unit tests for:
- Open/close functionality
- Message rendering
- State management
- Accessibility features

Run tests with:
```bash
npm test
```

## Deployment

1. Build your Docusaurus site:
```bash
npm run build
```

2. Deploy the static files to your hosting service

3. Ensure your backend API is properly configured and accessible

## Troubleshooting

### Chat Window Not Appearing
- Check that the component is properly imported and rendered
- Verify that CSS styles are loading correctly
- Ensure the component is not being blocked by other elements

### API Connection Issues
- Verify your backend API is running and accessible
- Check that CORS is properly configured
- Confirm API endpoint URLs are correct

### Mobile Responsiveness
- Test on various screen sizes
- Ensure touch targets are appropriately sized (minimum 44px)
- Verify the chat window doesn't block important content