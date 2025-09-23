# Development Guide

This guide provides instructions for setting up the development environment, managing dependencies, and running the application.

## Prerequisites

- **Python 3.8+**: Ensure you have a recent version of Python installed.
- **pip**: Python's package installer.
- **Git**: For version control.

## 1. Environment Setup

### Clone the Repository

First, clone the project repository to your local machine:
```bash
git clone <repository-url>
cd <repository-name>
```

### Create a Virtual Environment

It is highly recommended to use a virtual environment to manage project dependencies.

```bash
# Create the virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Install Dependencies

The required Python packages are listed in `requirements.txt`. The provided job extraction script uses `langchain`, `google-generativeai`, `beautifulsoup4`, `requests`, and others. You will also need a PDF processing library.

```bash
pip install -r requirements.txt
```
A sample `requirements.txt` would look like this:
```
# LLM and LangChain
langchain
langchain-core
langchain-google-genai
langchain_community

# Web Scraping and HTML Parsing
requests
beautifulsoup4
selenium
unstructured

# PDF Processing
pymupdf

# Vector Store & Embeddings
faiss-cpu # Or faiss-gpu if you have CUDA
langchain-experimental

# Utilities
python-dotenv
numpy
```

### Environment Variables

The application requires API keys and endpoints for the various LLMs. Create a `.env` file in the root of the project directory and populate it with the necessary credentials.

```env
# Fast LLM Configuration
FAST_LLM_API_KEY="your-fast-llm-api-key"
FAST_LLM_API_BASE="https://api.fastllm.com/v1"
FAST_LLM_MODEL_NAME="model-name"

# Context LLM Configuration (Example using Google)
CONTEXT_LLM_API_KEY="your-google-api-key"
CONTEXT_LLM_API_BASE="https://generativelanguage.googleapis.com/v1beta"
CONTEXT_LLM_MODEL_NAME="gemini-1.5-flash-latest"

# Embed LLM Configuration
EMBED_LLM_API_KEY="your-embed-llm-api-key"
EMBED_LLM_API_BASE="https://api.embedllm.com/v1"
EMBED_LLM_MODEL_NAME="embedding-model"

# Smart LLM Configuration
SMART_LLM_API_KEY="your-smart-llm-api-key"
SMART_LLM_API_BASE="https://api.smartllm.com/v1"
SMART_LLM_MODEL_NAME="smart-model-name"
```

## 2. Running the Application

The application can be run via a main script that orchestrates the entire CV tailoring process.

### Example Usage

Create a main script (e.g., `main.py`) that imports the necessary modules and executes the workflow.

```python
# main.py
from cv_processor import process_cv
from job_processor import process_job_posting
from similarity_analyzer import calculate_similarity
from cv_generator import generate_final_cv

def main():
    # 1. Define inputs
    cv_path = "path/to/your/cv.pdf"
    job_url = "https://example.com/job-posting/123"
    additional_info = "Enthusiastic about AI and machine learning..."

    # 2. Process CV and Job Posting
    cv_text, cv_keywords = process_cv(cv_path, additional_info)
    job_text, job_keywords = process_job_posting(url=job_url)

    # 3. Analyze Similarity
    # This step internally generates embeddings and calculates the score
    similarity_score = calculate_similarity(cv_keywords, job_keywords)
    print(f"Initial Cosine Similarity: {similarity_score:.4f}")

    # 4. Generate the final CV
    final_cv = generate_final_cv(
        raw_cv_text=cv_text,
        job_description_text=job_text,
        cv_keywords=cv_keywords,
        job_keywords=job_keywords,
        similarity_score=similarity_score
    )

    # 5. Save the output
    with open("final_cv.md", "w") as f:
        f.write(final_cv)

    print("Successfully generated tailored CV in final_cv.md")

if __name__ == "__main__":
    main()

```

To run the script:
```bash
python main.py
```