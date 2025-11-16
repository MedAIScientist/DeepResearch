# CLI Output and Messaging Guide

This document describes the enhanced CLI output and messaging system in Gazzali Research, particularly for academic mode.

## Overview

Gazzali Research provides rich, informative CLI output with:
- Visual progress indicators for each workflow stage
- Academic mode indicators and configuration display
- Citation counts and source quality metrics
- Refined question display when using `--refine`
- Stage-by-stage progress tracking
- Academic-specific success messages

## Output Stages

### Standard Mode

In standard research mode, the CLI displays:

1. **Environment Check**
   - API key validation
   - Configuration warnings
   - Service availability

2. **Research Stage**
   - Research agent launch
   - Progress indicators
   - Tool usage logs

3. **Results Display**
   - Research findings
   - Output file location
   - Report preview

### Academic Mode

Academic mode adds enhanced output with three distinct stages:

#### Stage 1: Question Refinement (if `--refine` flag used)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔍 STAGE 1: Question Refinement
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Analyzing research question for academic rigor...

✅ Question Refinement Complete!

Original Question:
  [Your original question]

Refined Questions:
  → 1. [First refined question - will be used]
    2. [Second refined question]
    3. [Third refined question]

Quality Assessment:
  • Question Type:  Descriptive/Comparative/Causal
  • Scope:          Appropriate/Too Broad/Too Narrow
  • Key Variables:  [List of identified variables]

Using refined question for research...
```

#### Stage 2: Deep Research

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔬 STAGE 2: Deep Research
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Academic Mode: Prioritizing peer-reviewed sources
Research Agent: Tongyi DeepResearch 30B
Search Strategy: Scholar-first with quality filtering

[Research agent output follows...]
```

#### Stage 3: Academic Report Generation

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📝 STAGE 3: Academic Report Generation
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Synthesizing research into academic format...
  • Format: Paper
  • Citation Style: APA
  • Target Length: 8,000 words

Generating structured sections...

✅ Academic Report Complete!

📁 Output:
  /path/to/outputs/reports/academic_paper_20241117_120000_topic.md

📊 Report Metrics:
  • Word Count:        7,842
  • Sections:          8
  • Citations:         45
  • Peer-Reviewed:     38 (84.4%)
  • Highly Cited:      12 sources

✓ Bibliography exported: /path/to/outputs/reports/academic_paper_20241117_120000_topic.bib
```

## Academic Mode Configuration Display

When academic mode is enabled, the CLI displays a formatted configuration box:

```
╔════════════════════════════════════════════════════════════════╗
║ 📚 ACADEMIC MODE ENABLED                                      ║
╚════════════════════════════════════════════════════════════════╝

Configuration:
  • Citation Style:     APA
  • Output Format:      Paper
  • Discipline:         General
  • Word Count Target:  8,000
  • Scholar Priority:   Enabled
```

## Source Quality Metrics

Academic mode displays detailed source quality metrics:

### Citation Count
Shows the total number of sources cited in the report:
```
• Citations:         45
```

### Peer-Reviewed Percentage
Indicates the percentage of sources from peer-reviewed venues (journals, conferences):
```
• Peer-Reviewed:     38 (84.4%)
```

### Highly Cited Sources
Counts sources with more than 100 citations:
```
• Highly Cited:      12 sources
```

## Success Messages

### Academic Mode Success

```
╔════════════════════════════════════════════════════════════════╗
║ ✅ ACADEMIC RESEARCH COMPLETE                              ║
╚════════════════════════════════════════════════════════════════╝

Your scholarly report is ready!
  • Peer-reviewed sources prioritized
  • Proper APA citations
  • Academic writing standards applied
  • Paper format structure
```

### Standard Mode Success

```
╔════════════════════════════════════════════════════════════════╗
║ ✅ RESEARCH COMPLETE                                       ║
╚════════════════════════════════════════════════════════════════╝
```

## Color Coding

The CLI uses color coding for better readability:

- **Green (✓, ✅)**: Success indicators, completed stages
- **Cyan**: Section headers, stage dividers
- **Yellow (⚠️)**: Warnings, non-critical issues
- **Red (❌)**: Errors, failures
- **Bold**: Important labels, section titles

## Progress Indicators

### Stage Headers
Each major stage is clearly marked with:
- Horizontal divider lines
- Stage number and name
- Emoji icon for visual identification

### Substep Indicators
Within stages, substeps are shown with:
- Bullet points for configuration items
- Checkmarks for completed actions
- Descriptive text for current operations

## Error Handling

### Configuration Warnings
Non-critical configuration issues are displayed with warning symbols:
```
⚠️  Configuration Warnings:
   - SERPER_API_KEY not set (web search may not work)
```

### Critical Errors
Critical errors that prevent execution are shown in red:
```
❌ Errors:
   - OPENROUTER_API_KEY is not set

Please export required API keys:
   export OPENROUTER_API_KEY="sk-or-v1-your-key"
```

## Examples

### Example 1: Standard Research

```bash
python -m gazzali.gazzali "What are the latest developments in quantum computing?"
```

Output shows:
1. Environment check
2. Research stage with agent output
3. Results display with report location

### Example 2: Academic Research with Refinement

```bash
python -m gazzali.gazzali --academic --refine --citation-style apa \
  "quantum computing applications"
```

Output shows:
1. Academic mode configuration
2. Stage 1: Question refinement with quality assessment
3. Stage 2: Deep research with academic indicators
4. Stage 3: Report generation with detailed metrics
5. Academic success message with quality indicators

### Example 3: Literature Review

```bash
python -m gazzali.gazzali --academic --output-format review \
  --discipline stem "machine learning in healthcare"
```

Output shows:
1. Academic configuration with "Review" format
2. Research stage with Scholar-first strategy
3. Report generation with literature review structure
4. Metrics showing peer-reviewed source percentage

## Customization

### Disabling Colors

If your terminal doesn't support colors, you can disable them by setting:
```bash
export NO_COLOR=1
```

### Verbose Output

For more detailed output during research, check the research agent logs in the output directory.

## Tips

1. **Monitor Progress**: Watch the stage indicators to understand where the process is
2. **Check Metrics**: Review citation counts and peer-review percentages to assess quality
3. **Review Warnings**: Address configuration warnings for optimal performance
4. **Save Output**: Redirect output to a file for later review:
   ```bash
   python -m gazzali.gazzali "question" 2>&1 | tee research.log
   ```

## Related Documentation

- [Academic Mode Guide](ACADEMIC_MODE.md) - Complete academic features guide
- [Citation Styles](CITATION_STYLES.md) - Citation formatting examples
- [Output Formats](OUTPUT_FORMATS.md) - Report format descriptions
- [Environment Setup](ENVIRONMENT_SETUP.md) - Configuration guide
