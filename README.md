# Knitty: Resume Factory

<div align="center">
  <img src="docs/images/Knitty_Logo.png" alt="Knitty Logo" width="256">
</div>

<div align="center">
  <strong>An intelligent CV tailoring system that optimizes resumes for specific job postings using advanced LLM technology and cosine similarity analysis.</strong>
</div>

<br>

## 🚀 Overview

Knitty is a production-ready AI-powered CV tailoring system that optimizes resumes for specific job postings. The system analyzes your existing CV alongside a target job posting, then generates an optimized version that better aligns with the job requirements while maintaining authenticity and professional quality.

You can access Knitty through:

- **🖥️ Web GUI**: User-friendly Streamlit interface for interactive CV enhancement
- **⚙️ API**: RESTful FastAPI backend for programmatic access and integration

## ✨ Key Features

- **🔄 Multi-LLM Architecture**: Leverages four specialized AI models for different tasks
- **📄 PDF Processing**: Extracts and processes CV content from PDF files
- **🌐 Web Scraping**: Automatically fetches job postings from LinkedIn and other platforms
- **🧠 RAG-Powered Analysis**: Uses Retrieval-Augmented Generation for intelligent job content extraction
- **📊 Similarity Scoring**: Measures CV-job alignment using cosine similarity
- **🎯 Smart Enhancement**: Generates tailored CVs while maintaining professional quality
- **🔁 Iterative Improvement**: Automatically retries generation if similarity doesn't improve
- **📱 HTML Export**: Converts final CVs to professional HTML format

## 🏗️ Architecture

The system operates through a sophisticated multi-stage pipeline:

```mermaid
---
config:
  theme: redux
---
flowchart TD
    A["CV PDF"] --> B["PDF Text Extraction"]
    A1["Additional Info"] --> B1["Combine CV Content"]
    B --> B1
    B1 --> C["CV Keyword Extraction<br>Fast LLM"] & D["CV Embedding Generation<br>Embed LLM"] & M["Smart LLM Enhancement"]
    E["Job URL/Text"] --> F{"Input Type?"}
    F -- URL --> G["Web Scraping<br>Playwright + BeautifulSoup"]
    F -- Text --> H["Direct Text Processing"]
    G --> I["RAG Processing<br>Context LLM + Vector Store"]
    H --> I
    I --> J["Job Keyword Extraction<br>Fast LLM"] & K["Job Embedding Generation<br>Embed LLM"] & M
    C --> L["Cosine Similarity Analysis"] & M
    D --> L
    J --> L & M
    K --> L
    L --> M
    M --> N["Enhanced CV Generation"]
    N --> O["Similarity Check"]
    O -- Improved --> P["Final CV Output"]
    O -- Not Improved --> Q["Iterative Retry"]
    Q --> M
    P --> R["HTML Export<br>Special Sauce API"] & S["Markdown Export"]
     A:::Ash
     M:::Ash
     E:::Ash
     L:::Ash
     P:::Ash
    classDef Ash stroke-width:1px, stroke-dasharray:none, stroke:#999999, fill:#EEEEEE, color:#000000
    style A fill:#e1f5fe
    style M fill:#f3e5f5
    style E fill:#e8f5e8
    style L fill:#fff3e0
    style P fill:#e8f5e8

```

### LLM Specialization

- **Fast LLM** (for example: GPT-OSS-120B): Quick keyword extraction from CV and job postings
- **Context LLM**: Large-context processing for web-scraped content and RAG operations
- **Embed LLM**: Generates high-quality embeddings for similarity analysis
- **Smart LLM** (Currently using: Gemini 2.5 Pro): Advanced CV enhancement and generation

## 🛠️ Technical Implementation

### Core Technologies

- **LangChain**: Document processing, embeddings, and LLM orchestration
- **Playwright**: Robust web scraping for job postings
- **BeautifulSoup**: HTML cleaning and text extraction
- **NumPy**: Mathematical operations for similarity calculations
- **PyPDF**: PDF text extraction and processing

### Advanced Features

- **RAG Pipeline**: Uses InMemoryVectorStore for intelligent content retrieval
- **Async Processing**: Non-blocking web scraping with proper Windows compatibility
- **Template System**: YAML-based CV templates for consistent formatting
- **Configuration Management**: File-based prompt and template management
- **Error Handling**: Comprehensive error recovery and retry mechanisms

## 🚀 Getting Started

### Installation

```bash
# Clone the repository
git clone https://github.com/Creative-Geek/Knitty.git
cd Knitty

# Install dependencies
pip install -e .

# Install Playwright browsers for web scraping
playwright install chromium
```

### Environment Setup

Create a `.env` file in the project root with your LLM API configurations:

```env
# Fast LLM (Keyword Extraction) - e.g., Groq Llama 3
FAST_LLM_API_KEY="your-api-key"
FAST_LLM_API_BASE="https://api.groq.com/openai/v1"
FAST_LLM_MODEL_NAME="llama3-8b-8192"

# Smart LLM (CV Enhancement) - e.g., OpenAI GPT or Google Gemini
SMART_LLM_API_KEY="your-api-key"
SMART_LLM_API_BASE="https://api.openai.com/v1"
SMART_LLM_MODEL_NAME="gpt-4-turbo"

# Embedding LLM (Similarity Analysis) - e.g., OpenAI Embeddings
EMBED_LLM_API_KEY="your-api-key"
EMBED_LLM_API_BASE="https://api.openai.com/v1"
EMBED_LLM_MODEL_NAME="text-embedding-ada-002"

# Optional: HTML Generation Service
SPECIAL_SAUCE_API_URL="https://cv-service.com/generate"
SPECIAL_SAUCE_API_KEY="your-service-key"
```

### Running the Application

#### Option 1: Web GUI (Streamlit)

```bash
streamlit run streamlit_app.py
```

Open your browser to `http://localhost:8501` and start enhancing CVs through an intuitive interface.

#### Option 2: API Server (FastAPI)

```bash
python app.py
# or
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

Access the API at `http://localhost:8000` with interactive API docs at `http://localhost:8000/docs`

#### Option 3: Jupyter Notebook

```bash
jupyter notebook notebook.ipynb
```

Great for experimentation and research.

## 📊 How It Works

### 1. Input Processing

- Extracts text from PDF CVs using PyPDFLoader
- Combines CV content with additional information
- Processes job postings via web scraping or direct text input

### 2. Keyword Analysis

- Uses Fast LLM to extract professional keywords from both sources
- Returns structured JSON arrays of relevant terms and phrases
- Focuses on technical skills, experience, and job requirements

### 3. Similarity Measurement

- Generates embeddings for keyword sets using specialized models
- Calculates cosine similarity to quantify CV-job alignment
- Establishes baseline metrics for improvement tracking

### 4. Intelligent Enhancement

- Uses Smart LLM to generate optimized CV based on analysis
- Maintains professional tone and template compliance
- Includes iterative improvement with similarity feedback

### 5. Quality Assurance

- Measures improvement in cosine similarity scores
- Automatically retries if enhancement doesn't improve alignment
- Exports final CV in both markdown and HTML formats

## 📈 Results

The system typically achieves:

- **Baseline Similarity**: 40-70% initial CV-job alignment
- **Improvement Range**: +5% to +15% similarity increase
- **Quality Metrics**: Professional presentation with strategic keyword integration
- **Processing Time**: ~30-60 seconds for complete enhancement

## 🔮 Future Vision

You'll have to wait for that 😉

## 🤝 Contributing

We welcome contributions to enhance and evolve Knitty! Areas where we could use help:

- **Frontend Enhancement**: Improve the Streamlit GUI with additional features
- **Backend Optimization**: Performance improvements to the FastAPI server
- **Model Fine-tuning**: Optimize LLM prompts and enhance CV generation quality
- **DevOps**: Docker containerization and cloud deployment setup
- **Testing**: Expand test coverage and add integration tests
- **Documentation**: API documentation and user guides
- **Feature Development**: New features like batch processing, templates, and analytics

## 📚 Documentation

- [Architecture Guide](docs/ARCHITECTURE.md) - Detailed system architecture
- [API Reference](docs/API_REFERENCE.md) - Function signatures and data models
- [Development Guide](docs/DEVELOPMENT_GUIDE.md) - Setup and development instructions
- [Scoring Process](docs/SCORING_PROCESS.md) - Similarity calculation methodology

## ⚖️ License

This project is currently in research and development phase. License terms will be established as the project evolves toward production release.

## 🙏 Acknowledgments

- LangChain team for excellent LLM orchestration tools
- OpenAI for embedding and language model APIs
- Playwright team for robust web automation capabilities
- The open-source community for inspiration and foundational technologies

---

<div align="center">
  <strong>Ready to revolutionize your job applications? Get started with Knitty today!</strong>
</div>
