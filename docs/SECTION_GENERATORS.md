# Section Generators Documentation

## Overview

The Academic Report Generator includes specialized section generator methods that handle the creation, extraction, and formatting of specific sections in academic reports. These methods ensure that reports meet academic standards and include all required components.

## Section Generator Methods

### 1. `_generate_abstract(content, max_words=250)`

**Purpose**: Generate or extract a concise abstract from report content.

**Functionality**:
- Extracts existing abstract if present in content
- Generates abstract from key sections (Introduction, Findings, Conclusion) if not present
- Ensures abstract stays within word count limits (default: 250 words)
- Provides structured summary of research question, methodology, findings, and implications

**Requirements Addressed**:
- 5.2: Structure reports with required sections including abstract

**Usage**:
```python
abstract = generator._generate_abstract(report_content, max_words=250)
```

**Output Format**:
- Concise summary (150-250 words)
- Includes key findings and implications
- Uses formal academic language
- Truncated with ellipsis if exceeds max_words

---

### 2. `_structure_literature_review(content)`

**Purpose**: Structure and organize literature review sections with proper academic organization.

**Functionality**:
- Validates existing structure (checks for subsections)
- Identifies thematic categories and research streams
- Ensures proper organization (thematic or chronological)
- Enhances transitions between sections
- Preserves well-structured content

**Requirements Addressed**:
- 3.2: Organize literature into thematic categories
- 3.3: Identify consensus and controversial areas

**Key Features**:
- Detects thematic indicators (theoretical frameworks, methodologies, findings, gaps)
- Identifies consensus and controversial areas
- Maintains chronological evolution of research
- Adds appropriate academic transitions

**Usage**:
```python
structured_review = generator._structure_literature_review(raw_content)
```

**Thematic Indicators Detected**:
- Theoretical frameworks and approaches
- Methodological approaches
- Empirical findings and evidence
- Research gaps and future directions
- Consensus and agreement areas
- Controversies and debates

---

### 3. `_extract_methodology_section(content)`

**Purpose**: Extract and validate methodology sections to ensure completeness.

**Functionality**:
- Validates presence of key methodological components
- Checks for research design description
- Verifies data collection methods are documented
- Ensures analysis techniques are described
- Identifies limitations and constraints

**Requirements Addressed**:
- 4.1: Extract and document research methodologies
- 4.4: Compare and contrast methodological approaches

**Key Components Validated**:
1. **Research Design**: Qualitative, quantitative, or mixed-methods approach
2. **Data Collection**: Sampling, surveys, interviews, observations, experiments
3. **Analysis Techniques**: Statistical tests, thematic coding, analytical methods
4. **Limitations**: Constraints, weaknesses, caveats

**Usage**:
```python
methodology = generator._extract_methodology_section(raw_methodology)
```

**Validation Keywords**:
- Design: "research design", "study design", "qualitative", "quantitative", "mixed-methods"
- Collection: "data collection", "sampling", "survey", "interview", "observation", "experiment"
- Analysis: "analysis", "statistical", "thematic", "coding", "regression", "ANOVA"
- Limitations: "limitation", "constraint", "weakness", "caveat"

---

### 4. `_format_citations(content)`

**Purpose**: Format citations and bibliography according to configured citation style.

**Functionality**:
- Identifies citation references in content
- Detects existing bibliography format
- Reformats citations to match configured style
- Generates bibliography from citation manager
- Handles various citation formats (inline, numbered, author-year)

**Requirements Addressed**:
- 2.2: Format citations in specified style
- 2.3: Generate bibliography sorted by author
- 2.4: Use inline citations in appropriate format

**Supported Citation Styles**:
- **APA 7th Edition**: (Author, Year) inline, hanging indent bibliography
- **MLA 9th Edition**: (Author Page) inline, works cited format
- **Chicago 17th**: Footnote or (Author Year) with full bibliography
- **IEEE**: [Number] inline, numbered references

**Usage**:
```python
formatted_bib = generator._format_citations(bibliography_content)
```

**Detection Patterns**:
- Numbered references: `[1]`, `[2]`, etc.
- Author-year: `(2023)`, `(Smith, 2023)`
- Author patterns: "et al.", " & ", ", and "
- Full citations: "Author. (Year). Title..."

---

### 5. `_generate_bibliography()`

**Purpose**: Generate complete formatted bibliography from citation manager.

**Functionality**:
- Retrieves all citations from citation manager
- Sorts citations alphabetically by author surname
- Formats each citation according to configured style
- Handles duplicate detection
- Assembles complete bibliography section

**Requirements Addressed**:
- 2.3: Generate bibliography sorted by author surname
- 2.4: Format in specified citation style
- 2.5: Detect and handle duplicate citations

**Process**:
1. Check citation manager for available citations
2. Sort citations by author surname (alphabetically)
3. Format each citation in configured style
4. Remove duplicates
5. Assemble final bibliography

**Usage**:
```python
bibliography = generator._generate_bibliography()
```

**Output Format**:
```
Author, A. A., & Author, B. B. (Year). Title of work. Journal Name, Volume(Issue), pages. DOI

Author, C. C. (Year). Book title. Publisher.

[Additional citations sorted alphabetically...]
```

---

## Helper Methods

### `_enhance_transitions(content)`

**Purpose**: Enhance transitions between paragraphs and sections.

**Functionality**:
- Improves flow between sections
- Adds appropriate academic transition phrases
- Maintains coherence throughout document

**Usage**:
```python
enhanced = generator._enhance_transitions(content)
```

---

### `_reformat_bibliography(content)`

**Purpose**: Reformat existing bibliography to match configured style.

**Functionality**:
- Parses existing bibliography
- Reformats to match configured citation style
- Falls back to citation manager if available

**Usage**:
```python
reformatted = generator._reformat_bibliography(existing_bib)
```

---

## Integration with Report Generation

These section generators are integrated into the main report generation workflow:

```python
# Generate report
report = generator.generate_report(
    question="Research question",
    research_results="Research findings",
    api_key="api-key"
)

# Section generators are called internally:
# 1. _parse_sections() - Extract sections from generated content
# 2. _generate_abstract() - Create/extract abstract
# 3. _structure_literature_review() - Organize literature review
# 4. _extract_methodology_section() - Validate methodology
# 5. _format_citations() - Format bibliography
# 6. _generate_bibliography() - Generate final bibliography
```

---

## Best Practices

### For Abstract Generation
- Keep abstracts between 150-250 words
- Include research question, methodology, key findings, and implications
- Use formal, objective language
- Avoid citations in abstracts (unless absolutely necessary)

### For Literature Review Structuring
- Organize thematically or chronologically
- Clearly identify research streams and frameworks
- Highlight consensus and controversial areas
- Explicitly state research gaps
- Use appropriate transitions between themes

### For Methodology Sections
- Include all four key components: design, collection, analysis, limitations
- Be specific about methods and techniques
- Justify methodological choices
- Acknowledge constraints and limitations

### For Citation Formatting
- Maintain consistency throughout document
- Use configured citation style consistently
- Ensure all in-text citations appear in bibliography
- Sort bibliography alphabetically by author surname
- Include all required bibliographic information (DOI, URL, etc.)

---

## Error Handling

### Missing Citations
If citation manager is empty:
```python
bibliography = generator._generate_bibliography()
# Returns: "No citations available."
```

### Incomplete Content
If section content is missing or empty:
```python
abstract = generator._generate_abstract("")
# Returns: "Abstract not available."
```

### Malformed Bibliography
If bibliography cannot be parsed:
```python
formatted = generator._format_citations(malformed_content)
# Falls back to citation manager or returns content as-is
```

---

## Examples

### Example 1: Generate Abstract from Full Report

```python
from gazzali.report_generator import AcademicReportGenerator
from gazzali.academic_config import AcademicConfig
from gazzali.citation_manager import CitationManager

config = AcademicConfig(citation_style="apa", output_format="paper")
citation_mgr = CitationManager()
generator = AcademicReportGenerator(config, citation_mgr)

# Full report content
report_content = """
## Introduction
This study examines the effects of climate change on coastal ecosystems...

## Findings
The analysis revealed significant impacts on biodiversity...

## Conclusion
These findings suggest urgent need for conservation efforts...
"""

# Generate abstract
abstract = generator._generate_abstract(report_content, max_words=200)
print(abstract)
```

### Example 2: Structure Literature Review

```python
# Raw literature review content
raw_review = """
Previous research has examined climate impacts extensively.
Smith (2020) found significant temperature increases.
Jones (2021) reported biodiversity losses.
However, Brown (2022) suggested adaptation mechanisms exist.
"""

# Structure the review
structured = generator._structure_literature_review(raw_review)
print(structured)
```

### Example 3: Generate Bibliography

```python
# Add citations to manager
citation_mgr.add_citation(Citation(
    authors=["Smith, J.", "Doe, A."],
    year=2023,
    title="Climate Change Impacts",
    venue="Nature",
    doi="10.1234/nature.2023"
))

# Generate bibliography
bibliography = generator._generate_bibliography()
print(bibliography)
# Output: Smith, J., & Doe, A. (2023). Climate Change Impacts. Nature. https://doi.org/10.1234/nature.2023
```

---

## Future Enhancements

Potential improvements for section generators:

1. **AI-Powered Abstract Generation**: Use LLM to generate abstracts from full reports
2. **Advanced Literature Review Structuring**: Automatic thematic clustering and organization
3. **Methodology Validation**: Check for completeness and suggest improvements
4. **Citation Network Analysis**: Identify highly cited works and citation patterns
5. **Multi-Language Support**: Generate sections in multiple languages
6. **Template-Based Generation**: Use discipline-specific templates for sections

---

## Related Documentation

- [Academic Configuration](ACADEMIC_CONFIG.md) - Configuration options for academic mode
- [Citation Manager](CITATION_MANAGER.md) - Citation tracking and formatting
- [Academic Prompts](ACADEMIC_PROMPTS.md) - Prompts for academic content generation
- [Report Generation Pipeline](REPORTING_PIPELINE.md) - Complete report generation workflow

---

## Support

For issues or questions about section generators:
1. Check the [FAQ](../FAQ.md)
2. Review the [Design Document](../.kiro/specs/academic-research-assistant/design.md)
3. Consult the [Requirements Document](../.kiro/specs/academic-research-assistant/requirements.md)
