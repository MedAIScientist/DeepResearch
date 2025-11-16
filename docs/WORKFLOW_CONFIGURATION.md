# Workflow Configuration Guide

## Overview

Gazzali Research provides a flexible workflow configuration system that allows you to:

1. **Use preset workflow templates** for common research tasks
2. **Customize workflows** by overriding specific settings
3. **Save custom workflows** for reuse across projects
4. **Load custom workflows** to maintain consistency

This guide explains how to use and manage workflow configurations effectively.

---

## Quick Start

### List Available Workflows

```bash
python -m gazzali.gazzali --list-workflows
```

This displays all available preset workflow templates with their descriptions, word count ranges, and minimum source requirements.

### Use a Preset Workflow

```bash
python -m gazzali.gazzali --academic --workflow literature_review \
    "What are the current approaches to explainable AI in healthcare?"
```

### Save a Custom Workflow

```bash
# Configure your settings and save
python -m gazzali.gazzali --academic \
    --citation-style apa \
    --output-format review \
    --discipline stem \
    --word-count 6000 \
    --save-workflow my_stem_review \
    "Your research question"
```

### Load a Custom Workflow

```bash
python -m gazzali.gazzali --academic --load-workflow my_stem_review \
    "Another research question"
```

---

## Preset Workflow Templates

### 1. Literature Review

**Purpose**: Comprehensive synthesis of existing research on a topic

**Configuration**:
- Output Format: Review
- Word Count: 6,000 words
- Min Peer-Reviewed: 10 sources
- Quality Threshold: 7/10

**Search Strategy**:
- Comprehensive literature search across multiple time periods
- Prioritizes recent publications (last 5 years) plus seminal works
- Searches for review articles, meta-analyses, and highly-cited papers
- Identifies key authors and citation networks
- Includes both theoretical and empirical papers

**Best For**:
- Understanding the current state of research
- Identifying research trends and themes
- Finding research gaps
- Preparing for dissertation literature reviews

**Example**:
```bash
python -m gazzali.gazzali --academic --workflow literature_review \
    "How has research on remote work productivity evolved since 2020?"
```

---

### 2. Systematic Review

**Purpose**: Structured, protocol-driven review following systematic methodology

**Configuration**:
- Output Format: Review
- Word Count: 8,000 words
- Min Peer-Reviewed: 15 sources
- Quality Threshold: 8/10
- Includes Methodology: Yes

**Search Strategy**:
- Follows systematic review protocol (PICO framework)
- Establishes explicit inclusion/exclusion criteria
- Searches multiple databases with structured terms
- Documents search process and results
- Assesses quality of included studies
- Extracts data systematically

**Best For**:
- Evidence-based practice questions
- Clinical or policy decision-making
- Meta-analyses and systematic syntheses
- High-rigor academic publications

**Example**:
```bash
python -m gazzali.gazzali --academic --workflow systematic_review \
    "What is the effectiveness of cognitive behavioral therapy for treating anxiety disorders?"
```

---

### 3. Methodology Comparison

**Purpose**: Comparative analysis of different research methodologies

**Configuration**:
- Output Format: Paper
- Word Count: 7,000 words
- Min Peer-Reviewed: 12 sources
- Quality Threshold: 7/10
- Includes Methodology: Yes

**Search Strategy**:
- Searches for papers using diverse methodological approaches
- Includes both qualitative and quantitative studies
- Prioritizes methodological papers with detailed methods sections
- Looks for methodological critiques and debates
- Covers experimental, survey, case study, ethnographic, and mixed-methods approaches

**Best For**:
- Designing research methodology
- Understanding methodological trade-offs
- Justifying methodology choices
- Methodological dissertations or papers

**Example**:
```bash
python -m gazzali.gazzali --academic --workflow methodology_comparison \
    "How do different methodologies compare for studying user experience in mobile apps?"
```

---

### 4. Theoretical Analysis

**Purpose**: Deep analysis of theoretical frameworks and conceptual approaches

**Configuration**:
- Output Format: Paper
- Word Count: 8,000 words
- Min Peer-Reviewed: 15 sources
- Quality Threshold: 8/10
- Includes Methodology: No

**Search Strategy**:
- Searches for theoretical and conceptual papers
- Prioritizes original theoretical papers, frameworks, and critiques
- Includes seminal works (even if older)
- Searches for papers that apply, test, extend, or critique theories
- Looks for theoretical debates and competing frameworks
- Includes interdisciplinary theoretical perspectives

**Best For**:
- Theoretical dissertations
- Conceptual papers
- Theory development
- Philosophical analyses

**Example**:
```bash
python -m gazzali.gazzali --academic --workflow theoretical_analysis \
    "What are the major theoretical frameworks for understanding human motivation?"
```

---

## Customizing Workflows

### Override Workflow Settings

You can use a preset workflow and override specific settings:

```bash
# Use literature review but with different word count and citation style
python -m gazzali.gazzali --academic --workflow literature_review \
    --word-count 10000 \
    --citation-style mla \
    "Your question"
```

### Combine with Other Features

Workflows work seamlessly with other Gazzali features:

```bash
# Workflow + Question refinement
python -m gazzali.gazzali --academic --workflow systematic_review \
    --refine \
    "Broad research topic"

# Workflow + Specific discipline
python -m gazzali.gazzali --academic --workflow theoretical_analysis \
    --discipline social \
    "Your question"

# Workflow + Bibliography export
python -m gazzali.gazzali --academic --workflow literature_review \
    --export-bib \
    "Your question"
```

---

## Custom Workflows

### Creating Custom Workflows

Custom workflows allow you to save your preferred configuration for reuse:

```bash
# Create a custom workflow for short STEM reviews
python -m gazzali.gazzali --academic \
    --output-format review \
    --discipline stem \
    --citation-style ieee \
    --word-count 4000 \
    --save-workflow short_stem_review \
    "Your question"
```

This saves the configuration to `.gazzali/workflows/short_stem_review.json` in your project directory.

### Loading Custom Workflows

Once saved, you can load custom workflows by name:

```bash
python -m gazzali.gazzali --academic --load-workflow short_stem_review \
    "Another STEM research question"
```

### Managing Custom Workflows

Custom workflows are stored as JSON files in `.gazzali/workflows/`:

```bash
# List your custom workflows
ls -la .gazzali/workflows/

# View a workflow configuration
cat .gazzali/workflows/short_stem_review.json

# Delete a workflow
rm .gazzali/workflows/short_stem_review.json
```

### Custom Workflow File Format

Custom workflows are stored as JSON:

```json
{
  "name": "Short STEM Review",
  "config": {
    "citation_style": "ieee",
    "output_format": "review",
    "discipline": "stem",
    "word_count_target": 4000,
    "include_abstract": true,
    "include_methodology": false,
    "scholar_priority": true,
    "export_bibliography": false,
    "min_peer_reviewed": 8,
    "source_quality_threshold": 7
  },
  "created_at": "2024-01-15T10:30:00"
}
```

You can manually edit these files to fine-tune configurations.

---

## Configuration Priority

When multiple configuration sources are present, Gazzali uses this priority order (highest to lowest):

1. **Command-line arguments** (e.g., `--word-count 5000`)
2. **Custom workflow** (loaded with `--load-workflow`)
3. **Preset workflow template** (loaded with `--workflow`)
4. **Environment variables** (from `.env` file)
5. **Default values**

### Example Priority Resolution

```bash
# This command:
python -m gazzali.gazzali --academic \
    --workflow literature_review \
    --word-count 10000 \
    "Your question"

# Results in:
# - Output format: review (from workflow template)
# - Word count: 10000 (from command-line, overrides template's 6000)
# - Min sources: 10 (from workflow template)
# - Citation style: apa (from environment or default)
```

---

## Best Practices

### 1. Start with Preset Templates

Begin with a preset workflow template that matches your research type, then customize as needed:

```bash
# Good: Start with template, customize minimally
python -m gazzali.gazzali --academic --workflow literature_review \
    --discipline social \
    "Your question"
```

### 2. Save Frequently Used Configurations

If you repeatedly use the same configuration, save it as a custom workflow:

```bash
# Save your preferred configuration
python -m gazzali.gazzali --academic \
    --workflow systematic_review \
    --discipline medical \
    --citation-style apa \
    --word-count 12000 \
    --save-workflow medical_systematic \
    "First question"

# Reuse it easily
python -m gazzali.gazzali --academic --load-workflow medical_systematic \
    "Second question"
```

### 3. Use Descriptive Workflow Names

Choose clear, descriptive names for custom workflows:

```bash
# Good names
--save-workflow stem_literature_review_short
--save-workflow social_science_proposal
--save-workflow humanities_theoretical_analysis

# Avoid generic names
--save-workflow my_workflow
--save-workflow config1
```

### 4. Document Your Custom Workflows

Keep a README in your `.gazzali/workflows/` directory documenting your custom workflows:

```bash
# Create a README
cat > .gazzali/workflows/README.md << EOF
# Custom Workflows

## stem_literature_review_short
- Purpose: Quick STEM literature reviews
- Word count: 4000
- Citation style: IEEE
- Use for: Conference papers, preliminary research

## social_science_proposal
- Purpose: Social science research proposals
- Word count: 6000
- Citation style: APA
- Use for: Grant applications, dissertation proposals
EOF
```

### 5. Version Control Your Workflows

Include custom workflows in version control for team consistency:

```bash
# Add to git
git add .gazzali/workflows/
git commit -m "Add custom research workflows"
```

---

## Workflow Validation

Gazzali automatically validates workflow configurations and warns about potential issues:

### Common Validation Warnings

**Word Count Too Low**:
```
⚠️  Word count target (500) is very low. Consider at least 500 words for meaningful academic content.
```

**Word Count Too High**:
```
⚠️  Word count target (60000) is very high. Consider breaking into multiple documents or reducing scope.
```

**Abstract Format Mismatch**:
```
⚠️  Abstract format typically requires 250-500 words, but target is 5000. Consider reducing word count target.
```

**Quality Threshold Out of Range**:
```
⚠️  Source quality threshold must be between 0 and 10 (got 15).
```

---

## Troubleshooting

### Workflow Not Found

**Problem**: `❌ Workflow not found: my_workflow`

**Solutions**:
1. Check spelling: `--workflow literature_review` (use underscores)
2. List available workflows: `--list-workflows`
3. Verify custom workflow exists: `ls .gazzali/workflows/`

### Custom Workflow Load Failed

**Problem**: `❌ Failed to load workflow: [error]`

**Solutions**:
1. Check JSON syntax: `cat .gazzali/workflows/my_workflow.json | python -m json.tool`
2. Verify file permissions: `ls -la .gazzali/workflows/`
3. Recreate the workflow if corrupted

### Configuration Not Applied

**Problem**: Settings from workflow not being used

**Solutions**:
1. Check priority order (command-line args override workflows)
2. Verify academic mode is enabled: `--academic`
3. Check for conflicting environment variables

---

## Advanced Usage

### Programmatic Workflow Management

You can also manage workflows programmatically:

```python
from gazzali.workflows import (
    get_workflow_template,
    WorkflowType,
    create_custom_workflow
)
from gazzali.academic_config import AcademicConfig

# Load a preset template
template = get_workflow_template(WorkflowType.LITERATURE_REVIEW)
config = template.academic_config

# Create a custom workflow
custom = create_custom_workflow(
    name="My Custom Workflow",
    description="Specialized workflow for my research",
    base_template=WorkflowType.SYSTEMATIC_REVIEW,
    word_count_target=10000,
    citation_style="mla"
)

# Access workflow properties
print(f"Search strategy: {template.search_strategy}")
print(f"Required sections: {template.required_sections}")
print(f"Quality criteria: {template.quality_criteria}")
```

### Workflow Templates in Scripts

Use workflows in automated research scripts:

```python
#!/usr/bin/env python3
import subprocess
import sys

questions = [
    "Question 1",
    "Question 2",
    "Question 3"
]

for question in questions:
    subprocess.run([
        sys.executable, "-m", "gazzali.gazzali",
        "--academic",
        "--workflow", "literature_review",
        "--discipline", "stem",
        question
    ])
```

---

## Examples by Research Type

### Dissertation Literature Review

```bash
python -m gazzali.gazzali --academic \
    --workflow literature_review \
    --discipline social \
    --word-count 15000 \
    --citation-style apa \
    --export-bib \
    --save-workflow dissertation_lit_review \
    "Your dissertation topic"
```

### Conference Paper

```bash
python -m gazzali.gazzali --academic \
    --workflow methodology_comparison \
    --discipline stem \
    --word-count 4000 \
    --citation-style ieee \
    "Your conference paper topic"
```

### Grant Proposal

```bash
python -m gazzali.gazzali --academic \
    --output-format proposal \
    --discipline medical \
    --word-count 5000 \
    --citation-style apa \
    --refine \
    "Your research proposal"
```

### Journal Article

```bash
python -m gazzali.gazzali --academic \
    --workflow systematic_review \
    --discipline medical \
    --word-count 8000 \
    --citation-style apa \
    --export-bib \
    "Your systematic review question"
```

---

## Summary

Workflow configuration in Gazzali Research provides:

✅ **Preset templates** for common research tasks
✅ **Customization** through command-line overrides
✅ **Reusability** via saved custom workflows
✅ **Consistency** across research projects
✅ **Flexibility** to adapt to any research need

Start with a preset template, customize as needed, and save your configuration for future use. This ensures consistent, high-quality academic research output every time.

For more information, see:
- [Workflow Templates Documentation](WORKFLOW_TEMPLATES.md)
- [Academic Mode Guide](ACADEMIC_MODE.md)
- [Citation Styles Guide](CITATION_STYLES.md)
