# Quickstart Guide: RAG Chatbot Backend-Frontend Integration

## Overview
This guide will help you set up and run the RAG Chatbot Backend-Frontend integration locally. The integration connects the Docusaurus frontend with the FastAPI RAG agent backend, enabling users to ask questions about book content through an embedded chat interface. The implementation follows the constitution requirements for mobile-first design, dark mode compatibility, and zero layout breaks.

## Prerequisites
- Node.js (v16 or higher)
- Python (v3.8 or higher)
- Access to OpenAI API key
- Access to Qdrant vector database
- Git
- Ensure you have followed the constitution requirements for development environment

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Backend Setup
1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Set up environment variables by copying the example:
```bash
cp .env.example .env
# Edit .env with your actual API keys and configuration
```

4. Start the backend server:
```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Frontend Setup (Docusaurus)
1. Navigate to the Docusaurus directory:
```bash
cd docusaurus  # or wherever your Docusaurus site is located
```

2. Install dependencies:
```bash
npm install
```

3. Start the Docusaurus development server:
```bash
npm start
```

### 4. Verify Integration
1. The backend should be running on `http://localhost:8000`
2. The frontend should be running on `http://localhost:3000`
3. Access any book page in the Docusaurus frontend
4. Look for the chat interface widget in the bottom-right corner (per constitution requirement)
5. Test by submitting a query and verifying you receive a response

## Configuration

### Environment Variables
Ensure the following variables are set in your backend `.env` file:
- `OPENAI_API_KEY`: Your OpenAI API key
- `QDRANT_URL`: URL to your Qdrant instance
- `QDRANT_API_KEY`: API key for Qdrant (if required)
- `QDRANT_COLLECTION_NAME`: Name of your Qdrant collection

### Constitution Compliance Settings
The chat widget is configured to meet all constitution requirements:
- Position: Bottom-right corner, 20px from edges (fixed positioning)
- Initial state: Collapsed icon/button (non-intrusive)
- Interaction: Click-to-open only (no auto-expansion)
- Size: Max 400px width on desktop, full-width minus 20px on mobile
- Theme: Uses CSS variables for automatic light/dark mode compatibility

## Testing the Integration

### Basic Query Test
1. Go to any book page in the Docusaurus frontend
2. Click the chat widget icon to expand it
3. Type a question about the book content in the chat interface
4. Submit the query
5. Verify you receive a relevant, grounded response from the backend (no hallucination)
6. Check that sources are properly attributed in the response

### Selected Text Test
1. Select some text on a book page (not in the chat widget)
2. The chat interface should capture this selection when you open it
3. Submit the query with the selected text context
4. Verify the selected text is included as context in the backend request
5. Check that the response is contextually relevant to the selected text

### Mobile Responsiveness Test
1. Open the Docusaurus site on a mobile device or use browser dev tools
2. Verify the chat widget appears correctly positioned
3. Test that the expanded chat interface is fully usable on mobile
4. Confirm the widget width adapts to full-width minus 20px as required

### Dark Mode Test
1. Toggle the Docusaurus site to dark mode
2. Verify the chat widget automatically adapts to dark theme
3. Check that all text remains readable and colors are appropriate
4. Confirm all interactive elements remain visible and accessible

### Zero Layout Break Test
1. Load a book page with the chat widget loaded
2. Verify the page content layout is not affected by the widget
3. Check that the widget uses fixed positioning and doesn't impact document flow
4. Confirm navigation and footer elements remain unaffected

### Error Handling Test
1. Temporarily stop the backend server
2. Try submitting a query from the frontend
3. Verify appropriate error message is displayed (user-friendly, not exposing internals)
4. Restart the backend and confirm normal operation resumes

## Performance Testing

### Page Load Impact
1. Measure initial page load time with the chat widget loaded
2. Verify the widget code is lazy-loaded and doesn't block initial page rendering
3. Confirm the widget doesn't significantly impact Core Web Vitals

### Response Time Test
1. Submit multiple queries and measure response times
2. Verify 95% of queries respond within 10 seconds as specified in requirements
3. Check that loading indicators provide feedback during processing

## Troubleshooting

### Common Issues

#### Chat Widget Not Appearing
- Verify the component is properly imported and rendered in your Docusaurus layout
- Check browser console for JavaScript errors
- Ensure the fixed positioning CSS is not being overridden

#### Backend Not Responding
- Verify backend server is running on port 8000
- Check that environment variables are correctly set
- Confirm API keys are valid and have necessary permissions
- Check CORS configuration on the backend

#### CORS Errors
- Ensure backend is configured to allow requests from frontend origin
- Check backend logs for CORS-related error messages
- Verify the frontend URL is added to the allowed origins list

#### Layout Breaks
- Verify the widget uses fixed positioning (not affecting document flow)
- Check that no CSS is interfering with page layout
- Confirm the widget doesn't cause unwanted scrolling or reflow

#### Dark Mode Issues
- Verify CSS variables are properly defined and used
- Check that all colors adapt properly to the theme
- Confirm the widget respects the Docusaurus theme context

#### Mobile Responsiveness Issues
- Verify the responsive width settings are correctly applied
- Check that touch targets meet the 44px minimum requirement
- Confirm the interface is usable on various screen sizes

## Next Steps
- Customize the chat interface styling while maintaining constitution compliance
- Implement additional accessibility features (keyboard navigation, ARIA labels)
- Add analytics to track usage while respecting privacy requirements
- Set up proper error monitoring and logging
- Conduct comprehensive testing on various devices and browsers