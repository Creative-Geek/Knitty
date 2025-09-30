# Scoring Process Documentation

This document explains the cosine similarity scoring process used in the Knitty CV Tailoring System as implemented in the Jupyter notebook.

## Overview

The scoring system uses cosine similarity to measure how well a CV aligns with a job posting by comparing their keyword embeddings. The process involves extracting keywords, generating vector embeddings, and calculating similarity scores before and after CV enhancement.

## Scoring Methodology

### 1. Keyword Extraction

**CV Keywords Extraction:**

```python
# Extract professional keywords from CV using Fast LLM
cvKeywordsPrompt = cvKeywordsPrompt.format(cvText=cvText)
cvKeywords = FAST_LLM.invoke([("human", cvKeywordsPrompt)])
```

The system extracts keywords including:

- Technical skills (programming languages, tools, frameworks)
- Professional skills (leadership, analysis, problem-solving)
- Industry terms and domain expertise
- Job titles and roles
- Action verbs demonstrating capabilities

**Job Keywords Extraction:**

```python
# Extract relevant keywords from job posting using Fast LLM
jobKeywordsPrompt = jobKeywordsPrompt.format(jobPostingText=jobPostingText)
jobKeywords = FAST_LLM.invoke([("human", jobKeywordsPrompt)])
```

Keywords are returned as JSON arrays, for example:

```json
[
  "IT Help Desk",
  "Network troubleshooting",
  "Hardware diagnostics",
  "Remote access",
  "Support tickets",
  "Analytical skills"
]
```

### 2. Embedding Generation

**Vector Embedding Process:**

```python
def embedSingle(text):
    """Generate single embedding for entire text (no chunking)"""
    embeddings = OpenAIEmbeddings(
        model=os.getenv("EMBED_LLM_MODEL_NAME"),
        api_key=os.getenv("EMBED_LLM_API_KEY"),
        base_url=os.getenv("EMBED_LLM_API_BASE"),
    )

    # Get single embedding for the whole text
    embedding_vector = embeddings.embed_query(text)
    return np.array(embedding_vector)
```

**Embedding Characteristics:**

- Dimension: 3072 (OpenAI embedding model standard)
- Input: Keyword strings converted to text
- Output: NumPy arrays representing semantic meaning
- Model: OpenAI-compatible embedding model

### 3. Cosine Similarity Calculation

**Mathematical Implementation:**

```python
def cosine_similarity(a, b):
    """Calculate cosine similarity between two vectors"""
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
```

**Formula:**

```text
cosine_similarity = (A · B) / (||A|| × ||B||)
```

Where:

- A · B = dot product of vectors A and B
- ||A|| = L2 norm (magnitude) of vector A
- ||B|| = L2 norm (magnitude) of vector B

**Score Range:** -1 to 1

- 1: Perfect alignment (identical semantic meaning)
- 0: Orthogonal (no relationship)
- -1: Opposite meaning (rare in practice)

### 4. Scoring Pipeline

**Initial Similarity Calculation:**

```python
# Generate embeddings for CV and job keywords
cvEmbeddingVector = embedSingle(cvKeywords.content)
jobEmbeddingVector = embedSingle(jobKeywords.content)

# Calculate baseline similarity
currentCosineSimilarity = cosine_similarity(cvEmbeddingVector, jobEmbeddingVector)
print(f"Initial Cosine Similarity: {currentCosineSimilarity:.6f}")
```

**Post-Enhancement Similarity:**

```python
# Generate embedding for enhanced CV
newCvEmbeddingVector = embedSingle(finalCV)

# Calculate improved similarity
newCosineSimilarity = cosine_similarity(newCvEmbeddingVector, jobEmbeddingVector)

# Measure improvement
improvement = float(newCosineSimilarity - currentCosineSimilarity)
print(f"New Cosine Similarity: {newCosineSimilarity:.6f}")
print(f"Improvement over previous: {improvement:+.6f}")
```

## Iterative Improvement Process

### Similarity-Based Feedback Loop

The system includes an iterative improvement mechanism:

```python
if newCosineSimilarity <= currentCosineSimilarity:
    # Provide similarity feedback to Smart LLM
    similarityString = f"New Cosine Similarity: {newCosineSimilarity:.6f}; Improvement over previous: {float(newCosineSimilarity - currentCosineSimilarity):+.6f}"

    # Retry with feedback
    cvEnhanceMessages = [
        ("human", cvEnhancePromptFormatted),
        ("assistant", finalCV),
        ("human", similarityString),
    ]

    # Generate improved version
    response = SMART_LLM.invoke(cvEnhanceMessages)
    finalCV = response.content
```

### Improvement Validation

After retry, the system measures final improvement:

```python
# Final similarity measurement
newCvEmbeddingVector = embedSingle(finalCV)
newCosineSimilarity = cosine_similarity(newCvEmbeddingVector, jobEmbeddingVector)
print(f"Final Cosine Similarity: {newCosineSimilarity:.6f}")
```

## Scoring Interpretation

### Typical Score Ranges

Based on the notebook example:

**Initial Score Range:** 0.40 - 0.70

- Represents baseline alignment between original CV and job posting
- Example: 0.573196 (57.32% similarity)

**Target Improvement:** +0.05 to +0.15

- Meaningful improvement typically ranges from 5% to 15%
- Example: +0.039725 improvement (3.97% increase)

**High-Quality Alignment:** 0.65+

- Scores above 65% indicate strong CV-job alignment
- Achieved through strategic keyword integration and content optimization

### Score Quality Factors

**Positive Contributors:**

- Relevant technical skills matching job requirements
- Professional experience aligned with role responsibilities
- Industry-specific terminology and domain expertise
- Action verbs demonstrating required capabilities
- Educational background matching job qualifications

**Potential Limitations:**

- Keyword stuffing may not improve semantic similarity
- Over-optimization can reduce natural language flow
- Missing context may limit embedding quality
- Generic keywords provide less improvement than specific terms

## Implementation Notes

### Embedding Model Considerations

**Model Selection:**

- Uses OpenAI-compatible embedding models
- Consistent dimensionality across all embeddings
- Semantic understanding of professional terminology

**API Configuration:**

```python
embeddings = OpenAIEmbeddings(
    model=os.getenv("EMBED_LLM_MODEL_NAME"),
    api_key=os.getenv("EMBED_LLM_API_KEY"),
    base_url=os.getenv("EMBED_LLM_API_BASE"),
)
```

### Performance Characteristics

**Processing Time:**

- Keyword extraction: ~2-5 seconds per document
- Embedding generation: ~1-2 seconds per text
- Similarity calculation: <1 second (NumPy operations)

**Accuracy Factors:**

- Quality of keyword extraction prompts
- Relevance of extracted keywords to job requirements
- Embedding model's understanding of professional terminology
- Balance between keyword integration and natural language

### Validation and Quality Assurance

**Automatic Validation:**

- JSON parsing validation for keyword extraction
- Vector dimension consistency checking
- Similarity score bounds validation (-1 to 1)
- Improvement measurement accuracy

**Manual Review Points:**

- Keywords relevance to actual job requirements
- CV enhancement quality and naturalness
- Template compliance and formatting
- Overall professional presentation

## Example Scoring Session

From the notebook execution:

```text
Initial Processing:
- CV Keywords: 95+ professional terms extracted
- Job Keywords: 47+ job-specific terms extracted
- Initial Cosine Similarity: 0.573196

Enhancement Process:
- Smart LLM optimization with template compliance
- Strategic keyword integration
- Professional experience reframing

Results:
- New Cosine Similarity: 0.612921
- Improvement: +0.039725 (+3.97%)
- Final alignment: 61.29% semantic similarity
```

This demonstrates the system's ability to measurably improve CV-job alignment while maintaining professional quality and template compliance.
