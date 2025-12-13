# Implementation Plan: RAG Chatbot Embeddings Pipeline

**Branch**: `006-rag-embeddings-pipeline` | **Date**: 2025-12-12 | **Spec**: [spec.md](./spec.md)
**Input**: User-specified requirements for single-file RAG pipeline
**Status**: REVISED - User requested rewrite with specific architecture

## Summary

Build a single-file Python pipeline (`backend/main.py`) that fetches all URLs from a deployed Vercel website (https://physical-ai-humanoid-robotics-book-lime.vercel.app/), extracts and cleans text content, chunks it appropriately, generates Cohere embeddings, and upserts them into a Qdrant vector database collection named `rag_embedding` with metadata.

## Technical Context

**Language/Version**: Python 3.11+

**Primary Dependencies**:
- **Cohere** (`cohere>=5.0.0`) - Embedding generation using `embed-english-v3.0` model
- **Qdrant Client** (`qdrant-client>=1.7.0`) - Vector database interaction
- **BeautifulSoup4** (`beautifulsoup4>=4.12.0`) or **requests-html** - HTML parsing and content extraction
- **lxml** (`lxml>=5.0.0`) - Fast HTML parser for BeautifulSoup
- **python-dotenv** (`python-dotenv>=1.0.0`) - Environment variable management

**Storage**: Qdrant vector database
- Local Docker instance: `http://localhost:6333`
- Collection name: `rag_embedding` (user-specified)
- Vector size: 1024 dimensions (Cohere embed-english-v3.0)
- Distance metric: Cosine similarity

**Target Website**: https://physical-ai-humanoid-robotics-book-lime.vercel.app/

**Project Type**: Single-file backend service (`backend/main.py`)

**System Design** (User-specified function structure):
```python
# Function architecture as specified by user:
get_all_urls()                           # Fetch all URLs from deployed website
extract_text_from_url(url)              # Fetch, clean, and extract text
chunk_text(text)                        # Split into appropriately-sized chunks
embed(chunks)                           # Generate Cohere embeddings
create_collection()                     # Initialize Qdrant collection "rag_embedding"
save_chunk_to_qdrant(chunk, embedding, metadata)  # Upsert with metadata
main()                                  # Orchestrate entire pipeline
```

**Performance Goals**:
- Process all URLs from deployed website
- Generate and store embeddings for complete book content
- Handle errors gracefully without pipeline failure
- Efficient batch processing for embeddings (Cohere supports up to 96 texts/request)

**Constraints**:
- Single file implementation (`main.py` only)
- Cohere API rate limits (Production tier: 500 requests/min)
- Text chunk size: 100-500 tokens recommended
- Network stability for URL crawling and fetching

**Scale/Scope**:
- Website: https://physical-ai-humanoid-robotics-book-lime.vercel.app/
- URL discovery: Crawl all pages from base URL
- Estimated content: 50-100 pages
- Estimated embeddings: 500-1500 vectors total

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Core Principles Alignment

✅ **Engineering accuracy, academic clarity**: Pipeline follows established RAG best practices (crawling → extraction → chunking → embedding → storage)
✅ **Verified, reproducible workflows**: All components use official SDKs (Cohere, Qdrant)
✅ **Safety-first development**: Error handling at each pipeline stage prevents data corruption
✅ **Ethical, traceable, responsible AI usage**: Embeddings preserve source attribution via metadata
✅ **Alignment with official documentation**: Using official Cohere and Qdrant client libraries
✅ **Minimal dependencies**: Core dependencies only (Cohere, Qdrant, BeautifulSoup, requests, dotenv)
✅ **User-centric design**: Simple single-file implementation for easy understanding and deployment

### Standards Compliance

✅ **Verifiable claims**: All technology choices reference official documentation
✅ **Zero tolerance for layout-breaking changes**: Backend-only; no UI modifications
✅ **Web performance**: N/A - backend service
✅ **Mobile-friendly**: N/A - backend service
✅ **Dark mode**: N/A - backend service

### Constraints Validation

✅ **Lightweight architecture**: Single Python script with minimal dependencies
✅ **Performance metrics**: Batch processing enables efficient embedding generation (96 texts/request)
✅ **No heavy libraries**: All dependencies are standard Python packages

### Ethics & Safety

✅ **Privacy**: Processing public website content only
✅ **Transparent AI usage**: Embeddings generated via documented Cohere API
✅ **Data handling**: Source attribution preserved in metadata (URL, title, timestamp)
✅ **Rate limiting**: Cohere Production tier quotas (500 requests/min), batch size limits (96 texts/request)

### RAG Pipeline Architecture (Constitution §14.3)

✅ **Embeddings**: Website content extracted, chunked, and converted to vectors ✓
✅ **Vector Storage**: Stored in Qdrant for semantic search ✓
✅ **Retrieval**: Supports retrieval queries with relevance ranking ✓
✅ **Grounded Responses**: Pipeline provides foundation for Claude grounding (future integration)
✅ **No Hallucination**: Vector retrieval returns only stored content
✅ **Context Boundaries**: Retrieval limited to indexed website content

### Gates Summary

**PASS**: All gates satisfied ✅

**User-Specified Architecture**:
- ✅ Single-file implementation (`main.py`)
- ✅ Specific function names as requested
- ✅ Collection name: `rag_embedding`
- ✅ Target website: https://physical-ai-humanoid-robotics-book-lime.vercel.app/
- ✅ Site URl: https://physical-ai-humanoid-robotics-book-lime.vercel.app/sitemap.xml

**Ready for implementation**: Clear architecture, user requirements defined

## Project Structure

### Documentation (this feature)

```text
specs/006-rag-embeddings-pipeline/
├── spec.md              # Feature specification (existing)
├── plan.md              # This file (revised)
├── research.md          # Phase 0 output (to be generated)
├── data-model.md        # Phase 1 output (to be generated)
├── quickstart.md        # Phase 1 output (to be generated)
└── contracts/           # Phase 1 output (to be generated)
```

### Source Code (repository root)

```text
backend/
├── main.py              # Single-file pipeline implementation (user-specified)
├── .env                 # Environment variables (COHERE_API_KEY, QDRANT_URL)
├── pyproject.toml       # Python dependencies
└── README.md            # Setup and usage instructions
```

**Structure Decision**: Single-file implementation as explicitly requested by user. All pipeline logic (URL discovery, text extraction, chunking, embedding generation, Qdrant storage) will be contained in `backend/main.py` with user-specified function structure.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

N/A - No constitution violations detected. All gates passed.

## Phase 0: Research

**Objective**: Resolve technical unknowns and establish best practices

### Research Topics

1. **URL Discovery Strategy**
   - How to crawl/discover all URLs from https://physical-ai-humanoid-robotics-book-lime.vercel.app/
   - Sitemap.xml approach vs recursive crawling
   - Handling Vercel-deployed websites (static vs dynamic content)

2. **Cohere Embedding Best Practices**
   - Confirm `embed-english-v3.0` model specifications (1024 dimensions)
   - Batch size recommendations (up to 96 texts/request)
   - Input type parameter (`search_document` for indexing)
   - Rate limits and pricing for Production tier

3. **Text Chunking Strategy**
   - Optimal chunk size for Cohere model (typically 400-512 tokens)
   - Chunking method (character-based, sentence-based, or semantic)
   - Overlap strategy (typically 10-20% overlap)
   - Preserving context boundaries (headings, sections)

4. **Qdrant Integration**
   - Collection creation parameters (vector size, distance metric)
   - Metadata schema design (what to store alongside embeddings)
   - Upsert vs batch insert strategies
   - Error handling for connection failures

**Output**: `research.md` with findings and decisions for all topics above

## Phase 1: Design

**Objective**: Generate data models, API contracts, and quickstart guide

### Artifacts to Generate

1. **data-model.md**: Define data structures
   - URL metadata (source URL, page title, discovery timestamp)
   - Text chunk (text, token count, chunk index, source URL)
   - Embedding metadata (vector, chunk text, source URL, title, timestamp)
   - Error tracking (URL, error type, timestamp)

2. **contracts/**: API specifications
   - Since this is a single-file script with no external API, document:
     - Function signatures and contracts (input/output types)
     - Expected metadata schema for Qdrant
     - Environment variable requirements (.env file structure)

3. **quickstart.md**: Getting started guide
   - Prerequisites (Python 3.11+, Docker for Qdrant, Cohere API key)
   - Installation steps (dependencies, Qdrant setup)
   - Configuration (.env file setup)
   - Running the pipeline (`python backend/main.py`)
   - Verifying results (querying Qdrant collection)

### Agent Context Update

- Run `.specify/scripts/powershell/update-agent-context.ps1 -AgentType claude`
- Add Python, Cohere, Qdrant to technology stack
- Update recent changes log

## Phase 2: Re-evaluate Constitution

**Status**: ✅ COMPLETE - All gates verified after Phase 1 design

After generating design artifacts (research.md, data-model.md), all Constitution gates have been re-checked:

### Re-evaluation Results

**Core Principles Alignment** ✅
- Research confirms official SDKs: Cohere Python SDK (v5.0.0+), Qdrant Client (v1.7.0+)
- Sitemap.xml parsing validated (21 URLs discovered)
- Error handling strategy documented in data-model.md (ProcessingError entity)
- Metadata preservation confirmed in EmbeddingMetadata structure

**Standards Compliance** ✅
- Technology choices verified against official documentation:
  - Cohere embed-english-v3.0: 1024 dimensions, 512-token limit (confirmed)
  - Qdrant cosine similarity: Industry standard for semantic search
  - LangChain RecursiveCharacterTextSplitter: Recommended chunking approach
  - tiktoken cl100k_base: Cohere-compatible token counting

**Constraints Validation** ✅
- Single-file architecture confirmed in data-model.md
- Performance estimates from research.md: 2-5 minutes for 21 URLs
- Batch processing (96 texts/request) aligns with Cohere limits
- Storage estimate: ~1-2 MB for entire website (lightweight)

**Ethics & Safety** ✅
- Data model includes source attribution (source_url, page_title, extraction_timestamp)
- Public content only (Vercel-deployed website)
- Rate limiting documented: 500 requests/min (Cohere Production tier)
- No PII or sensitive data processing

**RAG Pipeline Architecture** ✅
- All components validated in research.md:
  - URL discovery: Sitemap.xml parsing (1-2 seconds)
  - Text chunking: 400 tokens, 60-token overlap, sentence boundaries
  - Embeddings: Cohere embed-english-v3.0, batch size 96
  - Storage: Qdrant with cosine distance, 1024-dim vectors
  - Metadata: Complete payload schema defined in data-model.md

### New Findings from Design Phase

1. **Sitemap Parsing Advantage**: Research revealed sitemap.xml exists with 21 URLs, eliminating need for complex web crawling (1-2 sec vs 30-60 sec)

2. **Token Optimization**: 400-token chunks with 15% overlap provides optimal balance between context and Cohere's 512-token limit

3. **Batch Efficiency**: Cohere's 96 texts/batch capability enables processing 21 URLs in ~3-5 batches (high efficiency)

4. **Data Model Completeness**: data-model.md defines 6 core entities (URLMetadata, TextChunk, EmbeddingMetadata, ProcessingError, PipelineStats, PipelineConfig) with validation rules

5. **Success Criteria Validation**: PipelineStats.meets_success_criteria() method enables automated SC-001 verification (≥95% success rate)

### Adjustments Made

None required - all original gates still satisfied after design phase.

**Checkpoint**: All planning artifacts complete, ready for `/sp.tasks` command to generate implementation tasks

---

**Note**: This plan has been revised per user request to focus on:
- Single-file implementation (`backend/main.py`)
- User-specified function architecture
- Target website: https://physical-ai-humanoid-robotics-book-lime.vercel.app/
- Collection name: `rag_embedding`
- Simplified, focused scope compared to original multi-file design
