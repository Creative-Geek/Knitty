# Development Guide

> **⚠️ ALPHA VERSION:** This project is experimental and in active development.

This guide provides instructions for setting up and running the Knitty CV Tailoring System notebook, including environment configuration, dependencies, and usage patterns.

## Prerequisites

- **Python 3.8+**: Ensure you have a recent version of Python installed
- **Jupyter Notebook or JupyterLab**: For running the main notebook
- **Git**: For version control and cloning the repository

## Environment Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd Knitty
```

### 2. Create Virtual Environment

Using `uv` (recommended, as shown in project):

```bash
# Install uv if not already installed
pip install uv

# Create and activate virtual environment
uv venv
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
```

Alternative using standard Python:

```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

The project uses `pyproject.toml` and `uv.lock` for dependency management:

```bash
# Using uv (recommended)
uv sync

# Or using pip
pip install -e .
```

### Core Dependencies

Based on the actual notebook implementation:

```toml
[dependencies]
# AI/ML Libraries
langchain = "^0.1.0"
langchain-community = "^0.0.20"
langchain-openai = "^0.0.6"
langchain-core = "^0.1.0"

# Web Processing
beautifulsoup4 = "^4.12.0"
playwright = "^1.40.0"
requests = "^2.31.0"

# Data Processing
numpy = "^1.24.0"
python-dotenv = "^1.0.0"

# Jupyter Environment
jupyter = "^1.0.0"
ipykernel = "^6.25.0"
```

### 4. Install Playwright Browsers

Playwright requires browser installation:

```bash
playwright install chromium
```

### 5. Environment Variables

Create a `.env` file in the project root with your API configurations:

```env
# Fast LLM (for keyword extraction)
FAST_LLM_API_KEY=your-groq-api-key
FAST_LLM_API_BASE=https://api.groq.com/openai/v1
FAST_LLM_MODEL_NAME=llama3-8b-8192

# Smart LLM (for CV enhancement)
SMART_LLM_API_KEY=your-openai-api-key
SMART_LLM_API_BASE=https://api.openai.com/v1
SMART_LLM_MODEL_NAME=gpt-4

# Embedding LLM
EMBED_LLM_API_KEY=your-openai-api-key
EMBED_LLM_API_BASE=https://api.openai.com/v1
EMBED_LLM_MODEL_NAME=text-embedding-ada-002

# Optional: HTML Generation Service
SPECIAL_SAUCE_API_URL=your-html-api-endpoint
SPECIAL_SAUCE_API_KEY=your-html-api-key
```

## Running the Application

> **⚠️ Both interfaces are in ALPHA stage - experimental only**

### Option 1: FastAPI Backend (⚠️ ALPHA)

```bash
python app.py
# or
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

Access the API at `http://localhost:8000` with interactive docs at `http://localhost:8000/docs`

### Option 2: Streamlit GUI (⚠️ ALPHA)

```bash
streamlit run streamlit_app.py
```

### Option 3: Jupyter Notebook (Development/Research)

```bash
jupyter notebook
# or
jupyter lab
```

### 2. Open the Main Notebook

Navigate to and open `notebook.ipynb` in your Jupyter environment.

### 3. Prepare Input Files

Place your files in the `examples/` directory:

- **CV**: `examples/cv.pdf` (your PDF resume)
- **Additional Info**: `examples/additionalInfo.txt` (optional candidate information)
- **Job Posting**: Either provide a URL in the notebook or save text to `examples/jobPostingText.txt`

### 4. Execute the Notebook

Run the notebook cells sequentially:

1. **Setup Environment**: Loads dependencies and configurations
2. **Get Inputs**: Configure CV path, job posting URL/text, and additional info
3. **Static Inputs**: Loads prompts and templates from `config/` directory
4. **Process Inputs**: Extracts CV text and processes job posting
5. **Make AI Calls**: Performs keyword extraction and similarity analysis
6. **Resume Enhancement**: Generates optimized CV using Smart LLM
7. **HTML Generation**: (Optional) Converts to HTML format

## Configuration Files

The system uses several configuration files in the `config/` directory:

### Prompts

- `cvKeywordsPrompt.txt`: CV keyword extraction prompt
- `jobKeywordsPrompt.txt`: Job keyword extraction prompt
- `jobRagPrompt.txt`: Job posting RAG extraction prompt
- `cvEnhancePrompt.txt`: CV enhancement prompt

### Templates

- `cvTemplate.txt`: Output CV template structure

## Usage Patterns

### Basic Usage

```python
# 1. Set input paths
cvPath = "examples/cv.pdf"
jobPostingUrl = "https://linkedin.com/jobs/view/123456"
additionalInfoPath = "examples/additionalInfo.txt"

# 2. Process inputs (run notebook cells)
# 3. Review generated CV in examples/cv.md
```

### URL vs Text Input

**For Job URLs**:

```python
jobPostingUrl = "https://linkedin.com/jobs/view/123456"
# System will scrape and process automatically
```

**For Direct Text**:

```python
jobPostingUrl = ""  # Leave empty
# Place job text in examples/jobPostingText.txt
```

### Customizing Prompts

Edit files in `config/` directory to customize:

- Keyword extraction criteria
- CV enhancement instructions
- Output template structure

## Output Files

The notebook generates several output files:

- `examples/cv.md`: Enhanced CV in markdown format
- `examples/cv3.html`: HTML version (if HTML generation enabled)
- Console output: Similarity scores and processing logs

## Troubleshooting

### Common Issues

**Import Errors**:

```bash
# Ensure all dependencies are installed
uv sync
# or
pip install -r requirements.txt
```

**API Key Errors**:

- Verify `.env` file exists and contains valid API keys
- Check API endpoint URLs are correct
- Ensure sufficient API credits/quota

**Playwright Issues**:

```bash
# Reinstall browsers
playwright install chromium
```

**PDF Processing Errors**:

- Ensure PDF is not password-protected
- Verify file path is correct
- Check PDF contains extractable text (not just images)

### Performance Optimization

**For Large Job Postings**:

- The RAG implementation may struggle with very large pages
- Consider preprocessing to extract relevant sections

**For Multiple CVs**:

- Restart kernel between different CV processing sessions
- Clear output to manage memory usage

**API Rate Limits**:

- Add delays between API calls if hitting rate limits
- Consider using different API providers for different LLM roles

## Development Notes

### Notebook Structure

The notebook is organized into logical sections:

1. Environment setup and imports
2. Input configuration and loading
3. Processing functions definition
4. Execution pipeline
5. Output generation and validation

### Future Web Application

The notebook serves as a prototype for a future web application:

- Template structure is web-ready (YAML + Markdown)
- Functions can be extracted into modules
- Configuration system supports multiple environments
- Output format suitable for web rendering

### Extension Points

Areas for future enhancement:

- Batch processing multiple CVs
- Additional output formats (PDF, DOCX)
- Integration with job board APIs
- Advanced similarity metrics
- User interface development
