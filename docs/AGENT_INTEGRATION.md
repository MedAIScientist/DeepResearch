# Academic Prompts Integration in Research Agent

## Overview

The Gazzali Research system integrates academic-specific prompts into the DeepResearch agent to enhance scholarly research capabilities. When academic mode is enabled, the agent uses specialized prompts that prioritize peer-reviewed sources, proper citation practices, and rigorous methodology.

## Architecture

### Component Flow

```
gazzali.py (CLI)
    ↓
    Sets environment variables:
    - GAZZALI_ACADEMIC_MODE
    - GAZZALI_DISCIPLINE
    - GAZZALI_OUTPUT_FORMAT
    - GAZZALI_CITATION_STYLE
    ↓
run_multi_react.py
    ↓
react_agent.py (MultiTurnReactAgent)
    ↓
    Reads environment variables
    ↓
    Loads academic prompts if enabled
    ↓
    Applies discipline-specific modifiers
```

### Academic Mode Detection

The research agent detects academic mode through environment variables set by the CLI:

1. **GAZZALI_ACADEMIC_MODE**: Set to "true" when `--academic` flag is used
2. **GAZZALI_DISCIPLINE**: Academic discipline (stem, social, humanities, medical, general)
3. **GAZZALI_OUTPUT_FORMAT**: Desired output format (paper, review, proposal, abstract, presentation)
4. **GAZZALI_CITATION_STYLE**: Citation format (apa, mla, chicago, ieee)

## Implementation Details

### Modified Files

#### 1. `src/gazzali/DeepResearch/inference/react_agent.py`

**Changes:**
- Added import for academic prompts module
- Added academic mode detection in `_run()` method
- Replaced standard `SYSTEM_PROMPT` with `get_academic_research_prompt()` when academic mode is enabled
- Applied discipline-specific and format-specific prompt modifiers

**Key Code:**
```python
# Academic mode detection
academic_mode = os.getenv("GAZZALI_ACADEMIC_MODE", "false").lower() == "true"

if academic_mode and ACADEMIC_PROMPTS_AVAILABLE:
    # Get configuration from environment
    discipline = os.getenv("GAZZALI_DISCIPLINE", "general")
    output_format = os.getenv("GAZZALI_OUTPUT_FORMAT", "paper")
    
    # Generate academic prompt with modifiers
    system_prompt = get_academic_research_prompt(
        discipline=discipline,
        output_format=output_format
    )
```

#### 2. `src/gazzali/gazzali.py`

**Changes:**
- Updated `run_research()` function to accept `academic_config` parameter
- Set environment variables before launching research agent
- Pass academic configuration to research function calls

**Key Code:**
```python
# Set academic mode environment variables
if academic_mode and academic_config:
    os.environ["GAZZALI_ACADEMIC_MODE"] = "true"
    os.environ["GAZZALI_DISCIPLINE"] = academic_config.discipline.value
    os.environ["GAZZALI_OUTPUT_FORMAT"] = academic_config.output_format.value
    os.environ["GAZZALI_CITATION_STYLE"] = academic_config.citation_style.value
```

## Academic Prompt Features

### 1. Source Prioritization

The academic prompt instructs the agent to:
- **Always use Google Scholar first** before general web searches
- Prioritize peer-reviewed journals, conference proceedings, and academic books
- Evaluate source credibility based on publication venue and author credentials
- Aim for at least 5-10 peer-reviewed sources per research question

### 2. Citation Metadata Extraction

The prompt requires extraction of:
- Authors (full names)
- Publication year
- Title
- Venue (journal, conference, publisher)
- Volume, issue, and page numbers
- DOI and URL
- Citation count from Google Scholar
- Abstract

### 3. Methodology Identification

The agent is instructed to:
- Identify research design (experimental, observational, survey, etc.)
- Document data collection methods
- Extract sample characteristics
- Note data analysis techniques
- Identify limitations and ethical considerations
- Classify as quantitative, qualitative, or mixed-methods

### 4. Critical Analysis

The prompt emphasizes:
- Evidence quality assessment
- Identification of potential biases
- Analysis of conflicting findings
- Evaluation of generalizability
- Balanced discussion of strengths and limitations

## Discipline-Specific Modifiers

### STEM Disciplines

**Focus:**
- Technical and scientific terminology
- Experimental design and statistical analysis
- Reproducibility and empirical validation
- Mathematical notation and equations

**Source Priorities:**
- Nature, Science, IEEE, ACM journals
- Experimental studies and systematic reviews
- Preprints from arXiv, bioRxiv

### Social Sciences

**Focus:**
- Social science theoretical frameworks
- Qualitative and quantitative methods
- Validity, reliability, generalizability
- Cultural context and human behavior

**Source Priorities:**
- American Sociological Review, Psychological Science
- Longitudinal studies and RCTs
- Government statistics and demographic data

### Humanities

**Focus:**
- Critical theory and hermeneutics
- Textual analysis and close reading
- Historical methods and archival research
- Interpretive frameworks

**Source Priorities:**
- Humanities journals and university presses
- Primary sources and archival materials
- Scholarly monographs

### Medical/Health Sciences

**Focus:**
- Clinical terminology and diagnostic criteria
- Evidence-based practice
- Clinical trials and systematic reviews
- Patient outcomes and safety

**Source Priorities:**
- NEJM, Lancet, JAMA, BMJ
- Cochrane systematic reviews
- Clinical practice guidelines
- FDA/EMA reports

## Output Format Modifiers

### Research Paper
- Full structure: Abstract, Introduction, Literature Review, Methodology, Findings, Discussion, Conclusion
- Comprehensive, in-depth analysis
- Extensive citations and thorough discussion

### Literature Review
- Thematic analysis organized by themes or chronologically
- Synthesis of existing literature
- Identification of patterns, contradictions, and gaps
- Future research directions

### Research Proposal
- Background, Research Questions, Literature Review, Proposed Methodology
- Forward-looking analysis
- Emphasis on feasibility and significance

### Conference Abstract
- Concise 250-300 words
- Background, Methods, Results, Conclusions
- Clear, accessible language

### Presentation
- Key points and main findings
- Bullet points and clear headings
- Focus on main ideas and practical implications

## Usage Examples

### Basic Academic Mode

```bash
python -m gazzali.gazzali --academic "Impact of AI on education"
```

This enables:
- Academic research prompts
- Scholar-first search strategy
- Default APA citations
- Paper format output
- General discipline settings

### STEM Research Paper

```bash
python -m gazzali.gazzali --academic --discipline stem \
    --output-format paper --citation-style ieee \
    "Machine learning approaches to protein folding"
```

This enables:
- STEM-specific terminology and methodology focus
- IEEE citation format
- Full research paper structure
- Technical and scientific emphasis

### Social Sciences Literature Review

```bash
python -m gazzali.gazzali --academic --discipline social \
    --output-format review --citation-style apa \
    "Social media effects on adolescent mental health"
```

This enables:
- Social science theoretical frameworks
- Literature review structure
- APA citation format
- Focus on qualitative and quantitative methods

### Medical Research Proposal

```bash
python -m gazzali.gazzali --academic --discipline medical \
    --output-format proposal --citation-style ama \
    "Novel immunotherapy approaches for cancer treatment"
```

This enables:
- Medical terminology and clinical focus
- Research proposal structure
- AMA citation format
- Evidence-based practice emphasis

## Troubleshooting

### Academic Prompts Not Loading

**Symptom:** Agent uses standard prompts despite `--academic` flag

**Possible Causes:**
1. Import error in `react_agent.py`
2. Environment variables not set correctly
3. Academic prompts module not found

**Solution:**
- Check console output for "Academic Mode: Loading enhanced academic research prompts"
- Verify `ACADEMIC_PROMPTS_AVAILABLE` is True
- Check Python path includes gazzali package

### Discipline Modifiers Not Applied

**Symptom:** Generic academic prompts used instead of discipline-specific

**Possible Causes:**
1. Invalid discipline value
2. Environment variable not set
3. Typo in discipline name

**Solution:**
- Verify discipline is one of: stem, social, humanities, medical, general
- Check `GAZZALI_DISCIPLINE` environment variable
- Use lowercase discipline names

### Scholar Tool Not Prioritized

**Symptom:** Agent uses general search before Scholar

**Possible Causes:**
1. Academic mode not enabled
2. Prompt not loaded correctly
3. Agent ignoring prompt instructions

**Solution:**
- Verify academic mode is enabled
- Check system prompt includes Scholar-first instructions
- Review agent logs for tool call order

## Testing

### Manual Testing

1. **Test Academic Mode Activation:**
   ```bash
   python -m gazzali.gazzali --academic "test question"
   ```
   Expected: Console shows "🎓 Academic Mode: Loading enhanced academic research prompts"

2. **Test Discipline Modifiers:**
   ```bash
   python -m gazzali.gazzali --academic --discipline stem "test question"
   ```
   Expected: Console shows "Discipline: STEM"

3. **Test Scholar-First Strategy:**
   - Run academic mode research
   - Check agent logs for tool calls
   - Verify `google_scholar` called before `search`

### Automated Testing

See `tests/test_academic_agent_integration.py` for unit tests covering:
- Academic mode detection
- Prompt loading
- Discipline modifier application
- Environment variable handling

## Performance Considerations

### Token Usage

Academic prompts are longer than standard prompts due to:
- Detailed source prioritization instructions
- Citation metadata extraction requirements
- Methodology identification guidelines
- Discipline-specific modifiers

**Impact:** ~2-3x increase in system prompt tokens

**Mitigation:**
- Prompts are loaded once per research session
- Modifiers are applied selectively based on discipline
- Core instructions remain concise

### Research Time

Academic mode may increase research time due to:
- Scholar-first search strategy (Scholar queries slower than web search)
- More thorough source evaluation
- Citation metadata extraction

**Impact:** ~20-30% increase in research time

**Mitigation:**
- Parallel Scholar queries when possible
- Caching of Scholar results
- Efficient metadata extraction

## Future Enhancements

### Planned Features

1. **Dynamic Prompt Adjustment:**
   - Adjust prompt complexity based on question type
   - Reduce prompt length for simple queries

2. **Citation Manager Integration:**
   - Pass citation manager instance to agent
   - Real-time citation tracking during research

3. **Source Quality Filtering:**
   - Implement source scoring in agent
   - Filter low-quality sources automatically

4. **Methodology Extraction:**
   - Structured methodology data extraction
   - Methodology comparison across studies

5. **Theoretical Framework Tracking:**
   - Identify and track theoretical frameworks
   - Build theory-evidence connections

## References

- Academic Prompts Module: `src/gazzali/prompts/academic_prompts.py`
- Academic Configuration: `src/gazzali/academic_config.py`
- Research Agent: `src/gazzali/DeepResearch/inference/react_agent.py`
- CLI Interface: `src/gazzali/gazzali.py`

## Support

For issues or questions about academic prompt integration:
1. Check console output for error messages
2. Verify environment variables are set correctly
3. Review agent logs for prompt loading
4. Consult troubleshooting section above

---

**Last Updated:** 2024-11-17
**Version:** 1.0.0
