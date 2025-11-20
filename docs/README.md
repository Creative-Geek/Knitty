# Knitty: CV Tailoring System

> **⚠️ ALPHA VERSION:** This entire project is experimental and in active development.

This project is a Jupyter notebook-based application designed to automatically tailor a candidate's curriculum vitae (CV) to a specific job description. The system analyzes the candidate's CV and target job posting, extracts relevant keywords, and rewrites the CV to maximize alignment with job requirements using AI-powered enhancement.

The goal is to improve the chances of passing through automated screening systems (ATS) and catching recruiter attention by strategically highlighting the most relevant aspects of a candidate's profile.

## Available Interfaces

- **FastAPI Backend** (⚠️ ALPHA): REST API for programmatic access
- **Streamlit GUI** (⚠️ ALPHA): Web interface for interactive enhancement
- **Jupyter Notebook**: For research and experimentation

**⚠️ All interfaces are experimental and not recommended for production use.**

## Core Features

- **PDF CV Processing**: Extracts text from PDF CVs and incorporates additional candidate information
- **Job Posting Analysis**: Processes job postings from URLs using web scraping and RAG (Retrieval Augmented Generation) or accepts direct text input
- **AI-Powered Keyword Extraction**: Uses LLMs to identify professionally relevant keywords from both CV and job descriptions
- **Semantic Similarity Scoring**: Calculates cosine similarity between CV and job keywords using vector embeddings
- **Intelligent CV Enhancement**: Rewrites CVs using advanced LLMs to strategically incorporate job-specific keywords while maintaining professional quality
- **Template-Based Output**: Generates enhanced CVs in a structured markdown format suitable for web applications
- **Iterative Improvement**: Includes feedback loops to optimize similarity scores through multiple enhancement attempts

## Workflow Overview

The notebook implements a streamlined four-stage process:

1. **Input Processing**: Loads CV (PDF), additional information, and job posting (URL or text)
2. **Keyword Extraction**: Extracts professional keywords from both CV and job posting using Fast LLM
3. **Similarity Analysis**: Converts keywords to embeddings and calculates cosine similarity score
4. **CV Enhancement**: Uses Smart LLM to generate an optimized CV based on extracted insights and similarity feedback

## Documentation

- **[ARCHITECTURE.md](ARCHITECTURE.md)**: Technical implementation details and data flow
- **[API_REFERENCE.md](API_REFERENCE.md)**: Functions, prompts, and data structures
- **[DEVELOPMENT_GUIDE.md](DEVELOPMENT_GUIDE.md)**: Setup instructions and usage guide
- **[SCORING_PROCESS.md](SCORING_PROCESS.md)**: Detailed cosine similarity scoring methodology
