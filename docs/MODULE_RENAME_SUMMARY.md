# Module Rename Summary

## What Changed

To improve code clarity, we renamed two key modules in the report generation system:

### Before (Confusing Names)
```
src/gazzali/
├── report_generator.py              # Actually contained DATA MODELS
└── academic_report_generator.py     # Actually contained GENERATION LOGIC
```

### After (Clear Names)
```
src/gazzali/
├── report_models.py                 # DATA MODELS & FORMATTING ✨
└── report_generator.py              # GENERATION LOGIC ✨
```

## Why This Matters

The old naming was confusing because:
- `report_generator.py` didn't generate reports - it just defined data structures
- `academic_report_generator.py` was too verbose and redundant
- The relationship between the two files wasn't clear

The new naming makes it immediately obvious:
- `report_models.py` = "What a report IS" (structure and formatting)
- `report_generator.py` = "How to CREATE a report" (generation logic)

## What Each Module Does

### `report_models.py` (Data Models & Formatting)

**Contains:**
- `AcademicReport` class - Main report data structure
- `ResearchMetadata` class - Metadata about research process
- Section constants (SECTION_ABSTRACT, SECTION_INTRODUCTION, etc.)
- Output methods:
  - `to_markdown()` - Convert to Markdown
  - `to_latex()` - Convert to LaTeX
  - `save()` - Save to file
  - `get_format_template()` - Get format info
- Helper: `create_empty_report()`

**Responsibilities:**
- ✅ Define report structure
- ✅ Store report content
- ✅ Format output (Markdown, LaTeX)
- ✅ Save to files
- ❌ NOT responsible for generating content
- ❌ NOT responsible for calling AI models

### `report_generator.py` (Generation Logic)

**Contains:**
- `AcademicReportGenerator` class - Main generator
- Methods for:
  - Calling synthesis models (OpenAI/OpenRouter)
  - Parsing AI responses into sections
  - Formatting citations
  - Validating structure
  - Assembling reports
- Helper: `generate_academic_report()`

**Responsibilities:**
- ✅ Orchestrate report generation
- ✅ Call AI synthesis models
- ✅ Parse AI responses
- ✅ Format citations
- ✅ Validate structure
- ❌ NOT responsible for output formatting
- ❌ NOT responsible for file I/O

## Migration Guide

### If you were importing from the old modules:

**Old imports:**
```python
# OLD - Don't use these anymore
from gazzali.report_generator import AcademicReport, ResearchMetadata
from gazzali.academic_report_generator import AcademicReportGenerator
```

**New imports:**
```python
# NEW - Use these instead
from gazzali.report_models import AcademicReport, ResearchMetadata
from gazzali.report_generator import AcademicReportGenerator
```

### Common import patterns:

**For working with report data models:**
```python
from gazzali.report_models import (
    AcademicReport,
    ResearchMetadata,
    create_empty_report,
    SECTION_ABSTRACT,
    SECTION_INTRODUCTION,
    # ... other section constants
)
```

**For generating reports:**
```python
from gazzali.report_generator import (
    AcademicReportGenerator,
    generate_academic_report,  # Convenience function
)
```

**Complete example:**
```python
from gazzali.academic_config import AcademicConfig
from gazzali.citation_manager import CitationManager
from gazzali.report_generator import AcademicReportGenerator
from gazzali.report_models import ResearchMetadata

# Configure
config = AcademicConfig(citation_style="apa", output_format="paper")
citation_mgr = CitationManager()

# Generate
generator = AcademicReportGenerator(config, citation_mgr)
report = generator.generate_report(
    question="Your research question",
    research_results="Research findings...",
    api_key="your-api-key",
)

# Output
report.save("output.md", format="markdown")
report.save("output.tex", format="latex")
```

## Files Updated

All imports have been updated in:
- ✅ `src/gazzali/report_generator.py`
- ✅ `tests/test_report_generation.py`
- ✅ `docs/REPORTING_PIPELINE.md`
- ✅ `docs/OUTPUT_FORMATS.md`
- ✅ `docs/ACADEMIC_REPORT_GENERATION.md`
- ✅ `docs/SCHOLAR_CITATION_INTEGRATION.md`
- ✅ `docs/SECTION_GENERATORS.md`

## Testing

All 22 integration tests pass with the new module names:
```bash
python3 -m pytest tests/test_report_generation.py -v
# 22 passed in 0.05s ✅
```

## Benefits of This Change

1. **Clarity** - Module names now match their actual purpose
2. **Discoverability** - New developers can immediately understand the architecture
3. **Maintainability** - Clear separation of concerns makes code easier to maintain
4. **Consistency** - Follows common naming patterns (models vs logic)
5. **Documentation** - Self-documenting code through better naming

## Related Documentation

- [Reporting Pipeline Architecture](REPORTING_PIPELINE.md) - Complete architecture guide
- [Output Formats](OUTPUT_FORMATS.md) - Format specifications and usage
- [Academic Report Generation](ACADEMIC_REPORT_GENERATION.md) - Generation workflow

## Questions?

If you have questions about the rename or need help updating your code:
1. Check the [Reporting Pipeline](REPORTING_PIPELINE.md) documentation
2. Look at the examples in this document
3. Review the test file: `tests/test_report_generation.py`
