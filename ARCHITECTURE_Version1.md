# System Architecture and Data Flow

This document provides a detailed description of the architecture for the Intelligent CV Tailoring System, outlining the components, the flow of data, and the role of each LLM.

## System Components

The application is composed of several interconnected modules, each responsible for a specific part of the workflow.

1.  **Input Processor**: Handles the initial data ingestion.
2.  **CV Processor**: Extracts text and keywords from the user's CV.
3.  **Job Posting Processor**: Scrapes and extracts text and keywords from the job posting.
4.  **Similarity Analyzer**: Calculates the match score between the CV and the job.
5.  **CV Generator**: Produces the final, tailored CV.

## LLM Configuration

The system is designed to work with four user-provided LLMs. Configuration for these models (API base URLs, API keys, and model names) must be managed centrally and supplied to the relevant components.

-   **Fast LLM**: A cheap and fast model for keyword extraction.
-   **Context LLM**: A model with a large context window for processing entire web pages.
-   **Embed LLM**: A model specialized in creating text embeddings.
-   **Smart LLM**: A powerful, large model for the final CV revision task.

## Data Flow Diagram

```
+----------------+      +--------------------+      +-------------------------+
|   User Input   |----->|  Input Processor   |----->|     CV Processor        |
| (CV, Job, Info)|      +--------------------+      | (PDF Extract, Add Info) |
+----------------+                                 +------------+------------+
                                                                 |
                                                                 v
+-----------------------------+                        +--------------------+
|  CV Keywords (JSON Array)   |<-----------------------|     Fast LLM       |
+-----------------------------+                        |(Keyword Extraction)|
                                                       +--------------------+
                                                                 ^
                                                                 |
+---------------------------------+      +-----------------------+-----------------------+
| Job Post Keywords (JSON Array)  |<-----|         Job Posting Processor                 |
+---------------------------------+      | (URL Scrape -> Context LLM -> Fast LLM)       |
                                         +-----------------------------------------------+
                                                                 |
                                                                 v
+-------------------------+      +-------------------------+     +-------------------------+
| CV Keyword Embeddings   |      | Job Keyword Embeddings  |     |                         |
+------------+------------+      +-------------+-----------+     |                         |
             |                                 |                 |                         |
             +-----------------+---------------+                 |
                               |                                 |
                               v                                 v
+-------------------------+      +-------------------------+     +-------------------------+
|  Similarity Analyzer    |----->|      CV Generator       |<----|    Raw CV & Job Text    |
| (Cosine Similarity)     |      |      (Smart LLM)        |     +-------------------------+
+-------------------------+      +------------+------------+
                                              |
                                              v
+-------------------------+
|  Final Tailored CV      |
|  (Markdown Output)      |
+-------------------------+
```

## Step-by-Step Process

1.  **CV Processing**:
    - The `Input Processor` receives the CV. If it's a PDF, a library like `PyMuPDF` is used to extract raw text.
    - The optional "additional info" text is appended to the raw CV text.
    - The combined text is sent to the **Fast LLM** with the specified prompt to extract a JSON array of professional keywords.

2.  **Job Posting Processing**:
    - If a URL is provided, the `RAGJobExtractor` script is invoked. This script uses the **Context LLM** to intelligently extract the core job description from the site's HTML.
    - If raw text is provided, it is used directly.
    - The resulting job description text is sent to the **Fast LLM** with the same keyword extraction prompt to get a JSON array of keywords.

3.  **Similarity Analysis**:
    - The two JSON arrays of keywords (from the CV and the job post) are passed to the **Embed LLM** to generate vector embeddings for each list.
    - The `Similarity Analyzer` then takes these two embeddings and calculates the cosine similarity score using the provided Python function. This score quantifies the initial match.

4.  **Final CV Generation**:
    - The `CV Generator` orchestrates the final step. It gathers all the necessary components:
        - The raw CV text (with additional info).
        - The extracted job description text.
        - The list of CV keywords.
        - The list of job posting keywords.
        - The calculated cosine similarity score.
    - These artifacts are formatted into the final prompt for the **Smart LLM**.
    - The **Smart LLM** is instructed to revise the resume content to align with the job, incorporate keywords naturally, and structure the output according to the provided markdown template.
    - The final output is the revised CV in markdown format.