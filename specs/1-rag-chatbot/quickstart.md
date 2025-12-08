# Quickstart Guide: RAG Chatbot Integration

This guide provides quick integration scenarios and validation steps for the RAG Chatbot.

## 1. Initial Setup and Local Verification

### 1.1. Backend Setup (FastAPI)

1.  Navigate to the `book-backend/` directory.
2.  Install dependencies: `pip install -r requirements.txt`
3.  Start the FastAPI server: `uvicorn main:app --reload`
4.  Verify API endpoints:
    *   Access `http://localhost:8000/docs` to see the OpenAPI UI.
    *   Test a `/embed` request with sample text.
    *   Test a `/store` request with a generated embedding.
    *   Test a `/query` request with a sample query.
    *   Test a `/chat` request after content has been stored and queried.

### 1.2. Frontend Integration (Docusaurus)

1.  Navigate to the `robotic-book/` directory.
2.  Install dependencies: `npm install`
3.  Start the Docusaurus development server: `npm run start`
4.  Verify chatbot UI component integration:
    *   Open `http://localhost:3000` in your browser.
    *   Confirm the chatbot icon/widget is visible on a book page.
    *   Interact with the chatbot through the UI.

## 2. End-to-End Test Scenario

### Scenario: Ask a question from a book chapter

1.  **Prerequisites:** Backend is running, Docusaurus is serving the book.
2.  **Steps:**
    *   Open a chapter in the Docusaurus book (e.g., "Chapter 1: The Fundamentals of Physical AI").
    *   Activate the chatbot UI.
    *   Type a question directly related to the chapter content, e.g., "What is the Sense-Plan-Act cycle?".
    *   Submit the query.
3.  **Expected Outcome:** The chatbot responds with information derived from that chapter, accurately describing the Sense-Plan-Act cycle.

## 3. Deployment Verification

### 3.1. Frontend Deployment (Vercel/Netlify)

1.  Deploy the Docusaurus frontend to the chosen platform.
2.  Access the live site.
3.  Verify the chatbot UI is present and functions correctly, making calls to the deployed backend.

### 3.2. Backend Deployment (Render/Fly.io)

1.  Deploy the FastAPI backend to the chosen platform.
2.  Verify the backend API endpoints are accessible and functional (e.g., using `curl` or Postman).
3.  Confirm integration with Neon Postgres and Qdrant Cloud.
