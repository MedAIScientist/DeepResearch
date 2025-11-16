# Academic Report Generation Pipeline

This document explains the architecture and workflow of the academic report generation system in Gazzali Research.

## Architecture Overview

The report generation system is split into two main modules with clear separation of concerns:

### 1. `report_generator.py` - Data Models & Formatting

**Purpose**: Defines the structure of academic reports and how they are formatted for output.

**Key Components**:
- `AcademicReport` - Main data model containing title, abstract, sections, bibliography
- `ResearchMetadata` - Metadata about sources, authors, methodologies
- Section constants - Standard names (SECTION_ABSTRACT, SECTION_INTRODUCTION, etc.)
- Output methods:
  - `to_markdown()` - Convert report to Markdown format
  - `to_latex()` - Convert report to LaTeX format
  - `save()` - Save report to file with format detection
  - `get_format_template()` - Get format-specific template info

**Think of it as**: The "container" and "formatter" - it holds the report data and knows how to display it.

### 2. `academic_report_generator.py` - Generation Logic

**Purpose**: Orchestrates the process of generating report content using AI models.

**Key Components**:
- `AcademicReportGenerator` - Main class that generates reports
- Methods for:
  - Calling synthesis models (OpenAI/OpenRouter)
  - Parsing AI-generated content into sections
  - Formatting citations and bibliography
  - Validating report structure
  - Assembling final report

**Think of it as**: The "factory" - it creates and populates the report container.

## Data Flow

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Input                                                     │
│    - Research question                                       │
│    - Research results (from research agent)                  │
│    - Academic configuration (citation style, format, etc.)   │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. AcademicReportGenerator (academic_report_generator.py)   │
│    ┌─────────────────────────────────────────────────────┐  │
│    │ a. Prepare synthesis prompt                         │  │
│    │    - Load academic writing guidelines               │  │
│    │    - Add discipline-specific requirements           │  │
│    │    - Include citation style instructions            │  │
│    └─────────────────────────────────────────────────────┘  │
│    ┌─────────────────────────────────────────────────────┐  │
│    │ b. Call synthesis model                             │  │
│    │    - Send prompt to AI (e.g., grok-2-1212)          │  │
│    │    - Receive generated report content               │  │
│    └─────────────────────────────────────────────────────┘  │
│    ┌─────────────────────────────────────────────────────┐  │
│    │ c. Parse and structure content                      │  │
│    │    - Extract sections (Abstract, Intro, etc.)       │  │
│    │    - Identify bibliography                          │  │
│    │    - Validate structure                             │  │
│    └─────────────────────────────────────────────────────┘  │
│    ┌─────────────────────────────────────────────────────┐  │
│    │ d. Format citations                                 │  │
│    │    - Use CitationManager to format bibliography     │  │
│    │    - Apply citation style (APA, MLA, etc.)          │  │
│    └─────────────────────────────────────────────────────┘  │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. AcademicReport (report_generator.py)                     │
│    ┌─────────────────────────────────────────────────────┐  │
│    │ Report object created with:                         │  │
│    │ - Title                                             │  │
│    │ - Abstract                                          │  │
│    │ - Sections (OrderedDict)                           │  │
│    │ - Bibliography                                      │  │
│    │ - Metadata                                          │  │
│    │ - Citation style                                    │  │
│    │ - Output format                                     │  │
│    └─────────────────────────────────────────────────────┘  │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. Output (report_generator.py methods)                     │
│    ┌──────────────┬──────────────┬──────────────┐          │
│    │ to_markdown()│  to_latex()  │    save()    │          │
│    │              │              │              │          │
│    │ Markdown     │ LaTeX        │ File with    │          │
│    │ format       │ format       │ auto-detect  │          │
│    └──────────────┴──────────────┴──────────────┘          │
└─────────────────────────────────────────────────────────────┘
```

## Usage Examples

### Basic Usage

```python
from gazzali.academic_config import AcademicConfig, CitationStyle, OutputFormat
from gazzali.citation_manager import CitationManager
from gazzali.academic_report_generator import AcademicReportGenerator

# 1. Configure academic settings
config = AcademicConfig(
    citation_style=CitationStyle.APA,
    output_format=OutputFormat.PAPER,
    discipline="stem",
    word_count_target=8000,
)

# 2. Initialize citation manager
citation_manager = CitationManager()

# 3. Create generator
generator = AcademicReportGenerator(config, citation_manager)

# 4. Generate report
report = generator.generate_report(
    question="What are the effects of climate change?",
    research_results="[research findings from research agent]",
    api_key="your-api-key",
)

# 5. Output report
report.save("climate_report.md", format="markdown")
report.save("climate_report.tex", format="latex")
```

### Using the Convenience Function

```python
from gazzali.academic_report_generator import generate_academic_report

# One-line generation with defaults
report = generate_academic_report(
    question="What are the effects of climate change?",
    research_results="[research findings]",
    api_key="your-api-key",
)

report.save("report.md")
```

## Module Responsibilities

### `report_generator.py` is responsible for:

✅ Defining report structure (data models)  
✅ Storing report content (sections, bibliography, metadata)  
✅ Converting reports to different formats (Markdown, LaTeX)  
✅ Saving reports to files  
✅ Providing format templates and validation info  

❌ NOT responsible for generating content  
❌ NOT responsible for calling AI models  
❌ NOT responsible for parsing AI responses  

### `academic_report_generator.py` is responsible for:

✅ Orchestrating report generation workflow  
✅ Calling synthesis models with academic prompts  
✅ Parsing AI-generated content into sections  
✅ Formatting citations and bibliography  
✅ Validating report structure  
✅ Assembling final AcademicReport objects  

❌ NOT responsible for output formatting (delegates to AcademicReport)  
❌ NOT responsible for file I/O (delegates to AcademicReport.save())  

## Why This Separation?

### Benefits:

1. **Single Responsibility Principle**
   - Each module has one clear purpose
   - Easier to understand and maintain

2. **Testability**
   - Can test data models independently of generation logic
   - Can test formatting without calling AI models
   - Can mock the generator when testing output formats

3. **Flexibility**
   - Can add new output formats without touching generation logic
   - Can change AI models without affecting data structures
   - Can reuse AcademicReport for manually created reports

4. **Clear Dependencies**
   - `report_generator.py` has minimal dependencies (just config and citation manager)
   - `academic_report_generator.py` depends on report_generator (imports models)
   - One-way dependency makes the architecture clean

## Common Patterns

### Creating an Empty Report

```python
from gazzali.report_generator import create_empty_report
from gazzali.academic_config import AcademicConfig

config = AcademicConfig(output_format="paper")
report = create_empty_report("My Research Paper", config)

# Report has empty sections based on format
print(report.get_section_names())
# ['Introduction', 'Literature Review', 'Methodology', ...]
```

### Manually Populating a Report

```python
# Create empty report
report = create_empty_report("My Paper", config)

# Add content manually
report.abstract = "This study examines..."
report.sections["Introduction"] = "Climate change is..."
report.sections["Conclusion"] = "In conclusion..."
report.bibliography = citation_manager.generate_bibliography()

# Calculate word count
report.calculate_word_count()

# Save
report.save("manual_report.md")
```

### Validating Report Structure

```python
# Generate report
report = generator.generate_report(...)

# Validate
issues = generator.validate_report_structure(report)

if issues:
    print("Validation issues found:")
    for issue in issues:
        print(f"  - {issue}")
else:
    print("Report structure is valid!")
```

## File Organization

```
src/gazzali/
├── report_generator.py              # DATA MODELS & FORMATTING
│   ├── AcademicReport (class)
│   ├── ResearchMetadata (class)
│   ├── Section constants
│   └── create_empty_report()
│
├── academic_report_generator.py     # GENERATION LOGIC
│   ├── AcademicReportGenerator (class)
│   └── generate_academic_report()
│
├── academic_config.py               # Configuration
├── citation_manager.py              # Citation handling
└── prompts/
    └── academic_prompts.py          # Prompt templates
```

## Summary

- **`report_generator.py`** = "What a report IS" (structure and formatting)
- **`academic_report_generator.py`** = "How to CREATE a report" (generation logic)

Both work together but have distinct, non-overlapping responsibilities. The naming could be clearer (e.g., `report_models.py` vs `report_generator.py`), but the current structure follows good software engineering principles.
