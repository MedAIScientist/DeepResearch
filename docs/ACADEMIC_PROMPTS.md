# Academic Prompts Documentation

## Overview

The academic prompts module provides specialized system prompts for conducting rigorous academic research with Gazzali Research. These prompts are designed to ensure scholarly standards, proper citation practices, and evidence-based analysis.

## Table of Contents

- [Core Features](#core-features)
- [Academic Research Prompt](#academic-research-prompt)
- [Academic Synthesis Prompt](#academic-synthesis-prompt)
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

## Academic Synthesis Prompt

### Overview

The `ACADEMIC_SYNTHESIS_PROMPT` is used for generating comprehensive academic reports from research findings. While the research prompt guides the agent in gathering information, the synthesis prompt ensures the final report meets rigorous academic writing standards.

### Key Features

#### 1. Academic Writing Style Requirements

**Formal and Objective Tone**:
- Professional academic language throughout
- Third-person perspective (no "I," "we," "you")
- No contractions or colloquialisms
- Precise, technical terminology
- Clear, appropriately complex sentences

**Hedging Language and Certainty Indicators**:
- **Strong evidence**: "demonstrates," "shows," "establishes," "confirms"
- **Moderate evidence**: "suggests," "indicates," "supports," "implies"
- **Weak evidence**: "may," "might," "appears to," "could"
- **Speculation**: "it is possible that," "one explanation could be"

#### 2. Structured Section Requirements

The synthesis prompt enforces a complete academic report structure:

- **Abstract** (150-250 words): Concise summary of entire report
- **Introduction**: Background, context, research questions
- **Literature Review**: Thematic synthesis of existing research
- **Methodology**: Research methods used in reviewed studies
- **Findings**: Main results and evidence
- **Discussion**: Interpretation and implications
- **Implications**: Theoretical and practical applications
- **Limitations**: Constraints and gaps in research
- **Conclusion**: Summary and future directions
- **References**: Complete bibliography

#### 3. Citation Formatting Instructions

The prompt includes detailed instructions for four major citation styles:

- **APA 7th Edition**: (Author, Year) format with hanging indent bibliography
- **MLA 9th Edition**: (Author Page) format with Works Cited
- **Chicago 17th Edition**: (Author Year) or footnote format
- **IEEE**: Numbered [1] format with numbered references

Each style includes specific formatting rules for:
- In-text citations (single author, multiple authors, direct quotes)
- Reference list entries (journals, books, chapters, websites)
- Formatting conventions (italics, punctuation, capitalization)

#### 4. Methodology and Limitations Discussion

**Methodology Requirements**:
- Describe research methods across reviewed studies
- Classify methodologies (qualitative, quantitative, mixed-methods)
- Identify specific techniques (surveys, experiments, case studies)
- Discuss sample characteristics and data analysis
- Compare methodological approaches
- Evaluate appropriateness and rigor

**Limitations Requirements**:
- Acknowledge limitations of individual studies
- Identify common methodological constraints
- Discuss potential biases (selection, publication, funding)
- Note limitations in generalizability
- Identify research gaps and unanswered questions
- Present limitations objectively

#### 5. Theoretical Framework Integration

The prompt requires integration of theoretical frameworks throughout:
- Identify and explain relevant theories
- Define key theoretical constructs
- Describe relationships between constructs
- Explain how theories are operationalized
- Compare different theoretical perspectives
- Discuss how findings support or challenge theories

#### 6. Research Implications and Future Directions

**Implications Requirements**:
- **Theoretical implications**: Contributions to knowledge and theory
- **Practical implications**: Applications for practitioners and policymakers
- **Policy implications**: Evidence-based recommendations

**Future Directions Requirements**:
- Identify specific unanswered questions
- Suggest methodological improvements
- Recommend underexplored areas
- Propose studies to resolve conflicts
- Be specific and actionable

### Function: `get_academic_synthesis_prompt()`

Generate customized synthesis prompts with citation style, format, and discipline modifiers.

```python
from gazzali.prompts import get_academic_synthesis_prompt

# Basic usage with APA citations
prompt = get_academic_synthesis_prompt(citation_style="apa")

# Full customization
prompt = get_academic_synthesis_prompt(
    citation_style="apa",
    output_format="paper",
    discipline="stem",
    word_count_target=8000,
    additional_instructions="Emphasize recent studies from 2020-2024."
)
```

### Citation Style Options

#### APA (American Psychological Association)
- In-text: (Smith, 2020) or Smith (2020)
- Multiple authors: (Smith et al., 2020)
- Reference format: Author, A. A. (Year). Title. *Journal*, *volume*(issue), pages.
- Best for: Psychology, education, social sciences

#### MLA (Modern Language Association)
- In-text: (Smith 45) or Smith argues (45)
- Multiple authors: (Smith et al. 45)
- Works Cited format: Author, First. "Title." *Journal*, vol. X, no. Y, Year, pp. xx-xx.
- Best for: Humanities, literature, languages

#### Chicago (Author-Date)
- In-text: (Smith 2020, 45) or Smith (2020, 45)
- Reference format: Author, First Last. Year. "Title." *Journal* volume (issue): pages.
- Best for: History, humanities, some social sciences

#### IEEE (Institute of Electrical and Electronics Engineers)
- In-text: [1] or [1]-[3]
- Reference format: [1] A. A. Author, "Title," *Journal*, vol. X, no. Y, pp. xx-xx, Year.
- Best for: Engineering, computer science, technical fields

### Quality Checklist

The synthesis prompt includes a comprehensive quality checklist:

- ✓ All sections present and in correct order
- ✓ Formal, objective, third-person writing
- ✓ No contractions or informal language
- ✓ Appropriate hedging language
- ✓ All claims properly cited
- ✓ Consistent citation formatting
- ✓ Complete bibliography
- ✓ Methodology and limitations discussed
- ✓ Theoretical frameworks integrated
- ✓ Implications clearly stated
- ✓ Future directions specific and actionable
- ✓ Abstract concise and self-contained

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

### Example 5: Synthesis Prompt for APA Research Paper

```python
from gazzali.prompts import get_academic_synthesis_prompt

# Generate synthesis prompt for a comprehensive research paper
synthesis_prompt = get_academic_synthesis_prompt(
    citation_style="apa",
    output_format="paper",
    discipline="social",
    word_count_target=8000
)

# Use this prompt with the synthesis model to generate the final report
# The model will:
# - Format citations in APA 7th edition style
# - Structure output as a full research paper
# - Use social science terminology
# - Target approximately 8,000 words
```

### Example 6: MLA Literature Review

```python
synthesis_prompt = get_academic_synthesis_prompt(
    citation_style="mla",
    output_format="review",
    discipline="humanities",
    word_count_target=5000,
    additional_instructions="""
    Focus on thematic organization of literature.
    Emphasize textual analysis and critical interpretation.
    Include discussion of primary and secondary sources.
    """
)

# The model will generate an MLA-formatted literature review
```

### Example 7: IEEE Technical Paper

```python
synthesis_prompt = get_academic_synthesis_prompt(
    citation_style="ieee",
    output_format="paper",
    discipline="stem",
    word_count_target=6000,
    additional_instructions="""
    Include technical specifications and mathematical notation.
    Emphasize experimental methodology and quantitative results.
    Use tables and figures for data presentation.
    """
)

# The model will generate an IEEE-formatted technical paper
```

### Example 8: Chicago Research Proposal

```python
synthesis_prompt = get_academic_synthesis_prompt(
    citation_style="chicago",
    output_format="proposal",
    discipline="general",
    word_count_target=4000,
    additional_instructions="""
    Emphasize feasibility and significance of proposed research.
    Include detailed methodology section with timeline.
    Discuss expected contributions to the field.
    """
)

# The model will generate a Chicago-formatted research proposal
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
