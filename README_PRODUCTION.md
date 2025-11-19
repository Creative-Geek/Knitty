# Knitty: Production Setup Guide

This guide explains how to run Knitty in production mode with FastAPI and Streamlit.

## 🚀 Quick Start

### 1. Installation

```bash
# Install dependencies
pip install -e .

# Install Playwright browsers
playwright install chromium
```

### 2. Environment Configuration

Create a `.env` file in the project root:

```env
# Fast LLM (Keyword Extraction)
FAST_LLM_API_KEY=your-api-key
FAST_LLM_API_BASE=https://api.groq.com/openai/v1
FAST_LLM_MODEL_NAME=llama3-8b-8192

# Smart LLM (CV Enhancement)
SMART_LLM_API_KEY=your-api-key
SMART_LLM_API_BASE=https://api.openai.com/v1
SMART_LLM_MODEL_NAME=gemini-2.5-pro

# Embedding LLM
EMBED_LLM_API_KEY=your-api-key
EMBED_LLM_API_BASE=https://api.openai.com/v1
EMBED_LLM_MODEL_NAME=text-embedding-ada-002

# Optional: HTML Generation API
SPECIAL_SAUCE_API_URL=https://cv-service.com/generate
SPECIAL_SAUCE_API_KEY=your-service-key
```

### 3. Running FastAPI Server

```bash
# Development mode
python app.py

# Or using uvicorn directly
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at `http://localhost:8000`

API documentation: `http://localhost:8000/docs`

### 4. Running Streamlit GUI

```bash
streamlit run streamlit_app.py
```

The GUI will be available at `http://localhost:8501`

## 📡 API Endpoints

### POST `/api/v1/enhance-cv`

Enhance a CV to match a job posting.

**Request:**
- `cv_file`: PDF file (multipart/form-data)
- `job_posting_url`: Optional URL to job posting
- `job_posting_text`: Optional direct job posting text
- `additional_info`: Optional additional CV information

**Response:**
```json
{
  "enhanced_cv": "...",
  "baseline_similarity": 0.42,
  "final_similarity": 0.52,
  "improvement": 0.10,
  "cv_keywords": "[...]",
  "job_keywords": "[...]"
}
```

### POST `/api/v1/extract-keywords`

Extract keywords from a CV.

**Request:**
- `cv_file`: PDF file (multipart/form-data)

**Response:**
```json
{
  "keywords": "[...]"
}
```

### POST `/api/v1/calculate-similarity`

Calculate cosine similarity between two texts.

**Request:**
```json
{
  "text_a": "First text",
  "text_b": "Second text"
}
```

**Response:**
```json
{
  "similarity": 0.75
}
```

### GET `/health`

Health check endpoint.

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=knitty --cov-report=html

# Run specific test file
pytest tests/test_similarity.py
```

## 📦 Project Structure

```
knitty/
├── knitty/
│   ├── __init__.py
│   ├── api/              # FastAPI application
│   │   ├── __init__.py
│   │   └── app.py
│   ├── config/           # Configuration management
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   └── prompts.py
│   ├── core/             # Core business logic
│   │   ├── __init__.py
│   │   ├── cv_processor.py
│   │   ├── job_processor.py
│   │   ├── similarity.py
│   │   ├── enhancer.py
│   │   ├── pipeline.py
│   │   └── llm_clients.py
│   └── utils/            # Utilities
│       ├── __init__.py
│       └── logging_config.py
├── tests/                # Test suite
├── app.py                # FastAPI entry point
├── streamlit_app.py      # Streamlit GUI
└── pyproject.toml        # Dependencies
```

## 🔧 Configuration

### Settings

All settings are loaded from environment variables via `pydantic-settings`. See `knitty/config/settings.py` for available options.

### Logging

Logging is configured via `knitty/utils/logging_config.py`. Set `LOG_LEVEL` environment variable to control verbosity.

## 🐳 Docker (Optional)

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml ./
RUN pip install -e .

COPY . .

# Install Playwright
RUN playwright install chromium
RUN playwright install-deps chromium

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 📝 Notes

- The FastAPI server runs on port 8000 by default
- Streamlit runs on port 8501 by default
- Make sure Playwright browsers are installed for web scraping
- Configure CORS appropriately for production use
- Consider adding authentication/authorization for production

