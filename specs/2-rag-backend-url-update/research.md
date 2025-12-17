# Research Document: RAG Backend URL Update

**Feature**: RAG Backend URL Update
**Date**: 2025-12-17

## Decision: Frontend API URL Update
- **Location**: `robotic-book/src/components/ChatbotUI.jsx`, line 29
- **Current URL**: `http://127.0.0.1:8000/query`
- **Target URL**: `https://physical-ai-humanoid-robotics-book-v4wt.onrender.com/query`
- **Rationale**: Matches requirement to use deployed Render backend instead of localhost

## Decision: CORS Configuration
- **Location**: `backend/src/main.py`, lines 36-43
- **Current Configuration**: `allow_origins=["*"]` (already allows all origins)
- **Status**: No changes needed - configuration already supports cross-origin requests
- **Rationale**: Backend already properly configured for frontend access

## Decision: Request/Response Contract Preservation
- **Request Format**: Maintained exactly as-is (query, context, session_id)
- **Response Handling**: Preserved existing logic for processing backend responses
- **Error Handling**: Kept existing error handling patterns for network issues
- **Rationale**: Requirement to maintain existing request/response contracts

## Decision: Implementation Approach
- **Primary**: Direct URL replacement in frontend component
- **Alternative**: Environment variable configuration (for future enhancement)
- **Rationale**: Direct approach meets immediate requirements with minimal changes