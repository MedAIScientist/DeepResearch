# Scholar Tool and Citation Manager Integration

## Overview

The Scholar tool is fully integrated with the Citation Manager to provide automatic citation tracking and bibliography generation. This integration happens transparently during all Scholar searches, ensuring that every academic source consulted is properly tracked and can be cited in your research outputs.

## How It Works

### Automatic Citation Tracking

When you perform a Google Scholar search using the Scholar tool, the following happens automatically:

1. **Search Execution**: The Scholar tool queries Google Scholar via the Serper API
2. **Metadata Extraction**: For each result, comprehensive bibliographic metadata is extracted
3. **Citation Creation**: A Citation object is created with all available metadata
4. **Automatic Storage**: The citation is automatically added to the Citation Manager
5. **Deduplication**: The Citation Manager checks for duplicates and prevents double-counting

This entire process is transparent to the user - you simply search, and citations are tracked automatically.

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Scholar Tool                              │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  google_scholar_with_serp(query)                       │ │
│  │                                                         │ │
│  │  1. Query Serper API                                   │ │
│  │  2. For each result:                                   │ │
│  │     - Extract metadata (_extract_metadata)             │ │
│  │     - Create Citation (_create_citation_from_result)   │ │
│  │     - Add to Citation Manager                          │ │
│  └────────────────────────────────────────────────────────┘ │
│                           │                                  │
│                           ▼                                  │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Citation Manager (self.citation_manager)              │ │
│  │                                                         │ │
│  │  - Stores all citations                                │ │
│  │  - Deduplicates entries                                │ │
│  │  - Formats citations                                   │ │
│  │  - Generates bibliographies                            │ │
│  │  - Exports to BibTeX/RIS                               │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## Implementation Details

### Citation Creation Process

The Scholar tool's `_create_citation_from_result` method converts Scholar search results into Citation objects:

```python
def _create_citation_from_result(self, metadata: Dict[str, Any]) -> Optional[Citation]:
    """
    Create a Citation object from extracted metadata.
    
    Args:
        metadata: Structured metadata dictionary from Scholar result
    
    Returns:
        Citation object or None if creation fails
    """
    # Map venue type string to enum
    venue_type_map = {
        'journal': VenueType.JOURNAL,
        'conference': VenueType.CONFERENCE,
        'book': VenueType.BOOK,
        'preprint': VenueType.PREPRINT,
        'thesis': VenueType.THESIS,
        'other': VenueType.OTHER,
    }
    venue_type = venue_type_map.get(metadata['venue_type'], VenueType.OTHER)
    
    # Create citation using CitationManager
    citation = self.citation_manager.create_citation_from_metadata(
        title=metadata['title'],
        authors=metadata['authors'],
        year=metadata['year'],
        venue=metadata['venue'],
        url=metadata['url'],
        venue_type=venue_type,
        citation_count=metadata['citation_count'],
        abstract=metadata['abstract'],
        pdf_url=metadata['pdf_url'],
        is_open_access=metadata['is_open_access'],
    )
    
    return citation
```

### Metadata Captured

For each Scholar result, the following metadata is automatically captured and stored:

#### Bibliographic Data
- **Title**: Full paper title
- **Authors**: List of author names
- **Year**: Publication year
- **Venue**: Journal, conference, or publication venue name
- **Volume**: Volume number (for journals)
- **Issue**: Issue number (for journals)
- **Pages**: Page numbers or range

#### Identifiers
- **DOI**: Digital Object Identifier (when available)
- **URL**: Web link to the paper
- **PDF URL**: Direct link to PDF (when available)

#### Metrics
- **Citation Count**: Number of times the paper has been cited
- **Highly Cited Flag**: Automatically set for papers with 100+ citations

#### Content
- **Abstract**: Paper abstract or snippet
- **Keywords**: Extracted keywords (when available)

#### Classification
- **Venue Type**: Classified as journal, conference, book, preprint, thesis, or other
- **Paper Type**: Identified as empirical, review, theoretical, or unknown
- **Methodology**: Identified research methods (qualitative, quantitative, mixed-methods, etc.)

#### Access
- **Open Access Flag**: Indicates if the paper is freely accessible
- **Access Date**: Date the source was accessed

## Usage Examples

### Basic Usage

```python
from src.gazzali.tools.tool_scholar import Scholar

# Initialize Scholar tool (Citation Manager created automatically)
scholar = Scholar()

# Perform a search - citations tracked automatically
result = scholar.call({
    "query": "machine learning in healthcare"
})

# Access the citation manager
citation_manager = scholar.get_citation_manager()

# Check how many citations were tracked
print(f"Total citations: {len(citation_manager)}")
```

### Accessing Tracked Citations

```python
# Get statistics about tracked citations
stats = citation_manager.get_statistics()
print(f"Total citations: {stats['total_citations']}")
print(f"Open access papers: {stats['open_access_citations']}")
print(f"Citations with DOI: {stats['citations_with_doi']}")
print(f"Venue types: {stats['venue_type_counts']}")

# Iterate through all citations
for citation in citation_manager:
    print(f"{citation.title} ({citation.year})")
    print(f"  Authors: {', '.join(citation.authors[:3])}")
    print(f"  Citations: {citation.citation_count}")
    print()
```

### Generating Bibliography

```python
# Generate bibliography in APA style
apa_bibliography = citation_manager.generate_bibliography(
    CitationStyle.APA,
    sort_by_author=True
)
print(apa_bibliography)

# Generate in other styles
mla_bibliography = citation_manager.generate_bibliography(CitationStyle.MLA)
chicago_bibliography = citation_manager.generate_bibliography(CitationStyle.CHICAGO)
ieee_bibliography = citation_manager.generate_bibliography(CitationStyle.IEEE)
```

### Getting Inline Citations

```python
# Get a specific citation by ID
citation_id = "smith_2023_abc123"  # Example ID
citation = citation_manager.get_citation(citation_id)

if citation:
    # Get inline citation in different styles
    apa_inline = citation.get_inline_citation(CitationStyle.APA)
    # Returns: "(Smith, 2023)"
    
    mla_inline = citation.get_inline_citation(CitationStyle.MLA)
    # Returns: "(Smith)"
    
    # With page number
    apa_with_page = citation.get_inline_citation(CitationStyle.APA, page="42")
    # Returns: "(Smith, 2023, p. 42)"
```

### Exporting Citations

```python
# Export to BibTeX for reference managers (Zotero, Mendeley, etc.)
citation_manager.export_bibtex("my_research.bib")

# Export to RIS format
citation_manager.export_ris("my_research.ris")
```

### Complete Research Workflow

```python
from src.gazzali.tools.tool_scholar import Scholar
from src.gazzali.citation_manager import CitationStyle

# Initialize Scholar tool
scholar = Scholar()

# Perform multiple searches on related topics
scholar.call({"query": "deep learning medical imaging"})
scholar.call({"query": "convolutional neural networks radiology"})
scholar.call({"query": "AI diagnosis chest x-ray"})

# Access citation manager
cm = scholar.get_citation_manager()

# Review what was found
stats = cm.get_statistics()
print(f"\n=== Research Summary ===")
print(f"Total unique papers found: {stats['total_citations']}")
print(f"Open access papers: {stats['open_access_citations']}")
print(f"Papers with DOI: {stats['citations_with_doi']}")
print(f"\nVenue distribution:")
for venue_type, count in stats['venue_type_counts'].items():
    print(f"  {venue_type}: {count}")

# Generate formatted bibliography
print(f"\n=== Bibliography (APA Style) ===")
bibliography = cm.generate_bibliography(CitationStyle.APA, sort_by_author=True)
print(bibliography)

# Export for use in reference manager
cm.export_bibtex("literature_review.bib")
print(f"\nExported {stats['total_citations']} citations to literature_review.bib")
```

## Benefits

### 1. Zero Manual Entry
No need to manually copy and paste citation information. Every Scholar search automatically captures all bibliographic data.

### 2. Consistent Formatting
All citations are formatted consistently according to your chosen style (APA, MLA, Chicago, IEEE).

### 3. Automatic Deduplication
If you search for the same paper multiple times, it's only added once to your citation database.

### 4. Rich Metadata
Beyond basic citation info, you get citation counts, abstracts, methodology information, and more.

### 5. Easy Export
Export your entire bibliography to BibTeX or RIS format for use in reference managers like Zotero or Mendeley.

### 6. Inline Citation Support
Generate properly formatted inline citations for use in your writing.

### 7. Source Tracking
Complete record of all sources consulted during your research, even if you don't cite them all.

## Advanced Features

### Citation Statistics

Track your research progress with built-in statistics:

```python
stats = citation_manager.get_statistics()

# Available statistics:
# - total_citations: Total number of unique citations
# - incomplete_citations: Citations missing some metadata
# - citations_with_doi: Citations with DOI identifiers
# - open_access_citations: Freely accessible papers
# - venue_type_counts: Distribution by publication type
```

### Filtering Citations

```python
# Get only journal articles
journals = [c for c in citation_manager if c.venue_type == VenueType.JOURNAL]

# Get highly cited papers (100+ citations)
highly_cited = [c for c in citation_manager if c.citation_count and c.citation_count >= 100]

# Get open access papers
open_access = [c for c in citation_manager if c.is_open_access]

# Get recent papers (last 3 years)
from datetime import datetime
current_year = datetime.now().year
recent = [c for c in citation_manager if c.year and c.year >= current_year - 3]
```

### Custom Citation IDs

Citation IDs are automatically generated using a hash of the title, first author, and year. The format is:

```
{author_lastname}_{year}_{hash}
```

Example: `smith_2023_a1b2c3d4`

This ensures:
- Human-readable IDs
- Uniqueness across your citation database
- Consistency across multiple searches

## Integration with Research Workflow

### In Academic Research Agent

When using the academic research agent, the Scholar tool's Citation Manager is automatically used to track all sources:

```python
# The research agent uses Scholar tool internally
# All citations are automatically tracked
research_results = research_agent.run(
    question="What are the latest advances in AI for medical diagnosis?",
    academic_mode=True
)

# Access citations from the Scholar tool
scholar_tool = research_agent.get_tool("google_scholar")
citation_manager = scholar_tool.get_citation_manager()

# Generate bibliography for your research report
bibliography = citation_manager.generate_bibliography(CitationStyle.APA)
```

### In Report Generation

The Citation Manager integrates with the Academic Report Generator:

```python
from src.gazzali.report_generator import AcademicReportGenerator

# Create report generator with citation manager
report_generator = AcademicReportGenerator(
    config=academic_config,
    citation_manager=citation_manager  # Pass the Scholar tool's citation manager
)

# Generate report with automatic citations
report = report_generator.generate_report(
    question="Research question",
    research_results="Research findings...",
    api_key="your_api_key"
)

# Report includes properly formatted citations and bibliography
```

## Troubleshooting

### Citations Not Being Tracked

**Problem**: Citations don't appear in the Citation Manager after searches.

**Solutions**:
1. Verify Scholar tool has Citation Manager initialized:
   ```python
   assert scholar.citation_manager is not None
   ```

2. Check if search returned results:
   ```python
   result = scholar.call({"query": "your query"})
   # If result contains "No results found", no citations will be added
   ```

3. Verify Citation Manager is accessible:
   ```python
   cm = scholar.get_citation_manager()
   assert cm is not None
   ```

### Incomplete Citations

**Problem**: Some citations are marked as incomplete.

**Explanation**: Citations are marked incomplete when they're missing critical metadata (title, authors, or year).

**Solutions**:
1. Check which citations are incomplete:
   ```python
   incomplete = [c for c in citation_manager if c.is_incomplete]
   for citation in incomplete:
       print(f"Incomplete: {citation.title}")
       print(f"  Has authors: {bool(citation.authors)}")
       print(f"  Has year: {bool(citation.year)}")
   ```

2. Manually complete citations if needed:
   ```python
   citation = citation_manager.get_citation(citation_id)
   if citation.is_incomplete:
       # Update missing fields
       citation.year = 2023
       citation.authors = ["Smith, John"]
       citation.is_incomplete = False
   ```

### Duplicate Citations

**Problem**: Same paper appears multiple times.

**Explanation**: The Citation Manager uses title and authors for deduplication. Slight variations in these fields can cause duplicates.

**Solution**: The Citation Manager automatically handles most duplicates. For edge cases:
```python
# Manually check for potential duplicates
from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio() > 0.9

citations = list(citation_manager)
for i, c1 in enumerate(citations):
    for c2 in citations[i+1:]:
        if similar(c1.title, c2.title):
            print(f"Potential duplicate:")
            print(f"  1: {c1.title} ({c1.citation_id})")
            print(f"  2: {c2.title} ({c2.citation_id})")
```

## Requirements Addressed

This integration addresses the following requirements from the Gazzali Research specification:

- **Requirement 1.3**: Extract and preserve bibliographic metadata including authors, publication year, journal name, volume, issue, page numbers, and DOI
- **Requirement 2.1**: Automatically capture citation information for every source consulted during research
- **Requirement 2.2**: Format citations according to configurable academic styles (APA, MLA, Chicago, IEEE)
- **Requirement 2.3**: Generate comprehensive bibliography section with all cited sources
- **Requirement 2.5**: Detect and flag duplicate citations to maintain bibliography consistency
- **Requirement 14.2**: Extract citation counts, publication venues, and author information from Google Scholar results

## Testing

Comprehensive tests for the Scholar-Citation Manager integration are available in:

```
tests/test_scholar_citation_integration.py
```

Run tests with:

```bash
python -m pytest tests/test_scholar_citation_integration.py -v
```

Test coverage includes:
- Citation creation from Scholar results
- Automatic addition to Citation Manager
- Metadata extraction accuracy
- Deduplication logic
- Bibliography generation
- Export functionality
- Inline citation generation
- Statistics tracking

## Related Documentation

- [Scholar Tool Documentation](SCHOLAR_TOOL.md) - Complete Scholar tool features
- [Citation Manager Documentation](CITATION_MANAGER.md) - Citation formatting and management
- [Academic Configuration](ACADEMIC_CONFIG.md) - Configuring academic mode
- [Academic Prompts](ACADEMIC_PROMPTS.md) - Academic-specific prompts

## Future Enhancements

Potential improvements to the integration:

1. **Citation Network Analysis**: Visualize citation relationships between tracked papers
2. **Impact Metrics**: Track h-index, impact factor, and other metrics
3. **Automatic Updates**: Periodically update citation counts for tracked papers
4. **Smart Recommendations**: Suggest related papers based on citation patterns
5. **Collaborative Features**: Share citation databases across research teams
6. **Version Control**: Track changes to citations over time
7. **Quality Scoring**: Automatically assess source quality and credibility
8. **Annotation Support**: Add notes and tags to citations

## Support

For issues or questions about the Scholar-Citation Manager integration:

1. Check this documentation for common solutions
2. Review the [Scholar Tool Documentation](SCHOLAR_TOOL.md)
3. Examine the [Citation Manager Documentation](CITATION_MANAGER.md)
4. Run the integration tests to verify functionality
5. Check the main README for general setup and configuration

## Summary

The Scholar-Citation Manager integration provides seamless, automatic citation tracking for all academic research conducted through the Scholar tool. This integration ensures that:

- Every source is properly tracked
- Citations are consistently formatted
- Bibliographies are automatically generated
- Export to reference managers is simple
- Research workflow is streamlined

No manual citation entry is required - just search, and let the integration handle the rest.
