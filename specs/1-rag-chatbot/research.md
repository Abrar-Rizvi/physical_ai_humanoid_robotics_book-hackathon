# Research Notes: RAG Chatbot Integration

## Research Topics:

### 1. Integrating OpenAI Agents/ChatKit with FastAPI

-   **Goal:** Understand best practices and potential pitfalls when connecting OpenAI's chatbot development tools with a FastAPI backend.
-   **Key Questions:**
    -   How to handle API key management securely?
    -   What are the optimal communication patterns between the frontend (Docusaurus-embedded chatbot) and the FastAPI backend?
    -   Are there existing libraries or design patterns for this integration?

### 2. Optimizing Qdrant for Book Content Embeddings

-   **Goal:** Determine the most effective way to chunk, embed, and store the Docusaurus book content in Qdrant for efficient and accurate retrieval.
-   **Key Questions:**
    -   What chunking strategies (e.g., fixed size, semantic, recursive) are best suited for book content?
    -   Which embedding models provide the best performance for this domain?
    -   How to configure Qdrant collections for optimal search performance (e.g., indexing, distance metrics)?

### 3. Deployment Strategies for Backend and Frontend

-   **Goal:** Outline the deployment process for the FastAPI backend (with Neon Postgres and Qdrant) and the Docusaurus frontend.
-   **Key Questions:**
    -   How to deploy FastAPI applications to Render or Fly.io, considering serverless Postgres and external Qdrant?
    -   What are the CI/CD considerations for both frontend (Vercel/Netlify) and backend?
    -   How to manage environment variables and secrets in production?
