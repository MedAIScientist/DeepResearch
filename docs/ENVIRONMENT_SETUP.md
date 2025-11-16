# Environment Setup Guide

This guide explains how to configure Gazzali Research using environment variables for both general research and academic-specific features.

## Table of Contents

- [Quick Start](#quick-start)
- [Core Configuration](#core-configuration)
- [Academic Research Settings](#academic-research-settings)
- [Configuration Methods](#configuration-methods)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)

## Quick Start

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your API keys:
   ```bash
   OPENROUTER_API_KEY="sk-or-your-openrouter-key"
   SERPER_API_KEY="serper-your-key"
   JINA_API_KEY="jina-your-key"
   ```

3. (Optional) Configure academic settings for scholarly research:
   ```bash
   CITATION_STYLE="apa"
   OUTPUT_FORMAT="paper"
   DISCIPLINE="stem"
   ```

4. Run Gazzali Research:
   ```bash
   python -m src.gazzali.ask "Your research question"
   ```

## Core Configuration

### Required API Keys

These API keys are required for Gazzali Research to function:

#### `OPENROUTER_API_KEY`
- **Required**: Yes
- **Description**: API key for OpenRouter (provides access to various LLMs)
- **Format**: `sk-or-...`
- **Get it from**: [openrouter.ai](https://openrouter.ai/)

#### `SERPER_API_KEY`
- **Required**: Yes
- **Description**: API key for Serper (Google search API)
- **Format**: Custom key from Serper
- **Get it from**: [serper.dev](https://serper.dev/)

#### `JINA_API_KEY`
- **Required**: Yes
- **Description**: API key for Jina Reader (web content extraction)
- **Format**: Custom key from Jina
- **Get it from**: [jina.ai](https://jina.ai/)

### Optional Core Settings

#### `MODEL_PATH`
- **Default**: Empty (uses default model)
- **Description**: Path to custom model configuration
- **Example**: `"/path/to/model"`

#### `OUTPUT_PATH`
- **Default**: Empty (uses default output directory)
- **Description**: Custom path for saving research outputs
- **Example**: `"./research_outputs"`

#### `TEMPERATURE`
- **Default**: `0.85`
- **Description**: Model temperature for response generation (0.0-2.0)
- **Higher values**: More creative/random outputs
- **Lower values**: More focused/deterministic outputs

#### `PRESENCE_PENALTY`
- **Default**: `1.1`
- **Description**: Penalty for token repetition (0.0-2.0)
- **Higher values**: Less repetition

#### `MAX_WORKERS`
- **Default**: `1`
- **Description**: Number of parallel workers for research tasks

#### `ROLLOUT_COUNT`
- **Default**: `1`
- **Description**: Number of research rollouts to perform

### OpenRouter Configuration

#### `OPENROUTER_MAX_RETRIES`
- **Default**: `3`
- **Description**: Maximum retry attempts for failed API calls

#### `OPENROUTER_TIMEOUT`
- **Default**: `180`
- **Description**: Request timeout in seconds

#### `OPENROUTER_RETRY_BASE`
- **Default**: `0.5`
- **Description**: Base delay for exponential backoff (seconds)

#### `OPENROUTER_RETRY_MAX_SLEEP`
- **Default**: `6`
- **Description**: Maximum sleep time between retries (seconds)

### Reporting Model Configuration

#### `REPORT_MODEL`
- **Default**: `x-ai/grok-4-fast`
- **Description**: Model used for report synthesis
- **Options**: Any OpenRouter-supported model
- **Examples**: 
  - `x-ai/grok-4-fast` (fast, high quality)
  - `anthropic/claude-3.5-sonnet` (excellent for academic writing)
  - `openai/gpt-4-turbo` (strong general performance)

#### `REPORT_CONTEXT_LIMIT`
- **Default**: `2000000`
- **Description**: Maximum context tokens for report generation

#### `REPORT_MAX_TOKENS`
- **Default**: `800000`
- **Description**: Maximum output tokens for reports

## Academic Research Settings

These settings enable and configure academic-specific features for scholarly research.

### Citation Style

#### `CITATION_STYLE`
- **Default**: `apa`
- **Options**: `apa`, `mla`, `chicago`, `ieee`
- **Description**: Academic citation format for inline citations and bibliography

**Citation Style Details:**

| Style | Full Name | Common In | Inline Format | Example |
|-------|-----------|-----------|---------------|---------|
| `apa` | APA 7th Edition | Psychology, Education, Social Sciences | (Author, Year) | (Smith, 2023) |
| `mla` | MLA 9th Edition | Humanities, Literature, Arts | (Author Page) | (Smith 45) |
| `chicago` | Chicago 17th Edition | History, Arts, Humanities | (Author Year) or Footnotes | (Smith 2023) |
| `ieee` | IEEE Style | Engineering, Computer Science | [Number] | [1] |

**Example:**
```bash
CITATION_STYLE="apa"
```

### Output Format

#### `OUTPUT_FORMAT`
- **Default**: `paper`
- **Options**: `paper`, `review`, `proposal`, `abstract`, `presentation`
- **Description**: Document structure and format for generated reports

**Format Details:**

| Format | Description | Typical Length | Sections |
|--------|-------------|----------------|----------|
| `paper` | Full research paper | 5,000-10,000 words | Abstract, Introduction, Literature Review, Methodology, Findings, Discussion, Conclusion, References |
| `review` | Literature review | 4,000-8,000 words | Abstract, Introduction, Thematic Analysis, Research Gaps, Future Directions, References |
| `proposal` | Research proposal | 3,000-6,000 words | Background, Research Questions, Literature Review, Proposed Methodology, Expected Outcomes, Timeline, References |
| `abstract` | Conference abstract | 250-500 words | Single structured paragraph or short sections |
| `presentation` | Presentation summary | 1,000-2,000 words | Overview, Key Findings, Implications, Conclusions |

**Example:**
```bash
OUTPUT_FORMAT="review"
```

### Academic Discipline

#### `DISCIPLINE`
- **Default**: `general`
- **Options**: `general`, `stem`, `social`, `humanities`, `medical`
- **Description**: Discipline-specific terminology and conventions

**Discipline Details:**

| Discipline | Focus Areas | Terminology | Methodology Emphasis |
|------------|-------------|-------------|---------------------|
| `general` | Interdisciplinary | Accessible, clear | Mixed methods |
| `stem` | Science, Technology, Engineering, Math | Technical, quantitative | Experimental, statistical |
| `social` | Psychology, Sociology, Economics | Social science frameworks | Surveys, mixed methods |
| `humanities` | Literature, Philosophy, History | Critical theory, interpretive | Textual analysis, hermeneutics |
| `medical` | Medicine, Clinical Research | Clinical, evidence-based | Clinical trials, systematic reviews |

**Example:**
```bash
DISCIPLINE="stem"
```

### Word Count Target

#### `WORD_COUNT_TARGET`
- **Default**: `8000`
- **Range**: `500` - `50000`
- **Description**: Target word count for generated reports

**Recommendations:**
- **Abstract**: 250-500 words
- **Conference paper**: 3,000-5,000 words
- **Journal article**: 5,000-10,000 words
- **Literature review**: 8,000-15,000 words
- **Dissertation chapter**: 10,000-20,000 words

**Example:**
```bash
WORD_COUNT_TARGET="5000"
```

### Section Inclusion

#### `INCLUDE_ABSTRACT`
- **Default**: `true`
- **Options**: `true`, `false`
- **Description**: Include abstract section in reports (except when OUTPUT_FORMAT is `abstract`)

**Example:**
```bash
INCLUDE_ABSTRACT="true"
```

#### `INCLUDE_METHODOLOGY`
- **Default**: `true`
- **Options**: `true`, `false`
- **Description**: Include methodology section in reports

**Example:**
```bash
INCLUDE_METHODOLOGY="false"
```

### Search Strategy

#### `SCHOLAR_PRIORITY`
- **Default**: `true`
- **Options**: `true`, `false`
- **Description**: Prioritize Google Scholar searches over general web search

When enabled, the system will:
1. Search Google Scholar first for academic sources
2. Extract citation metadata from scholarly articles
3. Fall back to general web search if needed
4. Prioritize peer-reviewed sources in synthesis

**Example:**
```bash
SCHOLAR_PRIORITY="true"
```

### Bibliography Export

#### `EXPORT_BIBLIOGRAPHY`
- **Default**: `false`
- **Options**: `true`, `false`
- **Description**: Export bibliography to separate `.bib` file (BibTeX format)

When enabled, a BibTeX file will be created alongside the report containing all citations in a format compatible with LaTeX and reference managers (Zotero, Mendeley, etc.).

**Example:**
```bash
EXPORT_BIBLIOGRAPHY="true"
```

### Source Quality Controls

#### `MIN_PEER_REVIEWED_SOURCES`
- **Default**: `5`
- **Range**: `0` - `100`
- **Description**: Minimum number of peer-reviewed sources to include

The system will warn if this threshold is not met during research. Set to `0` to disable this check.

**Example:**
```bash
MIN_PEER_REVIEWED_SOURCES="10"
```

#### `SOURCE_QUALITY_THRESHOLD`
- **Default**: `7`
- **Range**: `0` - `10`
- **Description**: Minimum quality score for sources

**Quality Scoring:**
- **10**: Peer-reviewed journal articles, conference proceedings
- **7**: Institutional publications, government reports, university websites
- **5**: Professional organizations, established news outlets
- **3**: General websites, blogs
- **0**: Any source (no filtering)

**Example:**
```bash
SOURCE_QUALITY_THRESHOLD="8"
```

## Configuration Methods

Gazzali Research supports multiple configuration methods with the following priority order:

1. **Command-line arguments** (highest priority)
2. **Environment variables** (from `.env` file)
3. **Default values** (lowest priority)

### Method 1: Environment File (Recommended)

Edit your `.env` file:

```bash
# Academic settings
CITATION_STYLE="apa"
OUTPUT_FORMAT="paper"
DISCIPLINE="stem"
WORD_COUNT_TARGET="8000"
SCHOLAR_PRIORITY="true"
```

### Method 2: Command-Line Arguments

Override environment settings with CLI flags:

```bash
python -m src.gazzali.ask \
  --academic \
  --citation-style mla \
  --output-format review \
  --discipline humanities \
  --word-count 5000 \
  "Your research question"
```

### Method 3: Programmatic Configuration

Use the `AcademicConfig` class in Python:

```python
from src.gazzali.academic_config import AcademicConfig, CitationStyle, OutputFormat

# Load from environment
config = AcademicConfig.from_env()

# Or create manually
config = AcademicConfig(
    citation_style=CitationStyle.APA,
    output_format=OutputFormat.PAPER,
    discipline="stem",
    word_count_target=8000
)
```

## Examples

### Example 1: STEM Research Paper

```bash
# .env configuration
CITATION_STYLE="ieee"
OUTPUT_FORMAT="paper"
DISCIPLINE="stem"
WORD_COUNT_TARGET="6000"
SCHOLAR_PRIORITY="true"
MIN_PEER_REVIEWED_SOURCES="10"
SOURCE_QUALITY_THRESHOLD="8"
INCLUDE_ABSTRACT="true"
INCLUDE_METHODOLOGY="true"
```

### Example 2: Humanities Literature Review

```bash
# .env configuration
CITATION_STYLE="mla"
OUTPUT_FORMAT="review"
DISCIPLINE="humanities"
WORD_COUNT_TARGET="8000"
SCHOLAR_PRIORITY="true"
MIN_PEER_REVIEWED_SOURCES="15"
SOURCE_QUALITY_THRESHOLD="7"
INCLUDE_ABSTRACT="true"
```

### Example 3: Social Science Research Proposal

```bash
# .env configuration
CITATION_STYLE="apa"
OUTPUT_FORMAT="proposal"
DISCIPLINE="social"
WORD_COUNT_TARGET="4000"
SCHOLAR_PRIORITY="true"
MIN_PEER_REVIEWED_SOURCES="8"
SOURCE_QUALITY_THRESHOLD="7"
INCLUDE_METHODOLOGY="true"
EXPORT_BIBLIOGRAPHY="true"
```

### Example 4: Conference Abstract

```bash
# .env configuration
CITATION_STYLE="apa"
OUTPUT_FORMAT="abstract"
DISCIPLINE="medical"
WORD_COUNT_TARGET="300"
SCHOLAR_PRIORITY="true"
MIN_PEER_REVIEWED_SOURCES="5"
SOURCE_QUALITY_THRESHOLD="9"
```

### Example 5: Quick General Research (Non-Academic)

```bash
# .env configuration - minimal academic settings
SCHOLAR_PRIORITY="false"
SOURCE_QUALITY_THRESHOLD="3"
MIN_PEER_REVIEWED_SOURCES="0"
```

## Troubleshooting

### Issue: Citations Not Appearing

**Symptoms**: Generated report lacks citations or bibliography

**Solutions:**
1. Ensure `SCHOLAR_PRIORITY="true"` to enable academic source discovery
2. Check that `MIN_PEER_REVIEWED_SOURCES` is not set too high
3. Verify your research question is specific enough for academic sources
4. Lower `SOURCE_QUALITY_THRESHOLD` if too restrictive

### Issue: Report Too Short/Long

**Symptoms**: Generated report doesn't match expected length

**Solutions:**
1. Adjust `WORD_COUNT_TARGET` to desired length
2. Ensure `OUTPUT_FORMAT` matches your needs (abstract vs. paper)
3. Check that `INCLUDE_ABSTRACT` and `INCLUDE_METHODOLOGY` are set appropriately
4. Consider breaking very long reports into multiple queries

### Issue: Wrong Citation Format

**Symptoms**: Citations don't match expected style

**Solutions:**
1. Verify `CITATION_STYLE` is set correctly (apa, mla, chicago, ieee)
2. Check for typos in the style name (must be lowercase)
3. Ensure `.env` file is in the project root directory
4. Try overriding with command-line flag: `--citation-style apa`

### Issue: Not Enough Academic Sources

**Symptoms**: Warning about insufficient peer-reviewed sources

**Solutions:**
1. Refine your research question to be more specific
2. Lower `MIN_PEER_REVIEWED_SOURCES` if appropriate
3. Ensure `SCHOLAR_PRIORITY="true"` is enabled
4. Check that Google Scholar is accessible (not blocked by firewall)
5. Verify `SERPER_API_KEY` is valid and has quota remaining

### Issue: Environment Variables Not Loading

**Symptoms**: Settings from `.env` file are ignored

**Solutions:**
1. Ensure `.env` file is in the project root (same directory as `.env.example`)
2. Check file permissions (must be readable)
3. Verify no syntax errors in `.env` file (no spaces around `=`)
4. Restart your terminal/IDE after editing `.env`
5. Check for typos in variable names (case-sensitive)

### Issue: Invalid Configuration Values

**Symptoms**: Errors about invalid settings

**Solutions:**
1. Check that enum values are lowercase (e.g., `apa` not `APA`)
2. Verify boolean values are `true` or `false` (lowercase)
3. Ensure numeric values are valid integers
4. Check that `SOURCE_QUALITY_THRESHOLD` is between 0-10
5. Verify `WORD_COUNT_TARGET` is between 500-50000

## Advanced Configuration

### Custom Model Selection

For academic writing, consider these models:

```bash
# Excellent for academic writing
REPORT_MODEL="anthropic/claude-3.5-sonnet"

# Fast and cost-effective
REPORT_MODEL="x-ai/grok-4-fast"

# Strong reasoning for complex topics
REPORT_MODEL="openai/gpt-4-turbo"
```

### Performance Tuning

For faster research with acceptable quality:

```bash
TEMPERATURE="0.7"
MAX_WORKERS="2"
OPENROUTER_TIMEOUT="120"
```

For highest quality (slower):

```bash
TEMPERATURE="0.85"
MAX_WORKERS="1"
OPENROUTER_TIMEOUT="300"
```

### Cost Optimization

To reduce API costs:

```bash
# Use faster, cheaper models
REPORT_MODEL="x-ai/grok-4-fast"

# Reduce word count
WORD_COUNT_TARGET="5000"

# Lower source requirements
MIN_PEER_REVIEWED_SOURCES="3"

# Reduce retries
OPENROUTER_MAX_RETRIES="2"
```

## See Also

- [Academic Configuration Guide](ACADEMIC_CONFIG.md) - Detailed academic features
- [Chunked Workflow](CHUNKED_WORKFLOW.md) - Research decomposition strategy
- [Reporting Pipeline](REPORTING_PIPELINE.md) - Report generation process
- [README](../README.md) - Main project documentation

## Support

For issues or questions:
1. Check this documentation first
2. Review example configurations above
3. Verify API keys are valid and have quota
4. Check the project README for updates
5. Open an issue on the project repository
