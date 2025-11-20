# 🚀 Knitty Quick Start Guide

> **⚠️ ALPHA VERSION:** This project is experimental. Use for testing and development only.

Get up and running with Knitty in 5 minutes!

## Step 1: Install Dependencies

```bash
# Install Python packages
pip install -r requirements.txt

# Install Playwright browsers (required for web scraping)
playwright install chromium
```

## Step 2: Configure Environment

Create a `.env` file in the project root:

```env
# Fast LLM (for keyword extraction)
FAST_LLM_API_KEY=your-api-key-here
FAST_LLM_API_BASE=https://api.groq.com/openai/v1
FAST_LLM_MODEL_NAME=llama3-8b-8192

# Smart LLM (for CV enhancement)
SMART_LLM_API_KEY=your-api-key-here
SMART_LLM_API_BASE=https://api.openai.com/v1
SMART_LLM_MODEL_NAME=gemini-2.5-pro

# Embedding LLM (for similarity calculation)
EMBED_LLM_API_KEY=your-api-key-here
EMBED_LLM_API_BASE=https://api.openai.com/v1
EMBED_LLM_MODEL_NAME=text-embedding-ada-002
```

## Step 3: Choose Your Interface

> **⚠️ Both interfaces are in ALPHA stage - experimental only**

### Option A: FastAPI (⚠️ ALPHA)

```bash
python app.py
```

Then open your browser to:

- API Documentation: `http://localhost:8000/docs`
- Health Check: `http://localhost:8000/health`

**Example API Call:**

```bash
curl -X POST "http://localhost:8000/api/v1/enhance-cv" \
  -F "cv_file=@examples/cv.pdf" \
  -F "job_posting_text=Software Engineer position..."
```

### Option B: Streamlit GUI (⚠️ ALPHA)

```bash
streamlit run streamlit_app.py
```

Then open your browser to `http://localhost:8501`

## Step 4: Use It!

### Using FastAPI

See the interactive API documentation at `http://localhost:8000/docs` for:

- Request formats
- Response schemas
- Try-it-out functionality

### Using Streamlit GUI

1. Upload your CV (PDF file)
2. Provide job posting (URL or paste text)
3. Add any additional information (optional)
4. Click "Enhance My CV"
5. Wait for processing (~30-60 seconds)
6. Download your enhanced CV!

## 🧪 Test It Works

```bash
# Run tests
pytest

# Check health
curl http://localhost:8000/health
```

## 📚 Next Steps

- Read `README_PRODUCTION.md` for detailed setup
- Check `DEPLOYMENT.md` for production deployment
- See `TRANSFORMATION_SUMMARY.md` for architecture overview

## ❓ Troubleshooting

### "Module not found" errors

```bash
pip install -r requirements.txt
```

### Playwright errors

```bash
playwright install chromium
```

### API key errors

- Check your `.env` file exists
- Verify all API keys are set correctly
- Ensure API keys have proper permissions

### Port already in use

- FastAPI: Change port in `app.py` (default: 8000)
- Streamlit: Use `--server.port 8502` flag

## 🎉 You're Ready!

Start enhancing CVs with AI-powered optimization!
