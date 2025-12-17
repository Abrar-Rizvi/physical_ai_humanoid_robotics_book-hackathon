# Implementation Plan: RAG Backend URL Update

**Feature**: RAG Backend URL Update
**Branch**: 2-rag-backend-url-update
**Created**: 2025-12-17
**Status**: Draft

## Technical Context

This implementation plan outlines the changes needed to update the existing RAG chatbot system to use the deployed Render backend instead of a local backend. The key components identified are:

### Frontend Component
- **File**: `robotic-book/src/components/ChatbotUI.jsx`
- **Current API URL**: `http://127.0.0.1:8000/query` (line 29)
- **API Method**: POST
- **Request Payload**: { query, context, session_id }
- **Response Format**: { answer, sources, status }

### Backend API Server
- **File**: `backend/src/main.py`
- **Current CORS Configuration**: Already allows all origins (`allow_origins=["*"]`)
- **API Endpoint**: `/query` (POST method)
- **API Server**: FastAPI with uvicorn

### Target Backend
- **Render URL**: `https://physical-ai-humanoid-robotics-book-v4wt.onrender.com/`
- **API Endpoint**: `/query` (same path, different base URL)

### Unknowns (NEEDS CLARIFICATION)
- None remaining - all resolved through code analysis

## Constitution Check

### Alignment with Project Constitution
- ✅ **Engineering accuracy, academic clarity**: Changes maintain existing functionality while updating configuration
- ✅ **Verified, reproducible robotics & AI workflows**: Backend change preserves RAG pipeline integrity
- ✅ **Minimal dependencies**: Only configuration change, no new dependencies
- ✅ **User-centric design**: Improves user experience by enabling production backend access
- ✅ **Zero tolerance for layout-breaking changes**: Only API configuration changes, no UI modifications

### Potential Violations
- None identified - all changes align with constitution requirements

### Risk Assessment
- **Low Risk**: Configuration-only changes, preserving existing logic
- **Low Risk**: CORS already configured properly in backend
- **Low Risk**: Frontend request/response contracts remain unchanged

## Gates

### Gate 1: Technical Feasibility ✅
- Frontend API call can be updated to use Render URL
- Backend already has proper CORS configuration
- Same API endpoint structure maintained

### Gate 2: Constitution Compliance ✅
- All implementation approaches align with constitution requirements
- Changes are minimal and focused on configuration only

### Gate 3: Production Requirements ✅
- Backend already configured for cross-origin requests
- API contracts remain unchanged
- Error handling preserved

### Gate 4: Integration Compatibility ✅
- Frontend request format matches backend expectations
- Response handling remains unchanged
- Session management preserved

## Phase 0: Research

### Decision: Frontend API URL Update
- **Primary**: Replace `http://127.0.0.1:8000/query` with `https://physical-ai-humanoid-robotics-book-v4wt.onrender.com/query`
- **Rationale**: Matches requirement to use deployed Render backend instead of localhost

### Decision: CORS Configuration
- **Primary**: No changes needed - backend already allows all origins
- **Rationale**: Current CORS configuration `allow_origins=["*"]` already supports cross-origin requests

### Decision: Error Handling
- **Primary**: Preserve existing error handling patterns
- **Rationale**: Maintain consistency with existing user experience for network errors

## Phase 1: Data Model

### API Request Model
- **Endpoint**: `/query` (POST)
- **Request Body**:
  - `query`: string (user query text)
  - `context`: string (optional context, currently empty)
  - `session_id`: string (session identifier)
- **Response Body**:
  - `answer`: string (AI response)
  - `sources`: array (source documents)
  - `status`: string (optional status field)

### API Configuration Entity
- **Properties**:
  - `apiBaseUrl`: string (base URL for API calls)
  - `apiEndpoints`: object (endpoint paths relative to base URL)
  - `timeout`: number (request timeout in milliseconds)

## Phase 2: Implementation Plan

### Phase 2A: Frontend API URL Update
**Tasks**:
1. Update API URL in `robotic-book/src/components/ChatbotUI.jsx`
2. Replace `http://127.0.0.1:8000/query` with `https://physical-ai-humanoid-robotics-book-v4wt.onrender.com/query`
3. Preserve all request payload structure
4. Maintain existing error handling
5. Test API call functionality

### Phase 2B: Backend CORS Verification
**Tasks**:
1. Verify current CORS configuration in `backend/src/main.py`
2. Confirm `allow_origins=["*"]` setting is appropriate
3. Ensure all required methods and headers are allowed
4. No changes needed (configuration already correct)

### Phase 2C: Environment Configuration (Optional)
**Tasks**:
1. Consider adding environment variable for API URL (future enhancement)
2. For now, hardcode Render URL to meet immediate requirements
3. Preserve existing configuration patterns

### Phase 2D: Testing and Validation
**Tasks**:
1. Test frontend API calls to Render backend
2. Verify response handling remains functional
3. Confirm no CORS errors occur
4. Validate error handling for network issues
5. Ensure all existing functionality preserved

## Phase 3: Testing Strategy

### Unit Tests
- API URL configuration tests
- Request/response handling tests
- Error condition tests

### Integration Tests
- End-to-end chat functionality
- Cross-origin request handling
- Backend response validation

### User Acceptance Tests
- All acceptance scenarios from spec
- Production backend communication
- CORS policy compliance
- Error handling verification

## Phase 4: Deployment

### Frontend Deployment
- Update deployed frontend with new API configuration
- Verify production environment compatibility
- Test with actual Render backend

### Backend Verification
- Confirm Render backend is accessible
- Validate API endpoint availability
- Test response format compatibility

## Success Criteria Verification

- [ ] API requests sent to Render backend URL instead of localhost (FR-001)
- [ ] Same API endpoint paths maintained (FR-002)
- [ ] Request logic and payload structure preserved (FR-003)
- [ ] Only API base URL updated (FR-004)
- [ ] CORS configuration allows frontend requests (FR-005, FR-006)
- [ ] Frontend successfully communicates with deployed backend (FR-007)
- [ ] Network errors handled gracefully (FR-008)
- [ ] Authentication and security headers maintained (FR-009)
- [ ] 100% of requests go to Render backend (SC-001)
- [ ] Zero CORS-related errors (SC-002)
- [ ] Response time under 5 seconds (SC-003)
- [ ] All functionality works without regression (SC-004)
- [ ] Successful API responses with 200 status (SC-005)

## Risk Mitigation

### Technical Risks
- **Backend Unavailability**: Implement proper error handling for Render backend downtime
- **Network Timeouts**: Maintain existing timeout handling mechanisms
- **CORS Issues**: Backend already configured for cross-origin requests

### Integration Risks
- **API Compatibility**: Same endpoint structure maintained
- **Response Format**: Existing response handling preserved
- **Session Management**: Same session ID generation approach

### Deployment Risks
- **Environment Differences**: Test thoroughly in production-like environment
- **URL Configuration**: Verify HTTPS protocol usage for Render deployment