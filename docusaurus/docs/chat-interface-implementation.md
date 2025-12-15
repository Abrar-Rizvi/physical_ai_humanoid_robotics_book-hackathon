# Chat Interface Implementation Guide

## Overview

The Chat Interface component provides a seamless way for users to interact with the RAG (Retrieval-Augmented Generation) chatbot directly within the book content pages. The component follows the constitution requirements for mobile-first design, dark mode compatibility, and zero layout breaks.

## Architecture

### Component Structure
- `ChatInterface.jsx` - Main React component
- `ChatInterface.css` - Constitution-compliant styling
- `types/chat.d.ts` - TypeScript type definitions
- `services/api.js` - API communication layer
- `utils/textSelection.js` - Text selection utilities
- `services/session.js` - Session management

### Key Features
- Fixed-position chat widget (bottom-right, 20px offset)
- Click-to-open functionality (no auto-expansion)
- Responsive design (max 400px desktop, full-width-20px mobile)
- Dark mode compatibility using CSS variables
- Selected text integration
- Session management with local storage
- Input validation and sanitization
- Accessibility features (ARIA labels, keyboard navigation)

## API Integration

The component communicates with the backend RAG agent through the API service:

```javascript
const response = await sendQuery({
  query: userQuery,
  context: selectedTextContext, // optional
  session_id: currentSessionId, // optional
  metadata: {
    page_url: window.location.href,
    timestamp: new Date().toISOString(),
    user_agent: navigator.userAgent,
    selected_text_metadata: selectedTextData // optional
  }
});
```

## Text Selection

The component uses the browser's Selection API to capture selected text:

- `getSelectedTextWithMetadata()` - Gets selected text with position and container information
- Context is automatically included when sending queries
- Selection metadata includes container tag, ID, and class for better context

## Session Management

Sessions are managed using local storage:

- Each session contains messages and metadata
- Sessions persist across page reloads
- Multiple sessions are supported but only one active at a time

## Error Handling

Comprehensive error handling includes:

- Network error detection and user-friendly messages
- Timeout handling (30 second default)
- Rate limit detection
- Input validation errors
- Server error handling

## Validation & Sanitization

Inputs are validated according to data-model.md requirements:

- Query: 1-2000 characters
- Context: 1-5000 characters (if provided)
- XSS prevention through input sanitization
- Proper error messages for validation failures

## Accessibility

The component includes:

- Proper ARIA labels and roles
- Keyboard navigation support (Enter, Escape, Space)
- Screen reader compatibility
- Focus management
- Semantic HTML structure

## Styling

CSS follows constitution requirements:

- Fixed positioning (bottom-right corner)
- Responsive design
- CSS variables for theme compatibility
- Touch-optimized targets (min 44px)
- Zero layout breaks (fixed position, doesn't affect document flow)

## Testing

Unit tests are available in:
- `src/components/__tests__/ChatInterface.test.js`
- `src/services/__tests__/api.test.js`
- `src/utils/__tests__/textSelection.test.js`

## Environment Configuration

The component uses environment variables:

```bash
# .env.example
REACT_APP_API_BASE_URL=http://localhost:8000
```

## Integration

To integrate the chat component into Docusaurus pages:

1. Import the component: `import ChatInterface from './path/to/ChatInterface';`
2. Add to your layout or page component
3. Ensure API backend is running and accessible

## Performance

The component is optimized for performance:
- Efficient state management with React hooks
- Memoization where appropriate
- Minimal DOM updates
- Lazy loading capabilities
- Lightweight CSS with no external dependencies