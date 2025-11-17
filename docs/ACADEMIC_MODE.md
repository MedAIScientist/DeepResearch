# Academic Mode Documentation

## Overview

Gazzali Research's **Academic Mode** transforms the standard research assistant into a specialized scholarly research tool designed for academic researchers, graduate students, and professionals who need peer-reviewed, properly cited research outputs. Named after Al-Ghazali (1058-1111), the renowned Islamic philosopher and scholar, this mode embodies rigorous academic standards and systematic scholarly investigation.

Academic Mode provides:

- **Citation Management** — Automatic tracking and formatting in APA, MLA, Chicago, and IEEE styles
- **Scholar-First Search** — Prioritizes Google Scholar and peer-reviewed sources over general web content
- **Academic Writing Standards** — Formal, objective, third-person perspective with proper hedging language
- **Structured Sections** — Abstract, Introduction, Literature Review, Methodology, Discussion, etc.
- **Discipline-Specific Conventions** — Tailored terminology and writing style for STEM, social sciences, humanities, and medical fields
- **Bibliography Generation** — Properly formatted reference lists with optional BibTeX export
- **Research Question Refinement** — Transform broad topics into focused, answerable research questions
- **Quality Assurance** — Source credibility evaluation and peer-review prioritization

---

## Quick Start

### Enable Academic Mode

Add the `--academic` flag to any research command:

```bash
python -m gazzali.gazzali --academic "Impact of AI on education"
```

### Academic Mode with Citation Style

```bash
python -m gazzali.gazzali --academic --citation-style apa \
    "Effects of remote work on employee productivity"
```

### Complete Academic Workflow

```bash
python -m gazzali.gazzali --academic \
    --citation-style apa \
    --output-format paper \
    --discipline social \
    --refine \
    --export-bib \
    "Social media effects on adolescent mental health"
```

---

## Core Features

### 1. Citation Management

Academic Mode automatically tracks and formats all sources consulted during research.


**Features**:
- Captures bibliographic metadata (authors, year, title, journal, DOI, etc.)
- Formats inline citations: `(Author, Year)` or `[Number]`
- Generates properly formatted bibliography
- Detects and flags duplicate citations
- Supports multiple citation styles

**Supported Citation Styles**:

| Style | Format | Best For |
|-------|--------|----------|
| APA 7th | (Author, Year) | Psychology, Education, Social Sciences |
| MLA 9th | (Author Page) | Humanities, Literature, Arts |
| Chicago 17th | Footnotes or (Author Year) | History, Arts, Humanities |
| IEEE | [Number] | Engineering, Computer Science, Technology |

**Example Usage**:

```bash
# APA style (default)
python -m gazzali.gazzali --academic --citation-style apa "Your question"

# IEEE style for engineering
python -m gazzali.gazzali --academic --citation-style ieee "Your question"

# Export bibliography to .bib file
python -m gazzali.gazzali --academic --export-bib "Your question"
```

**Output Example** (APA):
```
Recent studies have shown significant improvements in student engagement 
through AI-powered tutoring systems (Smith & Johnson, 2023). However, 
concerns about data privacy remain prevalent (Chen et al., 2024).

References

Chen, L., Wang, M., & Zhang, Y. (2024). Privacy concerns in educational 
    AI systems. Journal of Educational Technology, 45(2), 123-145. 
    https://doi.org/10.1234/jet.2024.45.2.123

Smith, J., & Johnson, A. (2023). AI tutoring systems and student 
    engagement: A meta-analysis. Educational Psychology Review, 35(4), 
    567-589. https://doi.org/10.1234/epr.2023.35.4.567
```

---

### 2. Scholar-First Search Strategy

Academic Mode prioritizes scholarly sources over general web content.

**Search Priority**:
1. **Google Scholar** — Peer-reviewed journals, conference proceedings, academic books
2. **Institutional Sources** — University repositories, research institutions
3. **General Web** — Only for supplementary information or recent developments

**Source Quality Scoring**:
- Peer-reviewed journal articles: 10/10
- Conference proceedings: 9/10
- Academic books: 9/10
- Institutional reports: 7/10
- Preprints (arXiv, bioRxiv): 6/10
- General web sources: 3/10

**Configuration**:

```bash
# Set minimum quality threshold (default: 7)
export SOURCE_QUALITY_THRESHOLD=8

# Set minimum peer-reviewed sources (default: 5)
export MIN_PEER_REVIEWED_SOURCES=10
```

**Benefits**:
- Higher credibility and reliability
- Proper citation metadata
- Access to methodology and data
- Peer-review quality assurance
- Citation network exploration

---

### 3. Academic Writing Standards

Academic Mode enforces formal academic writing conventions.

**Writing Style Requirements**:
- **Formal tone** — No contractions, colloquialisms, or informal expressions
- **Third-person perspective** — Objective, impersonal voice
- **Hedging language** — Appropriate use of "suggests," "indicates," "may," "appears to"
- **Precise terminology** — Discipline-specific vocabulary
- **Evidence-based claims** — All assertions supported by citations

**Example Comparison**:

❌ **Standard Mode**:
```
AI is definitely going to change education. It's already making 
things better for students and teachers love it.
```

✅ **Academic Mode**:
```
Artificial intelligence appears to be transforming educational 
practices (Smith & Johnson, 2023). Preliminary evidence suggests 
improvements in student engagement (Chen et al., 2024), though 
further research is needed to establish long-term effects.
```

---

### 4. Structured Academic Sections

Academic Mode generates reports with proper academic structure.

**Paper Format** (default):
- Abstract
- Introduction
- Literature Review
- Methodology
- Findings
- Discussion
- Conclusion
- References

**Literature Review Format**:
- Abstract
- Introduction
- Thematic Analysis
- Research Gaps
- Future Directions
- References

**Research Proposal Format**:
- Background
- Research Questions
- Literature Review
- Proposed Methodology
- Expected Outcomes
- Timeline
- References

**Example**:

```bash
# Full research paper
python -m gazzali.gazzali --academic --output-format paper "Your question"

# Literature review
python -m gazzali.gazzali --academic --output-format review "Your question"

# Research proposal
python -m gazzali.gazzali --academic --output-format proposal "Your question"
```

---

### 5. Discipline-Specific Conventions

Academic Mode adapts terminology, methodology focus, and writing conventions to your discipline.


**Supported Disciplines**:

#### STEM (Science, Technology, Engineering, Mathematics)

**Characteristics**:
- Technical and scientific terminology
- Emphasis on experimental design and quantitative methods
- Statistical analysis and reproducibility
- Precise numerical data and equations
- SI units and standard nomenclature

**Example**:
```bash
python -m gazzali.gazzali --academic --discipline stem \
    --citation-style ieee \
    "Novel approaches to quantum error correction"
```

#### Social Sciences

**Characteristics**:
- Social science constructs and frameworks
- Mixed qualitative and quantitative methods
- Emphasis on validity, reliability, generalizability
- Ethical considerations for human subjects
- Statistical and thematic analysis

**Example**:
```bash
python -m gazzali.gazzali --academic --discipline social \
    --citation-style apa \
    "Impact of social media on political polarization"
```

#### Humanities

**Characteristics**:
- Critical theory and hermeneutics
- Textual analysis and close reading
- Historical and cultural context
- Interpretive frameworks
- Engagement with scholarly debates

**Example**:
```bash
python -m gazzali.gazzali --academic --discipline humanities \
    --citation-style mla \
    "Postcolonial perspectives in contemporary literature"
```

#### Medical/Health Sciences

**Characteristics**:
- Clinical terminology and diagnostic criteria
- Evidence-based medicine hierarchy
- Patient outcomes and safety
- RCTs, systematic reviews, meta-analyses
- CONSORT/PRISMA reporting guidelines

**Example**:
```bash
python -m gazzali.gazzali --academic --discipline medical \
    --citation-style apa \
    "Effectiveness of cognitive behavioral therapy for chronic pain"
```

---

### 6. Research Question Refinement

Transform broad topics into focused, answerable research questions using FINER criteria.

**FINER Criteria**:
- **F**easible — Can be investigated with available resources
- **I**nteresting — Engaging to researchers and stakeholders
- **N**ovel — Fills a gap or extends knowledge
- **E**thical — Meets ethical standards
- **R**elevant — Important to field or practice

**Usage**:

```bash
python -m gazzali.gazzali --academic --refine "Broad research topic"
```

**Example Refinement**:

**Input**: "AI in education"

**Output**:
```
Original Question:
  AI in education

Refined Questions:
  → 1. How do AI-powered adaptive learning systems affect student 
       achievement in K-12 mathematics education?
    2. What are the ethical implications of using AI for automated 
       essay grading in higher education?
    3. How do teachers perceive and integrate AI tools into their 
       instructional practices?

Quality Assessment:
  • Question Type:  Comparative
  • Scope:          Appropriate
  • Key Variables:  AI systems, student achievement, grade level, subject area
```

**Benefits**:
- Focused, specific research questions
- Clear scope and boundaries
- Identified variables and populations
- Improved feasibility assessment

---

## Command-Line Options

### Academic Mode Flags

#### `--academic`
Enable academic research mode.

```bash
python -m gazzali.gazzali --academic "Your question"
```

#### `--citation-style {apa,mla,chicago,ieee}`
Specify citation format (default: apa).

```bash
python -m gazzali.gazzali --academic --citation-style mla "Your question"
```

#### `--output-format {paper,review,proposal,abstract,presentation}`
Specify document format (default: paper).

```bash
python -m gazzali.gazzali --academic --output-format review "Your question"
```

#### `--discipline {general,stem,social,humanities,medical}`
Specify academic discipline (default: general).

```bash
python -m gazzali.gazzali --academic --discipline stem "Your question"
```

#### `--refine`
Refine research question before starting.

```bash
python -m gazzali.gazzali --academic --refine "Broad topic"
```

#### `--word-count COUNT`
Target word count for report (default: 8000).

```bash
python -m gazzali.gazzali --academic --word-count 5000 "Your question"
```

#### `--export-bib`
Export bibliography to .bib file.

```bash
python -m gazzali.gazzali --academic --export-bib "Your question"
```

---

## Workflow Examples

### Example 1: Dissertation Literature Review

**Scenario**: Comprehensive literature review for dissertation

```bash
python -m gazzali.gazzali --academic \
    --output-format review \
    --discipline social \
    --citation-style apa \
    --word-count 15000 \
    --export-bib \
    --refine \
    "The role of social capital in entrepreneurial success"
```

**Output**:
- 15,000-word literature review
- APA citations throughout
- Thematic organization
- Research gaps identified
- Bibliography exported to .bib file

---

### Example 2: Conference Paper

**Scenario**: Short paper for academic conference

```bash
python -m gazzali.gazzali --academic \
    --output-format paper \
    --discipline stem \
    --citation-style ieee \
    --word-count 4000 \
    "Machine learning approaches to protein structure prediction"
```

**Output**:
- 4,000-word research paper
- IEEE citations
- STEM-focused methodology
- Concise, conference-ready format

---

### Example 3: Grant Proposal

**Scenario**: Research proposal for funding application

```bash
python -m gazzali.gazzali --academic \
    --output-format proposal \
    --discipline medical \
    --citation-style apa \
    --word-count 6000 \
    --refine \
    "Novel immunotherapy approaches for pancreatic cancer"
```

**Output**:
- 6,000-word research proposal
- Refined research questions
- Medical terminology and conventions
- Proposed methodology section
- Expected outcomes and timeline

---

### Example 4: Systematic Review

**Scenario**: Evidence-based systematic review

```bash
python -m gazzali.gazzali --academic \
    --workflow systematic_review \
    --discipline medical \
    --citation-style apa \
    --export-bib \
    "Effectiveness of mindfulness interventions for anxiety disorders"
```

**Output**:
- 8,000-word systematic review
- 15+ peer-reviewed sources
- Quality assessment of studies
- PRISMA-style methodology
- Comprehensive bibliography

---

### Example 5: Theoretical Analysis

**Scenario**: Deep theoretical exploration

```bash
python -m gazzali.gazzali --academic \
    --workflow theoretical_analysis \
    --discipline humanities \
    --citation-style chicago \
    --word-count 10000 \
    "Phenomenological approaches to understanding consciousness"
```

**Output**:
- 10,000-word theoretical analysis
- Chicago-style citations
- Humanities writing conventions
- Engagement with philosophical debates
- Multiple theoretical perspectives

---

## Configuration

### Environment Variables

Configure default academic settings in `.env`:

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
```

### Configuration Priority

Settings are applied in this order (highest to lowest priority):

1. **Command-line arguments** — `--citation-style apa`
2. **Workflow templates** — `--workflow literature_review`
3. **Environment variables** — `.env` file
4. **Default values** — Built-in defaults

---

## Output Files

### Academic Report

Main academic report with proper formatting:

```
outputs/reports/academic_paper_20240115_103000_your_question.md
```

**Contents**:
- Structured sections (Abstract, Introduction, etc.)
- Inline citations in specified style
- Properly formatted bibliography
- Academic writing style
- Discipline-specific terminology

### Bibliography File

Separate bibliography in BibTeX format (if `--export-bib`):

```
outputs/reports/academic_paper_20240115_103000_your_question.bib
```

**Contents**:
```bibtex
@article{smith2023ai,
  author = {Smith, John and Johnson, Alice},
  title = {AI Tutoring Systems and Student Engagement},
  journal = {Educational Psychology Review},
  year = {2023},
  volume = {35},
  number = {4},
  pages = {567--589},
  doi = {10.1234/epr.2023.35.4.567}
}
```

### Progress Report

Research progress tracking (academic mode only):

```
outputs/reports/progress_20240115_103000.json
```

---

## Quality Metrics

Academic Mode tracks and reports quality metrics:

### Source Quality

```
📊 Report Metrics:
  • Word Count:        8,247
  • Sections:          8
  • Citations:         23
  • Peer-Reviewed:     18 (78.3%)
  • Highly Cited:      5 sources
```

**Metrics Explained**:
- **Word Count** — Total words in report
- **Sections** — Number of structured sections
- **Citations** — Total unique sources cited
- **Peer-Reviewed** — Percentage from peer-reviewed sources
- **Highly Cited** — Sources with 100+ citations

### Quality Thresholds

Academic Mode enforces minimum quality standards:

- **Minimum peer-reviewed sources**: 5 (configurable)
- **Source quality threshold**: 7/10 (configurable)
- **Citation completeness**: 90%+ with full metadata

---

## Advanced Features

### 1. Methodology Extraction

Automatically extracts and documents research methodologies from papers.

**Extracted Information**:
- Study design (experimental, survey, case study, etc.)
- Data collection methods
- Sample sizes and characteristics
- Analytical techniques
- Limitations and constraints

**Example Output**:
```
Methodology

The reviewed studies employed diverse methodological approaches. 
Quantitative studies (n=12) utilized experimental designs with 
sample sizes ranging from 50 to 500 participants (Smith et al., 
2023; Chen et al., 2024). Qualitative studies (n=5) employed 
semi-structured interviews and thematic analysis (Johnson & Lee, 
2023). Mixed-methods approaches (n=3) combined surveys with 
follow-up interviews to triangulate findings (Wang et al., 2024).
```

### 2. Theoretical Framework Integration

Identifies and explains theoretical frameworks used in research.

**Extracted Information**:
- Theoretical models and frameworks
- Key constructs and definitions
- Relationships between constructs
- Empirical applications
- Theoretical debates

**Example Output**:
```
Theoretical Framework

This review is grounded in Social Cognitive Theory (Bandura, 1986), 
which posits that learning occurs through observation, imitation, 
and modeling within a social context. The theory emphasizes the 
reciprocal relationship between personal factors, behavior, and 
environmental influences. Recent applications of this framework 
to online learning environments (Smith & Johnson, 2023) have 
extended the theory to account for digital social interactions.
```

### 3. Research Impact Analysis

Analyzes citation counts and research influence.

**Features**:
- Identifies highly cited papers (100+ citations)
- Tracks citation trends over time
- Identifies seminal works in the field
- Documents research impact and influence

**Example Output**:
```
Research Impact

Several highly influential studies have shaped this field. The 
seminal work by Smith and Johnson (2020, cited 1,247 times) 
established the foundational framework still used today. Recent 
meta-analyses (Chen et al., 2023, cited 342 times) have synthesized 
findings across 50+ studies, providing robust evidence for the 
effectiveness of these interventions.
```

### 4. Interdisciplinary Research Support

Integrates perspectives from multiple disciplines.

**Features**:
- Searches across multiple academic disciplines
- Identifies disciplinary perspectives
- Highlights convergence and divergence
- Translates discipline-specific terminology
- Synthesizes cross-disciplinary insights

**Example**:
```bash
# Interdisciplinary research
python -m gazzali.gazzali --academic \
    --discipline general \
    "Climate change adaptation: Integrating social, economic, and environmental perspectives"
```

---

## Troubleshooting

### Issue: Insufficient Peer-Reviewed Sources

**Symptom**:
```
⚠️  Warning: Only 3 peer-reviewed sources found (minimum: 5)
```

**Solutions**:
1. Broaden search terms
2. Adjust time range (include older seminal works)
3. Lower quality threshold temporarily: `export SOURCE_QUALITY_THRESHOLD=6`
4. Use `--refine` to improve question specificity

### Issue: Citation Extraction Failed

**Symptom**:
```
⚠️  Warning: Incomplete citation metadata for some sources
```

**Solutions**:
1. Check internet connection
2. Verify SERPER_API_KEY is set correctly
3. Sources will still be included with [Incomplete] flag
4. Manually complete citations in output file if needed

### Issue: Academic Report Generation Failed

**Symptom**:
```
❌ Academic report generation failed: ...
```

**Solutions**:
1. Check OPENROUTER_API_KEY is valid
2. Ensure sufficient API credits
3. Verify academic modules installed: `pip install -r requirements.txt`
4. Check output directory permissions

### Issue: Wrong Citation Style

**Symptom**: Citations not in expected format

**Solutions**:
1. Verify `--citation-style` flag: `--citation-style apa`
2. Check environment variable: `echo $CITATION_STYLE`
3. Ensure no conflicting workflow settings
4. Regenerate report with correct style

### Issue: Report Too Short/Long

**Symptom**: Word count doesn't match target

**Solutions**:
1. Adjust `--word-count` parameter
2. Check if question scope matches target length
3. Use `--refine` to adjust question scope
4. Consider different output format (abstract vs. paper)

---

## Best Practices

### 1. Start with Question Refinement

Always use `--refine` for broad topics:

```bash
python -m gazzali.gazzali --academic --refine "Broad topic"
```

This ensures focused, answerable research questions.

### 2. Choose Appropriate Output Format

Match format to your needs:

- **Paper** — Full research papers, journal articles
- **Review** — Literature reviews, state-of-the-art surveys
- **Proposal** — Grant applications, dissertation proposals
- **Abstract** — Conference submissions, brief summaries
- **Presentation** — Talks, presentations, teaching materials

### 3. Select Correct Discipline

Use discipline-specific settings for better results:

```bash
# STEM research
--discipline stem --citation-style ieee

# Social sciences
--discipline social --citation-style apa

# Humanities
--discipline humanities --citation-style mla

# Medical research
--discipline medical --citation-style apa
```

### 4. Export Bibliography

Always export bibliography for reference management:

```bash
python -m gazzali.gazzali --academic --export-bib "Your question"
```

Import the .bib file into Zotero, Mendeley, or EndNote.

### 5. Use Workflow Templates

Start with preset workflows for common tasks:

```bash
# Literature review
python -m gazzali.gazzali --academic --workflow literature_review "Your question"

# Systematic review
python -m gazzali.gazzali --academic --workflow systematic_review "Your question"
```

See [Workflow Configuration Guide](WORKFLOW_CONFIGURATION.md) for details.

### 6. Verify Source Quality

Check the quality metrics in the output:

```
📊 Report Metrics:
  • Peer-Reviewed:     18 (78.3%)
```

Aim for 70%+ peer-reviewed sources for academic work.

### 7. Review and Edit

Academic Mode produces high-quality drafts, but always:

- Verify citations are complete and accurate
- Check for discipline-specific terminology
- Ensure arguments are well-supported
- Add your own analysis and insights
- Proofread for clarity and coherence

---

## Integration with Reference Managers

### Zotero

```bash
# Export bibliography
python -m gazzali.gazzali --academic --export-bib "Your question"

# Import to Zotero
# File → Import → Select .bib file
```

### Mendeley

```bash
# Export bibliography
python -m gazzali.gazzali --academic --export-bib "Your question"

# Import to Mendeley
# File → Import → BibTeX → Select .bib file
```

### EndNote

```bash
# Export bibliography
python -m gazzali.gazzali --academic --export-bib "Your question"

# Import to EndNote
# File → Import → File → Select .bib file
# Import Option: BibTeX
```

---

## Comparison: Standard vs. Academic Mode

| Feature | Standard Mode | Academic Mode |
|---------|---------------|---------------|
| **Sources** | General web, news, blogs | Peer-reviewed journals, Scholar |
| **Citations** | URLs only | Full bibliographic data |
| **Writing Style** | Conversational | Formal academic |
| **Structure** | Flexible | Structured sections |
| **Quality Control** | Basic | Peer-review prioritization |
| **Bibliography** | No | Yes, with export |
| **Discipline Settings** | No | Yes (STEM, social, etc.) |
| **Question Refinement** | No | Yes (FINER criteria) |
| **Word Count Target** | ~2000 | 4000-15000 (configurable) |

---

## Frequently Asked Questions

### Q: Can I use Academic Mode for non-academic research?

**A**: Yes! Academic Mode is beneficial for any research requiring:
- Credible, peer-reviewed sources
- Proper citations and references
- Formal writing style
- Structured analysis

### Q: How much does Academic Mode cost?

**A**: Academic Mode uses the same APIs as standard mode (OpenRouter, Serper, Jina). Costs depend on:
- Research complexity
- Number of sources consulted
- Report length
- Model selection

Typical cost: $0.50-$2.00 per research session.

### Q: Can I customize citation styles?

**A**: Currently supports APA, MLA, Chicago, and IEEE. For other styles:
1. Use closest available style
2. Manually adjust in output file
3. Use reference manager for conversion

### Q: How accurate are the citations?

**A**: Citation accuracy depends on source metadata availability:
- Google Scholar results: 90%+ complete
- Web sources: 70-80% complete
- Incomplete citations flagged with [Incomplete]

Always verify citations before publication.

### Q: Can I use my own research papers?

**A**: Currently, Gazzali searches public sources. To include your own papers:
1. Ensure they're indexed in Google Scholar
2. Include specific search terms
3. Manually add citations if needed

### Q: Does Academic Mode support languages other than English?

**A**: Currently optimized for English. For other languages:
- Research agent may return mixed-language results
- Citations may be incomplete for non-English sources
- Consider using English search terms for better results

### Q: How do I cite Gazzali Research in my work?

**A**: Gazzali is a research tool, not a source. Cite the original sources it finds, not Gazzali itself. Always verify and read original sources.

### Q: Can I use Academic Mode for systematic reviews?

**A**: Yes! Use the systematic review workflow:

```bash
python -m gazzali.gazzali --academic --workflow systematic_review "Your question"
```

However, for publication-quality systematic reviews:
- Manually verify search strategy
- Document inclusion/exclusion criteria
- Perform quality assessment
- Follow PRISMA guidelines

---

## See Also

- [CLI Interface Documentation](CLI_INTERFACE.md) — Complete command-line reference
- [Citation Styles Guide](CITATION_STYLES.md) — Detailed citation formatting examples
- [Output Formats Reference](OUTPUT_FORMATS.md) — Document format specifications
- [Discipline Settings](DISCIPLINE_SETTINGS.md) — Discipline-specific conventions
- [Workflow Configuration](WORKFLOW_CONFIGURATION.md) — Workflow templates and customization
- [Environment Setup](ENVIRONMENT_SETUP.md) — Configuration and API keys

---

## Support and Feedback

For issues, questions, or suggestions:

1. Check this documentation and troubleshooting section
2. Review [GitHub Issues](https://github.com/MedAIScientist/DeepResearch/issues)
3. Open a new issue with:
   - Command used
   - Error messages
   - Expected vs. actual behavior
   - Environment details (OS, Python version)

---

## Credits

Academic Mode builds on:
- **Alibaba Tongyi DeepResearch** — Research agent
- **xAI grok-4-fast** — Synthesis model
- **Google Scholar** (via Serper) — Academic search
- **Jina AI Reader** — Content extraction

Named after **Al-Ghazali** (1058-1111), whose systematic approach to scholarship and commitment to rigorous intellectual inquiry inspire this tool's academic features.

---

**Last Updated**: January 2024  
**Version**: 1.0.0
