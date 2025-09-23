# Intelligent CV Tailoring System

This project is a sophisticated application designed to automatically tailor a candidate's curriculum vitae (CV) to a specific job description. By leveraging a suite of four distinct Large Language Models (LLMs), the system analyzes the candidate's CV and the target job posting, identifies key skills and qualifications, and rewrites the CV to maximize its alignment with the job requirements.

The goal is to significantly improve the chances of passing through automated screening systems (ATS) and catching the attention of recruiters by highlighting the most relevant aspects of a candidate's profile.

## Core Features

- **Automated CV and Job Description Analysis**: Extracts text from PDFs and scrapes job descriptions from URLs.
- **Multi-LLM Architecture**: Utilizes different LLMs for specialized tasks:
    - **Fast LLM**: For quick and efficient keyword extraction.
    - **Context LLM**: For processing large documents like web-scraped job postings.
    - **Embed LLM**: For generating vector embeddings for similarity analysis.
    - **Smart LLM**: For high-quality, context-aware CV revision.
- **Keyword Extraction & Matching**: Identifies critical keywords from both the CV and the job description.
- **Similarity Scoring**: Calculates a cosine similarity score to quantify the match between the CV and the job before and after revision.
- **Intelligent CV Revision**: Rewrites the CV to strategically incorporate job-specific keywords and align the candidate's experience with the role's requirements.

## Development Workflow

The development process is broken down into four main stages:

1.  **Input Processing**: The system ingests the user's CV (PDF or text), optional additional information, and a job posting (URL or text).
2.  **Keyword Analysis**: It extracts professionally relevant keywords from both the CV and the job posting using the **Fast LLM**.
3.  **Similarity Calculation**: The extracted keywords are converted into numerical vectors (embeddings) using the **Embed LLM**, and their similarity is calculated.
4.  **CV Generation**: The **Smart LLM** receives the original CV, the job description, the keyword lists, and the similarity score. It then generates a new, optimized version of the CV based on a provided template.

For a more detailed technical breakdown, please refer to the [ARCHITECTURE.md](ARCHITECTURE.md) file.