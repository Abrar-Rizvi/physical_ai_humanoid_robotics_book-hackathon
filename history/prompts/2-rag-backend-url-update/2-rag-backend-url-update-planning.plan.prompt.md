---
id: 2
title: rag-backend-url-update-planning
stage: plan
date: '2025-12-17'
surface: agent
model: Claude Sonnet 4.5
feature: rag-backend-url-update
branch: 2-rag-backend-url-update
user: Claude Code User
command: /sp.plan
labels:
  - backend
  - url
  - cors
  - deployment
  - rag
  - planning
links:
  spec: specs/2-rag-backend-url-update/spec.md
  plan: specs/2-rag-backend-url-update/plan.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/2-rag-backend-url-update/plan.md
  - specs/2-rag-backend-url-update/research.md
  - specs/2-rag-backend-url-update/data-model.md
  - specs/2-rag-backend-url-update/contracts/api-contracts.yaml
  - specs/2-rag-backend-url-update/quickstart.md
tests: []
---

# Prompt

```
Update the existing chatbot system to use the deployed RAG backend on Render instead of a local backend, ensuring secure and functional API communication and CORS compatibility without changing existing logic.

Context

Backend (RAG agent) was previously running locally.

Backend is now deployed on Render.

Frontend chatbot already exists and makes API calls.

Backend entry point is main.py.

Goal is to update configuration only, not rewrite logic.

Scope

Update frontend API base URL

Enable / update CORS in backend

Maintain existing request/response contracts

Ensure production readiness

Phase 1: Identify Existing API Integration
Goals

Locate the exact place where the chatbot frontend communicates with the backend.

Tasks

Find the file where the chatbot sends messages to the backend.

Identify any localhost or hardcoded local URLs.

Confirm request method, endpoint path, and payload structure.

Phase 2: Update Frontend API Endpoint
Goals

Point the chatbot to the deployed Render backend.

Tasks

Replace local API base URL with the Render deployment URL.

Preserve existing endpoint paths.

Avoid changing request logic, headers, or payload.

Ensure the frontend still handles responses the same way.

Phase 3: Configure CORS in Backend (main.py)
Goals

Allow frontend requests to reach the deployed backend successfully.

Tasks

Add or update CORS middleware in main.py.

Allow frontend origin(s) or use wildcard during initial testing.

Allow required HTTP methods (GET, POST, OPTIONS).

Allow required headers (Content-Type, Authorization).

Ensure no RAG, embedding, or routing logic is modified.

Phase 4: Environment & Safety Checks
Goals

Make the setup production-safe and maintainable.

Tasks

Ensure no local URLs remain in production code.

Confirm Render environment variables (if any) remain intact.

Avoid exposing secrets or keys in frontend code.
```

# Response

Created a comprehensive implementation plan for updating the RAG chatbot to use the deployed Render backend instead of the local backend. The plan includes:

- Detailed technical context with analysis of both frontend and backend components
- Research findings showing the exact locations of API calls and CORS configuration
- Data models for API configuration, requests, responses, and chat messages
- API contracts documenting the /query endpoint and expected request/response formats
- Quickstart guide with step-by-step instructions for the update process
- Comprehensive testing checklist and rollback plan

Key findings:
- Frontend file: robotic-book/src/components/ChatbotUI.jsx (line 29 with localhost URL)
- Backend file: backend/src/main.py (already has proper CORS configuration)
- Target URL: https://physical-ai-humanoid-robotics-book-v4wt.onrender.com/query
- No changes needed to request/response contracts - only URL update required

The plan ensures secure and functional API communication while maintaining all existing logic and achieving production readiness.