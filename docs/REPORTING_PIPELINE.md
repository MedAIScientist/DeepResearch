# Academic Report Generator - Data Models Documentation

## Overview

The Academic Report Generator module (`src/gazzali/report_generator.py`) provides data models and utilities for creating structured academic reports with proper formatting, citations, and section organization. This module is the foundation for generating publication-quality academic documents.

## Core Data Models

### ResearchMetadata

The `ResearchMetadata` dataclass captures information about the research process and sources consulted.

#### Attributes

- **question** (str): Original research question
- **refined_question** (Optional[str]): Refined version of the question (if applicable)
- **discipline** (str): Academic discipline (e.g., "stem", "social", "humanities")
- **search_strategy** (str): Description of search approach used
- **sources_consulted** (int): Total number of sources examined
- **peer_reviewed_sources** (int): Number of peer-reviewed sources
- **date_range** (tuple[str, str]): Coverage period as (start_date, end_date)
- **key_authors** (List[str]): Prominent authors in the field
- **key_theories** (List[str]): Theoretical frameworks identified
- **methodologies_found** (List[str]): Research methodologies encountered
- **generated_at** (datetime): Timestamp of report generation

#### Methods

```python
# Convert to dictionary
metadata_dict = metadata.to_dict()

# Calculate peer-reviewed percentage
percentage = metadata.get_peer_reviewed_percentage()
```

#### Example Usage

```python
from src.gazzali.report_generator import ResearchMetadata

metadata = ResearchMetadata(
    question="What are the effects of climate change on coral reefs?",
    refined_question="How does ocean acidification impact coral reef biodiversity in tropical regions?",
    discipline="stem",
    search_strategy="Scholar-first search with focus on peer-reviewed journals",
    sources_consulted=45,
    peer_reviewed_sources=38,
    date_range=("2015", "2024"),
    key_authors=["Hughes, T.P.", "Hoegh-Guldberg, O.", "Pandolfi, J.M."],
    key_theories=["Ocean acidification theory", "Coral bleaching mechanisms"],
    methodologies_found=["Field studies", "Laboratory experiments", "Meta-analysis"]
)

print(f"Peer-reviewed: {metadata.get_peer_reviewed_percentage():.1f}%")
```

### AcademicReport

The `AcademicReport` dataclass represents a complete academic report with all sections, citations, and metadata.

#### Attributes

- **title** (str): Report title
- **abstract** (str): Abstract text (if included)
- **keywords** (List[str]): Keywords for the report
- **sections** (OrderedDict[str, str]): Section name → content mapping
- **bibliography** (str): Formatted bibliography/references section
- **metadata** (Optional[ResearchMetadata]): Research metadata
- **citation_style** (CitationStyle): Citation style used (APA, MLA, Chicago, IEEE)
- **output_format** (OutputFormat): Output format type (paper, review, proposal, etc.)
- **word_count** (int): Total word count
- **generated_at** (datetime): Generation timestamp

#### Methods

##### Output Generation

```python
# Convert to Markdown
markdown_text = report.to_markdown()

# Convert to LaTeX
latex_text = report.to_latex()

# Save to file
report.save("output.md", format="markdown")
report.save("output.tex", format="latex")
```

##### Section Management

```python
# Get section content
intro = report.get_section("Introduction")

# Add or update section
report.add_section("Methodology", "This study employed...", position=2)

# Remove section
report.remove_section("Limitations")

# Get all section names
section_names = report.get_section_names()
```

##### Utilities

```python
# Calculate word count
total_words = report.calculate_word_count()

# Convert to dictionary
report_dict = report.to_dict()

# String representation
print(report)
```

#### Example Usage

```python
from collections import OrderedDict
from src.gazzali.report_generator import AcademicReport, ResearchMetadata
from src.gazzali.academic_config import CitationStyle, OutputFormat

# Create metadata
metadata = ResearchMetadata(
    question="What are the impacts of remote work on productivity?",
    discipline="social",
    sources_consulted=32,
    peer_reviewed_sources=28
)

# Create report
report = AcademicReport(
    title="The Impact of Remote Work on Employee Productivity: A Systematic Review",
    abstract="This systematic review examines...",
    keywords=["remote work", "productivity", "work-from-home", "organizational behavior"],
    citation_style=CitationStyle.APA,
    output_format=OutputFormat.REVIEW,
    metadata=metadata
)

# Add sections
report.add_section("Introduction", "The COVID-19 pandemic accelerated...")
report.add_section("Thematic Analysis", "Three major themes emerged...")
report.add_section("Research Gaps", "Despite extensive research...")
report.add_section("Future Directions", "Future research should focus on...")

# Set bibliography
report.bibliography = "Smith, J. (2023). Remote work trends..."

# Calculate word count
report.calculate_word_count()

# Save report
report.save("remote_work_review.md", format="markdown")
```

## Standard Section Constants

The module provides constants for standard academic section names:

```python
SECTION_ABSTRACT = "Abstract"
SECTION_INTRODUCTION = "Introduction"
SECTION_LITERATURE_REVIEW = "Literature Review"
SECTION_METHODOLOGY = "Methodology"
SECTION_FINDINGS = "Findings"
SECTION_DISCUSSION = "Discussion"
SECTION_IMPLICATIONS = "Implications"
SECTION_LIMITATIONS = "Limitations"
SECTION_CONCLUSION = "Conclusion"
SECTION_REFERENCES = "References"
SECTION_BACKGROUND = "Background"
SECTION_RESEARCH_QUESTIONS = "Research Questions"
SECTION_THEMATIC_ANALYSIS = "Thematic Analysis"
SECTION_RESEARCH_GAPS = "Research Gaps"
SECTION_FUTURE_DIRECTIONS = "Future Directions"
SECTION_PROPOSED_METHODOLOGY = "Proposed Methodology"
SECTION_EXPECTED_OUTCOMES = "Expected Outcomes"
SECTION_TIMELINE = "Timeline"
```

Use these constants to ensure consistent section naming:

```python
from src.gazzali.report_generator import SECTION_INTRODUCTION, SECTION_METHODOLOGY

report.add_section(SECTION_INTRODUCTION, "...")
report.add_section(SECTION_METHODOLOGY, "...")
```

## Helper Functions

### create_empty_report()

Creates an empty academic report with proper structure based on configuration.

```python
from src.gazzali.report_generator import create_empty_report
from src.gazzali.academic_config import AcademicConfig, OutputFormat

# Create configuration
config = AcademicConfig(
    output_format=OutputFormat.PAPER,
    citation_style=CitationStyle.APA,
    include_abstract=True,
    include_methodology=True
)

# Create empty report
report = create_empty_report(
    title="My Research Paper",
    config=config,
    metadata=metadata
)

# Report now has empty sections based on output format
print(report.get_section_names())
# Output: ['Introduction', 'Literature Review', 'Methodology', 'Findings', 'Discussion', 'Conclusion']
```

## Output Formats

### Markdown Format

The `to_markdown()` method generates a clean Markdown document:

```markdown
# Report Title

---
**Generated**: 2024-01-15 14:30:00
**Citation Style**: APA
**Word Count**: 5432
**Keywords**: keyword1, keyword2, keyword3
---

## Abstract

Abstract text here...

## Introduction

Introduction text here...

## References

Bibliography here...
```

### LaTeX Format

The `to_latex()` method generates a basic LaTeX document:

```latex
\documentclass[12pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage{graphicx}
\usepackage{hyperref}
\usepackage{cite}

\title{Report Title}
\date{January 15, 2024}

\begin{document}
\maketitle

\begin{abstract}
Abstract text here...
\end{abstract}

\noindent\textbf{Keywords:} keyword1, keyword2, keyword3

\section{Introduction}
Introduction text here...

\section{References}
Bibliography here...

\end{document}
```

## Integration with Other Modules

### With AcademicConfig

The report structure is determined by the `AcademicConfig`:

```python
from src.gazzali.academic_config import AcademicConfig, OutputFormat
from src.gazzali.report_generator import create_empty_report

# Paper format
config = AcademicConfig(output_format=OutputFormat.PAPER)
report = create_empty_report("Title", config)
# Sections: Abstract, Introduction, Literature Review, Methodology, Findings, Discussion, Conclusion

# Review format
config = AcademicConfig(output_format=OutputFormat.REVIEW)
report = create_empty_report("Title", config)
# Sections: Abstract, Introduction, Thematic Analysis, Research Gaps, Future Directions

# Proposal format
config = AcademicConfig(output_format=OutputFormat.PROPOSAL)
report = create_empty_report("Title", config)
# Sections: Background, Research Questions, Literature Review, Proposed Methodology, Expected Outcomes, Timeline
```

### With CitationManager

The bibliography is generated by the `CitationManager` and added to the report:

```python
from src.gazzali.citation_manager import CitationManager, CitationStyle
from src.gazzali.report_generator import AcademicReport

# Generate bibliography
citation_manager = CitationManager()
# ... add citations ...
bibliography = citation_manager.generate_bibliography(style=CitationStyle.APA)

# Add to report
report = AcademicReport(title="My Paper")
report.bibliography = bibliography
```

## Best Practices

### 1. Always Calculate Word Count

After populating sections, calculate the word count:

```python
report.add_section("Introduction", intro_text)
report.add_section("Findings", findings_text)
report.calculate_word_count()
```

### 2. Use Section Constants

Use the provided constants for consistency:

```python
# Good
report.add_section(SECTION_METHODOLOGY, text)

# Avoid
report.add_section("Methodology", text)  # Typos possible
```

### 3. Include Metadata

Always include research metadata for transparency:

```python
metadata = ResearchMetadata(
    question=original_question,
    sources_consulted=len(sources),
    peer_reviewed_sources=peer_reviewed_count
)

report = AcademicReport(title=title, metadata=metadata)
```

### 4. Validate Output Format

Ensure sections match the output format:

```python
config = AcademicConfig(output_format=OutputFormat.ABSTRACT)
report = create_empty_report(title, config)
# Only creates Abstract section, appropriate for conference abstracts
```

### 5. Handle Long Reports

For very long reports, consider breaking into multiple files:

```python
# Save main report
report.save("main_report.md")

# Save bibliography separately
with open("bibliography.md", "w") as f:
    f.write(f"# References\n\n{report.bibliography}")
```

## Requirements Addressed

This module addresses the following requirements from the specification:

- **5.2**: Structured academic report sections (Abstract, Introduction, Literature Review, etc.)
- **12.1**: Research implications and impact analysis (Implications section)
- **12.2**: Theoretical and practical contributions (Discussion section)
- **12.3**: Future research directions (Future Directions section)

## Future Enhancements

Planned enhancements for future versions:

1. **PDF Export**: Direct PDF generation using ReportLab or similar
2. **Word Export**: Generate .docx files for Microsoft Word
3. **Template System**: Customizable section templates
4. **Figure Management**: Embed and reference figures/tables
5. **Cross-References**: Automatic section and citation cross-referencing
6. **Version Control**: Track report revisions and changes
7. **Collaborative Editing**: Support for multi-author reports
8. **Style Validation**: Check adherence to journal-specific styles

## Troubleshooting

### Issue: Word count seems incorrect

**Solution**: Ensure you call `calculate_word_count()` after adding all sections:

```python
report.add_section("Introduction", text)
report.calculate_word_count()  # Updates word_count attribute
```

### Issue: LaTeX special characters not escaped

**Solution**: The `_escape_latex()` method handles common special characters. For complex LaTeX, consider using raw LaTeX strings:

```python
# For equations, use raw LaTeX
report.add_section("Results", r"The equation $E = mc^2$ shows...")
```

### Issue: Section order is wrong

**Solution**: Use the `position` parameter when adding sections:

```python
# Insert at specific position (0-indexed)
report.add_section("Methodology", text, position=2)
```

### Issue: Bibliography not appearing

**Solution**: Ensure bibliography is set before saving:

```python
report.bibliography = citation_manager.generate_bibliography()
report.save("output.md")
```

## See Also

- [Academic Configuration](ACADEMIC_CONFIG.md) - Configuration options
- [Citation Manager](CITATION_MANAGER.md) - Citation management
- [Academic Prompts](ACADEMIC_PROMPTS.md) - Prompt engineering for academic content
