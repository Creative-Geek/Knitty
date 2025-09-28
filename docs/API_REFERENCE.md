# API Reference and Data Models

This document defines the actual data structures, function signatures, and LLM prompts used in the Knitty CV Tailoring System notebook implementation.

## Data Models

### 1. Keyword Extraction Output

**Description**: JSON array output from Fast LLM after processing CV or job description text.

**Format**: JSON Array of Strings

**Example**:

```json
[
  "Python",
  "C++",
  "JavaScript",
  "TypeScript",
  "React",
  "Node.js",
  "Flask",
  "FastAPI",
  "Django",
  "LLMs",
  "Agent AI",
  "LangChain",
  "Google Cloud",
  "Azure",
  "Docker",
  "GitHub",
  "Git",
  "Linux",
  "Problem Solving",
  "Communication",
  "Teamwork",
  "Software Engineer"
]
```

### 2. Job Description Extraction Output

**Description**: Structured JSON output from RAG-based job posting extraction.

**Format**: JSON Object

**Structure**:

```json
{
  "role_summary": "Entry-level IT Help Desk professional responsible for managing IT assets, troubleshooting network, hardware and software issues, and delivering user support across the main office and branch locations.",
  "key_responsibilities": [
    "Manage IT department assets.",
    "Solve network problems and device issues in main office and branches.",
    "Install internet networking in new branches.",
    "Provide support in person, over the phone, or via remote access."
  ],
  "required_qualifications": [
    "0-2 years working as a Help Desk.",
    "Basic knowledge of networking and firewalls.",
    "Advanced knowledge of computer hardware systems.",
    "Excellent analytical and diagnostic skills."
  ],
  "preferred_qualifications": null
}
```

### 3. CV Template Structure

**Description**: YAML frontmatter + Markdown template for enhanced CV output.

**Format**: Markdown with YAML header

**Structure**:

```yaml
---
name: Candidate Name
header:
  - text: |
      <span style="font-style: italic; font-weight: normal; display: block; margin-top: -7.5px; margin-bottom:5px;">
      Professional Title
      </span>
  - text: <span class="iconify" data-icon="tabler:mail"></span> email@example.com
    link: mailto:email@example.com
  - text: <span class="iconify" data-icon="tabler:phone"></span> +1234567890
  - text: <span class="iconify" data-icon="tabler:map-pin"></span> City, Country
  - text: <span class="iconify" data-icon="tabler:world"></span> website.com
    link: https://website.com
  - text: <span class="iconify" data-icon="tabler:brand-github"></span> github.com/username
    link: https://github.com/username
  - text: <span class="iconify" data-icon="tabler:brand-linkedin"></span> linkedin.com/in/profile
    link: https://linkedin.com/in/profile
---

## Profile
Brief professional summary...

## Technical Experience
Work experience entries...

## Projects
Project descriptions...

## Skills
Technical and soft skills...

## Education
Educational background...
```

## Core Functions

### 1. Configuration Loading

```python
def load_config_file(filename):
    """Load configuration files from the config directory"""
    config_path = os.path.join('config', filename)
    with open(config_path, 'r', encoding='utf-8') as file:
        return file.read().strip()
```

### 2. Web Scraping and Content Extraction

```python
async def fetchUrl(jobPostingUrl):
    """Fetch job posting content using Playwright"""
    # Handles Windows asyncio policies
    # Returns raw HTML content

def cleanHTML(jobPostingHTML):
    """Extract clean text from HTML using BeautifulSoup"""
    # Removes scripts, styles, and formatting
    # Returns plain text content

async def extract_job_posting_from_url(jobPostingUrl):
    """Complete pipeline for URL-based job extraction"""
    # Fetches HTML, cleans it, applies RAG, returns structured JSON
```

### 3. Embedding and Similarity

```python
def embedSingle(text):
    """Generate single embedding for entire text (no chunking)"""
    # Uses OpenAI-compatible embedding model
    # Returns NumPy array of embeddings

def cosine_similarity(a, b):
    """Calculate cosine similarity between two vectors"""
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
```

### 4. CV Enhancement

```python
def formatCvEnhancePrompt(cvTemplate, cvText, jobPostingText, cvKeywords, jobKeywords, currentCosineSimilarity):
    """Format the complete prompt for CV enhancement"""
    # Combines all context into Smart LLM prompt

def generateFinalCV(cvEnhancePromptFormatted):
    """Generate enhanced CV using Smart LLM"""
    # Returns enhanced CV in markdown format
```

## LLM Prompts

### 1. CV Keyword Extraction Prompt

**File**: `config/cvKeywordsPrompt.txt`

**Purpose**: Extract professional keywords from CV text using Fast LLM.

**Key Instructions**:

- Extract professionally relevant keywords for job matching
- Focus on technical skills, professional skills, industry terms, job titles
- Return JSON array of strings
- Normalize variations and include both technical and soft skills

**Template Variables**: `{cvText}`

### 2. Job Keyword Extraction Prompt

**File**: `config/jobKeywordsPrompt.txt`

**Purpose**: Extract relevant keywords from job posting text using Fast LLM.

**Key Instructions**:

- Same structure as CV keyword extraction
- Focus on job-specific requirements and qualifications
- Extract skills, tools, responsibilities, and qualifications

**Template Variables**: `{jobPostingText}`

### 3. Job RAG Extraction Prompt

**File**: `config/jobRagPrompt.txt`

**Purpose**: Extract structured job information from web-scraped content.

**Key Instructions**:

- Parse job description and filter out boilerplate
- Extract role summary, responsibilities, and qualifications
- Return clean JSON with specific fields
- Focus on essential, role-specific information

**Output Fields**:

- `role_summary`: 1-2 sentence executive summary
- `key_responsibilities`: Action-oriented duties list
- `required_qualifications`: Non-negotiable requirements
- `preferred_qualifications`: Optional requirements (or null)

### 4. CV Enhancement Prompt

**File**: `config/cvEnhancePrompt.txt`

**Purpose**: Rewrite CV to align with job description using Smart LLM.

**Key Instructions**:

- Maximize cosine similarity between CV and job keywords
- Naturally incorporate relevant keywords and experiences
- Maintain professional tone and avoid keyword stuffing
- Use quantifiable achievements and action verbs
- Follow provided template structure exactly

**Template Variables**:

- `{cvTemplate}`: Complete CV template structure
- `{cvText}`: Original CV and additional information
- `{jobPostingText}`: Job description or structured JSON
- `{cvKeywords}`: Extracted CV keywords JSON array
- `{jobKeywords}`: Extracted job keywords JSON array
- `{currentCosineSimilarity}`: Current similarity score

## Environment Variables

### Required Configuration

```env
# Fast LLM (Keyword Extraction)
FAST_LLM_API_KEY=your-fast-llm-api-key
FAST_LLM_API_BASE=https://api.groq.com/openai/v1
FAST_LLM_MODEL_NAME=llama3-8b-8192

# Smart LLM (CV Enhancement)
SMART_LLM_API_KEY=your-smart-llm-api-key
SMART_LLM_API_BASE=https://api.openai.com/v1
SMART_LLM_MODEL_NAME=gpt-4

# Embedding LLM
EMBED_LLM_API_KEY=your-embed-api-key
EMBED_LLM_API_BASE=https://api.openai.com/v1
EMBED_LLM_MODEL_NAME=text-embedding-ada-002

# Optional: External HTML Generation
SPECIAL_SAUCE_API_URL=your-html-conversion-api
SPECIAL_SAUCE_API_KEY=your-html-api-key
```

## File Structure

```text
config/
├── cvTemplate.txt          # CV output template
├── cvKeywordsPrompt.txt     # CV keyword extraction prompt
├── jobKeywordsPrompt.txt    # Job keyword extraction prompt
├── jobRagPrompt.txt         # Job RAG extraction prompt
└── cvEnhancePrompt.txt      # CV enhancement prompt

examples/
├── cv.pdf                   # Input CV file
├── cv.md                    # Enhanced CV output
├── cv.html / cv1.html       # HTML versions
├── jobPostingText.txt       # Job posting text input
└── additionalInfo.txt       # Additional candidate info

notebook.ipynb               # Main implementation
```

## Error Handling

### Common Issues and Solutions

**JSON Parsing Errors**:

- LLM may wrap JSON in code blocks
- Implementation strips `` json` and  `` markers
- Validates JSON structure before processing

**Embedding Failures**:

- Large text may exceed API limits
- Current implementation processes full keyword strings
- TODO: Implement batch processing for large inputs

**Similarity Score Validation**:

- Scores should be between -1 and 1
- Implementation includes retry logic for poor improvements
- Provides feedback to Smart LLM for optimization
