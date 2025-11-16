# Gazzali Research CLI Interface

## Overview

The Gazzali Research CLI (`gazzali.py`) is the main command-line interface for the academic AI research assistant. It provides both standard research capabilities and enhanced academic features including citation management, literature review synthesis, and scholarly output formats.

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys
```

## Basic Usage

### Interactive Mode

Launch the CLI without arguments to enter interactive mode:

```bash
python -m gazzali.gazzali
```

You'll be prompted to enter your research question. Press Enter twice (blank line) to submit.

### Direct Question Mode

Provide your research question as a command-line argument:

```bash
python -m gazzali.gazzali "What are the major AI safety milestones in 2024?"
```

## Academic Mode

Enable academic mode with the `--academic` flag for enhanced scholarly features:

```bash
python -m gazzali.gazzali --academic "Impact of AI on education"
```

### Academic Mode Features

- **Citation Management**: Automatic tracking and formatting of sources
- **Scholar Priority**: Prioritizes Google Scholar over general web search
- **Academic Writing Style**: Formal, objective, third-person perspective
- **Structured Sections**: Abstract, Introduction, Literature Review, etc.
- **Bibliography Generation**: Properly formatted reference list

## Command-Line Arguments

### Positional Arguments

- `question` - Research question (optional in interactive mode)

### Academic Mode Arguments

#### `--academic`
Enable academic research mode with enhanced features.

```bash
python -m gazzali.gazzali --academic "Research question"
```

#### `--citation-style {apa,mla,chicago,ieee}`
Specify citation format style (default: apa).

```bash
python -m gazzali.gazzali --academic --citation-style mla "Research question"
```

**Supported Styles:**
- `apa` - APA 7th Edition (default)
- `mla` - MLA 9th Edition
- `chicago` - Chicago 17th Edition
- `ieee` - IEEE Citation Style

#### `--output-format {paper,review,proposal,abstract,presentation}`
Specify output document format (default: paper).

```bash
python -m gazzali.gazzali --academic --output-format review "Research question"
```

**Supported Formats:**
- `paper` - Full research paper with all sections
- `review` - Literature review format
- `proposal` - Research proposal format
- `abstract` - Conference abstract (250-300 words)
- `presentation` - Presentation-ready summary

#### `--discipline {general,stem,social,humanities,medical}`
Specify academic discipline for terminology and conventions (default: general).

```bash
python -m gazzali.gazzali --academic --discipline stem "Research question"
```

**Supported Disciplines:**
- `general` - General academic writing
- `stem` - Science, Technology, Engineering, Mathematics
- `social` - Social sciences (psychology, sociology, economics)
- `humanities` - Humanities (literature, philosophy, history)
- `medical` - Medical and health sciences

#### `--refine`
Refine research question before starting research.

```bash
python -m gazzali.gazzali --academic --refine "Broad research topic"
```

This uses the QuestionRefiner to:
- Assess question quality using FINER criteria
- Identify question type (descriptive, comparative, causal)
- Suggest scope improvements
- Generate focused research questions

#### `--word-count COUNT`
Specify target word count for report (default: 8000).

```bash
python -m gazzali.gazzali --academic --word-count 5000 "Research question"
```

#### `--export-bib`
Export bibliography to separate .bib file.

```bash
python -m gazzali.gazzali --academic --export-bib "Research question"
```

### General Arguments

#### `--chunked`
Enable chunked research mode for very large topics.

```bash
python -m gazzali.gazzali --chunked "Map the global AI regulation landscape"
```

Chunked mode:
- Decomposes large questions into sub-questions
- Researches each chunk independently
- Synthesizes results into comprehensive report

#### `--no-keep`
Do not keep temporary dataset files (default: files are cleaned up).

```bash
python -m gazzali.gazzali --no-keep "Research question"
```

#### `--output-dir PATH`
Specify custom output directory (default: `<project>/outputs`).

```bash
python -m gazzali.gazzali --output-dir ./my_research "Research question"
```

## Usage Examples

### Example 1: Standard Research

```bash
python -m gazzali.gazzali "What are the latest developments in quantum computing?"
```

### Example 2: Academic Paper with APA Citations

```bash
python -m gazzali.gazzali \
  --academic \
  --citation-style apa \
  --output-format paper \
  "Impact of artificial intelligence on educational outcomes"
```

### Example 3: Literature Review in Social Sciences

```bash
python -m gazzali.gazzali \
  --academic \
  --output-format review \
  --discipline social \
  --citation-style apa \
  "Social media effects on adolescent mental health"
```

### Example 4: STEM Research Proposal

```bash
python -m gazzali.gazzali \
  --academic \
  --output-format proposal \
  --discipline stem \
  --citation-style ieee \
  "Novel approaches to carbon capture technology"
```

### Example 5: Medical Research with Question Refinement

```bash
python -m gazzali.gazzali \
  --academic \
  --discipline medical \
  --refine \
  --export-bib \
  "Treatment options for chronic pain"
```

### Example 6: Conference Abstract

```bash
python -m gazzali.gazzali \
  --academic \
  --output-format abstract \
  --word-count 300 \
  "Machine learning applications in drug discovery"
```

### Example 7: Chunked Research for Large Topics

```bash
python -m gazzali.gazzali \
  --chunked \
  --academic \
  --output-format review \
  "Comprehensive analysis of global climate change policies"
```

## Environment Variables

You can configure default settings using environment variables in `.env`:

```bash
# Academic Mode Settings
ACADEMIC_MODE=true
CITATION_STYLE=apa
OUTPUT_FORMAT=paper
DISCIPLINE=general
SCHOLAR_PRIORITY=true
WORD_COUNT_TARGET=8000

# Citation Export
EXPORT_BIBLIOGRAPHY=false

# Advanced Academic Settings
SOURCE_QUALITY_THRESHOLD=7
MIN_PEER_REVIEWED_SOURCES=5
METHODOLOGY_EXTRACTION=true
THEORY_EXTRACTION=true

# API Keys
OPENROUTER_API_KEY=sk-or-v1-your-key
SERPER_API_KEY=your-serper-key
JINA_API_KEY=your-jina-key

# Research Agent Settings
TEMPERATURE=0.85
PRESENCE_PENALTY=1.1
MAX_WORKERS=1
ROLLOUT_COUNT=1

# Report Generation
REPORT_MODEL=x-ai/grok-4-fast
```

## Output Files

The CLI generates several output files in the output directory:

### Standard Mode

- `outputs/iter*.jsonl` - Raw research results from DeepResearch agent
- `outputs/reports/report_TIMESTAMP.md` - Basic markdown report
- `outputs/reports/comprehensive_TIMESTAMP.md` - Comprehensive synthesis report

### Academic Mode

- `outputs/reports/academic_FORMAT_TIMESTAMP_QUESTION.md` - Academic report
- `outputs/reports/academic_FORMAT_TIMESTAMP_QUESTION.bib` - Bibliography (if `--export-bib`)

### Chunked Mode

- `outputs/reports/chunked_synthesis_TIMESTAMP_QUESTION.md` - Synthesized chunked report

## Workflow

1. **Environment Check**: Validates API keys and configuration
2. **Question Input**: Gets question from user (interactive or argument)
3. **Question Refinement** (optional): Refines broad topics into specific questions
4. **Configuration Display** (academic mode): Shows academic settings
5. **Research Execution**: Runs DeepResearch agent
6. **Result Processing**: Extracts and displays findings
7. **Report Generation**: Creates formatted reports
8. **Bibliography Export** (optional): Exports citations to .bib file
9. **Cleanup**: Removes temporary files (unless `--no-keep`)

## Troubleshooting

### API Key Issues

```
❌ Errors:
   - OPENROUTER_API_KEY is not set
```

**Solution**: Export your OpenRouter API key:
```bash
export OPENROUTER_API_KEY="sk-or-v1-your-key"
```

### Research Process Failed

```
❌ Research process failed: ...
```

**Solution**: Check that:
- API keys are valid
- Internet connection is stable
- DeepResearch inference directory exists
- Python dependencies are installed

### Academic Report Generation Failed

```
⚠️  Academic report generation not available: ...
```

**Solution**: Ensure academic modules are available:
```bash
pip install -r requirements.txt
```

### Question Refinement Failed

```
⚠️  Question refinement failed: ...
```

**Solution**: 
- Check API key is valid
- Ensure QuestionRefiner module is available
- Try without `--refine` flag

## Migration from ask.py

The new `gazzali.py` CLI maintains backward compatibility with `ask.py`:

```bash
# Old way
python -m gazzali.ask "Research question"

# New way (equivalent)
python -m gazzali.gazzali "Research question"
```

All existing functionality from `ask.py` is preserved in `gazzali.py`, with additional academic features available via the `--academic` flag.

## Advanced Usage

### Custom Report Models

Override the default synthesis model:

```bash
export REPORT_MODEL="anthropic/claude-3.5-sonnet"
python -m gazzali.gazzali --academic "Research question"
```

**Supported Models:**
- `x-ai/grok-4-fast` (default)
- `anthropic/claude-3.5-sonnet`
- `openai/gpt-4o`
- `moonshotai/kimi-k2-0905`

### Combining Multiple Flags

```bash
python -m gazzali.gazzali \
  --academic \
  --citation-style chicago \
  --output-format proposal \
  --discipline humanities \
  --refine \
  --word-count 6000 \
  --export-bib \
  --output-dir ./my_research \
  "Philosophical implications of artificial consciousness"
```

## See Also

- [Academic Mode Documentation](ACADEMIC_MODE.md)
- [Citation Styles Guide](CITATION_STYLES.md)
- [Output Formats Reference](OUTPUT_FORMATS.md)
- [Discipline Settings](DISCIPLINE_SETTINGS.md)
- [Environment Setup](ENVIRONMENT_SETUP.md)
