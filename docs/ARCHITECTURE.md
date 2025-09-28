# System Architecture and Implementation

This document provides a detailed description of the Knitty CV Tailoring System architecture as implemented in the Jupyter notebook, outlining the actual data flow, components, and LLM integration patterns.

## System Overview

Knitty is implemented as a Jupyter notebook that processes CVs and job postings through a sequential pipeline using AI models for keyword extraction, similarity analysis, and content enhancement. The system is designed for interactive use and experimentation rather than production deployment.

## Core Components

### 1. Environment Setup and Configuration

- **Environment Variables**: Manages API keys and endpoints for different LLM providers
- **Dependencies**: Uses LangChain, OpenAI, BeautifulSoup, Playwright, and NumPy
- **Configuration Files**: Stores prompts and templates in the `config/` directory

### 2. Input Processing

- **CV Processing**:
  - Extracts text from PDF files using PyPDFLoader
  - Combines CV text with additional candidate information
  - Handles text encoding and formatting
- **Job Posting Processing**:
  - Accepts URLs or direct text input
  - Uses Playwright for web scraping when URL provided
  - Implements RAG (Retrieval Augmented Generation) for content extraction

### 3. LLM Integration

The system uses 2-3 LLM endpoints (not the documented "four distinct LLMs"):

**Fast LLM**:

- Used for keyword extraction from both CV and job postings
- Configured via `FAST_LLM_*` environment variables
- Typically a cost-effective model like GPT-3.5 or Groq

**Smart LLM**:

- Used for final CV enhancement and generation
- Configured via `SMART_LLM_*` environment variables
- Typically a more capable model like GPT-4 or Claude

**Embed LLM**:

- Used for generating vector embeddings
- Configured via `EMBED_LLM_*` environment variables
- Uses OpenAI-compatible embedding models

### 4. RAG Implementation for Job Extraction

When processing job URLs, the system implements a sophisticated RAG pipeline:

```python
# Web scraping with Playwright
async def fetchUrl(jobPostingUrl):
    # Handles Windows-specific asyncio policies
    # Uses headless Chromium for content extraction

# HTML cleaning and text extraction
def cleanHTML(jobPostingHTML):
    # Removes scripts, styles, and formatting
    # Extracts clean text content

# Document embedding and retrieval
def embed(text):
    # Chunks text using RecursiveCharacterTextSplitter
    # Creates in-memory vector store
    # Returns searchable embeddings

# RAG-based content extraction
def doRAG(jobExtractedText):
    # Retrieves relevant job posting sections
    # Uses Context LLM to extract structured job data
    # Returns JSON with role summary, responsibilities, qualifications
```

## Data Flow Pipeline

The actual implementation follows this sequence:

```text
1. Setup Environment
   ├── Load API keys and configurations
   ├── Import dependencies (LangChain, OpenAI, etc.)
   └── Load prompts and templates from config/

2. Input Processing
   ├── CV: PDF → PyPDFLoader → Raw Text + Additional Info
   └── Job: URL → Playwright → HTML → BeautifulSoup → Clean Text
                                    ↓
                              RAG Processing → Structured JSON

3. Keyword Extraction (Parallel)
   ├── CV Text → Fast LLM → JSON Array of Keywords
   └── Job Text → Fast LLM → JSON Array of Keywords

4. Similarity Analysis
   ├── CV Keywords → Embed LLM → Vector Embeddings
   ├── Job Keywords → Embed LLM → Vector Embeddings
   └── Cosine Similarity Calculation → Similarity Score

5. CV Enhancement
   ├── All Data → Smart LLM → Enhanced CV (Markdown)
   ├── Similarity Check → If No Improvement → Retry with Feedback
   └── Final Output → Save to examples/cv.md

6. Optional: HTML Generation
   └── Enhanced CV → External API → HTML/PDF Output
```

## Key Implementation Details

### Cosine Similarity Calculation

```python
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
```

### Iterative Improvement Process

The system includes a feedback loop for optimization:

- Measures similarity before and after enhancement
- If no improvement, provides feedback to Smart LLM
- Retries enhancement with similarity score context
- Validates final improvement

### Template-Based Output

Uses a structured markdown template stored in `config/cvTemplate.txt`:

- YAML frontmatter for metadata
- Structured sections (Profile, Projects, Skills, Experience, Education)
- Iconify integration for visual elements
- Web-application ready format

## Environment Configuration

Required environment variables:

```env
# Fast LLM (Keyword Extraction)
FAST_LLM_API_KEY=your-api-key
FAST_LLM_API_BASE=https://api.groq.com/openai/v1
FAST_LLM_MODEL_NAME=llama3-8b-8192

# Smart LLM (CV Enhancement)
SMART_LLM_API_KEY=your-api-key
SMART_LLM_API_BASE=https://api.openai.com/v1
SMART_LLM_MODEL_NAME=gpt-4

# Embedding LLM
EMBED_LLM_API_KEY=your-api-key
EMBED_LLM_API_BASE=https://api.openai.com/v1
EMBED_LLM_MODEL_NAME=text-embedding-ada-002

# Optional: HTML Generation API
SPECIAL_SAUCE_API_URL=your-html-api-endpoint
SPECIAL_SAUCE_API_KEY=your-html-api-key
```

## Dependencies

Actual dependencies used in the notebook:

```python
# Core AI/ML
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate

# Web Processing
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import requests

# Utilities
from dotenv import load_dotenv
import numpy as np
import json
import os
```
