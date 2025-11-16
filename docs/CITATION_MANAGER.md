# Citation Manager Documentation

## Overview

The Citation Manager module (`src/gazzali/citation_manager.py`) provides comprehensive citation tracking, formatting, and bibliography generation for Gazzali Research. It supports multiple academic citation styles and handles automatic deduplication of sources.

## Features

- **Multi-Style Citation Formatting**: Supports APA 7th, MLA 9th, Chicago 17th, and IEEE citation styles
- **Automatic Deduplication**: Prevents duplicate citations based on title and author matching
- **Bibliography Generation**: Creates formatted bibliographies sorted by author
- **Export Capabilities**: Export citations to BibTeX and RIS formats
- **Citation Extraction**: Extract citation metadata from Google Scholar results and web pages
- **Inline Citations**: Generate in-text citations in various formats

## Requirements Addressed

- **Requirement 2.1**: Automatic citation capture for all sources consulted
- **Requirement 2.2**: Citation formatting in multiple academic styles (APA, MLA, Chicago, IEEE)
- **Requirement 2.5**: Citation deduplication and tracking

## Core Classes

### Citation

Represents a single academic citation with complete bibliographic metadata.

**Key Attributes:**
- `citation_id`: Unique identifier (auto-generated)
- `authors`: List of author names
- `year`: Publication year
- `title`: Publication title
- `venue`: Publication venue (journal, conference, book)
- `venue_type`: Type of venue (journal, conference, book, preprint, thesis, web)
- `doi`: Digital Object Identifier
- `url`: Web URL
- `citation_count`: Number of citations (from Scholar)
- `is_incomplete`: Flag for citations with missing metadata

**Key Methods:**
- `format(style)`: Format citation in specified style (APA, MLA, Chicago, IEEE)
- `get_inline_citation(style, page)`: Generate inline citation for text
- `to_bibtex()`: Export as BibTeX entry
- `to_ris()`: Export as RIS entry

### CitationManager

Manages a collection of citations with tracking and formatting capabilities.

**Key Methods:**
- `add_citation(citation)`: Add citation with automatic deduplication
- `get_citation(citation_id)`: Retrieve citation by ID
- `generate_bibliography(style, sort_by_author)`: Generate formatted bibliography
- `export_bibtex(filepath)`: Export all citations to .bib file
- `export_ris(filepath)`: Export all citations to .ris file
- `create_citation_from_metadata(...)`: Create Citation from metadata
- `extract_from_scholar_result(result)`: Extract citation from Scholar result
- `extract_from_webpage(content, url)`: Extract citation from webpage
- `get_statistics()`: Get collection statistics

## Usage Examples

### Creating Citations

```python
from gazzali.citation_manager import CitationManager, Citation, VenueType

# Initialize manager
manager = CitationManager()

# Create citation from metadata
citation = manager.create_citation_from_metadata(
    title="Deep Learning for Natural Language Processing",
    authors=["Smith, John", "Doe, Jane"],
    year=2023,
    venue="Journal of AI Research",
    venue_type=VenueType.JOURNAL,
    volume="45",
    issue="3",
    pages="123-145",
    doi="10.1234/jair.2023.45.3.123"
)

# Add to manager
citation_id = manager.add_citation(citation)
```

### Formatting Citations

```python
from gazzali.citation_manager import CitationStyle

# Format in different styles
apa_format = citation.format(CitationStyle.APA)
# Output: Smith, J., & Doe, J. (2023). Deep Learning for Natural Language Processing. 
#         Journal of AI Research, 45(3), 123-145. https://doi.org/10.1234/jair.2023.45.3.123

mla_format = citation.format(CitationStyle.MLA)
# Output: Smith, John, and Jane Doe. "Deep Learning for Natural Language Processing." 
#         Journal of AI Research, vol. 45, no. 3, 2023, pp. 123-145.

# Generate inline citation
inline = citation.get_inline_citation(CitationStyle.APA)
# Output: (Smith & Doe, 2023)

inline_with_page = citation.get_inline_citation(CitationStyle.APA, page="125")
# Output: (Smith & Doe, 2023, p. 125)
```

### Generating Bibliography

```python
# Add multiple citations
manager.add_citation(citation1)
manager.add_citation(citation2)
manager.add_citation(citation3)

# Generate bibliography in APA style
bibliography = manager.generate_bibliography(CitationStyle.APA, sort_by_author=True)
print(bibliography)
```

### Extracting from Scholar Results

```python
# Scholar result dictionary
scholar_result = {
    'title': 'Attention Is All You Need',
    'authors': 'Vaswani, Ashish, Shazeer, Noam, Parmar, Niki',
    'year': 2017,
    'venue': 'Advances in Neural Information Processing Systems',
    'citation_count': 50000,
    'url': 'https://arxiv.org/abs/1706.03762',
    'abstract': 'The dominant sequence transduction models...'
}

# Extract citation
citation = manager.extract_from_scholar_result(scholar_result)
if citation:
    citation_id = manager.add_citation(citation)
```

### Extracting from Web Pages

```python
# Extract citation from HTML content
html_content = """
<html>
<head>
    <meta name="citation_title" content="Machine Learning Basics">
    <meta name="citation_author" content="Johnson, Alice">
    <meta name="citation_author" content="Smith, Bob">
    <meta name="citation_publication_date" content="2023">
    <meta name="citation_journal_title" content="AI Review">
    <meta name="DC.Identifier" content="doi:10.1234/air.2023.123">
</head>
</html>
"""

citation = manager.extract_from_webpage(html_content, "https://example.com/article")
if citation:
    citation_id = manager.add_citation(citation)
```

### Extracting from Plain Text

```python
# Extract citation from unstructured text (fallback method)
text = """
"Deep Learning Applications in Healthcare"
by Anderson, Michael, Williams, Sarah
Published in Medical AI Journal (2022)
doi:10.5678/maj.2022.456
"""

citation = manager.extract_from_text(text, url="https://example.com")
if citation:
    citation_id = manager.add_citation(citation)
```

### Exporting Citations

```python
# Export to BibTeX
manager.export_bibtex('outputs/references.bib')

# Export to RIS
manager.export_ris('outputs/references.ris')
```

### Getting Statistics

```python
stats = manager.get_statistics()
print(f"Total citations: {stats['total_citations']}")
print(f"Incomplete citations: {stats['incomplete_citations']}")
print(f"Citations with DOI: {stats['citations_with_doi']}")
print(f"Open access: {stats['open_access_citations']}")
print(f"By venue type: {stats['venue_type_counts']}")
```

## Citation Styles

### APA 7th Edition

**Format**: Author, A. A., & Author, B. B. (Year). Title of work. *Journal Name*, *volume*(issue), pages. https://doi.org/xxx

**Inline**: (Author, Year) or (Author, Year, p. X)

**Features**:
- Up to 20 authors listed, then ellipsis
- Ampersand (&) before last author
- Sentence case for titles
- DOI preferred over URL

### MLA 9th Edition

**Format**: Author, First. "Title of Work." *Journal Name*, vol. X, no. Y, Year, pp. X-Y.

**Inline**: (Author Page) or (Author)

**Features**:
- First author inverted, et al. for 3+ authors
- Title in quotes for articles
- Access date included for web sources

### Chicago 17th Edition

**Format**: Author, First. Year. "Title of Work." *Journal Name* volume, no. issue: pages. https://doi.org/xxx

**Inline**: (Author, Year) or (Author Year, page)

**Features**:
- Author-date system
- Up to 3 authors listed, then et al.
- Flexible formatting for different source types

### IEEE

**Format**: F. M. Author, "Title of work," *Journal Name*, vol. X, no. Y, pp. X-Y, Year. doi: xxx

**Inline**: [Number]

**Features**:
- Numbered references
- Initials before surname
- Up to 6 authors, then et al.
- Abbreviated journal names

## Deduplication Logic

The Citation Manager automatically detects and prevents duplicate citations:

1. **Title Matching**: Normalizes titles (lowercase, stripped) for comparison
2. **Author Matching**: Compares author sets for exact matches
3. **Return Existing**: If duplicate found, returns existing citation_id

This ensures bibliography consistency and prevents redundant entries.

## Citation ID Generation

Citation IDs are automatically generated using:
- First author's last name (up to 10 characters)
- Publication year
- MD5 hash of title + first author + year (8 characters)

**Format**: `{author}_{year}_{hash}`

**Example**: `smith_2023_a1b2c3d4`

This creates human-readable yet unique identifiers.

## Citation Extraction

The Citation Manager provides three extraction methods for different source types:

### 1. Scholar Result Extraction (`extract_from_scholar_result`)

Extracts citation metadata from Google Scholar search results.

**Expected Input Format**:
```python
{
    'title': str,
    'authors': str (comma-separated) or list,
    'year': str or int,
    'venue': str,
    'citation_count': int (optional),
    'url': str,
    'abstract': str (optional),
    'doi': str (optional),
    'pdf_url': str (optional)
}
```

**Features**:
- Parses comma-separated author strings
- Detects venue type (journal, conference, preprint)
- Extracts citation counts and abstracts
- Handles missing fields gracefully

### 2. Webpage Extraction (`extract_from_webpage`)

Extracts citation metadata from HTML content using meta tags and heuristics.

**Extraction Strategies**:
- **Title**: Checks citation_title, DC.Title, og:title, twitter:title, <title>, <h1>
- **Authors**: Checks citation_author (multiple), DC.Creator, author meta tags
- **Year**: Checks citation_publication_date, citation_year, DC.Date, article:published_time
- **DOI**: Checks citation_doi, DC.Identifier, doi: patterns in content

**Supported Meta Tag Standards**:
- Citation meta tags (used by academic publishers)
- Dublin Core (DC.*) meta tags
- Open Graph (og:*) meta tags
- Twitter Card meta tags

### 3. Plain Text Extraction (`extract_from_text`)

Fallback method for extracting citations from unstructured text using regex patterns.

**Extraction Patterns**:
- **Title**: Quoted text, "Title:" prefix, first substantial line
- **Authors**: "Last, First" format, "by Author" patterns
- **Year**: Years in parentheses, after "published/year/date:", 4-digit years
- **DOI**: Standard DOI patterns (10.xxxx/...)

**Use Cases**:
- Parsing citation strings
- Extracting from plain text documents
- Fallback when HTML parsing fails

### Extraction Error Handling

All extraction methods:
- Return `None` if extraction fails completely
- Create incomplete citations if some metadata is missing
- Log errors without crashing
- Preserve URL even if other fields are missing

## Incomplete Citations

Citations are flagged as incomplete when missing critical metadata:
- No title
- No authors
- No year

Incomplete citations are:
- Marked with `is_incomplete = True`
- Appended with `[Incomplete citation]` in formatted output
- Still tracked and included in bibliography
- Counted in statistics for quality monitoring

## Integration with Research Workflow

The Citation Manager integrates with:

1. **Scholar Tool**: Automatically extracts citations from Google Scholar results
2. **Visit Tool**: Extracts citations from visited web pages
3. **Research Agent**: Tracks all sources consulted during research
4. **Report Generator**: Formats citations and generates bibliography for reports

## Best Practices

1. **Always Use Manager**: Create citations through CitationManager for automatic ID generation
2. **Check for Duplicates**: Manager handles this automatically, but be aware
3. **Provide Complete Metadata**: Include DOI, volume, issue, pages when available
4. **Use Appropriate Venue Type**: Helps with correct formatting
5. **Export Regularly**: Save bibliography to external formats for backup

## Future Enhancements

Potential future additions:
- Direct integration with Zotero/Mendeley
- PDF metadata extraction
- Citation network visualization
- More citation styles (Vancouver, Harvard, etc.)
- Citation quality scoring
- Automatic DOI lookup

## Error Handling

The module handles errors gracefully:
- Invalid metadata returns None or incomplete citation
- Missing fields use defaults or empty strings
- Extraction failures are logged but don't crash
- Invalid citation IDs return error messages

## Performance Considerations

- **Deduplication**: O(n) check against existing citations
- **Sorting**: O(n log n) for bibliography generation
- **Memory**: Stores all citations in memory (consider persistence for large collections)
- **Export**: Writes to disk, may be slow for thousands of citations

## Testing

See `tests/test_citation_manager.py` for comprehensive unit tests covering:
- Citation formatting in all styles
- Bibliography generation
- Deduplication logic
- Export formats
- Extraction methods
- Edge cases and error handling
