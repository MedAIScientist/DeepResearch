# Google Scholar Tool - Advanced Search Features

## Overview

The enhanced Google Scholar tool provides comprehensive academic search capabilities with metadata extraction, citation tracking, and advanced search operators. This tool is the primary interface for discovering peer-reviewed academic literature in Gazzali Research.

## Basic Usage

### Standard Search

```python
# Simple query
result = scholar_tool.call({"query": "machine learning in healthcare"})

# Multiple queries
result = scholar_tool.call({
    "query": [
        "deep learning medical diagnosis",
        "neural networks radiology"
    ]
})
```

## Advanced Search Features

### 1. Search by Author

Find all papers by a specific author, optionally filtered by additional terms.

**Parameters:**
- `query`: Additional search terms (optional, can be empty string)
- `author`: Author name in format "FirstName LastName"

**Example:**
```python
# Find all papers by Geoffrey Hinton
result = scholar_tool.call({
    "query": "",
    "author": "Geoffrey Hinton"
})

# Find papers by Geoffrey Hinton about deep learning
result = scholar_tool.call({
    "query": "deep learning",
    "author": "Geoffrey Hinton"
})
```

**Use Cases:**
- Tracking an author's research output
- Finding seminal works by key researchers
- Identifying research groups and collaborations
- Literature review focused on specific authors

### 2. Search for Citing Papers

Find papers that cite a specific work to understand its impact and follow-up research.

**Parameters:**
- `query`: Base search query (used to find the original paper)
- `citing_paper`: Title of the paper to find citations for

**Example:**
```python
# Find papers citing "Attention Is All You Need"
result = scholar_tool.call({
    "query": "transformer architecture",
    "citing_paper": "Attention Is All You Need"
})
```

**Use Cases:**
- Understanding research impact
- Finding follow-up studies
- Identifying research trends
- Citation network analysis
- Discovering how methods are applied

**Note:** The tool will search for the specified paper and display its citation count. For full citation network exploration, the results include links to Google Scholar pages where citing papers can be accessed.

### 3. Search for Related Papers

Discover papers related to a specific work based on similar topics, keywords, and authors.

**Parameters:**
- `query`: Base search query
- `related_to`: Title of the paper to find related works for

**Example:**
```python
# Find papers related to BERT
result = scholar_tool.call({
    "query": "language models",
    "related_to": "BERT: Pre-training of Deep Bidirectional Transformers"
})
```

**Use Cases:**
- Discovering similar research approaches
- Finding alternative methodologies
- Identifying parallel research streams
- Comprehensive literature review
- Understanding research context

**Note:** The tool searches for papers with similar keywords and topics. Results may include works by the same authors or from the same research area.

### 4. Query Optimization with Academic Operators

The tool automatically optimizes queries using academic search operators to improve result relevance.

**Automatic Optimizations:**

1. **Exact Phrase Matching**: Technical terms are automatically wrapped in quotes
   - Input: `machine learning healthcare`
   - Optimized: `"machine learning" healthcare`

2. **Author Filtering**: When author parameter is used
   - Input: `query="neural networks", author="Yann LeCun"`
   - Optimized: `neural networks author:"Yann LeCun"`

3. **Title Filtering**: Search for terms in paper titles
   - Automatically applied for high-precision searches

**Supported Operators:**

| Operator | Purpose | Example |
|----------|---------|---------|
| `"exact phrase"` | Match exact phrase | `"deep learning"` |
| `author:"Name"` | Filter by author | `author:"Geoffrey Hinton"` |
| `intitle:term` | Term must be in title | `intitle:transformer` |
| `allintitle:terms` | All terms in title | `allintitle:attention mechanism` |
| `source:"venue"` | Filter by publication venue | `source:"Nature"` |
| `-term` | Exclude term | `machine learning -survey` |

**Manual Operator Usage:**

You can also manually include operators in your query:

```python
# Search for papers with "transformer" in title by specific author
result = scholar_tool.call({
    "query": 'intitle:transformer author:"Ashish Vaswani"'
})

# Exclude survey papers
result = scholar_tool.call({
    "query": "machine learning healthcare -survey -review"
})

# Search in specific journal
result = scholar_tool.call({
    "query": 'source:"Nature Medicine" AI diagnosis'
})
```

## Metadata Extraction

All search results include comprehensive metadata:

### Bibliographic Information
- **Title**: Full paper title with link
- **Authors**: List of authors (up to 3 shown, "et al." for more)
- **Year**: Publication year
- **Venue**: Journal, conference, or publication venue
- **Venue Type**: Classified as journal, conference, book, preprint, thesis, or other

### Citation Metrics
- **Citation Count**: Number of times cited
- **Highly Cited Flag**: Marked if 100+ citations
- **Citation Impact**: Indicates seminal works

### Content Analysis
- **Abstract/Snippet**: Brief description or abstract
- **Paper Type**: Classified as empirical, review, theoretical, or unknown
- **Methodology**: Identified research methods (qualitative, quantitative, mixed-methods, etc.)

### Access Information
- **URL**: Link to paper
- **PDF URL**: Direct PDF link if available
- **Open Access Flag**: Indicates freely accessible papers

### Related Resources
- **Related Papers URL**: Link to related works on Google Scholar

## Result Format

Results are formatted with summary statistics and detailed entries:

```
Google Scholar search for 'machine learning healthcare' found 10 results:

## Summary
- Total results: 10
- Highly cited papers (100+ citations): 3
- Open access papers: 5
- Total citations: 1,247
- Paper types: empirical: 6, review: 2, theoretical: 2

## Scholar Results

1. [Deep Learning in Medical Imaging](https://example.com/paper.pdf)
   Authors: Smith, J., Johnson, A., Williams, B.
   Publication: Nature Medicine, 2020
   Cited by: 342 [HIGHLY CITED]
   Type: empirical | Methods: quantitative, computational
   [OPEN ACCESS]
   Deep learning models have shown remarkable performance in medical image analysis...

2. [Survey of AI in Healthcare](https://example.com/paper2.pdf)
   Authors: Brown, C., Davis, E. et al.
   Publication: Journal of Medical AI, 2021
   Cited by: 156 [HIGHLY CITED]
   Type: review
   This comprehensive review examines the application of artificial intelligence...
```

## Integration with Citation Manager

When the Citation Manager is available, the Scholar tool automatically:

1. **Creates Citation Objects**: Converts search results to structured citations
2. **Tracks Sources**: Maintains database of all consulted sources
3. **Enables Bibliography Generation**: Citations can be formatted in APA, MLA, Chicago, or IEEE styles
4. **Supports Export**: Citations can be exported to BibTeX or RIS formats

## Best Practices

### For Literature Reviews

1. **Start Broad**: Begin with general queries to understand the field
   ```python
   result = scholar_tool.call({"query": "climate change adaptation"})
   ```

2. **Identify Key Authors**: Note frequently appearing authors
   ```python
   result = scholar_tool.call({
       "query": "adaptation strategies",
       "author": "Key Researcher Name"
   })
   ```

3. **Follow Citations**: Examine highly cited papers and their citations
   ```python
   result = scholar_tool.call({
       "query": "seminal work",
       "citing_paper": "Important Paper Title"
   })
   ```

4. **Explore Related Work**: Find papers in the same research stream
   ```python
   result = scholar_tool.call({
       "query": "related research",
       "related_to": "Key Paper Title"
   })
   ```

### For Methodology Research

1. **Use Specific Terms**: Include methodology keywords
   ```python
   result = scholar_tool.call({
       "query": "randomized controlled trial machine learning"
   })
   ```

2. **Filter by Paper Type**: Look for empirical studies
   - Results automatically classify paper types
   - Focus on papers marked as "empirical"

3. **Examine Methods**: Review the methodology field in results
   - Identifies qualitative, quantitative, mixed-methods approaches

### For Citation Network Analysis

1. **Find Seminal Works**: Look for highly cited papers
   - Results flag papers with 100+ citations
   - Total citation counts provided in summary

2. **Track Research Evolution**: Use citing papers to see how research developed
   ```python
   result = scholar_tool.call({
       "query": "original topic",
       "citing_paper": "Seminal Work Title"
   })
   ```

3. **Identify Research Clusters**: Use related papers to find research communities
   ```python
   result = scholar_tool.call({
       "query": "research area",
       "related_to": "Representative Paper"
   })
   ```

## Query Optimization Tips

### For Precision (Fewer, More Relevant Results)

- Use exact phrases: `"specific technical term"`
- Filter by title: `intitle:keyword`
- Specify author: `author:"Researcher Name"`
- Limit to venue: `source:"Journal Name"`

### For Recall (More Comprehensive Results)

- Use broader terms without quotes
- Include synonyms: `(machine learning OR artificial intelligence)`
- Avoid restrictive filters
- Use multiple related queries

### For Recent Research

- Include year in query: `machine learning 2023`
- Sort results by date (when viewing on Scholar)
- Focus on preprints for cutting-edge work

### For Foundational Research

- Look for highly cited papers (100+ citations)
- Search for "review" or "survey" papers
- Examine papers from 5-10 years ago for established methods

## Limitations and Workarounds

### API Limitations

**Issue**: Serper API may not support all Google Scholar features directly

**Workarounds**:
- Citation network exploration: Results include links to Scholar pages
- Advanced filters: Use manual operators in queries
- Full-text access: PDF links provided when available

### Rate Limiting

**Issue**: API requests may be rate-limited

**Workarounds**:
- Tool includes automatic retry with exponential backoff
- Batch queries processed in parallel (max 3 concurrent)
- Results cached by Citation Manager (when available)

### Metadata Completeness

**Issue**: Not all papers have complete metadata

**Workarounds**:
- Tool extracts maximum available information
- Incomplete citations flagged for manual review
- URL always preserved for reference

## Error Handling

The tool handles various error conditions gracefully:

- **No Results**: Returns message suggesting broader query
- **API Timeout**: Retries up to 5 times with backoff
- **Invalid Parameters**: Returns clear error message
- **Missing API Key**: Fails with configuration error

## Configuration

### Environment Variables

```bash
# Required: Serper API key for Google Scholar access
SERPER_API_KEY=your_api_key_here

# Alternative key name (legacy support)
SERPER_KEY_ID=your_api_key_here
```

### Getting a Serper API Key

1. Visit [serper.dev](https://serper.dev)
2. Sign up for an account
3. Generate an API key
4. Add to your `.env` file

## Examples

### Example 1: Comprehensive Literature Review

```python
# Step 1: Broad search to understand field
results = scholar_tool.call({
    "query": "artificial intelligence medical diagnosis"
})

# Step 2: Focus on specific methodology
results = scholar_tool.call({
    "query": "deep learning medical diagnosis intitle:CNN"
})

# Step 3: Find key researchers
results = scholar_tool.call({
    "query": "medical imaging",
    "author": "Andrew Ng"
})

# Step 4: Explore citation network
results = scholar_tool.call({
    "query": "AI diagnosis",
    "citing_paper": "CheXNet: Radiologist-Level Pneumonia Detection"
})
```

### Example 2: Methodology Comparison

```python
# Find papers using different methodologies
results = scholar_tool.call({
    "query": [
        "qualitative study user experience AI",
        "quantitative analysis AI adoption healthcare",
        "mixed methods AI implementation"
    ]
})
```

### Example 3: Tracking Research Evolution

```python
# Find original work
original = scholar_tool.call({
    "query": '"Attention Is All You Need" transformer'
})

# Find papers citing it
citations = scholar_tool.call({
    "query": "transformer architecture",
    "citing_paper": "Attention Is All You Need"
})

# Find related developments
related = scholar_tool.call({
    "query": "attention mechanism",
    "related_to": "Attention Is All You Need"
})
```

## Requirements Addressed

This enhanced Scholar tool addresses the following requirements from the Gazzali Research specification:

- **Requirement 14.1**: Optimized Scholar queries with academic search operators
- **Requirement 14.2**: Extract citation counts, publication venues, and author information
- **Requirement 14.3**: Identify highly cited papers and seminal works
- **Requirement 14.4**: Retrieve related articles and citing papers for citation network exploration

## Future Enhancements

Potential future improvements:

1. **Direct Citation Network API**: If Serper adds citation network support
2. **Advanced Filtering**: Date ranges, impact factor, h-index filtering
3. **Full-Text Analysis**: Extract and analyze paper content when available
4. **Citation Graph Visualization**: Generate visual citation networks
5. **Automated Literature Mapping**: Identify research clusters and trends
6. **Integration with Other Databases**: PubMed, IEEE Xplore, ACM Digital Library

## Support

For issues or questions:
- Check the main README for general setup
- Review environment configuration in `docs/ENVIRONMENT_SETUP.md`
- Examine citation management in `docs/CITATION_MANAGER.md`
- See academic configuration in `docs/ACADEMIC_CONFIG.md`
