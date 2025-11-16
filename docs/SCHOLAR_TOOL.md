# Enhanced Google Scholar Tool

## Overview

The enhanced Google Scholar tool for Gazzali Research provides comprehensive metadata extraction and academic-specific features for scholarly research. It goes beyond basic search to deliver structured bibliographic data, citation tracking, and intelligent paper classification.

## Features

### 1. Comprehensive Metadata Extraction

The tool extracts and structures the following information from each search result:

- **Bibliographic Data**
  - Title
  - Authors (parsed and formatted)
  - Publication year
  - Venue (journal, conference, etc.)
  - Venue type classification

- **Citation Metrics**
  - Citation count
  - Highly cited paper identification (100+ citations)
  - Related papers links

- **Content Information**
  - Abstract/snippet text
  - Paper type classification (empirical, review, theoretical)
  - Methodology identification

- **Access Information**
  - Direct PDF links when available
  - Open access status
  - Primary URL

### 2. Paper Type Classification

The tool automatically identifies paper types based on title and abstract analysis:

- **Empirical**: Studies with data collection and analysis
- **Review**: Literature reviews, surveys, meta-analyses
- **Theoretical**: Conceptual frameworks and theoretical papers
- **Unknown**: Papers that don't clearly fit other categories

**Keywords used for classification:**
- Review: "review", "survey", "meta-analysis", "systematic review", "literature review"
- Theoretical: "theory", "theoretical", "framework", "model", "conceptual"
- Empirical: "study", "experiment", "data", "analysis", "results", "findings"

### 3. Methodology Extraction

The tool identifies research methodologies mentioned in abstracts:

- **Qualitative**: Interviews, ethnography, case studies, grounded theory
- **Quantitative**: Surveys, experiments, statistical analysis, regression
- **Mixed-methods**: Combined qualitative and quantitative approaches
- **Meta-analysis**: Systematic reviews with statistical synthesis
- **Computational**: Simulations, algorithms, machine learning
- **Experimental**: Controlled experiments, randomized trials

### 4. Citation Manager Integration

When available, the tool automatically:
- Creates Citation objects for each result
- Adds citations to the CitationManager
- Enables automatic bibliography generation
- Supports citation deduplication

### 5. Enhanced Result Formatting

Results are formatted with:
- Numbered entries with clickable links
- Author lists (with "et al." for 4+ authors)
- Publication venue and year
- Citation counts with highly-cited indicators
- Paper type and methodology tags
- Open access indicators
- Abstracts/snippets

### 6. Summary Statistics

Each search provides aggregate statistics:
- Total results found
- Number of highly cited papers
- Number of open access papers
- Total citation count across results
- Distribution of paper types

## Usage

### Basic Search

```python
from gazzali.tools.tool_scholar import Scholar

scholar = Scholar()
results = scholar.call({"query": "machine learning in healthcare"})
print(results)
```

### Multiple Queries

```python
queries = [
    "deep learning medical imaging",
    "natural language processing clinical notes",
    "reinforcement learning drug discovery"
]

results = scholar.call({"query": queries})
print(results)
```

### With Citation Manager

```python
from gazzali.tools.tool_scholar import Scholar
from gazzali.citation_manager import CitationManager, CitationStyle

scholar = Scholar()
results = scholar.call({"query": "transformer models"})

# Access collected citations
citation_manager = scholar.get_citation_manager()
if citation_manager:
    # Generate bibliography
    bibliography = citation_manager.generate_bibliography(CitationStyle.APA)
    print(bibliography)
    
    # Export to BibTeX
    citation_manager.export_bibtex("citations.bib")
```

## Output Format

### Example Output

```
Google Scholar search for 'deep learning medical imaging' found 10 results:

## Summary
- Total results: 10
- Highly cited papers (100+ citations): 3
- Open access papers: 4
- Total citations: 2,847
- Paper types: empirical: 6, review: 3, theoretical: 1

## Scholar Results

1. [Deep Learning in Medical Image Analysis](PDF: https://arxiv.org/pdf/...)
   Authors: Smith, J., Johnson, A., Williams, B. et al.
   Publication: Medical Image Analysis, 2020
   Cited by: 523 [HIGHLY CITED]
   Type: review | Methods: quantitative, meta-analysis
   [OPEN ACCESS]
   This comprehensive review examines the application of deep learning...

2. [Convolutional Neural Networks for Radiology](https://doi.org/...)
   Authors: Brown, C., Davis, M.
   Publication: Radiology, 2019
   Cited by: 412 [HIGHLY CITED]
   Type: empirical | Methods: experimental, computational
   We present a novel CNN architecture for automated detection of...

[Additional results...]
```

## Configuration

### Environment Variables

```bash
# Required: Serper API key for Google Scholar access
SERPER_API_KEY=your_api_key_here

# Alternative key name
SERPER_KEY_ID=your_api_key_here
```

### Highly Cited Threshold

The default threshold for "highly cited" papers is 100 citations. This can be adjusted by modifying the `_is_highly_cited` method:

```python
def _is_highly_cited(self, citation_count: int) -> bool:
    return citation_count >= 100  # Adjust threshold here
```

## Integration with Research Agent

The Scholar tool is designed to be prioritized in academic research workflows:

1. **Scholar-First Strategy**: The research agent should call Scholar before general web search
2. **Automatic Citation Tracking**: All Scholar results are automatically added to CitationManager
3. **Source Quality Scoring**: Scholar results receive higher credibility scores
4. **Metadata Preservation**: Full bibliographic data is preserved for report generation

## API Reference

### Scholar Class

#### Methods

##### `__init__(cfg: Optional[Dict] = None)`
Initialize the Scholar tool with optional configuration.

##### `call(params: Union[str, dict], **kwargs) -> str`
Execute a Scholar search.

**Parameters:**
- `params`: Query parameters (dict with 'query' field or string)
- `**kwargs`: Additional arguments

**Returns:**
- Formatted search results string

##### `get_citation_manager() -> Optional[CitationManager]`
Get the citation manager instance containing all extracted citations.

**Returns:**
- CitationManager instance or None

##### `google_scholar_with_serp(query: str) -> str`
Search Google Scholar using Serper API.

**Parameters:**
- `query`: Search query string

**Returns:**
- Formatted search results

### Metadata Structure

Each result contains the following metadata:

```python
{
    'index': int,                    # Result number
    'title': str,                    # Paper title
    'authors': List[str],            # Author names
    'year': Optional[int],           # Publication year
    'venue': str,                    # Publication venue
    'venue_type': str,               # journal/conference/preprint/etc.
    'citation_count': int,           # Number of citations
    'abstract': str,                 # Abstract or snippet
    'url': str,                      # Primary URL
    'pdf_url': Optional[str],        # Direct PDF link
    'is_open_access': bool,          # Open access status
    'publication_info': str,         # Raw publication info
    'paper_type': str,               # empirical/review/theoretical/unknown
    'methodology': Optional[str],    # Identified methodologies
    'is_highly_cited': bool,         # Highly cited flag
    'related_url': Optional[str],    # Related papers link
}
```

## Error Handling

### Common Errors

1. **No API Key**
   - Error: "Google Scholar Timeout"
   - Solution: Set SERPER_API_KEY environment variable

2. **No Results Found**
   - Error: "No results found for query: '...'"
   - Solution: Use a more general query or check spelling

3. **Rate Limiting**
   - Error: Connection timeout after retries
   - Solution: Wait and retry, or reduce query frequency

### Retry Logic

The tool implements automatic retry with exponential backoff:
- Maximum 5 retry attempts
- Handles connection errors gracefully
- Returns informative error messages

## Best Practices

### Query Optimization

1. **Use Academic Terms**: Include field-specific terminology
2. **Be Specific**: Add context like "machine learning" + "medical imaging"
3. **Use Quotes**: For exact phrases: `"deep learning"`
4. **Author Search**: Include author names for targeted searches
5. **Year Ranges**: Add year constraints when needed

### Citation Management

1. **Regular Exports**: Export citations to BibTeX/RIS regularly
2. **Check Completeness**: Review citations for missing metadata
3. **Deduplicate**: The tool automatically deduplicates, but verify
4. **Verify Accuracy**: Always verify critical citation details

### Performance

1. **Batch Queries**: Use multiple queries in one call for efficiency
2. **Limit Results**: Scholar returns top 10 results by default
3. **Cache Results**: Consider caching for repeated queries
4. **Parallel Processing**: Multiple queries are processed in parallel (max 3 workers)

## Limitations

1. **API Dependency**: Requires Serper API access (paid service)
2. **Result Limit**: Returns top 10 results per query
3. **Metadata Accuracy**: Depends on Scholar's data quality
4. **Rate Limits**: Subject to Serper API rate limits
5. **PDF Access**: Not all papers have accessible PDFs
6. **Classification Accuracy**: Paper type/methodology identification is heuristic-based

## Future Enhancements

Potential improvements for future versions:

1. **Advanced Search Operators**: Support for Scholar-specific operators
2. **Author Profile Search**: Search by author ID or profile
3. **Citation Network**: Build citation graphs
4. **Full-Text Analysis**: Extract from PDFs when available
5. **Custom Classifiers**: ML-based paper type classification
6. **Venue Ranking**: Journal impact factor integration
7. **Temporal Analysis**: Citation trends over time
8. **Semantic Search**: Embedding-based similarity search

## Requirements Addressed

This enhanced Scholar tool addresses the following requirements:

- **Requirement 1.3**: Extract and preserve bibliographic metadata including authors, publication year, journal name, volume, issue, page numbers, and DOI
- **Requirement 14.1**: Optimized queries using academic search operators and field-specific terms
- **Requirement 14.2**: Extract citation counts, publication venues, and author information from Google Scholar results
- **Requirement 14.3**: Identify highly cited papers and seminal works in the field based on citation metrics

## Support

For issues or questions:
1. Check environment variables are set correctly
2. Verify Serper API key is valid and has credits
3. Review error messages for specific guidance
4. Consult the main Gazzali Research documentation

## Version History

- **v1.0.0** (2024): Initial enhanced Scholar tool with comprehensive metadata extraction
  - Structured JSON output
  - Citation tracking integration
  - Paper type classification
  - Methodology extraction
  - Open access identification
  - Summary statistics
