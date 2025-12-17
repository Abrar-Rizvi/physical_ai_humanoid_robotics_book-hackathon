# Feature Specification: RAG Backend URL Update

**Feature Branch**: `2-rag-backend-url-update`
**Created**: 2025-12-17
**Status**: Draft
**Input**: User description: "You are working on an EXISTING RAG chatbot project.

Context:
- The backend (RAG agent) is already deployed on Render.
- The backend was previously running locally.
- The frontend chatbot already exists and is making API calls.
- The backend entry file is `main.py`.

Backend Deployment:
- Render backend base URL: < https://physical-ai-humanoid-robotics-book-v4wt.onrender.com/

Task:
Update the existing code to use the deployed Render backend instead of localhost.

Frontend Tasks:
1. Locate the chatbot frontend file where the API call is made.
2. Replace any `localhost` or local API URL with the Render backend URL.
3. Ensure the API endpoint path remains the same.
4. Do NOT change existing request logic, payload structure, or state management.
5. Only update the API base URL and related configuration.

Backend Tasks (main.py):
1. Enable CORS properly for frontend usage.
2. Allow requests from:
   - The frontend production domain (if known)
   - OR allow all origins temporarily using wildcard (*)
3. Ensure the"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Access Chatbot with Deployed Backend (Priority: P1)

As a website visitor, I want to interact with the RAG chatbot so that my queries are processed by the deployed backend instead of a local one.

**Why this priority**: This is critical for the chatbot to function properly in production, ensuring users get responses from the deployed RAG system instead of failing due to localhost connection issues.

**Independent Test**: The chatbot should successfully send queries to the deployed Render backend and receive responses without any connection errors.

**Acceptance Scenarios**:

1. **Given** I am using the chatbot on the website, **When** I send a message, **Then** the request should be sent to the Render backend URL and return a response
2. **Given** The chatbot is making API calls, **When** I inspect network requests, **Then** I should see requests going to the Render backend URL instead of localhost
3. **Given** I am on the website, **When** I interact with the chatbot, **Then** I should receive responses from the deployed RAG system without connection errors

---

### User Story 2 - Cross-Origin Request Handling (Priority: P2)

As a user, I want the frontend to successfully communicate with the deployed backend so that CORS issues don't prevent chat functionality.

**Why this priority**: Without proper CORS configuration, the frontend will be unable to communicate with the deployed backend due to browser security restrictions.

**Independent Test**: Frontend requests to the backend should not be blocked by CORS policies.

**Acceptance Scenarios**:

1. **Given** I am using the chatbot, **When** I send a message, **Then** the request should not be blocked by CORS policies
2. **Given** The frontend makes API requests, **When** I inspect browser console, **Then** I should not see CORS-related errors

---

### Edge Cases

- What happens when the deployed backend is temporarily unavailable?
- How does the system handle network timeouts when connecting to the Render backend?
- What occurs if the CORS configuration is not properly set up?
- How does the system handle different request origins (localhost vs production domain)?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST replace localhost API URLs with the Render backend URL (https://physical-ai-humanoid-robotics-book-v4wt.onrender.com/)
- **FR-002**: System MUST maintain the same API endpoint paths when switching from localhost to Render backend
- **FR-003**: System MUST preserve existing request logic, payload structure, and state management
- **FR-004**: System MUST update only the API base URL and related configuration
- **FR-005**: Backend (main.py) MUST enable CORS to allow requests from frontend domains
- **FR-006**: Backend MUST allow requests from the frontend production domain or all origins (*)
- **FR-007**: Frontend chatbot component MUST successfully communicate with the deployed backend
- **FR-008**: System MUST handle network errors gracefully when the deployed backend is unavailable
- **FR-009**: System MUST maintain existing authentication and security headers during the transition

### Key Entities *(include if feature involves data)*

- **API Configuration**: Contains the base URL for backend API calls, currently set to localhost
- **CORS Settings**: Backend configuration that controls which origins can make requests to the API
- **Chat Message**: Represents a message sent from frontend to backend, containing query and context information

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of chatbot API requests are successfully sent to the Render backend URL instead of localhost
- **SC-002**: Users experience zero CORS-related errors when interacting with the chatbot
- **SC-003**: Chatbot response time remains within acceptable limits (under 5 seconds) when using the deployed backend
- **SC-004**: All existing chatbot functionality continues to work without regression after the URL change
- **SC-005**: Network requests from frontend to backend complete successfully with 200 status codes