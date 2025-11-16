# Academic Configuration Guide

The Academic Configuration module provides comprehensive settings for academic research features in Gazzali, allowing customization of citation styles, output formats, discipline-specific conventions, and report structure.

## Overview

The `AcademicConfig` class manages all academic research settings and can be configured through:
- Environment variables
- Command-line arguments
- Direct instantiation with custom values

## Configuration Options

### Citation Style

Controls the citation format used in generated reports.

**Options:**
- `apa` - American Psychological Association (default)
- `mla` - Modern Language Association
- `chicago` - Chicago Manual of Style
- `ieee` - Institute of Electrical and Electronics Engineers

**Environment Variable:** `CITATION_STYLE`

**Example:**
```bash
export CITATION_STYLE="mla"
```

### Output Format

Determines the structure and style of the generated document.

**Options:**
- `paper` - Full research paper (default)
- `review` - Literature review
- `proposal` - Research proposal
- `abstract` - Conference abstract (250-300 words)
- `presentation` - Presentation-style summary

**Environment Variable:** `OUTPUT_FORMAT`

**Example:**
```bash
export OUTPUT_FORMAT="review"
```

### Discipline

Sets discipline-specific terminology and methodological conventions.

**Options:**
- `general` - Interdisciplinary (default)
- `stem` - Science, Technology, Engineering, Mathematics
- `social` - Social Sciences
- `humanities` - Humanities
- `medical` - Medical and Clinical Sciences

**Environment Variable:** `DISCIPLINE`

**Example:**
```bash
export DISCIPLINE="stem"
```

### Word Count Target

Target word count for the generated report.

**Default:** `8000`

**Environment Variable:** `WORD_COUNT_TARGET`

**Example:**
```bash
export WORD_COUNT_TARGET="10000"
```

**Validation:**
- Minimum recommended: 500 words
- Maximum recommended: 50,000 words
- Abstract format: 250-500 words

### Include Abstract

Whether to include an abstract section in the report.

**Default:** `true`

**Environment Variable:** `INCLUDE_ABSTRACT`

**Example:**
```bash
export INCLUDE_ABSTRACT="false"
```

### Include Methodology

Whether to include a methodology section in the report.

**Default:** `true`

**Environment Variable:** `INCLUDE_METHODOLOGY`

**Example:**
```bash
export INCLUDE_METHODOLOGY="false"
```

### Scholar Priority

Prioritize Google Scholar and academic databases over general web search.

**Default:** `true`

**Environment Variable:** `SCHOLAR_PRIORITY`

**Example:**
```bash
export SCHOLAR_PRIORITY="true"
```

### Export Bibliography

Export bibliography to a separate file.

**Default:** `false`

**Environment Variable:** `EXPORT_BIBLIOGRAPHY`

**Example:**
```bash
export EXPORT_BIBLIOGRAPHY="true"
```

### Minimum Peer-Reviewed Sources

Minimum number of peer-reviewed sources to include.

**Default:** `5`

**Environment Variable:** `MIN_PEER_REVIEWED_SOURCES`

**Example:**
```bash
export MIN_PEER_REVIEWED_SOURCES="10"
```

**Validation:**
- Must be non-negative

### Source Quality Threshold

Minimum quality score (0-10) for sources to be included.

**Default:** `7`

**Environment Variable:** `SOURCE_QUALITY_THRESHOLD`

**Example:**
```bash
export SOURCE_QUALITY_THRESHOLD="8"
```

**Validation:**
- Must be between 0 and 10

## Usage Examples

### Using Environment Variables

```bash
# Configure for a STEM literature review
export CITATION_STYLE="ieee"
export OUTPUT_FORMAT="review"
export DISCIPLINE="stem"
export WORD_COUNT_TARGET="6000"
export MIN_PEER_REVIEWED_SOURCES="15"

# Run your research command
python -m gazzali.ask "What are recent advances in quantum computing?"
```

### Using Python API

```python
from gazzali.academic_config import AcademicConfig, CitationStyle, OutputFormat, Discipline

# Create custom configuration
config = AcademicConfig(
    citation_style=CitationStyle.APA,
    output_format=OutputFormat.PAPER,
    discipline=Discipline.SOCIAL,
    word_count_target=10000,
    include_abstract=True,
    include_methodology=True,
    scholar_priority=True,
    min_peer_reviewed=8
)

# Validate configuration
issues = config.validate()
if issues:
    print("Configuration issues:", issues)

# Get prompt modifiers for AI
modifiers = config.get_prompt_modifiers()
print(modifiers["terminology"])
print(modifiers["methodology_focus"])

# Get report structure
sections = config.get_report_structure()
print("Report sections:", sections)
```

### Loading from Environment

```python
from gazzali.academic_config import AcademicConfig

# Load configuration from environment variables
config = AcademicConfig.from_env()

# Display configuration
print(config)
```

### Loading from Command-Line Arguments

```python
import argparse
from gazzali.academic_config import AcademicConfig

parser = argparse.ArgumentParser()
parser.add_argument('--citation-style', dest='citation_style')
parser.add_argument('--output-format', dest='output_format')
parser.add_argument('--discipline')
parser.add_argument('--word-count', type=int, dest='word_count')
parser.add_argument('--export-bib', action='store_true', dest='export_bib')

args = parser.parse_args()
config = AcademicConfig.from_args(args)
```

## Discipline-Specific Features

### STEM
- Technical and scientific terminology
- Focus on experimental design and quantitative methods
- Emphasis on reproducibility and empirical validation
- Statistical analysis and data-driven approaches

### Social Sciences
- Social science theoretical frameworks
- Qualitative and quantitative research methods
- Surveys, interviews, ethnography
- Emphasis on validity, reliability, generalizability

### Humanities
- Critical theory and hermeneutics
- Textual analysis and interpretation
- Historical and comparative methods
- Close reading and contextual understanding

### Medical
- Medical and clinical terminology
- Clinical trials and systematic reviews
- Evidence-based practice
- Patient outcomes and clinical significance

## Output Format Structures

### Paper
- Abstract (optional)
- Introduction
- Literature Review
- Methodology (optional)
- Findings
- Discussion
- Conclusion
- References

### Literature Review
- Abstract (optional)
- Introduction
- Thematic Analysis
- Research Gaps
- Future Directions
- References

### Research Proposal
- Background
- Research Questions
- Literature Review
- Proposed Methodology
- Expected Outcomes
- Timeline
- References

### Abstract
- Single section: Abstract (250-300 words)

### Presentation
- Overview
- Key Findings
- Implications
- Conclusions

## Validation

The configuration includes built-in validation to catch common issues:

```python
config = AcademicConfig(word_count_target=100)
issues = config.validate()
# Returns: ["Word count target (100) is very low. Consider at least 500 words..."]
```

Common validation checks:
- Word count within reasonable range
- Abstract format with appropriate word count
- Non-negative minimum peer-reviewed sources
- Quality threshold between 0-10

## Best Practices

1. **Match format to purpose**: Use `paper` for comprehensive research, `review` for literature surveys, `proposal` for grant applications
2. **Set realistic word counts**: 5,000-10,000 for papers, 3,000-6,000 for reviews, 250-300 for abstracts
3. **Enable Scholar priority**: For academic research, prioritize scholarly sources
4. **Discipline-specific settings**: Choose the appropriate discipline for better terminology and methodology guidance
5. **Validate before use**: Always call `validate()` to catch configuration issues early

## Integration with Research Pipeline

The academic configuration integrates with the research pipeline to:
- Modify AI prompts with discipline-specific instructions
- Structure reports according to format requirements
- Filter and prioritize sources based on quality thresholds
- Generate appropriate citations in the specified style
- Ensure minimum peer-reviewed source requirements

## Troubleshooting

**Issue:** Configuration not loading from environment
- **Solution:** Ensure environment variables are exported before running the application
- **Check:** Use `echo $CITATION_STYLE` to verify variable is set

**Issue:** Validation errors
- **Solution:** Review validation messages and adjust values accordingly
- **Check:** Call `config.validate()` to see specific issues

**Issue:** Unexpected report structure
- **Solution:** Verify `output_format` is set correctly
- **Check:** Use `config.get_report_structure()` to preview sections

## API Reference

### Classes

#### `AcademicConfig`
Main configuration dataclass with all academic settings.

#### `CitationStyle`
Enum for citation format options.

#### `OutputFormat`
Enum for document format options.

#### `Discipline`
Enum for academic discipline options.

### Functions

#### `get_default_config() -> AcademicConfig`
Returns a configuration instance with default values.

#### `AcademicConfig.from_env() -> AcademicConfig`
Creates configuration from environment variables.

#### `AcademicConfig.from_args(args) -> AcademicConfig`
Creates configuration from command-line arguments.

#### `config.get_prompt_modifiers() -> Dict[str, str]`
Returns discipline and format-specific prompt modifiers.

#### `config.get_report_structure() -> List[str]`
Returns ordered list of report sections for the format.

#### `config.validate() -> List[str]`
Validates configuration and returns list of issues.

#### `config.to_dict() -> Dict[str, Any]`
Converts configuration to dictionary representation.
