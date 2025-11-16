# Output Formats Documentation

This document describes the different output formats supported by Gazzali Research and their specific structures, use cases, and formatting conventions.

## Overview

Gazzali Research supports five output formats, each designed for specific academic purposes:

1. **Paper** - Full research paper format
2. **Review** - Literature review format
3. **Proposal** - Research proposal format
4. **Abstract** - Conference abstract format
5. **Presentation** - Presentation/slide format

Each format has a specific section structure, word count target, and formatting conventions.

## Format Specifications

### 1. Paper Format

**Purpose**: Complete research paper suitable for journal submission or thesis chapters.

**Target Word Count**: 6,000-10,000 words

**Required Sections**:
- Abstract (150-250 words)
- Introduction
- Literature Review
- Methodology
- Findings
- Discussion
- Conclusion
- References

**Structure Details**:

#### Abstract
- Concise summary of the entire paper
- Includes: background, methods, results, conclusions
- 150-250 words
- No citations
- Written in past tense for completed research

#### Introduction
- Research context and background
- Problem statement
- Research questions or hypotheses
- Significance of the study
- Paper organization overview
- 800-1,200 words

#### Literature Review
- Comprehensive review of existing research
- Organized thematically or chronologically
- Identifies research gaps
- Establishes theoretical framework
- 2,000-3,000 words
- Heavily cited

#### Methodology
- Research design description
- Data collection methods
- Sample/population description
- Analysis techniques
- Ethical considerations
- Limitations
- 1,000-1,500 words

#### Findings
- Presentation of research results
- Tables, figures, and statistical data
- Organized by research question or theme
- Objective reporting without interpretation
- 1,500-2,000 words

#### Discussion
- Interpretation of findings
- Comparison with existing literature
- Theoretical implications
- Practical implications
- Limitations discussion
- 1,500-2,000 words

#### Conclusion
- Summary of key findings
- Contributions to the field
- Future research directions
- Final thoughts
- 500-800 words

**Use Cases**:
- Journal article submission
- Thesis or dissertation chapters
- Comprehensive research reports
- Academic publications

**Example Command**:
```bash
python -m gazzali.ask "What are the effects of climate change on biodiversity?" \
  --academic \
  --output-format paper \
  --citation-style apa \
  --word-count 8000
```

---

### 2. Review Format

**Purpose**: Systematic literature review or state-of-the-art survey.

**Target Word Count**: 5,000-8,000 words

**Required Sections**:
- Abstract (150-250 words)
- Introduction
- Thematic Analysis
- Research Gaps
- Future Directions
- References

**Structure Details**:

#### Abstract
- Overview of review scope
- Key themes identified
- Main conclusions
- 150-250 words

#### Introduction
- Review objectives and scope
- Search strategy and inclusion criteria
- Organization of the review
- 800-1,000 words

#### Thematic Analysis
- Main body of the review
- Organized by themes, not chronologically
- Each theme has subsections
- Synthesizes findings across studies
- Identifies consensus and controversies
- 3,000-5,000 words
- Extensively cited

**Common Themes**:
- Theoretical frameworks
- Methodological approaches
- Key findings and patterns
- Contradictions and debates
- Contextual factors

#### Research Gaps
- Identifies what is not known
- Highlights methodological limitations
- Points to understudied areas
- Suggests needed research
- 800-1,200 words

#### Future Directions
- Recommendations for future research
- Methodological improvements
- Emerging trends
- Practical applications
- 500-800 words

**Use Cases**:
- Literature review papers
- Systematic reviews
- State-of-the-art surveys
- Background for grant proposals
- Comprehensive exam preparation

**Example Command**:
```bash
python -m gazzali.ask "Review the literature on machine learning in healthcare" \
  --academic \
  --output-format review \
  --citation-style apa \
  --discipline medical
```

---

### 3. Proposal Format

**Purpose**: Research proposal for funding applications or thesis proposals.

**Target Word Count**: 3,000-5,000 words

**Required Sections**:
- Background
- Research Questions
- Literature Review
- Proposed Methodology
- Expected Outcomes
- Timeline
- References

**Structure Details**:

#### Background
- Problem statement
- Significance and rationale
- Current state of knowledge
- Why this research is needed
- 800-1,000 words

#### Research Questions
- Specific research questions or hypotheses
- Objectives of the study
- Expected contributions
- 300-500 words

#### Literature Review
- Focused review of relevant literature
- Establishes theoretical foundation
- Justifies research approach
- Shorter than full paper review
- 1,000-1,500 words

#### Proposed Methodology
- Detailed research design
- Data collection plan
- Analysis strategy
- Timeline for each phase
- Resources required
- Ethical considerations
- 1,000-1,500 words

#### Expected Outcomes
- Anticipated findings
- Potential contributions
- Theoretical implications
- Practical applications
- Dissemination plan
- 500-800 words

#### Timeline
- Project phases
- Milestones and deliverables
- Time allocation
- Can be presented as a table or Gantt chart
- 200-300 words

**Use Cases**:
- Grant applications
- Thesis/dissertation proposals
- Research project planning
- Funding requests
- IRB applications

**Example Command**:
```bash
python -m gazzali.ask "Propose research on social media impact on mental health" \
  --academic \
  --output-format proposal \
  --citation-style apa \
  --discipline social
```

---

### 4. Abstract Format

**Purpose**: Conference abstract or brief research summary.

**Target Word Count**: 250-300 words

**Required Sections**:
- Abstract (single section, may have internal structure)

**Structure Details**:

The abstract is typically structured as a single paragraph or with minimal subsections:

#### Structured Abstract (Preferred)
- **Background**: 1-2 sentences on context and problem
- **Methods**: 2-3 sentences on research approach
- **Results**: 3-4 sentences on key findings
- **Conclusions**: 1-2 sentences on implications

#### Unstructured Abstract
- Single paragraph covering all elements
- Flows naturally from background to conclusions
- No explicit section headers

**Content Requirements**:
- Clear research question
- Brief methodology description
- Key findings with specific results
- Significance and implications
- No citations (typically)
- No abbreviations without definition
- Self-contained and understandable alone

**Use Cases**:
- Conference submissions
- Poster presentations
- Research summaries
- Grant abstracts
- Database indexing

**Example Command**:
```bash
python -m gazzali.ask "Summarize research on renewable energy adoption" \
  --academic \
  --output-format abstract \
  --citation-style apa \
  --word-count 300
```

---

### 5. Presentation Format

**Purpose**: Content for oral presentations or slide decks.

**Target Word Count**: 1,500-2,500 words (speaking notes)

**Required Sections**:
- Overview
- Key Findings
- Implications
- Conclusions

**Structure Details**:

#### Overview
- Brief introduction to topic
- Research question or objective
- Why it matters
- Bullet points preferred
- 300-500 words

#### Key Findings
- Main results organized by theme
- Visual descriptions (for slides)
- Bullet points with brief explanations
- Emphasis on most important findings
- 800-1,200 words

#### Implications
- What the findings mean
- Theoretical contributions
- Practical applications
- Who should care and why
- 400-600 words

#### Conclusions
- Summary of main points
- Take-home messages
- Future directions
- Call to action (if appropriate)
- 200-400 words

**Formatting Conventions**:
- Short sentences and bullet points
- Clear headings and subheadings
- Descriptions of visual elements
- Speaking notes format
- Minimal citations (key sources only)

**Use Cases**:
- Conference presentations
- Seminar talks
- Webinar content
- Lecture materials
- Stakeholder briefings

**Example Command**:
```bash
python -m gazzali.ask "Create presentation on AI ethics" \
  --academic \
  --output-format presentation \
  --citation-style apa \
  --word-count 2000
```

---

## File Format Options

### Markdown (.md)

**Default format** for all output types.

**Features**:
- Human-readable plain text
- Easy to edit and version control
- Convertible to other formats
- Supports basic formatting (headers, lists, emphasis)
- Includes metadata header

**Example**:
```markdown
# Research Paper Title

---
**Generated**: 2024-01-15 10:30:00
**Citation Style**: APA
**Word Count**: 8,245
**Keywords**: climate change, biodiversity, conservation
---

## Abstract

This study examines...

## Introduction

Climate change represents...
```

**Usage**:
```bash
# Markdown is the default
python -m gazzali.ask "Your question" --academic

# Or explicitly specify
report.save("output.md", format="markdown")
```

### LaTeX (.tex)

**Professional typesetting** for publication-ready documents.

**Features**:
- High-quality PDF output
- Professional formatting
- Mathematical equations support
- Citation management integration
- Journal-ready formatting

**Example**:
```latex
\documentclass[12pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage{graphicx}
\usepackage{hyperref}
\usepackage{cite}

\title{Research Paper Title}
\date{January 15, 2024}

\begin{document}
\maketitle

\begin{abstract}
This study examines...
\end{abstract}

\section{Introduction}
Climate change represents...

\end{document}
```

**Usage**:
```python
from gazzali.academic_report_generator import generate_academic_report

report = generate_academic_report(...)
report.save("output.tex", format="latex")
```

**Compilation**:
```bash
pdflatex output.tex
bibtex output
pdflatex output.tex
pdflatex output.tex
```

---

## Format Selection Guidelines

### Choose Paper Format When:
- Writing a complete research article
- Preparing thesis/dissertation chapters
- Need comprehensive coverage with all sections
- Target audience: academic peers and reviewers
- Publication is the goal

### Choose Review Format When:
- Synthesizing existing literature
- Conducting systematic review
- Preparing background for larger project
- Target audience: researchers entering the field
- Comprehensive understanding is the goal

### Choose Proposal Format When:
- Seeking research funding
- Planning a research project
- Preparing thesis proposal
- Target audience: funding agencies, committees
- Approval and resources are the goal

### Choose Abstract Format When:
- Submitting to conferences
- Creating research summaries
- Indexing in databases
- Target audience: conference attendees, database users
- Brief communication is the goal

### Choose Presentation Format When:
- Preparing oral presentations
- Creating slide content
- Briefing stakeholders
- Target audience: live audience, non-specialists
- Clear communication is the goal

---

## Customization Options

### Word Count Adjustment

Adjust target word count based on requirements:

```bash
# Shorter paper (5,000 words)
--word-count 5000

# Longer review (10,000 words)
--word-count 10000

# Brief abstract (250 words)
--word-count 250
```

### Section Inclusion

Control which sections are included:

```python
from gazzali.academic_config import AcademicConfig

config = AcademicConfig(
    output_format="paper",
    include_abstract=True,      # Include abstract
    include_methodology=False,  # Skip methodology
)
```

### Citation Style

Choose appropriate citation style for your field:

```bash
# APA (Psychology, Education, Social Sciences)
--citation-style apa

# MLA (Humanities, Literature)
--citation-style mla

# Chicago (History, Arts)
--citation-style chicago

# IEEE (Engineering, Computer Science)
--citation-style ieee
```

---

## Format Validation

Gazzali Research validates report structure to ensure compliance:

### Validation Checks:
- ✓ Required sections present
- ✓ Word count within reasonable range
- ✓ Citation style consistency
- ✓ Bibliography included
- ✓ Abstract length appropriate
- ✓ Section content not empty

### Validation Example:

```python
from gazzali.academic_report_generator import AcademicReportGenerator

generator = AcademicReportGenerator(config, citation_manager)
report = generator.generate_report(...)

# Validate structure
issues = generator.validate_report_structure(report)

if issues:
    print("Validation issues found:")
    for issue in issues:
        print(f"  - {issue}")
else:
    print("Report structure is valid!")
```

---

## Best Practices

### For All Formats:
1. **Start with clear research question** - Well-defined questions lead to better reports
2. **Use appropriate discipline settings** - Terminology and conventions matter
3. **Review and refine** - Generated reports benefit from human review
4. **Check citations** - Verify citation accuracy and completeness
5. **Validate structure** - Ensure all required sections are present

### Format-Specific Tips:

**Paper**:
- Allow sufficient word count (8,000+ words)
- Include comprehensive methodology
- Provide detailed discussion of limitations
- Use tables and figures for complex data

**Review**:
- Organize thematically, not chronologically
- Explicitly identify research gaps
- Compare and contrast different approaches
- Provide clear synthesis, not just summary

**Proposal**:
- Emphasize feasibility and significance
- Provide detailed methodology
- Include realistic timeline
- Address potential challenges

**Abstract**:
- Be concise and specific
- Include key numerical results
- Make it self-contained
- Avoid jargon and abbreviations

**Presentation**:
- Use bullet points and short sentences
- Focus on key messages
- Describe visual elements
- Include speaking notes

---

## Examples

### Complete Workflow Example

```bash
# 1. Generate a full research paper
python -m gazzali.ask \
  "What are the psychological effects of remote work?" \
  --academic \
  --output-format paper \
  --citation-style apa \
  --discipline social \
  --word-count 8000 \
  --export-bib

# 2. Generate a literature review
python -m gazzali.ask \
  "Review machine learning applications in drug discovery" \
  --academic \
  --output-format review \
  --citation-style ieee \
  --discipline stem \
  --word-count 6000

# 3. Generate a research proposal
python -m gazzali.ask \
  "Propose research on blockchain in supply chain management" \
  --academic \
  --output-format proposal \
  --citation-style apa \
  --discipline general \
  --word-count 4000

# 4. Generate a conference abstract
python -m gazzali.ask \
  "Summarize findings on CRISPR gene editing safety" \
  --academic \
  --output-format abstract \
  --citation-style apa \
  --discipline medical \
  --word-count 300
```

### Programmatic Usage Example

```python
from gazzali.academic_config import AcademicConfig, OutputFormat, CitationStyle
from gazzali.citation_manager import CitationManager
from gazzali.academic_report_generator import generate_academic_report

# Configure for literature review
config = AcademicConfig(
    citation_style=CitationStyle.APA,
    output_format=OutputFormat.REVIEW,
    discipline="stem",
    word_count_target=6000,
    include_abstract=True,
)

# Initialize citation manager
citation_mgr = CitationManager()

# Generate report
report = generate_academic_report(
    question="What are the latest advances in quantum computing?",
    research_results="[research findings here]",
    api_key="your-api-key",
    config=config,
    citation_manager=citation_mgr,
)

# Save in multiple formats
report.save("quantum_review.md", format="markdown")
report.save("quantum_review.tex", format="latex")

# Export bibliography
if config.export_bibliography:
    citation_mgr.export_bibtex("quantum_review.bib")

print(f"Generated {report.output_format.value} with {report.word_count} words")
print(f"Sections: {', '.join(report.get_section_names())}")
```

---

## Troubleshooting

### Issue: Report missing required sections

**Solution**: Check output format configuration and ensure synthesis model received proper instructions.

```python
# Validate report structure
issues = generator.validate_report_structure(report)
print(issues)
```

### Issue: Word count too low/high

**Solution**: Adjust word count target in configuration.

```python
config.word_count_target = 8000  # Adjust as needed
```

### Issue: Citations not formatted correctly

**Solution**: Verify citation style setting and citation manager has complete data.

```python
# Check citation style
print(f"Using citation style: {config.citation_style.value}")

# Check citations in manager
print(f"Citations tracked: {len(citation_manager)}")
```

### Issue: LaTeX compilation errors

**Solution**: Check for special characters that need escaping.

```python
# The to_latex() method handles basic escaping
# For complex content, manual review may be needed
report.save("output.tex", format="latex")
```

---

## Related Documentation

- [Academic Mode Guide](ACADEMIC_MODE.md) - Complete guide to academic features
- [Citation Styles](CITATION_STYLES.md) - Citation formatting examples
- [Discipline Settings](DISCIPLINE_SETTINGS.md) - Discipline-specific configurations
- [Academic Configuration](ACADEMIC_CONFIG.md) - Configuration options

---

## Summary

Gazzali Research provides five specialized output formats, each optimized for specific academic purposes:

| Format | Word Count | Use Case | Key Sections |
|--------|-----------|----------|--------------|
| Paper | 6,000-10,000 | Journal articles, theses | Abstract, Intro, Lit Review, Methods, Findings, Discussion, Conclusion |
| Review | 5,000-8,000 | Literature reviews | Abstract, Intro, Thematic Analysis, Gaps, Future Directions |
| Proposal | 3,000-5,000 | Grant applications | Background, Questions, Lit Review, Methods, Outcomes, Timeline |
| Abstract | 250-300 | Conference submissions | Single structured abstract |
| Presentation | 1,500-2,500 | Oral presentations | Overview, Key Findings, Implications, Conclusions |

Choose the format that best matches your academic communication needs, and customize with appropriate citation style, discipline settings, and word count targets.
