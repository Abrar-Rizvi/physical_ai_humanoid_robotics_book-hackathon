---
id: 1
title: rag-backend-url-update-specification
stage: spec
date: '2025-12-17'
surface: agent
model: Claude Sonnet 4.5
feature: rag-backend-url-update
branch: 2-rag-backend-url-update
user: Claude Code User
command: /sp.specify
labels:
  - backend
  - url
  - cors
  - deployment
  - rag
  - specification
links:
  spec: specs/2-rag-backend-url-update/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/2-rag-backend-url-update/spec.md
  - specs/2-rag-backend-url-update/checklists/requirements.md
tests: []
---

# Prompt

```
You are working on an EXISTING RAG chatbot project.

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
3. Ensure the
```

# Response

Created a comprehensive specification for updating the RAG chatbot to use the deployed Render backend instead of localhost. The specification includes:

- Detailed user scenarios with acceptance criteria
- Functional requirements covering URL updates, CORS configuration, and error handling
- Success criteria with measurable outcomes
- Edge cases and error handling considerations
- Quality validation checklist

The spec focuses on:
- Replacing localhost API URLs with the Render backend URL
- Maintaining existing API endpoint paths and request logic
- Enabling proper CORS configuration on the backend
- Preserving existing functionality while updating the backend connection
- Ensuring cross-origin requests work properly between frontend and backend

The specification is ready for the planning phase.