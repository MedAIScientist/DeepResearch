# Academic Prompts Documentation

## Overview

The academic prompts module provides specialized system prompts for conducting rigorous academic research with Gazzali Research. These prompts are designed to ensure scholarly standards, proper citation practices, and evidence-based analysis.

## Table of Contents

- [Core Features](#core-features)
- [Academic Research Prompt](#academic-research-prompt)
- [Customization](#customization)
- [Usage Examples](#usage-examples)
- [Best Practices](#best-practices)

## Core Features

The academic research prompt enhances the standard research workflow with:

### 1. Source Prioritization
- **Peer-reviewed sources first**: Journals, conferences, academic books
- **Scholar-first strategy**: Always use Google Scholar before general web search
- **Quality assessment**: Evaluate source credibility and impact
- **Citation metrics**: Track citation counts and influence

### 2. Citation Metadata Extraction
- **Complete bibliographic data**: Authors, year, venue, DOI, pages
- **Structured format**: Consistent citation information capture
- **Access tracking**: Document when and how sources were accessed
- **Citation counts**: Track academic impact metrics

### 3. Methodology Identification
- **Research design**: Experimental, observational, survey, case study, etc.
- **Data collection**: Methods and instruments used
- **Analysis techniques**: Statistical tests, qualitative coding, etc.
- **Limitations**: Acknowledged constraints and biases
- **Ethics**: IRB approval, consent, data protection

### 4. Theoretical Framework Analysis
- **Theory identification**: Name and describe frameworks used
- **Construct definition**: Key concepts and their relationships
- **Operationalization**: How theories are tested empirically
- **Contributions**: How research advances theory

### 5. Critical Evaluation
- **Evidence quality**: Internal/external validity, reliability
- **Bias assessment**: Selection, publication, funding biases
- **Conflicting evidence**: Document and analyze disagreements
- **Research gaps**: Identify unanswered questions

### 6. Academic Writing Standards
- **Formal tone**: Professional, objective language
- **Hedging language**: Appropriate certainty indicators
- **Third-person perspective**: Scholarly voice
- **Structured organization**: Clear hierarchical sections

## Academic Research Prompt

### Base Prompt Structure

The `ACADEMIC_RESEARCH_PROMPT` includes:

1. **Role Definition**: Academic research assistant specializing in scholarly investigation
2. **Source Prioritization Guidelines**: Peer-reviewed sources first, Scholar tool priority
3. **Citation Metadata Requirements**: Complete bibliographic information extraction
4. **Methodology Identification**: Research design, data collection, analysis techniques
5. **Critical Analysis Framework**: Evidence evaluation and quality assessment
6. **Academic Writing Standards**: Formal tone, hedging, structured organization
7. **Tool Descriptions**: Enhanced tool descriptions emphasizing academic use
8. **Research Workflow**: Step-by-step process for conducting academic research

### Key Differences from Standard Prompt

| Aspect | Standard Prompt | Academic Prompt |
|--------|----------------|-----------------|
| **Source Priority** | General web search | Peer-reviewed sources, Scholar first |
| **Citation** | Basic URL references | Complete bibliographic metadata |
| **Methodology** | Not emphasized | Detailed extraction and classification |
| **Theory** | Not emphasized | Identify and analyze frameworks |
| **Tone** | Professional | Formal academic style |
| **Evidence** | Factual reporting | Critical evaluation and quality assessment |
| **Structure** | Clear organization | Academic paper structure |

## Customization

### Function: `get_academic_research_prompt()`

Generate customized prompts with discipline and format modifiers.

```python
from gazzali.prompts import get_academic_research_prompt

# Basic usage
prompt = get_academic_research_prompt()

# With discipline modifier
prompt = get_academic_research_prompt(discipline="stem")

# With output format
prompt = get_academic_research_prompt(output_format="paper")

# Full customization
prompt = get_academic_research_prompt(
    discipline="social",
    output_format="review",
    additional_instructions="Focus on longitudinal studies from the past 5 years."
)
```

### Discipline Modifiers

#### STEM
- Technical and scientific terminology
- Mathematical notation and formulas
- Experimental design and quantitative methods
- Reproducibility and empirical validation
- Statistical significance and hypothesis testing

#### Social Sciences
- Social science frameworks and constructs
- Qualitative and quantitative methods
- Validity, reliability, generalizability
- Cultural context and human behavior
- Ethical considerations for human subjects

#### Humanities
- Critical theory and hermeneutics
- Textual analysis and interpretation
- Historical context and primary sources
- Philosophical implications
- Rhetoric and meaning-making

#### Medical/Health Sciences
- Medical and clinical terminology
- Clinical trials and systematic reviews
- Evidence-based practice
- Patient outcomes and safety
- Clinical significance
- Medical evidence hierarchies

#### General (Default)
- Interdisciplinary approach
- Accessible academic language
- Multiple perspectives
- Balanced depth and accessibility

### Output Format Modifiers

#### Paper (Default)
- Full research paper structure
- Abstract, Introduction, Literature Review, Methodology, Findings, Discussion, Conclusion
- In-depth analysis with extensive citations
- Comprehensive treatment of topic

#### Review
- Literature review structure
- Thematic or chronological organization
- Synthesis of existing research
- Research gaps and future directions
- Focus on comprehensive coverage

#### Proposal
- Research proposal structure
- Background, Research Questions, Literature Review, Proposed Methodology
- Expected Outcomes and Timeline
- Emphasis on feasibility and significance

#### Abstract
- Concise format (250-300 words)
- Background, Methods, Results, Conclusions
- Extremely focused on key findings
- Suitable for conference submission

#### Presentation
- Oral presentation structure
- Clear bullet points and headings
- Main ideas and practical implications
- Suitable for 15-20 minute talk

## Usage Examples

### Example 1: STEM Research Paper

```python
from gazzali.prompts import get_academic_research_prompt

prompt = get_academic_research_prompt(
    discipline="stem",
    output_format="paper"
)

# Use this prompt with the research agent
# The agent will:
# - Prioritize peer-reviewed STEM journals
# - Use technical terminology
# - Focus on experimental methods and statistical analysis
# - Structure output as a full research paper
```

### Example 2: Social Sciences Literature Review

```python
prompt = get_academic_research_prompt(
    discipline="social",
    output_format="review"
)

# The agent will:
# - Search for social science research
# - Focus on qualitative and quantitative methods
# - Organize findings thematically
# - Identify research gaps
# - Structure as a literature review
```

### Example 3: Medical Research with Custom Instructions

```python
prompt = get_academic_research_prompt(
    discipline="medical",
    output_format="paper",
    additional_instructions="""
    Focus specifically on randomized controlled trials (RCTs) and systematic reviews.
    Prioritize studies with large sample sizes (n > 1000).
    Include meta-analyses when available.
    Emphasize clinical outcomes and patient safety data.
    """
)

# The agent will follow medical research standards plus custom requirements
```

### Example 4: Interdisciplinary Conference Abstract

```python
prompt = get_academic_research_prompt(
    discipline="general",
    output_format="abstract",
    additional_instructions="""
    This is for an interdisciplinary conference.
    Make the language accessible to researchers from multiple fields.
    Emphasize practical applications and broader implications.
    """
)

# The agent will create a concise, accessible abstract
```

## Best Practices

### 1. Choose Appropriate Discipline

Select the discipline that best matches your research topic:
- **STEM**: Natural sciences, engineering, mathematics, computer science
- **Social**: Psychology, sociology, economics, political science, education
- **Humanities**: Literature, history, philosophy, languages, arts
- **Medical**: Medicine, nursing, public health, clinical research
- **General**: Interdisciplinary topics or when discipline is unclear

### 2. Match Format to Purpose

Select output format based on your goal:
- **Paper**: Comprehensive research report, thesis chapter, journal article
- **Review**: Literature synthesis, state-of-the-field overview
- **Proposal**: Grant application, research plan, dissertation proposal
- **Abstract**: Conference submission, brief summary
- **Presentation**: Talk preparation, seminar, lecture

### 3. Provide Clear Research Questions

The prompt works best with specific, focused research questions:

**Good**: "What are the effects of mindfulness-based interventions on anxiety symptoms in adolescents? What methodologies have been used?"

**Less Good**: "Tell me about mindfulness and anxiety."

### 4. Use Additional Instructions for Specificity

Add custom instructions for:
- Time period constraints: "Focus on studies from 2015-2024"
- Geographic scope: "Include only studies from European countries"
- Methodology preferences: "Prioritize longitudinal studies"
- Population specifics: "Focus on adult populations aged 18-65"
- Theoretical frameworks: "Use social cognitive theory as the primary lens"

### 5. Leverage Scholar-First Strategy

The prompt automatically prioritizes Google Scholar, but you can enhance this:
- Use specific academic search terms
- Include author names if known
- Specify journal names or conferences
- Use field-specific terminology

### 6. Review Citation Metadata

The prompt instructs the agent to extract complete citation information:
- Verify citations are complete and accurate
- Check DOIs and URLs work correctly
- Ensure author names are properly formatted
- Confirm publication years and venues

### 7. Assess Evidence Quality

The prompt includes critical evaluation guidelines:
- Review the agent's assessment of source credibility
- Check that highly cited papers are identified
- Verify that limitations are acknowledged
- Ensure conflicting evidence is discussed

### 8. Validate Methodology Descriptions

When the agent extracts methodology information:
- Confirm research designs are correctly identified
- Check that sample sizes and characteristics are accurate
- Verify statistical methods are properly described
- Ensure limitations are appropriately noted

## Integration with Academic Configuration

The academic prompts work seamlessly with `AcademicConfig`:

```python
from gazzali.academic_config import AcademicConfig
from gazzali.prompts import get_academic_research_prompt

# Load configuration
config = AcademicConfig.from_env()

# Generate matching prompt
prompt = get_academic_research_prompt(
    discipline=config.discipline.value,
    output_format=config.output_format.value
)

# Use prompt with research agent
# The agent will follow both the prompt guidelines and configuration settings
```

## Troubleshooting

### Issue: Agent not prioritizing academic sources

**Solution**: 
- Verify the prompt includes Scholar tool priority instructions
- Check that Google Scholar API/tool is properly configured
- Use more specific academic search terms
- Add explicit instruction: "Use google_scholar tool first"

### Issue: Incomplete citation metadata

**Solution**:
- Ensure the prompt includes citation extraction requirements
- Use the `visit` tool to access full paper content
- Add instruction: "Extract complete bibliographic information"
- Check that sources provide metadata (some web pages lack this)

### Issue: Methodology not being identified

**Solution**:
- Verify sources are empirical research papers (not opinion pieces)
- Add explicit instruction: "Identify and document research methodology"
- Use discipline-specific prompt modifier
- Focus on peer-reviewed journal articles

### Issue: Output not matching desired format

**Solution**:
- Use the appropriate `output_format` parameter
- Add explicit structure requirements in additional_instructions
- Review the format modifier to ensure it matches your needs
- Provide example structure in additional instructions

### Issue: Tone not sufficiently academic

**Solution**:
- Verify academic prompt is being used (not standard prompt)
- Add instruction: "Use formal academic language throughout"
- Specify discipline for appropriate terminology
- Review and edit output for tone consistency

## Related Documentation

- [Academic Configuration](ACADEMIC_CONFIG.md) - Configuration options for academic features
- [Citation Manager](CITATION_MANAGER.md) - Citation tracking and formatting
- [Environment Setup](ENVIRONMENT_SETUP.md) - Setting up academic research environment

## Support

For issues or questions about academic prompts:
1. Check this documentation for guidance
2. Review example usage in the codebase
3. Consult the requirements and design documents
4. Open an issue on the project repository

---

**Last Updated**: 2024
**Version**: 1.0
**Module**: `src/gazzali/prompts/academic_prompts.py`
