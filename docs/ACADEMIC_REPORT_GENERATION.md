# Academic Report Generation

This document describes the academic report generation system in Gazzali Research, which transforms research findings into structured, properly formatted academic documents.

## Overview

The `AcademicReportGenerator` class is the core component responsible for generating academic reports. It integrates with:
- **Synthesis Model**: AI model that generates report content
- **Citation Manager**: Tracks and formats citations
- **Academic Config**: Configuration for style, format, and discipline
- **Report Data Models**: Structured representation of academic reports

## Architecture

```
Research Results
      ↓
AcademicReportGenerator
      ↓
   ┌──────────────────────┐
   │ 1. Prepare Prompt    │ ← Academic Config
   │ 2. Call Synthesis    │ ← Synthesis Model
   │ 3. Parse Sections    │
   │ 4. Format Citations  │ ← Citation Manager
   │ 5. Generate Biblio   │
   │ 6. Assemble Report   │
   └──────────────────────┘
      ↓
AcademicReport Object
      ↓
   Output Files
   (Markdown/LaTeX)
```

## Core Components

### AcademicReportGenerator

The main class that orchestrates report generation.

```python
from gazzali.academic_report_generator import AcademicReportGenerator
from gazzali.academic_config import AcademicConfig
from gazzali.citation_manager import CitationManager

# Initialize components
config = AcademicConfig(
    citation_style="apa",
    output_format="paper",
    discipline="stem",
    word_count_target=8000
)

citation_manager = CitationManager()

# Create generator
generator = AcademicReportGenerator(config, citation_manager)

# Generate report
report = generator.generate_report(
    question="What are the effects of machine learning on healthcare?",
    research_results="[research findings from agent]",
    api_key="your-api-key",
    model="openai/grok-2-1212"
)

# Save report
report.save("healthcare_ml_report.md", format="markdown")
```

### Key Methods

#### `generate_report()`

Main method that generates a complete academic report.

**Parameters:**
- `question` (str): Original research question
- `research_results` (str): Raw research findings from research agent
- `api_key` (str): API key for synthesis model
- `metadata` (Optional[ResearchMetadata]): Research metadata
- `model` (str): Model identifier (default: "openai/grok-2-1212")

**Returns:**
- `AcademicReport`: Complete report with all sections and bibliography

**Process:**
1. Generates synthesis prompt with academic guidelines
2. Calls synthesis model to generate content
3. Parses content into structured sections
4. Formats citations and generates bibliography
5. Assembles final AcademicReport object

#### `validate_report_structure()`

Validates that a report has the required structure.

```python
issues = generator.validate_report_structure(report)
if issues:
    print("Validation issues found:")
    for issue in issues:
        print(f"  - {issue}")
else:
    print("Report structure is valid")
```

**Returns:**
- `List[str]`: List of validation issues (empty if valid)

**Checks:**
- All required sections present
- Sections not empty
- Bibliography exists
- Word count reasonable
- Citation style matches configuration

## Report Structure

### Standard Sections

The report structure depends on the `output_format` configuration:

#### Paper Format
1. **Abstract** (150-250 words)
2. **Introduction**
3. **Literature Review**
4. **Methodology** (if `include_methodology=True`)
5. **Findings**
6. **Discussion**
7. **Conclusion**
8. **References**

#### Literature Review Format
1. **Abstract**
2. **Introduction**
3. **Thematic Analysis**
4. **Research Gaps**
5. **Future Directions**
6. **References**

#### Research Proposal Format
1. **Background**
2. **Research Questions**
3. **Literature Review**
4. **Proposed Methodology**
5. **Expected Outcomes**
6. **Timeline**
7. **References**

#### Abstract Format
1. **Abstract** (250-300 words only)

#### Presentation Format
1. **Overview**
2. **Key Findings**
3. **Implications**
4. **Conclusions**

### Section Content Requirements

Each section must meet specific academic standards:

**Abstract:**
- Concise summary (150-250 words)
- Background, methods, results, conclusions
- No citations
- Self-contained

**Introduction:**
- Context and background
- Research question clearly stated
- Significance explained
- Report structure overview

**Literature Review:**
- Thematic organization
- Critical synthesis
- Identify consensus and controversies
- Research gaps highlighted
- Chronological evolution shown

**Methodology:**
- Research methods described
- Methodologies categorized
- Strengths and limitations discussed
- Ethical considerations addressed

**Findings:**
- Main results presented
- Organized logically
- Specific data and statistics
- All claims cited

**Discussion:**
- Interpretation of findings
- Connection to existing literature
- Implications analyzed
- Limitations acknowledged

**Conclusion:**
- Key findings summarized
- Main implications restated
- Future directions identified
- No new information

**References:**
- Complete bibliography
- Formatted in specified style
- Alphabetized by author
- All cited sources included

## Citation Integration

### Automatic Citation Formatting

The generator automatically formats citations using the `CitationManager`:

```python
# Citations are tracked during research
citation_manager.add_citation(citation)

# Bibliography is generated automatically
bibliography = generator._generate_bibliography()
```

### Citation Styles

Supported citation styles:
- **APA 7th Edition**: (Author, Year) inline
- **MLA 9th Edition**: (Author Page) inline
- **Chicago 17th Edition**: (Author Year) inline
- **IEEE**: [Number] inline

### In-Text Citation Format

Citations are integrated into the text:

```
Recent research demonstrates that X influences Y (Smith, 2020; Jones, 2021).
Smith (2020) found that X correlates with Y, while Jones (2021) reported 
conflicting results.
```

### Bibliography Format

The bibliography is automatically generated and formatted:

```
Smith, J. A., & Jones, B. C. (2020). Title of article. Journal Name, 15(3), 
    123-145. https://doi.org/10.1234/example

Jones, B. C., Wilson, D. E., & Brown, F. G. (2021). Title of book. Publisher.
```

## Academic Writing Standards

### Formal Tone

The synthesis model is prompted to maintain:
- Formal, professional language
- Objective, third-person perspective
- No contractions or colloquialisms
- Precise technical terminology
- Clear, direct sentences

### Hedging Language

Appropriate certainty indicators:
- **Strong evidence**: "demonstrates," "shows," "establishes"
- **Moderate evidence**: "suggests," "indicates," "supports"
- **Weak evidence**: "may," "appears to," "preliminary findings suggest"
- **Speculation**: "it is possible that," "one explanation could be"

### Examples

✓ **Good**: "The findings suggest a positive correlation between X and Y."
✗ **Bad**: "The findings prove that X definitely causes Y."

✓ **Good**: "Research indicates that this approach may be effective in certain contexts."
✗ **Bad**: "This approach is the best solution and always works."

## Discipline-Specific Customization

### STEM Disciplines

- Technical and scientific terminology
- Mathematical notation and equations
- Experimental design focus
- Statistical analysis emphasis
- Reproducibility requirements

### Social Sciences

- Social science constructs and frameworks
- Qualitative and quantitative methods
- Validity and reliability emphasis
- Cultural context consideration
- Ethical considerations for human subjects

### Humanities

- Critical theory and hermeneutics
- Textual analysis focus
- Historical context emphasis
- Interpretive frameworks
- Primary source engagement

### Medical/Health Sciences

- Clinical terminology
- Evidence-based practice focus
- Patient outcomes emphasis
- Clinical trial methodology
- Ethical considerations for patient care

## Output Formats

### Markdown

Default format for easy reading and editing:

```python
report.save("report.md", format="markdown")
```

Features:
- Clear section headers
- Proper formatting
- Easy to edit
- Version control friendly

### LaTeX

For publication-ready documents:

```python
report.save("report.tex", format="latex")
```

Features:
- Professional typesetting
- Academic formatting
- Citation support
- Figure and table support

## Convenience Function

For quick report generation:

```python
from gazzali.academic_report_generator import generate_academic_report

report = generate_academic_report(
    question="What are the effects of climate change?",
    research_results="[research findings]",
    api_key="your-api-key",
    config=config,  # Optional, uses defaults if None
    citation_manager=citation_mgr,  # Optional, creates new if None
    metadata=metadata,  # Optional
    model="openai/grok-2-1212"  # Optional, default model
)
```

## Error Handling

### Common Issues

**Missing Sections:**
```python
issues = generator.validate_report_structure(report)
# Returns: ["Missing required section: Methodology"]
```

**Low Word Count:**
```python
# Adjust word_count_target in config
config.word_count_target = 10000
```

**Citation Style Mismatch:**
```python
# Ensure config citation_style matches desired output
config.citation_style = CitationStyle.APA
```

### Synthesis Model Errors

```python
try:
    report = generator.generate_report(...)
except RuntimeError as e:
    print(f"Error generating report: {e}")
    # Handle error (retry, use different model, etc.)
```

## Best Practices

### 1. Configure Before Generation

Set up configuration properly before generating:

```python
config = AcademicConfig(
    citation_style="apa",
    output_format="paper",
    discipline="stem",
    word_count_target=8000,
    include_abstract=True,
    include_methodology=True
)
```

### 2. Track Citations During Research

Add citations as you discover sources:

```python
citation = citation_manager.create_citation_from_metadata(
    title="Paper Title",
    authors=["Smith, J.", "Jones, B."],
    year=2020,
    venue="Journal Name",
    url="https://example.com"
)
citation_manager.add_citation(citation)
```

### 3. Validate After Generation

Always validate the report structure:

```python
report = generator.generate_report(...)
issues = generator.validate_report_structure(report)
if issues:
    # Handle validation issues
    pass
```

### 4. Save in Multiple Formats

Save both Markdown and LaTeX versions:

```python
report.save("report.md", format="markdown")
report.save("report.tex", format="latex")
```

### 5. Export Bibliography Separately

For use in reference managers:

```python
citation_manager.export_bibtex("references.bib")
citation_manager.export_ris("references.ris")
```

## Integration with Research Workflow

### Complete Workflow Example

```python
from gazzali.academic_config import AcademicConfig
from gazzali.citation_manager import CitationManager
from gazzali.academic_report_generator import AcademicReportGenerator
from gazzali.report_generator import ResearchMetadata

# 1. Configure
config = AcademicConfig.from_env()

# 2. Initialize citation manager
citation_manager = CitationManager()

# 3. Conduct research (research agent adds citations)
# ... research process ...

# 4. Create metadata
metadata = ResearchMetadata(
    question="Research question",
    discipline="stem",
    sources_consulted=25,
    peer_reviewed_sources=18
)

# 5. Generate report
generator = AcademicReportGenerator(config, citation_manager)
report = generator.generate_report(
    question="Research question",
    research_results="[findings]",
    api_key=api_key,
    metadata=metadata
)

# 6. Validate
issues = generator.validate_report_structure(report)
if not issues:
    # 7. Save
    report.save("final_report.md")
    citation_manager.export_bibtex("references.bib")
```

## Future Enhancements

Planned improvements:
- Automatic abstract generation from content
- Literature review restructuring
- Methodology section enhancement
- Citation integration improvements
- Quality scoring and suggestions
- Multi-language support
- Template customization
- Collaborative editing support

## Requirements Addressed

This module addresses the following requirements:

- **5.1**: Academic writing style with formal tone
- **5.2**: Structured sections following academic conventions
- **5.3**: Hedging language and certainty indicators
- **5.4**: Formal language without colloquialisms
- **5.5**: Academic formatting standards for data presentation

## See Also

- [Academic Configuration](ACADEMIC_CONFIG.md)
- [Citation Manager](CITATION_MANAGER.md)
- [Academic Prompts](ACADEMIC_PROMPTS.md)
- [Report Data Models](REPORTING_PIPELINE.md)
