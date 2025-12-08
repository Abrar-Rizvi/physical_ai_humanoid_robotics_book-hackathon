# Implementation Plan: RAG Chatbot Integration

**Branch**: `1-rag-chatbot` | **Date**: 2025-12-08 | **Spec**: specs/1-rag-chatbot/spec.md
**Input**: Feature specification from `specs/1-rag-chatbot/spec.md`

## Summary

This plan outlines the implementation strategy for integrating a Retrieval-Augmented Generation (RAG) chatbot into the Docusaurus book. The chatbot will answer user questions based on book content, utilizing a FastAPI backend, OpenAI Agents/ChatKit SDKs, Neon Serverless Postgres, and Qdrant Cloud. It will be seamlessly embedded in the Docusaurus UI.

## Technical Context

**Language/Version**: Python 3.x (for FastAPI, OpenAI Agents/ChatKit SDKs backend), JavaScript/TypeScript (for Docusaurus frontend).
**Primary Dependencies**: OpenAI Agents/ChatKit SDKs, FastAPI, Neon Serverless Postgres (client library), Qdrant (client library).
**Storage**: Neon Serverless Postgres for logging/metadata, Qdrant Cloud for vector embeddings.
**Testing**: `pytest` (for backend), `Jest`/`React Testing Library` (for frontend components).
**Target Platform**: Frontend (Web: Vercel/Netlify), Backend (Serverless Python environment: Render/Fly.io).
**Project Type**: Hybrid (documentation site with embedded interactive chatbot).
**Performance Goals**: Chatbot response time under 3 seconds (SC-002 from spec).
**Constraints**: Low-cost hosting, no custom LLM training, no complex auth, responses strictly grounded in book content.
**Scale/Scope**: RAG chatbot for the Docusaurus book, answering questions from book content only.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

All relevant Constitution principles are adhered to. The RAG Chatbot integration aligns with:
- Section 6 (Scope): Explicitly includes "Integrated RAG Chatbot: Interactive Q&A based on book content."
- Section 9 (Ethics & Safety): Requirements for no hallucination and safe logging are covered by the spec.
- Section 14 (RAG Chatbot Integration): The plan fully aligns with the purpose, approved technologies, architectural rules, safety/ethics, and integration rules defined in this section.

## Project Structure

### Documentation (this feature)

```text
specs/1-rag-chatbot/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
└── contracts/
    └── rag_api.yaml     # OpenAPI specification for the RAG API
```

### Source Code (repository root)

```text
.
├── book-backend/          # FastAPI application for RAG services
│   ├── app/                 # Main application code
│   ├── tests/               # Backend tests
│   └── Dockerfile           # For deployment
├── robotic-book/          # Existing Docusaurus project (frontend)
│   └── src/
│       └── components/        # Frontend chatbot UI components
└── scripts/               # Utility scripts (e.g., content ingestion, embedding generation)
```
**Structure Decision**: The project will maintain a monorepo structure. The Docusaurus frontend resides in `robotic-book/`. A new `book-backend/` directory will be created at the project root for the FastAPI RAG services. Utility scripts for content processing will reside in a `scripts/` directory at the root.

## Complexity Tracking

N/A

## 1. Architecture Sketch

```mermaid
graph TD
    User --> Docusaurus[Docusaurus UI]
    Docusaurus -- API calls --> FastAPI[FastAPI Backend]

    subgraph RAG Pipeline
        FastAPI -- Embed / Query --> Qdrant[Qdrant Cloud (Vector DB)]
        FastAPI -- Store / Retrieve --> Neon[Neon Serverless Postgres (Metadata/Logs)]
        FastAPI -- Chat --> LLM[OpenAI Agents/ChatKit LLM]
    end

    BookContent[Book Content] -- Chunk & Embed --> Script[Ingestion Script]
    Script -- Store Embeddings --> Qdrant
    Script -- Store Metadata --> Neon
```

This architecture outlines the interaction between the Docusaurus frontend, the new FastAPI backend, and the various data and AI services involved in the RAG chatbot.

## 2. Section Structure

- **book-backend/**: Contains the FastAPI application, serving as the core RAG service.
- **robotic-book/src/components/**: Will house the frontend components necessary to embed and interact with the chatbot within the Docusaurus UI.
- **scripts/**: Dedicated for one-off or scheduled scripts, such as content ingestion and embedding generation.

## 3. Research Approach

Research on optimizing Qdrant for book content embeddings (chunking strategies, embedding models) and secure API key management for OpenAI Agents/ChatKit will be critical. Deployment strategies for serverless backend and frontend integration will also be explored.

## 4. Quality Validation

- **Backend Unit Tests**: `pytest` for FastAPI endpoints and RAG logic.
- **Frontend Integration Tests**: `Jest`/`React Testing Library` for chatbot UI components.
- **End-to-End Tests**: Verify the full RAG pipeline from Docusaurus UI query to LLM response.
- **Performance Testing**: Validate chatbot response time under varying load.
- **Groundedness Checks**: Automated or manual checks to ensure LLM responses are strictly from book content.

## 5. ADRs (Architectural Decision Records)

- **RAG Pipeline Design**: Document the specific choices for chunking, embedding models, and retrieval strategy.
- **Backend Deployment Platform**: Decision between Render and Fly.io with rationale.
- **Frontend Embedding Strategy**: How the chatbot UI component integrates with Docusaurus (e.g., React component, iframe, Docusaurus plugin).

## 6. Testing Strategy

- **Unit Tests**: For individual backend functions (embedding, retrieval, LLM interaction) and frontend components.
- **Integration Tests**: Verify communication between frontend and backend, and backend with Qdrant/Neon/OpenAI.
- **End-to-End Tests**: Simulate user interaction to validate the entire chatbot flow.
- **Performance Tests**: Using tools like `locust` or `pytest-benchmark`.
- **Groundedness Tests**: Develop specific test cases to challenge the chatbot's ability to stay within book context.

## 7. Dependencies

- **Backend Development**: Requires Qdrant Cloud setup, Neon Postgres instance, and OpenAI API key.
- **Frontend Development**: Requires a functional FastAPI backend for integration.
- **Content Ingestion**: Requires a robust script to parse Docusaurus markdown and generate embeddings.

## 8. Implementation Phases

- **Phase 0: Setup & Research**
    - Setup `book-backend/` folder and basic FastAPI project structure.
    - Research optimal chunking/embedding strategies for book content.
    - Research deployment options for FastAPI (Render vs. Fly.io).
- **Phase 1: Backend Core Development**
    - Implement `/embed` endpoint and content ingestion script.
    - Implement `/store` endpoint to save embeddings to Qdrant.
    - Implement `/query` endpoint to retrieve relevant content.
    - Implement `/chat` endpoint for LLM interaction and response generation.
- **Phase 2: Frontend Integration**
    - Develop Docusaurus React component for chatbot UI.
    - Integrate chatbot component into Docusaurus theme/pages.
    - Connect frontend UI to backend API endpoints.
- **Phase 3: Testing & Refinement**
    - Implement comprehensive unit, integration, and end-to-end tests.
    - Conduct performance and groundedness testing.
    - Refine RAG pipeline and LLM prompts based on test results.
- **Phase 4: Deployment**
    - Deploy FastAPI backend to chosen platform (Render/Fly.io).
    - Deploy Docusaurus frontend to chosen platform (Vercel/Netlify).
    - Verify end-to-end functionality in production environment.
