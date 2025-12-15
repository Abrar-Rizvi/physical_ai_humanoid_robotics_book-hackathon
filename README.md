# Humanoid Robotics Book with RAG Chatbot Integration

This project contains the implementation of a RAG (Retrieval-Augmented Generation) chatbot integrated into a Docusaurus-based documentation site for the Humanoid Robotics Book project.

## Project Structure

- `backend/` - FastAPI RAG agent backend
- `docusaurus/` - Docusaurus frontend with chatbot integration
- `specs/` - Specification documents for various features
- `history/` - Historical prompts and development records

## Frontend Chat Interface Integration

The chat interface is implemented as a React component that follows the constitution requirements for mobile-first design, dark mode compatibility, and zero layout breaks.

### Key Features

- **Fixed Position**: Bottom-right corner, 20px from edges
- **Click-to-Open**: Non-intrusive interface that doesn't auto-expand
- **Responsive Design**: Max 400px desktop, full-width minus 20px mobile
- **Dark Mode Support**: Uses CSS variables for automatic theme compatibility
- **Selected Text Integration**: Automatically includes selected text as context
- **Session Management**: Maintains conversation history in local storage
- **Accessibility**: Full keyboard navigation and ARIA support

### Components

- `docusaurus/src/components/ChatInterface.jsx` - Main chat component
- `docusaurus/src/components/ChatInterface.css` - Constitution-compliant styling
- `docusaurus/src/services/api.js` - API communication layer
- `docusaurus/src/utils/textSelection.js` - Text selection utilities
- `docusaurus/src/services/session.js` - Session management
- `docusaurus/src/types/chat.d.ts` - TypeScript type definitions

### Integration Instructions

1. **Environment Setup**:
   ```bash
   # Copy the example environment file
   cd docusaurus
   cp .env.example .env
   # Update REACT_APP_API_BASE_URL to point to your backend
   ```

2. **Backend Requirements**:
   - Ensure the FastAPI backend is running and accessible
   - The backend must expose `/query` and `/health` endpoints
   - Configure OpenAI and Qdrant as needed

3. **Docusaurus Integration**:
   - Import the ChatInterface component in your Docusaurus layout
   - The component uses fixed positioning and will not affect your document flow
   - No additional dependencies required beyond standard Docusaurus setup

4. **Usage**:
   - The chat interface will appear as a floating button in the bottom-right corner
   - Users can click to expand and interact with the RAG agent
   - Selected text on the page is automatically captured as context

### API Communication

The chat interface communicates with the backend using the following API calls:

- `POST /query` - Send user queries to the RAG agent
- `GET /health` - Check backend health status

### Configuration

The component is configured via environment variables:

- `REACT_APP_API_BASE_URL` - Base URL for the backend API (default: http://localhost:8000)

### Testing

Unit tests are available in:
- `docusaurus/src/components/__tests__/`
- `docusaurus/src/services/__tests__/`
- `docusaurus/src/utils/__tests__/`

## Backend Requirements

The frontend expects a backend with the following endpoints:

- `/query` - Accepts POST requests with query, context, and session_id
- `/health` - Returns system health status

See the API contract in `specs/001-rag-chatbot-frontend-integration/plan/contracts/openapi.yaml` for detailed specifications.

## Constitution Compliance

This implementation follows the project constitution requirements:
- Mobile-first responsive design
- Dark mode compatibility using CSS variables
- Zero layout breaks (fixed positioning)
- Lightweight implementation
- Accessibility features
- Click-to-open interaction model
- Touch-optimized targets (min 44px)

## Development

To run the Docusaurus frontend locally:

```bash
cd docusaurus
npm install
npm start
```

## Documentation

- Implementation guide: `docusaurus/docs/chat-interface-implementation.md`
- API contracts: `specs/001-rag-chatbot-frontend-integration/plan/contracts/openapi.yaml`
- Full specification: `specs/001-rag-chatbot-frontend-integration/spec.md`