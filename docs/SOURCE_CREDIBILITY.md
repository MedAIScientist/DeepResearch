# Source Credibility Evaluation

## Overview

The Source Credibility Evaluation system in Gazzali Research provides automated assessment of source quality and reliability. It helps ensure that academic research is based on credible, peer-reviewed sources by scoring and filtering sources based on multiple quality indicators.

## Credibility Scoring System

### Base Scores by Source Type

Sources are assigned base scores (0-10) based on their type:

| Source Type | Base Score | Description |
|------------|------------|-------------|
| Peer-Reviewed Journal | 10 | Academic journals with peer review process |
| Conference Proceedings | 9 | Academic conference papers (peer-reviewed) |
| Academic Book | 9 | Books from academic publishers |
| Institutional Publication | 7 | Publications from universities, research institutions |
| Thesis/Dissertation | 7 | Graduate-level academic theses |
| Government Report | 7 | Official government publications and reports |
| Preprint | 6 | Pre-publication manuscripts (not yet peer-reviewed) |
| Professional Publication | 5 | Industry publications, professional magazines |
| General Web | 3 | General websites without academic affiliation |
| Unknown | 2 | Sources with insufficient metadata |

### Score Adjustments

The final credibility score is calculated by adjusting the base score with:

1. **Venue Reputation** (30% weight)
   - High-impact journals (Nature, Science, Cell, Lancet, NEJM): +10.0
   - Well-known publishers (IEEE, ACM, Springer, Elsevier): +8.0-9.0
   - Reputable academic publishers: +7.0-8.0
   - Unknown venues: +3.0-6.0

2. **Citation Count** (bonus up to +1.0)
   - 1000+ citations: +1.0
   - 500-999 citations: +0.8
   - 100-499 citations: +0.6
   - 50-99 citations: +0.4
   - 10-49 citations: +0.2

3. **Recency** (10% weight)
   - 0-2 years old: 10.0
   - 3-5 years old: 9.0
   - 6-10 years old: 7.0
   - 11-20 years old: 5.0
   - 20+ years old: 3.0

4. **Open Access** (bonus +0.2)
   - Freely available sources receive a small bonus

### Quality Levels

Final scores are categorized into quality levels:

- **Excellent** (9.0-10.0): Highest quality, highly trusted sources
- **High** (7.5-8.9): High-quality academic sources
- **Good** (6.0-7.4): Acceptable academic sources
- **Moderate** (4.0-5.9): Moderate quality, use with caution
- **Low** (2.0-3.9): Low quality, verify with other sources
- **Very Low** (0.0-1.9): Very low quality, avoid if possible

## Peer-Review Detection

The system automatically identifies peer-reviewed sources based on:

1. **Source Type**: Journals, conference proceedings, academic books
2. **Venue Indicators**: Keywords like "journal", "proceedings", "transactions"
3. **Publisher Recognition**: Known academic publishers (Springer, Elsevier, IEEE, ACM, etc.)
4. **Domain Analysis**: Academic domains (.edu, .ac.uk, etc.)

## Quality Warnings

The system generates warnings for:

- **Low Credibility Score**: Overall score below 4.0
- **Non-Academic Sources**: General web sources without peer review
- **Preprints**: Not yet peer-reviewed publications
- **Low Citation Count**: Fewer than 5 citations
- **Outdated Publications**: More than 20 years old
- **Missing Venue Information**: Unknown publication venue

## Source Strengths

The system identifies strengths such as:

- **Peer-Reviewed**: Publication underwent peer review
- **High-Impact Venue**: Published in prestigious journal/conference
- **Well-Cited**: Significant number of citations
- **Open Access**: Freely available to all researchers
- **Academic Publication**: From recognized academic source

## Usage

### Basic Evaluation

```python
from gazzali.source_credibility import SourceCredibilityEvaluator

# Initialize evaluator with quality threshold
evaluator = SourceCredibilityEvaluator(min_quality_threshold=7.0)

# Evaluate a source
credibility = evaluator.evaluate_source(
    title="Machine Learning in Healthcare",
    venue="Nature Medicine",
    url="https://nature.com/articles/...",
    venue_type="journal",
    citation_count=450,
    year=2022,
    is_open_access=True
)

# Check results
print(f"Score: {credibility.score}/10")
print(f"Quality: {credibility.overall_quality}")
print(f"Peer-reviewed: {credibility.is_peer_reviewed}")
print(f"Warnings: {credibility.warnings}")
print(f"Strengths: {credibility.strengths}")
```

### Filtering Sources

```python
# Filter sources by quality threshold
sources = [
    {"title": "Paper 1", "venue": "Nature", "url": "...", "year": 2023},
    {"title": "Paper 2", "venue": "Blog Post", "url": "...", "year": 2023},
]

filtered_sources = evaluator.filter_low_quality_sources(sources)
# Only high-quality sources remain
```

### Statistics and Reporting

```python
# Get quality statistics
stats = evaluator.get_statistics()
print(f"Total sources: {stats['total_sources']}")
print(f"Peer-reviewed: {stats['peer_reviewed_percentage']:.1f}%")
print(f"Average score: {stats['average_score']:.2f}/10")

# Log summary to console
evaluator.log_quality_summary()
```

## Integration with Research Workflow

### Scholar Tool Integration

The Scholar tool automatically evaluates source credibility for all search results:

```python
from gazzali.tools.tool_scholar import Scholar

scholar = Scholar()
results = scholar.call({"query": "climate change impacts"})

# Each result includes credibility assessment
# Results are automatically scored and filtered
```

### Academic Mode

When academic mode is enabled, source credibility evaluation is automatic:

```bash
# Enable academic mode with quality threshold
export SOURCE_QUALITY_THRESHOLD=7
python -m gazzali.gazzali --academic "research question"
```

### Quality Threshold Configuration

Configure the minimum quality threshold via environment variable:

```bash
# Strict threshold (only high-quality sources)
export SOURCE_QUALITY_THRESHOLD=8

# Moderate threshold (good and above)
export SOURCE_QUALITY_THRESHOLD=6

# Permissive threshold (moderate and above)
export SOURCE_QUALITY_THRESHOLD=4
```

## Logging and Monitoring

### Quality Warnings

Low-quality sources trigger warnings in the log:

```
WARNING: Source quality below threshold (3.5 < 7.0): Blog post about AI... (general_web)
```

### Summary Reports

At the end of research, a quality summary is logged:

```
============================================================
SOURCE QUALITY SUMMARY
============================================================
Total sources evaluated: 25
Peer-reviewed sources: 18 (72.0%)
Average quality score: 7.85/10
High-quality sources (≥7.0): 20
Low-quality sources (<4.0): 2

Source type distribution:
  - peer_reviewed_journal: 15
  - conference_proceedings: 3
  - preprint: 4
  - general_web: 3
============================================================
```

## Best Practices

### For Researchers

1. **Set Appropriate Thresholds**: Use higher thresholds (7-8) for critical research
2. **Review Warnings**: Pay attention to quality warnings for important claims
3. **Balance Quality and Coverage**: Lower thresholds may be needed for emerging topics
4. **Check Peer-Review Status**: Prioritize peer-reviewed sources for key findings

### For Academic Writing

1. **Cite High-Quality Sources**: Use sources with scores ≥7.0 for main arguments
2. **Verify Low-Quality Sources**: Cross-check information from sources <6.0
3. **Note Preprints**: Clearly indicate when citing preprints (not yet peer-reviewed)
4. **Track Statistics**: Monitor peer-reviewed percentage (target: >70%)

### For Literature Reviews

1. **Systematic Filtering**: Apply consistent quality thresholds across all searches
2. **Document Criteria**: Record quality thresholds used in methodology
3. **Report Statistics**: Include source quality statistics in review
4. **Justify Inclusions**: Explain why lower-quality sources were included (if any)

## Limitations

### Known Limitations

1. **Venue Recognition**: May not recognize all reputable journals/conferences
2. **Emerging Fields**: New journals may be underrated
3. **Language Bias**: Primarily recognizes English-language venues
4. **Preprint Assessment**: Preprints may contain high-quality work despite lower scores
5. **Citation Lag**: Recent publications may have low citation counts

### Mitigation Strategies

1. **Manual Review**: Always review sources manually for critical research
2. **Domain Expertise**: Use domain knowledge to assess unfamiliar venues
3. **Multiple Indicators**: Consider multiple quality indicators, not just score
4. **Context Matters**: Adjust thresholds based on research context and field
5. **Update Regularly**: System is updated with new venue patterns

## Technical Details

### Source Type Detection

The system uses multiple heuristics to identify source types:

1. **URL Pattern Matching**: Recognizes academic domains and publishers
2. **Venue Analysis**: Parses venue names for type indicators
3. **Metadata Inspection**: Uses venue_type field when available
4. **Keyword Detection**: Identifies keywords like "journal", "conference", "preprint"

### Venue Reputation Assessment

Reputation is assessed through:

1. **Pattern Matching**: Regex patterns for high-impact journals
2. **Publisher Database**: Known publishers with reputation scores
3. **Domain Analysis**: Academic and institutional domains
4. **Default Scores**: Conservative defaults for unknown venues

### Performance Considerations

- **Fast Evaluation**: Scoring is performed in milliseconds
- **Batch Processing**: Can evaluate hundreds of sources efficiently
- **Memory Efficient**: Stores only summary statistics, not full source data
- **Logging Control**: Configurable logging levels to reduce noise

## Future Enhancements

Planned improvements include:

1. **Impact Factor Integration**: Incorporate journal impact factors
2. **Field-Specific Scoring**: Adjust scores based on academic discipline
3. **Machine Learning**: Train models on expert assessments
4. **Citation Network Analysis**: Consider citation network quality
5. **Retraction Checking**: Flag retracted papers
6. **Predatory Journal Detection**: Identify predatory publishers
7. **Custom Venue Lists**: Allow users to add trusted venues

## References

This system implements best practices from:

- GRADE (Grading of Recommendations Assessment, Development and Evaluation)
- Evidence-Based Medicine hierarchies
- Academic publishing standards
- Information literacy frameworks

## Support

For questions or issues with source credibility evaluation:

1. Check the logs for detailed quality assessments
2. Review the statistics summary for overall quality metrics
3. Adjust quality thresholds based on your research needs
4. Report unrecognized high-quality venues for system updates
