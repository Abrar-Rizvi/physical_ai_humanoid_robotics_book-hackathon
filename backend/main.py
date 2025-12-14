#!/usr/bin/env python3
"""
RAG Embeddings Pipeline - Single-file implementation

This script extracts content from a deployed Docusaurus website, generates
embeddings using Cohere, and stores them in Qdrant vector database.

Architecture:
- get_all_urls(): Fetch all URLs from sitemap.xml
- extract_text_from_url(url): Fetch, clean, and extract text
- chunk_text(text): Split into appropriately-sized chunks
- embed(chunks): Generate Cohere embeddings
- create_collection(): Initialize Qdrant collection
- save_chunk_to_qdrant(chunk, embedding, metadata): Upsert with metadata
- main(): Orchestrate entire pipeline
"""

import argparse
import hashlib
import logging
import os
import sys
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict, Any
from xml.etree import ElementTree as ET

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import cohere
from langchain_text_splitters import RecursiveCharacterTextSplitter
import tiktoken


# ============================================================================
# Exit Codes (per cli-interface.md)
# ============================================================================
EXIT_SUCCESS = 0           # All operations completed successfully
EXIT_PARTIAL_SUCCESS = 1   # Some URLs processed, some failed
EXIT_CONFIG_ERROR = 2      # Configuration error (missing API keys, invalid args)
EXIT_CONNECTION_ERROR = 3  # Cannot connect to Qdrant or Cohere
EXIT_PROCESSING_ERROR = 4  # Critical error during processing
EXIT_VALIDATION_ERROR = 5  # Validation failed (e.g., <95% success rate)


# ============================================================================
# Data Structures
# ============================================================================

@dataclass
class PipelineConfig:
    """Runtime configuration loaded from environment variables"""
    # Required
    cohere_api_key: str
    qdrant_url: str = "http://localhost:6333"
    qdrant_api_key: Optional[str] = None

    # Optional with defaults
    collection_name: str = "rag_embedding"
    cohere_model: str = "embed-english-v3.0"
    chunk_size: int = 400
    chunk_overlap: int = 60
    batch_size: int = 96
    sitemap_url: str = "https://physical-ai-humanoid-robotics-book-lime.vercel.app/sitemap.xml"

    @classmethod
    def from_env(cls) -> "PipelineConfig":
        """Load configuration from environment variables"""
        api_key = os.getenv("COHERE_API_KEY")
        if not api_key:
            raise ValueError("COHERE_API_KEY environment variable is required")

        return cls(
            cohere_api_key=api_key,
            qdrant_url=os.getenv("QDRANT_URL", "http://localhost:6333"),
            qdrant_api_key=os.getenv("QDRANT_API_KEY"),  # Optional, for Qdrant Cloud
            collection_name=os.getenv("QDRANT_COLLECTION_NAME", "rag_embedding"),
            cohere_model=os.getenv("COHERE_MODEL", "embed-english-v3.0"),
            chunk_size=int(os.getenv("CHUNK_SIZE_TOKENS", "400")),
            chunk_overlap=int(os.getenv("CHUNK_OVERLAP_TOKENS", "60")),
            batch_size=int(os.getenv("BATCH_SIZE", "96")),
            sitemap_url=os.getenv("SITEMAP_URL", "https://physical-ai-humanoid-robotics-book-lime.vercel.app/sitemap.xml")
        )


@dataclass
class URLMetadata:
    """Metadata for a discovered URL"""
    source_url: str
    page_title: Optional[str] = None
    discovery_timestamp: datetime = field(default_factory=datetime.utcnow)
    extraction_status: str = "pending"  # pending | success | failed
    error_message: Optional[str] = None


@dataclass
class ContentDocument:
    """Extracted content from a URL"""
    source_url: str
    page_title: str
    content_text: str
    extraction_timestamp: datetime
    content_hash: str
    word_count: int
    chapter: Optional[str] = None
    section: Optional[str] = None
    has_code: bool = False
    has_images: bool = False


@dataclass
class TextChunk:
    """A single chunk of text ready for embedding"""
    text: str
    token_count: int
    chunk_index: int
    source_url: str
    page_title: str
    section_headers: List[str] = field(default_factory=list)
    extraction_timestamp: datetime = field(default_factory=datetime.utcnow)


@dataclass
class ProcessingError:
    """Tracks errors during pipeline execution"""
    url: str
    error_type: str  # fetch | parse | chunk | embed | store
    error_message: str
    timestamp: datetime = field(default_factory=datetime.utcnow)
    stack_trace: Optional[str] = None


@dataclass
class PipelineStats:
    """Aggregated statistics for pipeline execution"""
    total_urls: int = 0
    successful_urls: int = 0
    failed_urls: int = 0
    total_chunks: int = 0
    total_embeddings: int = 0
    errors: List[ProcessingError] = field(default_factory=list)
    start_time: datetime = field(default_factory=datetime.utcnow)
    end_time: Optional[datetime] = None

    @property
    def success_rate(self) -> float:
        """Calculate success rate as percentage"""
        if self.total_urls == 0:
            return 0.0
        return (self.successful_urls / self.total_urls) * 100

    @property
    def duration_seconds(self) -> float:
        """Calculate total execution time in seconds"""
        if self.end_time is None:
            return 0.0
        return (self.end_time - self.start_time).total_seconds()

    def meets_success_criteria(self) -> bool:
        """Check if pipeline meets SC-001 (≥95% success rate)"""
        return self.success_rate >= 95.0


# ============================================================================
# Logging Setup
# ============================================================================

def setup_logging(verbose: bool = False, log_file: str = "pipeline.log") -> logging.Logger:
    """
    Setup logging infrastructure with file and console handlers

    Args:
        verbose: If True, use DEBUG level; otherwise INFO
        log_file: Path to log file

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger("rag_pipeline")
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)

    # Remove existing handlers
    logger.handlers.clear()

    # File handler (DEBUG level)
    file_handler = logging.FileHandler(log_file, mode='a', encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_format)

    # Console handler (INFO or DEBUG based on verbose flag)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG if verbose else logging.INFO)
    console_format = logging.Formatter('%(levelname)s: %(message)s')
    console_handler.setFormatter(console_format)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


# ============================================================================
# Qdrant Collection Management
# ============================================================================

def create_collection(config: PipelineConfig, logger: logging.Logger) -> None:
    """
    Initialize Qdrant collection with specified name and configuration

    Args:
        config: Pipeline configuration
        logger: Logger instance

    Raises:
        Exception: If collection creation fails
    """
    try:
        client = QdrantClient(url=config.qdrant_url, api_key=config.qdrant_api_key)

        # Check if collection exists
        collections = client.get_collections().collections
        collection_names = [col.name for col in collections]

        if config.collection_name in collection_names:
            logger.info(f"Collection '{config.collection_name}' already exists")
            return

        # Create collection
        client.create_collection(
            collection_name=config.collection_name,
            vectors_config=VectorParams(
                size=1024,  # Cohere embed-english-v3.0 dimension
                distance=Distance.COSINE
            )
        )

        logger.info(f"Created collection '{config.collection_name}' (1024-dim, cosine distance)")

    except Exception as e:
        logger.error(f"Failed to create collection: {e}")
        raise


def verify_qdrant_connection(config: PipelineConfig, logger: logging.Logger) -> bool:
    """
    Verify Qdrant connection is accessible

    Args:
        config: Pipeline configuration
        logger: Logger instance

    Returns:
        True if connection successful, False otherwise
    """
    try:
        client = QdrantClient(url=config.qdrant_url, api_key=config.qdrant_api_key)
        collections = client.get_collections()
        logger.debug(f"Qdrant connection successful: {len(collections.collections)} collections found")
        return True
    except Exception as e:
        logger.error(f"Qdrant connection failed: {e}")
        return False


# ============================================================================
# Utility Functions
# ============================================================================

def compute_content_hash(text: str) -> str:
    """
    Compute SHA-256 hash of content for change detection

    Args:
        text: Content text

    Returns:
        Hex digest of SHA-256 hash
    """
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def count_tokens(text: str, encoding_name: str = "cl100k_base") -> int:
    """
    Count tokens using tiktoken

    Args:
        text: Text to tokenize
        encoding_name: Encoding name (default: cl100k_base for Cohere)

    Returns:
        Number of tokens
    """
    encoding = tiktoken.get_encoding(encoding_name)
    return len(encoding.encode(text))


# ============================================================================
# URL Discovery
# ============================================================================

def get_all_urls(sitemap_url: str, logger: logging.Logger) -> List[str]:
    """
    Fetch all URLs from deployed website sitemap.xml

    Args:
        sitemap_url: URL to sitemap.xml
        logger: Logger instance

    Returns:
        List of URLs from sitemap

    Raises:
        Exception: If sitemap fetch or parsing fails
    """
    logger.info(f"Fetching sitemap from: {sitemap_url}")

    try:
        response = requests.get(sitemap_url, timeout=10)
        response.raise_for_status()

        root = ET.fromstring(response.content)

        # Parse sitemap namespace
        namespace = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        urls = []

        for url_elem in root.findall('s:url', namespace):
            loc = url_elem.find('s:loc', namespace)
            if loc is not None:
                urls.append(loc.text)

        logger.info(f"Discovered {len(urls)} URLs from sitemap")
        return urls

    except Exception as e:
        logger.error(f"Failed to fetch sitemap: {e}")
        raise


# ============================================================================
# Content Extraction (User Story 1)
# ============================================================================

def validate_url(url: str) -> bool:
    """
    Validate URL format (HTTP/HTTPS only, no malformed URLs)

    Args:
        url: URL to validate

    Returns:
        True if valid, False otherwise
    """
    from urllib.parse import urlparse

    try:
        parsed = urlparse(url)
        return parsed.scheme in ('http', 'https') and bool(parsed.netloc)
    except Exception:
        return False


def fetch_html(url: str, logger: logging.Logger, timeout: int = 30, max_retries: int = 3) -> Optional[str]:
    """
    Fetch HTML content from URL with retry logic

    Args:
        url: URL to fetch
        logger: Logger instance
        timeout: Request timeout in seconds
        max_retries: Maximum retry attempts

    Returns:
        HTML content if successful, None otherwise
    """
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry

    session = requests.Session()

    # Configure retry strategy
    retry_strategy = Retry(
        total=max_retries,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
        backoff_factor=1  # 1s, 2s, 4s...
    )

    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    try:
        response = session.get(url, timeout=timeout)
        response.raise_for_status()
        logger.debug(f"Successfully fetched HTML from {url} ({len(response.content)} bytes)")
        return response.text

    except requests.exceptions.Timeout:
        logger.warning(f"Timeout fetching {url} after {timeout}s")
        return None
    except requests.exceptions.HTTPError as e:
        logger.warning(f"HTTP error fetching {url}: {e.response.status_code}")
        return None
    except requests.exceptions.ConnectionError as e:
        logger.warning(f"Connection error fetching {url}: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error fetching {url}: {e}")
        return None


def parse_html_with_beautifulsoup(html: str, logger: logging.Logger) -> Optional[BeautifulSoup]:
    """
    Parse HTML with BeautifulSoup using lxml parser with fallbacks

    Args:
        html: HTML content
        logger: Logger instance

    Returns:
        BeautifulSoup object if successful, None otherwise
    """
    parsers = ['lxml', 'html.parser', 'html5lib']

    for parser in parsers:
        try:
            soup = BeautifulSoup(html, parser)
            logger.debug(f"Successfully parsed HTML with {parser}")
            return soup
        except Exception as e:
            logger.debug(f"Parser {parser} failed: {e}")
            continue

    logger.error("All HTML parsers failed")
    return None


def extract_docusaurus_content(soup: BeautifulSoup, url: str, logger: logging.Logger) -> Optional[ContentDocument]:
    """
    Extract content from Docusaurus page

    Args:
        soup: BeautifulSoup object
        url: Source URL
        logger: Logger instance

    Returns:
        ContentDocument if successful, None otherwise
    """
    # Docusaurus content selectors (priority order)
    selectors = [
        'article.theme-doc-markdown',
        'article[class*="docPage"]',
        'div.theme-doc-markdown',
        'main article',
        'main'
    ]

    content_elem = None
    for selector in selectors:
        content_elem = soup.select_one(selector)
        if content_elem:
            logger.debug(f"Found content using selector: {selector}")
            break

    if not content_elem:
        logger.warning(f"No content found for {url} - tried {len(selectors)} selectors")
        return None

    # Remove navigation elements
    for tag in content_elem.select('nav, aside, footer, header'):
        tag.decompose()

    # Remove Docusaurus UI elements
    for class_name in ['pagination-nav', 'tocCollapsible', 'theme-doc-footer', 'theme-doc-breadcrumbs']:
        for elem in content_elem.select(f'[class*="{class_name}"]'):
            elem.decompose()

    # Extract page title
    title_elem = soup.select_one('title')
    h1_elem = soup.select_one('h1')
    page_title = (title_elem.get_text(strip=True) if title_elem else
                  h1_elem.get_text(strip=True) if h1_elem else
                  url.split('/')[-1])

    # Extract chapter/section from URL path
    path_parts = url.rstrip('/').split('/')
    chapter = path_parts[-1] if len(path_parts) > 0 else None

    # Get text content
    text = content_elem.get_text(separator='\n', strip=True)

    # Preprocess text
    text = preprocess_text(logger)

    # Check for code blocks and images
    has_code = bool(content_elem.select('pre, code'))
    has_images = bool(content_elem.select('img'))

    # Compute content hash and word count
    content_hash = compute_content_hash(text)
    word_count = len(text.split())

    if word_count < 50:
        logger.warning(f"Content too short for {url}: {word_count} words")
        return None

    return ContentDocument(
        source_url=url,
        page_title=page_title,
        content_text=text,
        extraction_timestamp=datetime.utcnow(),
        content_hash=content_hash,
        word_count=word_count,
        chapter=chapter,
        section=None,  # Could be enhanced with heading extraction
        has_code=has_code,
        has_images=has_images
    )


def preprocess_text(text: str, logger: logging.Logger) -> str:
    """
    Clean and preprocess text content

    Args:
        text: Raw text content
        logger: Logger instance

    Returns:
        Cleaned text
    """
    import re

    # Normalize whitespace (preserve line breaks)
    lines = text.split('\n')
    cleaned_lines = []

    for line in lines:
        # Preserve code blocks (lines with significant indentation)
        if line.startswith('    ') or line.startswith('\t'):
            cleaned_lines.append(line)
        else:
            # Normalize spaces in regular text
            cleaned = re.sub(r'\s+', ' ', line.strip())
            if cleaned:
                cleaned_lines.append(cleaned)

    # Join lines and normalize multiple newlines
    text = '\n'.join(cleaned_lines)
    text = re.sub(r'\n{3,}', '\n\n', text)

    logger.debug(f"Preprocessed text: {len(text)} characters")
    return text


def extract_text_from_url(url: str, logger: logging.Logger) -> Optional[ContentDocument]:
    """
    Fetch, clean, and extract text from URL

    Args:
        url: URL to extract from
        logger: Logger instance

    Returns:
        ContentDocument if successful, None otherwise
    """
    # T016: Validate URL
    if not validate_url(url):
        logger.error(f"Invalid URL format: {url}")
        return None

    # T018: Fetch HTML
    html = fetch_html(url, logger)
    if not html:
        return None

    # T019: Parse HTML with BeautifulSoup
    soup = parse_html_with_beautifulsoup(html, logger)
    if not soup:
        return None

    # T020: Extract Docusaurus content
    # T021: Preprocess text (called within extract_docusaurus_content)
    # T022: Create ContentDocument
    # T023: Compute content hash (called within extract_docusaurus_content)
    doc = extract_docusaurus_content(soup, url, logger)

    if doc:
        logger.debug(f"✓ Extracted {doc.word_count} words from {url}")
    else:
        logger.warning(f"✗ Failed to extract content from {url}")

    return doc


# ============================================================================
# Text Chunking (User Story 2)
# ============================================================================

def chunk_text(
    doc: ContentDocument,
    config: PipelineConfig,
    logger: logging.Logger
) -> List[TextChunk]:
    """
    Split text into appropriately-sized chunks using LangChain

    Args:
        doc: ContentDocument with text to chunk
        config: Pipeline configuration
        logger: Logger instance

    Returns:
        List of TextChunk objects

    Implements:
        - T026: Tiktoken-based tokenization
        - T027: LangChain RecursiveCharacterTextSplitter integration
        - T028: Text Segment data structure (TextChunk)
        - T029: Chunking validation
    """
    # T026: Initialize tiktoken encoder
    encoding = tiktoken.get_encoding("cl100k_base")

    def count_tokens_func(text: str) -> int:
        """Count tokens using tiktoken"""
        return len(encoding.encode(text))

    # T027: Initialize LangChain text splitter
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.chunk_size,
        chunk_overlap=config.chunk_overlap,
        length_function=count_tokens_func,
        separators=["\n\n", "\n", ". ", " ", ""]  # Sentence-based splitting
    )

    # Split text into chunks
    text_chunks = splitter.split_text(doc.content_text)

    # T028 & T029: Create TextChunk objects with validation
    chunks: List[TextChunk] = []
    invalid_chunks = 0

    for idx, chunk_text in enumerate(text_chunks):
        token_count = count_tokens_func(chunk_text)

        # T029: Validate chunk size (must not exceed 512 tokens - Cohere limit)
        if token_count > 512:
            logger.warning(f"Chunk {idx} exceeds 512-token limit: {token_count} tokens - skipping")
            invalid_chunks += 1
            continue

        # Create TextChunk
        chunk = TextChunk(
            text=chunk_text,
            token_count=token_count,
            chunk_index=idx,
            source_url=doc.source_url,
            page_title=doc.page_title,
            section_headers=[doc.chapter] if doc.chapter else [],
            extraction_timestamp=doc.extraction_timestamp
        )
        chunks.append(chunk)

    # T029: Validation - check 95% of chunks are between 100-500 tokens (SC-007)
    if chunks:
        valid_range_chunks = sum(1 for c in chunks if 100 <= c.token_count <= 500)
        compliance_rate = (valid_range_chunks / len(chunks)) * 100

        logger.debug(f"Chunking compliance: {compliance_rate:.1f}% in 100-500 token range")

        if compliance_rate < 95.0:
            logger.warning(f"Chunking compliance {compliance_rate:.1f}% below 95% threshold")

    logger.info(f"Created {len(chunks)} chunks from {doc.word_count} words "
                f"(avg {sum(c.token_count for c in chunks) / len(chunks):.0f} tokens/chunk)")

    if invalid_chunks > 0:
        logger.warning(f"Skipped {invalid_chunks} chunks that exceeded 512-token limit")

    return chunks


# ============================================================================
# Embedding Generation (User Story 2)
# ============================================================================

def embed(
    chunks: List[TextChunk],
    config: PipelineConfig,
    logger: logging.Logger
) -> List[List[float]]:
    """
    Generate Cohere embeddings for text chunks

    Args:
        chunks: List of TextChunk objects
        config: Pipeline configuration
        logger: Logger instance

    Returns:
        List of embedding vectors (1024-dimensional)

    Implements:
        - T030: Cohere client initialization
        - T031: Batch embedding generation
        - T032: API retry logic
        - T033: Rate limiting handling
    """
    if not chunks:
        return []

    # T030: Initialize Cohere client
    client = cohere.ClientV2(api_key=config.cohere_api_key)

    # Extract text from chunks
    chunk_texts = [chunk.text for chunk in chunks]

    # T031: Batch embedding generation (max 96 texts/request)
    all_embeddings: List[List[float]] = []
    batch_size = min(config.batch_size, 96)  # Cohere limit

    logger.info(f"Generating embeddings for {len(chunks)} chunks in batches of {batch_size}")

    for i in range(0, len(chunk_texts), batch_size):
        batch = chunk_texts[i:i + batch_size]
        batch_num = (i // batch_size) + 1
        total_batches = (len(chunk_texts) + batch_size - 1) // batch_size

        logger.debug(f"Processing batch {batch_num}/{total_batches} ({len(batch)} texts)")

        # T032 & T033: Retry logic with exponential backoff for rate limiting
        max_retries = 3
        retry_count = 0
        success = False

        while retry_count < max_retries and not success:
            try:
                import time

                response = client.embed(
                    model=config.cohere_model,
                    texts=batch,
                    input_type="search_document",  # For indexing
                    embedding_types=["float"]
                )

                # Extract float embeddings
                batch_embeddings = response.embeddings.float
                all_embeddings.extend(batch_embeddings)

                logger.debug(f"✓ Batch {batch_num}/{total_batches}: Generated {len(batch_embeddings)} embeddings")
                success = True

            except Exception as e:
                retry_count += 1
                error_msg = str(e)

                # T033: Handle rate limiting (429 errors)
                if "429" in error_msg or "rate limit" in error_msg.lower():
                    wait_time = (2 ** retry_count)  # Exponential backoff: 2s, 4s, 8s
                    logger.warning(f"Rate limit hit - waiting {wait_time}s before retry {retry_count}/{max_retries}")
                    time.sleep(wait_time)
                else:
                    logger.error(f"Embedding generation failed: {error_msg}")
                    if retry_count < max_retries:
                        wait_time = 2 ** retry_count
                        logger.info(f"Retrying in {wait_time}s... (attempt {retry_count}/{max_retries})")
                        time.sleep(wait_time)
                    else:
                        logger.error(f"Failed after {max_retries} retries")
                        raise

    logger.info(f"✓ Generated {len(all_embeddings)} embeddings total")

    return all_embeddings


# ============================================================================
# Qdrant Storage (User Story 2)
# ============================================================================

def save_chunks_to_qdrant(
    chunks: List[TextChunk],
    embeddings: List[List[float]],
    config: PipelineConfig,
    logger: logging.Logger,
    dry_run: bool = False
) -> int:
    """
    Batch upsert chunks with embeddings and metadata to Qdrant

    Args:
        chunks: List of TextChunk objects
        embeddings: List of embedding vectors
        config: Pipeline configuration
        logger: Logger instance
        dry_run: If True, skip actual Qdrant writes

    Returns:
        Number of points successfully upserted

    Implements:
        - T034: Embedding Metadata payload structure
        - T035: Qdrant point creation
        - T036: Qdrant upsert operation
        - T037: Dry-run mode
    """
    import uuid

    if len(chunks) != len(embeddings):
        raise ValueError(f"Chunks and embeddings count mismatch: {len(chunks)} vs {len(embeddings)}")

    # T037: Dry-run mode
    if dry_run:
        logger.info(f"DRY RUN: Would upsert {len(chunks)} points to Qdrant collection '{config.collection_name}'")
        for idx, chunk in enumerate(chunks[:3]):  # Show first 3 as sample
            logger.debug(f"  Sample point {idx}: {chunk.page_title} - chunk {chunk.chunk_index} ({chunk.token_count} tokens)")
        return len(chunks)

    # T035: Create Qdrant points
    points = []

    for chunk, embedding in zip(chunks, embeddings):
        # Generate unique ID
        point_id = str(uuid.uuid4())

        # T034: Create metadata payload
        payload = {
            "text": chunk.text,
            "source_url": chunk.source_url,
            "page_title": chunk.page_title,
            "chunk_index": chunk.chunk_index,
            "token_count": chunk.token_count,
            "section_headers": chunk.section_headers,
            "extraction_timestamp": chunk.extraction_timestamp.isoformat(),
            "embedding_model": config.cohere_model,
        }

        # Create Qdrant point
        point = PointStruct(
            id=point_id,
            vector=embedding,
            payload=payload
        )
        points.append(point)

    # T036: Batch upsert to Qdrant
    try:
        client = QdrantClient(url=config.qdrant_url, api_key=config.qdrant_api_key)

        client.upsert(
            collection_name=config.collection_name,
            points=points
        )

        logger.info(f"✓ Upserted {len(points)} points to Qdrant collection '{config.collection_name}'")
        return len(points)

    except Exception as e:
        logger.error(f"Failed to upsert points to Qdrant: {e}")
        raise


# ============================================================================
# CLI Argument Parsing
# ============================================================================

def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments

    Returns:
        Parsed arguments namespace
    """
    parser = argparse.ArgumentParser(
        description="RAG Embeddings Pipeline - Extract, chunk, embed, and store book content",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --urls-file urls.txt
  python main.py --urls https://example.com/page1 https://example.com/page2
  python main.py --urls-file urls.txt --collection-name my_collection --verbose
  python main.py --urls-file urls.txt --dry-run --output-report report.json
        """
    )

    # Input sources (mutually exclusive)
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        '--urls-file',
        type=str,
        help='Path to file containing URLs (one per line, # for comments)'
    )
    input_group.add_argument(
        '--urls',
        nargs='+',
        help='Space-separated list of URLs to process'
    )

    # Collection configuration
    parser.add_argument(
        '--collection-name',
        type=str,
        default='rag_embedding',
        help='Qdrant collection name (default: rag_embedding)'
    )

    # Processing options
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose DEBUG-level logging'
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Process content without writing to Qdrant (useful for testing)'
    )

    parser.add_argument(
        '--force-reindex',
        action='store_true',
        help='Force re-indexing of all URLs (bypass content hash checks)'
    )

    # Pipeline tuning
    parser.add_argument(
        '--batch-size',
        type=int,
        help='Embedding batch size (default: from env BATCH_SIZE or 96)'
    )

    parser.add_argument(
        '--chunk-size',
        type=int,
        help='Text chunk size in tokens (default: from env CHUNK_SIZE_TOKENS or 400)'
    )

    parser.add_argument(
        '--chunk-overlap',
        type=int,
        help='Text chunk overlap in tokens (default: from env CHUNK_OVERLAP_TOKENS or 60)'
    )

    return parser.parse_args()


# ============================================================================
# Main Pipeline Execution
# ============================================================================

def process_urls(
    urls: List[str],
    config: PipelineConfig,
    logger: logging.Logger,
    dry_run: bool = False,
    force_reindex: bool = False
) -> PipelineStats:
    """
    Process multiple URLs through the complete pipeline

    Args:
        urls: List of URLs to process
        config: Pipeline configuration
        logger: Logger instance
        dry_run: If True, skip Qdrant writes
        force_reindex: If True, process all URLs regardless of content hash

    Returns:
        PipelineStats with execution statistics
    """
    stats = PipelineStats(total_urls=len(urls))

    # Verify Qdrant connection first
    if not verify_qdrant_connection(config, logger):
        logger.error("Cannot connect to Qdrant - exiting")
        raise ConnectionError("Qdrant connection failed")

    # Create collection if needed
    if not dry_run:
        create_collection(config, logger)

    # Process each URL
    for idx, url in enumerate(urls):
        logger.info(f"Processing URL {idx+1}/{len(urls)}: {url}")

        try:
            # Extract content
            doc = extract_text_from_url(url, logger)
            if not doc:
                stats.failed_urls += 1
                error = ProcessingError(
                    url=url,
                    error_type="fetch",
                    error_message="Failed to extract content"
                )
                stats.errors.append(error)
                continue

            # Chunk text
            chunks = chunk_text(doc, config, logger)
            if not chunks:
                stats.failed_urls += 1
                error = ProcessingError(
                    url=url,
                    error_type="chunk",
                    error_message="No valid chunks generated"
                )
                stats.errors.append(error)
                continue

            # Generate embeddings
            embeddings = embed(chunks, config, logger)
            if len(embeddings) != len(chunks):
                stats.failed_urls += 1
                error = ProcessingError(
                    url=url,
                    error_type="embed",
                    error_message=f"Embedding count mismatch: {len(chunks)} chunks, {len(embeddings)} embeddings"
                )
                stats.errors.append(error)
                continue

            # Store in Qdrant
            if not dry_run:
                points_upserted = save_chunks_to_qdrant(chunks, embeddings, config, logger)
                stats.total_chunks += len(chunks)
                stats.total_embeddings += len(embeddings)
            else:
                logger.info(f"Dry run: Would store {len(chunks)} chunks for {url}")
                stats.total_chunks += len(chunks)
                stats.total_embeddings += len(embeddings)

            stats.successful_urls += 1
            logger.info(f"✓ Completed {url} ({len(chunks)} chunks)")

        except Exception as e:
            stats.failed_urls += 1
            error = ProcessingError(
                url=url,
                error_type="processing",
                error_message=str(e)
            )
            stats.errors.append(error)
            logger.error(f"✗ Failed {url}: {e}")

    stats.end_time = datetime.utcnow()
    return stats


def main() -> int:
    """
    Main entry point - orchestrate the entire RAG embeddings pipeline

    Returns:
        Exit code (EXIT_SUCCESS, EXIT_PARTIAL_SUCCESS, etc.)
    """
    # Load environment variables
    load_dotenv()

    # Parse command-line arguments
    args = parse_arguments()

    # Setup logging
    logger = setup_logging(args.verbose)

    try:
        # Load configuration
        config = PipelineConfig.from_env()

        # Override config from command-line args
        if args.collection_name:
            config.collection_name = args.collection_name
        if args.batch_size:
            config.batch_size = args.batch_size
        if args.chunk_size:
            config.chunk_size = args.chunk_size
        if args.chunk_overlap:
            config.chunk_overlap = args.chunk_overlap

        # Get URLs to process
        if args.urls_file:
            with open(args.urls_file, 'r', encoding='utf-8') as f:
                urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        else:
            urls = args.urls

        logger.info(f"Starting RAG embeddings pipeline for {len(urls)} URLs")
        logger.info(f"Configuration: collection={config.collection_name}, "
                   f"model={config.cohere_model}, "
                   f"batch_size={config.batch_size}")

        # Process URLs
        stats = process_urls(
            urls=urls,
            config=config,
            logger=logger,
            dry_run=args.dry_run,
            force_reindex=args.force_reindex
        )

        # Report results
        duration = stats.duration_seconds
        logger.info(f"Pipeline completed in {duration:.1f}s")
        logger.info(f"Results: {stats.successful_urls}/{stats.total_urls} URLs successful "
                   f"({stats.success_rate:.1f}%)")
        logger.info(f"Processed {stats.total_chunks} chunks ({stats.total_embeddings} embeddings)")

        if stats.errors:
            logger.warning(f"{len(stats.errors)} processing errors occurred")

        # Determine exit code based on success criteria
        if stats.success_rate >= 95.0:
            logger.info("✓ Pipeline met success criteria (≥95% success rate)")
            return EXIT_SUCCESS
        elif stats.successful_urls > 0:
            logger.warning("⚠ Pipeline completed with partial success (<95% success rate)")
            return EXIT_PARTIAL_SUCCESS
        else:
            logger.error("✗ Pipeline failed - no URLs processed successfully")
            return EXIT_PROCESSING_ERROR

    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        return EXIT_CONFIG_ERROR
    except ConnectionError as e:
        logger.error(f"Connection error: {e}")
        return EXIT_CONNECTION_ERROR
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return EXIT_PROCESSING_ERROR


if __name__ == "__main__":
    sys.exit(main())