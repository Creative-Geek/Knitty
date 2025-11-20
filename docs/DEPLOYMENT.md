# Knitty Deployment Guide

## 🚀 Production Deployment

### Prerequisites

- Python 3.10 or higher
- Playwright browsers installed
- Environment variables configured

### Installation

```bash
# Clone repository
git clone <repository-url>
cd Knitty

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium
```

### Environment Setup

Create a `.env` file:

```env
FAST_LLM_API_KEY=your-key
FAST_LLM_API_BASE=https://api.groq.com/openai/v1
FAST_LLM_MODEL_NAME=llama3-8b-8192

SMART_LLM_API_KEY=your-key
SMART_LLM_API_BASE=https://api.openai.com/v1
SMART_LLM_MODEL_NAME=gemini-2.5-pro

EMBED_LLM_API_KEY=your-key
EMBED_LLM_API_BASE=https://api.openai.com/v1
EMBED_LLM_MODEL_NAME=text-embedding-ada-002
```

### Running FastAPI

```bash
# Development
python app.py

# Production (with gunicorn)
gunicorn app:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Running Streamlit

```bash
streamlit run streamlit_app.py
```

### Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright
RUN playwright install chromium
RUN playwright install-deps chromium

# Copy application
COPY . .

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:

```bash
docker build -t knitty .
docker run -p 8000:8000 --env-file .env knitty
```

### Systemd Service (Linux)

Create `/etc/systemd/system/knitty.service`:

```ini
[Unit]
Description=Knitty API Service
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/Knitty
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/uvicorn app:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl enable knitty
sudo systemctl start knitty
```

### Nginx Reverse Proxy

```nginx
server {
    listen 80;
    server_name api.knitty.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Security Considerations

1. **CORS Configuration**: Update CORS settings in `knitty/api/app.py` for production
2. **API Keys**: Never commit `.env` files
3. **Rate Limiting**: Consider adding rate limiting middleware
4. **Authentication**: Add API key authentication for production
5. **HTTPS**: Use HTTPS in production
6. **Input Validation**: All inputs are validated via Pydantic models

### Monitoring

- Health check endpoint: `GET /health`
- Logging: Configured via `knitty/utils/logging_config.py`
- Consider adding APM tools (e.g., Sentry, DataDog)

### Scaling

- Use multiple workers with gunicorn
- Consider using a task queue (Celery) for long-running jobs
- Use Redis for caching if needed
- Database for storing CVs/jobs (optional)

