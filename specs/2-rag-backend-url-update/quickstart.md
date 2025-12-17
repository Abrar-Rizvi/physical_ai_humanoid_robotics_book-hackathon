# Quickstart Guide: RAG Backend URL Update

**Feature**: RAG Backend URL Update
**Date**: 2025-12-17

## Overview
This guide provides instructions for updating the RAG chatbot frontend to use the deployed Render backend instead of the local development backend.

## Prerequisites
- Git repository access
- Node.js environment for frontend (already configured)
- Understanding of the current frontend codebase
- Access to the deployed Render backend URL

## Current Configuration
- **Frontend API URL**: `http://127.0.0.1:8000/query`
- **Target API URL**: `https://physical-ai-humanoid-robotics-book-v4wt.onrender.com/query`
- **Backend Technology**: FastAPI server
- **Frontend Component**: `robotic-book/src/components/ChatbotUI.jsx`

## Update Process

### 1. Update Frontend API Configuration
Edit the file `robotic-book/src/components/ChatbotUI.jsx`:

1. Locate line 29 with the fetch call:
   ```javascript
   const response = await fetch('http://127.0.0.1:8000/query', {
   ```

2. Replace with the Render backend URL:
   ```javascript
   const response = await fetch('https://physical-ai-humanoid-robotics-book-v4wt.onrender.com/query', {
   ```

### 2. Verify Backend CORS Configuration
The backend in `backend/src/main.py` already has proper CORS configuration:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # This allows requests from any frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```
No changes needed to backend configuration.

### 3. Test the Connection
1. Make sure the Render backend is accessible at the target URL
2. Test the chatbot functionality to ensure API calls are successful
3. Verify that responses are handled correctly by the frontend
4. Confirm no CORS errors in browser console

## Files to Modify
- `robotic-book/src/components/ChatbotUI.jsx` - Update API URL

## Files to Verify (No Changes Required)
- `backend/src/main.py` - Already has correct CORS configuration

## Testing Checklist
- [ ] Frontend successfully sends queries to Render backend
- [ ] Backend responses are properly handled by frontend
- [ ] No CORS errors in browser console
- [ ] Chat functionality works end-to-end
- [ ] Error handling still works for network issues
- [ ] Session management continues to function
- [ ] Source documents are properly displayed

## Environment-Specific Considerations
- **Development**: May want to keep localhost URL for local development
- **Production**: Use Render URL for deployed frontend
- **Testing**: Can test with either URL depending on backend availability

## Rollback Plan
If issues occur:
1. Revert the URL change in `robotic-book/src/components/ChatbotUI.jsx`
2. Change back to `http://127.0.0.1:8000/query`
3. Redeploy frontend if necessary

## Next Steps
1. Deploy the updated frontend with the new API URL
2. Monitor API calls to ensure they're going to the correct backend
3. Verify user experience remains unchanged
4. Consider implementing environment-specific configuration in the future