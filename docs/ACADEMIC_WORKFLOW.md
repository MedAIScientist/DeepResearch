# Academic Workflow in Gazzali Research CLI

This document describes the academic research workflow implemented in the Gazzali Research CLI, which provides enhanced features for scholarly research including citation management, literature review synthesis, and academic report generation.

## Overview

The academic workflow is activated using the `--academic` flag and provides:

- **Question Refinement**: Refine broad topics into specific research questions using FINER criteria
- **Citation Management**: Automatic tracking and formatting of sources in multiple citation styles
- **Scholar-First Search**: Prioritize peer-reviewed academic sources
- **Academic Report Generation**: Generate structured reports following academic conventions
- **Bibliography Export**: Export citations in BibTeX format for reference managers

## Command-Line Interface

### Basic Academic Research

```bash
python -m gazzali.gazzali --academic "Your research question"
```

This enables academic mode with default settings (APA citations, paper format).

### Full Academic Workflow

```bash
python -m gazzali.gazzali \
  --academic \
  --citation-style apa \
  --output-format paper \
  --discipline stem \
  --refine \
  --word-count 8000 \
  --export-bib \
  "Your broad research topic"
```

## Workflow Steps

### 1. Configuration Loading

When `--academic` flag is used, the system:

1. Loads academic configuration from environment variables (`.env` file)
2. Overrides with command-line arguments if provided
3. Validates configuration settings
4. Displays configuration summary

**Environment Variables:**
```bash
CITATION_STYLE=apa              # apa, mla, chicago, ieee
OUTPUT_FORMAT=paper             # paper, review, proposal, abstract, presentation
DISCIPLINE=general              # general, stem, social, humanities, medical
WORD_COUNT_TARGET=8000          # Target word count
SCHOLAR_PRIORITY=true           # Prioritize Scholar tool
EXPORT_BIBLIOGRAPHY=false       # Export .bib file
MIN_PEER_REVIEWED_SOURCES=5     # Minimum peer-reviewed sources
SOURCE_QUALITY_THRESHOLD=7      # Quality threshold (0-10)
```

### 2. Question Refinement (Optional)

When `--refine` flag is used:

1. Analyzes the broad topic using an LLM
2. Generates 3-5 specific research questions following FINER criteria:
   - **F**easible: Can be investigated with available resources
   - **I**nteresting: Engages researchers and has potential impact
   - **N**ovel: Addresses a gap in knowledge
   - **E**thical: Can be conducted ethically
   - **R**elevant: Has significance for theory, practice, or policy
3. Identifies question type (descriptive, comparative, causal, etc.)
4. Assesses scope and provides feasibility notes
5. Displays refined questions and uses the best one for research

**Example:**
```bash
# Input: "AI in education"
# Output: "What are the effects of AI-powered adaptive learning systems 
#          on student engagement and learning outcomes in K-12 mathematics education?"
```

### 3. Citation Manager Initialization

The system initializes a `CitationManager` instance that:

- Tracks all sources consulted during research
- Extracts bibliographic metadata (authors, year, title, venue, DOI)
- Detects and prevents duplicate citations
- Formats citations according to the selected style
- Generates sorted bibliographies

**Citation Styles Supported:**
- **APA 7th Edition**: (Author, Year) inline, hanging indent bibliography
- **MLA 9th Edition**: (Author Page) inline, works cited format
- **Chicago 17th Edition**: (Author Year) or footnotes with full bibliography
- **IEEE**: [Number] inline, numbered references

### 4. Research Execution

The research agent conducts deep research with academic enhancements:

1. **Scholar-First Strategy**: Prioritizes Google Scholar for peer-reviewed sources
2. **Source Quality Evaluation**: Scores sources based on credibility (peer-reviewed=10, institutional=7, web=3)
3. **Metadata Extraction**: Captures full bibliographic information
4. **Citation Tracking**: Automatically adds sources to CitationManager
5. **Methodology Identification**: Extracts research methods from papers
6. **Theory Extraction**: Identifies theoretical frameworks

**Research Process:**
```
Question → Scholar Search → Visit Papers → Extract Citations → General Search (if needed)
```

### 5. Academic Report Generation

After research completes, the system generates a structured academic report:

1. **Synthesis Model Call**: Uses advanced LLM (default: grok-2-1212) with academic prompts
2. **Section Structuring**: Organizes content into required sections based on output format
3. **Citation Formatting**: Formats inline citations and generates bibliography
4. **Academic Writing Style**: Ensures formal tone, third-person perspective, hedging language
5. **Quality Validation**: Checks for required sections and proper structure

**Report Sections by Format:**

**Paper Format:**
- Abstract
- Introduction
- Literature Review
- Methodology
- Findings
- Discussion
- Conclusion
- References

**Literature Review Format:**
- Abstract
- Introduction
- Thematic Analysis
- Research Gaps
- Future Directions
- References

**Research Proposal Format:**
- Background
- Research Questions
- Literature Review
- Proposed Methodology
- Expected Outcomes
- Timeline
- References

**Abstract Format:**
- Abstract (250-300 words)

**Presentation Format:**
- Overview
- Key Findings
- Implications
- Conclusions

### 6. Bibliography Export (Optional)

When `--export-bib` flag is used:

1. Generates BibTeX file with all citations
2. Saves to same directory as report with `.bib` extension
3. Compatible with LaTeX, Zotero, Mendeley, and other reference managers

**BibTeX Format:**
```bibtex
@article{smith_2020_a1b2c3d4,
  author = {Smith, John and Doe, Jane},
  title = {Machine Learning in Education},
  journal = {Journal of Educational Technology},
  year = {2020},
  volume = {15},
  number = {3},
  pages = {123-145},
  doi = {10.1234/jet.2020.123},
}
```

### 7. Output Saving

Reports are saved in multiple formats:

1. **Primary Report**: Basic markdown with research findings
2. **Academic Report**: Structured markdown with proper formatting
3. **Bibliography** (optional): BibTeX file for citations

**Output Directory Structure:**
```
outputs/
├── reports/
│   ├── report_20241117_143022.md           # Primary report
│   ├── academic_paper_20241117_143022_your_topic.md  # Academic report
│   └── academic_paper_20241117_143022_your_topic.bib # Bibliography (if --export-bib)
└── [research data files]
```

## Examples

### Example 1: STEM Research Paper

```bash
python -m gazzali.gazzali \
  --academic \
  --citation-style ieee \
  --output-format paper \
  --discipline stem \
  --word-count 6000 \
  "What are the latest advances in quantum computing error correction?"
```

**Output:**
- IEEE-style citations [1], [2], [3]
- Technical terminology and notation
- Focus on experimental methods and quantitative results
- Emphasis on reproducibility and statistical rigor

### Example 2: Social Sciences Literature Review

```bash
python -m gazzali.gazzali \
  --academic \
  --citation-style apa \
  --output-format review \
  --discipline social \
  --refine \
  "Social media and mental health"
```

**Refined Question:**
"What is the relationship between social media usage patterns and mental health outcomes among adolescents aged 13-18?"

**Output:**
- APA-style citations (Author, Year)
- Thematic organization of literature
- Mixed-methods research synthesis
- Discussion of cultural context and social dynamics

### Example 3: Humanities Research Proposal

```bash
python -m gazzali.gazzali \
  --academic \
  --citation-style mla \
  --output-format proposal \
  --discipline humanities \
  --export-bib \
  "Postcolonial perspectives in contemporary literature"
```

**Output:**
- MLA-style citations (Author Page)
- Theoretical framework discussion
- Interpretive analysis approach
- Proposal structure with timeline
- BibTeX export for reference management

### Example 4: Medical Research Abstract

```bash
python -m gazzali.gazzali \
  --academic \
  --citation-style apa \
  --output-format abstract \
  --discipline medical \
  --word-count 300 \
  "Efficacy of mRNA vaccines against COVID-19 variants"
```

**Output:**
- Concise 250-300 word abstract
- Clinical terminology and evidence hierarchy
- Focus on patient outcomes and safety
- Suitable for conference submission

## Configuration Options

### Citation Styles

| Style | Inline Format | Bibliography Format | Best For |
|-------|--------------|---------------------|----------|
| APA | (Author, Year) | Hanging indent, alphabetical | Psychology, Education, Social Sciences |
| MLA | (Author Page) | Works Cited, alphabetical | Humanities, Literature, Arts |
| Chicago | (Author Year) or footnotes | Full bibliography | History, Arts, Humanities |
| IEEE | [Number] | Numbered references | Engineering, Computer Science, Technology |

### Output Formats

| Format | Word Count | Sections | Use Case |
|--------|-----------|----------|----------|
| Paper | 6000-10000 | Full research paper | Journal submission, thesis chapters |
| Review | 5000-8000 | Literature synthesis | Literature reviews, state-of-the-art surveys |
| Proposal | 3000-5000 | Research plan | Grant applications, thesis proposals |
| Abstract | 250-300 | Summary only | Conference submissions, poster presentations |
| Presentation | 1500-2500 | Key points | Oral presentations, seminars |

### Disciplines

| Discipline | Focus | Terminology | Methodology Emphasis |
|------------|-------|-------------|---------------------|
| General | Interdisciplinary | Accessible | Flexible |
| STEM | Technical, quantitative | Scientific notation | Experimental, statistical |
| Social | Human behavior, society | Social science constructs | Surveys, mixed-methods |
| Humanities | Interpretation, culture | Theoretical frameworks | Textual analysis, hermeneutics |
| Medical | Clinical, evidence-based | Medical terminology | RCTs, systematic reviews |

## Advanced Features

### Source Quality Filtering

The system evaluates source credibility:

- **Peer-reviewed journals**: Score 10 (highest priority)
- **Institutional publications**: Score 7
- **General web sources**: Score 3
- **Minimum threshold**: Configurable (default: 7)

Sources below the threshold are flagged or filtered in academic mode.

### Methodology Extraction

Automatically identifies and documents:

- Research design (qualitative, quantitative, mixed-methods)
- Data collection methods (surveys, experiments, interviews)
- Sample characteristics and size
- Analytical techniques
- Limitations and constraints

### Theoretical Framework Integration

Extracts and discusses:

- Theoretical models and frameworks
- Key constructs and their relationships
- Operationalization of concepts
- Theoretical contributions

### Research Impact Analysis

Tracks and reports:

- Citation counts for key papers
- Highly cited works (>100 citations)
- Research implications (theoretical and practical)
- Future research directions

## Troubleshooting

### Issue: "Cannot refine question: API key not set"

**Solution:** Ensure `OPENROUTER_API_KEY` is set in your environment:
```bash
export OPENROUTER_API_KEY="sk-or-v1-your-key"
```

### Issue: "Academic report generation not available"

**Solution:** Check that all required modules are installed:
```bash
pip install -r requirements.txt
```

### Issue: "Insufficient peer-reviewed sources"

**Solution:** 
1. Broaden your search terms
2. Check Google Scholar API access
3. Lower `MIN_PEER_REVIEWED_SOURCES` in configuration
4. Use `--discipline general` for more flexible source requirements

### Issue: "Word count significantly below target"

**Solution:**
1. Increase `--word-count` parameter
2. Use more comprehensive output format (e.g., `paper` instead of `abstract`)
3. Provide more specific research question
4. Check that synthesis model has sufficient context

### Issue: "Bibliography export failed"

**Solution:**
1. Ensure write permissions in output directory
2. Check that citations were captured during research
3. Verify `--export-bib` flag is set
4. Check for special characters in filenames

## Integration with Reference Managers

### Zotero

1. Generate bibliography with `--export-bib`
2. In Zotero: File → Import → Select `.bib` file
3. Citations are automatically added to your library

### Mendeley

1. Generate bibliography with `--export-bib`
2. In Mendeley: File → Import → BibTeX → Select `.bib` file
3. Review and organize imported references

### LaTeX

1. Generate report with `--export-bib`
2. In your LaTeX document:
```latex
\bibliography{academic_paper_20241117_143022_your_topic}
\bibliographystyle{plain}
```
3. Compile with: `pdflatex → bibtex → pdflatex → pdflatex`

## Best Practices

### 1. Question Formulation

- **Use --refine for broad topics**: Let the system help narrow your focus
- **Be specific**: Include population, variables, and context
- **Follow FINER criteria**: Ensure questions are feasible and relevant

### 2. Citation Management

- **Always use --export-bib**: Build your reference library incrementally
- **Choose appropriate style**: Match your target publication venue
- **Review citations**: Check for completeness and accuracy

### 3. Output Format Selection

- **Paper**: For comprehensive research and journal submission
- **Review**: For literature synthesis and state-of-the-art surveys
- **Proposal**: For grant applications and research planning
- **Abstract**: For conference submissions
- **Presentation**: For oral presentations and seminars

### 4. Discipline Settings

- **Match your field**: Use appropriate discipline for terminology and conventions
- **STEM**: For technical, quantitative research
- **Social**: For human behavior and society studies
- **Humanities**: For interpretive and cultural analysis
- **Medical**: For clinical and evidence-based research

### 5. Quality Assurance

- **Review generated reports**: Check for accuracy and completeness
- **Verify citations**: Ensure proper attribution and formatting
- **Check methodology**: Validate research methods and analysis
- **Assess limitations**: Consider scope and constraints

## Future Enhancements

Planned features for future releases:

- **Direct database integration**: PubMed, IEEE Xplore, ACM Digital Library
- **PDF analysis**: Extract text and figures from papers
- **Citation network visualization**: Generate citation graphs
- **Collaborative features**: Share research projects and bibliographies
- **LaTeX export**: Generate publication-ready LaTeX documents
- **Systematic review tools**: PRISMA flow diagrams, quality assessment
- **Meta-analysis support**: Statistical synthesis of multiple studies
- **Institutional repository search**: University repositories and preprint servers

## Support and Feedback

For issues, questions, or feature requests:

1. Check this documentation first
2. Review the main README.md
3. Check existing issues on GitHub
4. Create a new issue with:
   - Command used
   - Error message or unexpected behavior
   - Expected outcome
   - System information

## References

- APA Style Guide (7th Edition): https://apastyle.apa.org/
- MLA Handbook (9th Edition): https://style.mla.org/
- Chicago Manual of Style (17th Edition): https://www.chicagomanualofstyle.org/
- IEEE Editorial Style Manual: https://www.ieee.org/content/dam/ieee-org/ieee/web/org/conferences/style_references_manual.pdf
- FINER Criteria: Hulley et al. (2013). Designing Clinical Research. 4th ed.

---

*Last Updated: November 17, 2024*
*Version: 1.0*
