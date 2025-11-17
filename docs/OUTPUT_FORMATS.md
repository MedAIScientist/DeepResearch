# Output Formats Guide

This document describes the academic output formats supported by Gazzali Research. Each format is optimized for specific academic purposes, with tailored structure, length, and emphasis to meet the requirements of different scholarly contexts.

## Table of Contents

- [Overview](#overview)
- [Paper Format](#paper-format)
- [Literature Review Format](#literature-review-format)
- [Research Proposal Format](#research-proposal-format)
- [Abstract Format](#abstract-format)
- [Presentation Format](#presentation-format)
- [Format Comparison](#format-comparison)
- [Usage Examples](#usage-examples)
- [Customization Options](#customization-options)
- [Best Practices](#best-practices)

## Overview

Gazzali Research supports five distinct output formats, each designed for specific academic contexts:

| Format | Purpose | Typical Length | Best For |
|--------|---------|----------------|----------|
| **Paper** | Full research paper | 6,000-12,000 words | Journal articles, dissertations, comprehensive reports |
| **Review** | Literature review | 5,000-10,000 words | State-of-the-art surveys, systematic reviews, thesis chapters |
| **Proposal** | Research proposal | 3,000-8,000 words | Grant applications, dissertation proposals, project plans |
| **Abstract** | Conference abstract | 250-500 words | Conference submissions, brief summaries |
| **Presentation** | Presentation slides | 1,000-2,000 words | Academic talks, teaching materials, seminars |

### Selecting a Format

Choose your output format using the `--output-format` flag:

```bash
python -m gazzali.gazzali --academic \
    --output-format paper \
    "Your research question"
```

Available options: `paper`, `review`, `proposal`, `abstract`, `presentation`

---

## Paper Format

### Purpose

The **Paper** format generates a complete research paper suitable for journal submission, dissertation chapters, or comprehensive academic reports. It follows traditional academic paper structure with full sections for introduction, literature review, methodology, findings, discussion, and conclusion.

### Structure

#### Standard Sections

1. **Abstract** (200-300 words)
   - Brief overview of the research
   - Key findings and implications
   - Structured or unstructured depending on discipline

2. **Introduction** (800-1,500 words)
   - Research context and background
   - Problem statement
   - Research questions or hypotheses
   - Significance and contribution
   - Paper organization overview

3. **Literature Review** (2,000-4,000 words)
   - Theoretical frameworks
   - Previous research synthesis
   - Thematic organization
   - Research gaps identification
   - Positioning of current work

4. **Methodology** (1,000-2,000 words)
   - Research design
   - Data collection methods
   - Sample/participants
   - Analytical techniques
   - Limitations and constraints

5. **Findings** (1,500-3,000 words)
   - Presentation of results
   - Data analysis
   - Statistical findings
   - Thematic findings
   - Tables and figures

6. **Discussion** (1,500-2,500 words)
   - Interpretation of findings
   - Comparison with previous research
   - Theoretical implications
   - Practical implications
   - Limitations
   - Future research directions

7. **Conclusion** (500-800 words)
   - Summary of key findings
   - Contributions to the field
   - Final implications
   - Closing remarks

8. **References**
   - Complete bibliography
   - Formatted in specified citation style

### Example Output Structure

```markdown
# [Research Paper Title]

## Abstract

This study investigates [topic] through [methodology]. Analysis of [data/sources] 
reveals [key findings]. Results indicate [main conclusions]. Implications for 
[field/practice] are discussed.

**Keywords**: keyword1, keyword2, keyword3, keyword4, keyword5

---

## 1. Introduction

### 1.1 Background

[Context and background information...]

### 1.2 Research Problem

[Problem statement and research gap...]

### 1.3 Research Questions

This study addresses the following research questions:
1. [Research question 1]
2. [Research question 2]

### 1.4 Significance

[Contribution and importance...]

---

## 2. Literature Review

### 2.1 Theoretical Framework

[Theoretical foundations...]

### 2.2 Previous Research

[Synthesis of existing literature...]

### 2.3 Research Gaps

[Identified gaps in knowledge...]

---

## 3. Methodology

### 3.1 Research Design

[Overall approach and design...]

### 3.2 Data Collection

[Methods and procedures...]

### 3.3 Analysis

[Analytical techniques...]

---

## 4. Findings

### 4.1 [Finding Category 1]

[Results and evidence...]

### 4.2 [Finding Category 2]

[Results and evidence...]

---

## 5. Discussion

### 5.1 Interpretation

[Analysis of findings...]

### 5.2 Implications

[Theoretical and practical implications...]

### 5.3 Limitations

[Study limitations...]

---

## 6. Conclusion

[Summary and final remarks...]

---

## References

[Complete bibliography in specified citation style...]
```

### Typical Word Count

- **Default**: 8,000 words
- **Range**: 6,000-12,000 words
- **Customizable**: Use `--word-count` flag

### Best Used For

- Journal article submissions
- Dissertation or thesis chapters
- Comprehensive research reports
- Academic monographs
- Technical reports requiring full documentation

### Discipline Variations

**STEM**: Emphasizes methodology, data analysis, reproducibility
**Social Sciences**: Balances qualitative and quantitative findings
**Humanities**: Focuses on textual analysis and interpretation
**Medical**: Follows CONSORT or similar reporting guidelines

---

## Literature Review Format

### Purpose

The **Review** format generates a comprehensive literature review that synthesizes existing research on a topic. It organizes findings thematically, identifies patterns and contradictions, and highlights research gaps. Ideal for systematic reviews, state-of-the-art surveys, and thesis literature review chapters.

### Structure

#### Standard Sections

1. **Abstract** (200-300 words)
   - Review scope and objectives
   - Search strategy summary
   - Key themes identified
   - Main conclusions

2. **Introduction** (800-1,200 words)
   - Topic background
   - Review objectives
   - Scope and boundaries
   - Search methodology
   - Organization of review

3. **Thematic Analysis** (3,000-6,000 words)
   - Organized by themes or chronologically
   - Synthesis of findings within each theme
   - Comparison across studies
   - Identification of patterns
   - Discussion of contradictions

4. **Research Gaps** (800-1,500 words)
   - Unanswered questions
   - Methodological limitations in existing research
   - Underexplored areas
   - Contradictory findings requiring resolution

5. **Future Directions** (500-1,000 words)
   - Recommended research priorities
   - Methodological improvements needed
   - Emerging trends
   - Practical implications for future work

6. **References**
   - Comprehensive bibliography
   - Typically 30-100+ sources

### Example Output Structure

```markdown
# Literature Review: [Topic]

## Abstract

This literature review examines [topic] by synthesizing [number] studies published 
between [years]. The review identifies [number] major themes: [theme1], [theme2], 
and [theme3]. Analysis reveals [key patterns] and highlights [research gaps]. 
Future research should focus on [recommendations].

---

## 1. Introduction

### 1.1 Background

[Context for the review...]

### 1.2 Review Objectives

This review aims to:
- [Objective 1]
- [Objective 2]
- [Objective 3]

### 1.3 Search Strategy

[Description of search methodology, databases, keywords, inclusion/exclusion criteria...]

---

## 2. Thematic Analysis

### 2.1 Theme 1: [Theme Name]

[Synthesis of research on this theme...]

**Key Studies**: [Author1 (Year), Author2 (Year)]

**Main Findings**: [Summary of findings...]

**Methodological Approaches**: [Common methods used...]

### 2.2 Theme 2: [Theme Name]

[Synthesis of research on this theme...]

### 2.3 Theme 3: [Theme Name]

[Synthesis of research on this theme...]

---

## 3. Research Gaps

### 3.1 Methodological Gaps

[Limitations in current research methods...]

### 3.2 Conceptual Gaps

[Theoretical or conceptual areas needing development...]

### 3.3 Empirical Gaps

[Unanswered empirical questions...]

---

## 4. Future Directions

### 4.1 Recommended Research Priorities

[Priority areas for future investigation...]

### 4.2 Methodological Recommendations

[Suggested improvements to research methods...]

### 4.3 Practical Implications

[Applications for practice and policy...]

---

## References

[Comprehensive bibliography...]
```

### Typical Word Count

- **Default**: 7,000 words
- **Range**: 5,000-10,000 words
- **Systematic reviews**: 8,000-15,000 words

### Best Used For

- Systematic literature reviews
- State-of-the-art surveys
- Dissertation literature review chapters
- Meta-analyses (with additional statistical analysis)
- Scoping reviews
- Critical reviews of a field

### Key Features

- **Thematic organization**: Groups studies by themes rather than chronologically
- **Synthesis focus**: Emphasizes patterns and connections across studies
- **Gap identification**: Explicitly identifies what's missing in current research
- **Comprehensive coverage**: Aims for thorough coverage of the field
- **Critical analysis**: Evaluates quality and contributions of reviewed studies

---

## Research Proposal Format

### Purpose

The **Proposal** format generates a forward-looking research proposal suitable for grant applications, dissertation proposals, or project planning. It justifies the proposed research, outlines methodology, and describes expected outcomes.

### Structure

#### Standard Sections

1. **Background** (1,000-1,500 words)
   - Problem context
   - Current state of knowledge
   - Significance of the problem
   - Rationale for proposed research

2. **Research Questions** (300-500 words)
   - Primary research questions
   - Secondary questions or hypotheses
   - Specific aims or objectives
   - Expected contributions

3. **Literature Review** (1,500-3,000 words)
   - Theoretical framework
   - Previous research synthesis
   - Research gaps
   - How proposed research addresses gaps

4. **Proposed Methodology** (1,500-2,500 words)
   - Research design
   - Data collection methods
   - Sample/participants
   - Analytical techniques
   - Feasibility considerations
   - Ethical considerations

5. **Expected Outcomes** (500-1,000 words)
   - Anticipated findings
   - Potential contributions
   - Theoretical implications
   - Practical applications
   - Dissemination plans

6. **Timeline** (300-500 words)
   - Project phases
   - Milestones
   - Deliverables
   - Duration estimates

7. **References**
   - Supporting bibliography

### Example Output Structure

```markdown
# Research Proposal: [Project Title]

## 1. Background

### 1.1 Problem Statement

[Description of the research problem...]

### 1.2 Significance

[Why this research matters...]

### 1.3 Current State of Knowledge

[What is currently known...]

---

## 2. Research Questions

### 2.1 Primary Research Question

[Main research question...]

### 2.2 Secondary Questions

1. [Secondary question 1]
2. [Secondary question 2]
3. [Secondary question 3]

### 2.3 Hypotheses

[If applicable, specific hypotheses to be tested...]

---

## 3. Literature Review

### 3.1 Theoretical Framework

[Theoretical foundations for the proposed research...]

### 3.2 Previous Research

[Synthesis of relevant existing research...]

### 3.3 Research Gaps

[Specific gaps this proposal addresses...]

---

## 4. Proposed Methodology

### 4.1 Research Design

[Overall approach: experimental, survey, qualitative, mixed-methods, etc...]

### 4.2 Participants/Sample

- **Population**: [Target population]
- **Sample Size**: [Proposed N with justification]
- **Sampling Strategy**: [How participants will be recruited]
- **Inclusion/Exclusion Criteria**: [Specific criteria]

### 4.3 Data Collection

[Detailed description of data collection procedures...]

### 4.4 Data Analysis

[Analytical techniques and procedures...]

### 4.5 Ethical Considerations

[IRB approval, informed consent, data protection, etc...]

### 4.6 Feasibility

[Why this research is feasible with available resources...]

---

## 5. Expected Outcomes

### 5.1 Anticipated Findings

[What the research is expected to reveal...]

### 5.2 Theoretical Contributions

[How findings will advance theory...]

### 5.3 Practical Applications

[Real-world applications and implications...]

### 5.4 Dissemination

[Plans for publishing and sharing results...]

---

## 6. Timeline

### Phase 1: Preparation (Months 1-3)
- Literature review completion
- IRB approval
- Instrument development

### Phase 2: Data Collection (Months 4-9)
- Participant recruitment
- Data collection
- Preliminary analysis

### Phase 3: Analysis (Months 10-15)
- Full data analysis
- Results interpretation
- Draft manuscript preparation

### Phase 4: Dissemination (Months 16-18)
- Manuscript submission
- Conference presentations
- Final report

---

## References

[Supporting bibliography...]
```

### Typical Word Count

- **Default**: 5,000 words
- **Range**: 3,000-8,000 words
- **Grant proposals**: May be longer (10,000+ words)

### Best Used For

- Grant applications (NSF, NIH, etc.)
- Dissertation proposals
- Thesis proposals
- Research project planning
- Funding requests
- Institutional review board (IRB) submissions

### Key Features

- **Forward-looking**: Describes research to be conducted
- **Justification focus**: Emphasizes why research is needed
- **Feasibility emphasis**: Demonstrates research is achievable
- **Timeline included**: Provides project schedule
- **Expected outcomes**: Describes anticipated contributions

---

## Abstract Format

### Purpose

The **Abstract** format generates a concise summary suitable for conference submissions, journal abstracts, or brief research summaries. It condenses the essential elements of research into 250-500 words.

### Structure

#### Standard Sections (Structured Abstract)

1. **Background/Context** (50-75 words)
   - Brief problem statement
   - Research context

2. **Methods** (75-100 words)
   - Research design
   - Data sources
   - Analytical approach

3. **Results** (100-150 words)
   - Key findings
   - Main results

4. **Conclusions** (50-75 words)
   - Implications
   - Significance

#### Alternative: Unstructured Abstract

Single paragraph covering all elements without explicit section headings.

### Example Output Structure

**Structured Abstract:**

```markdown
# [Research Title]

## Abstract

**Background**: [Problem context and research gap in 2-3 sentences...]

**Methods**: [Research design, data sources, and analytical approach in 3-4 sentences...]

**Results**: [Key findings with specific results in 4-5 sentences...]

**Conclusions**: [Main implications and significance in 2-3 sentences...]

**Keywords**: keyword1, keyword2, keyword3, keyword4, keyword5
```

**Unstructured Abstract:**

```markdown
# [Research Title]

## Abstract

[Single paragraph of 250-300 words covering background, methods, results, and 
conclusions in a flowing narrative...]

**Keywords**: keyword1, keyword2, keyword3, keyword4, keyword5
```

### Typical Word Count

- **Default**: 300 words
- **Range**: 250-500 words
- **Conference specific**: Follow conference guidelines (often 250 words)

### Best Used For

- Conference abstract submissions
- Journal article abstracts
- Poster presentations
- Brief research summaries
- Database indexing
- Quick overviews for stakeholders

### Key Features

- **Extreme concision**: Every word counts
- **Self-contained**: Understandable without reading full paper
- **Specific results**: Includes actual findings, not just "results will be discussed"
- **Keywords**: 3-5 keywords for indexing
- **No citations**: Typically no references in abstracts

### Discipline Variations

**STEM**: Structured abstract with quantitative results
**Social Sciences**: May be structured or unstructured
**Humanities**: Typically unstructured, narrative style
**Medical**: Highly structured (Background, Methods, Results, Conclusions)

---

## Presentation Format

### Purpose

The **Presentation** format generates content optimized for oral presentations, teaching materials, or seminar talks. It emphasizes clarity, key points, and visual organization suitable for slides or spoken delivery.

### Structure

#### Standard Sections

1. **Overview** (200-300 words)
   - Topic introduction
   - Presentation objectives
   - Key questions addressed

2. **Key Findings** (600-1,000 words)
   - Main results organized by theme
   - Bullet points and clear headings
   - Visual summaries (described)
   - Evidence highlights

3. **Implications** (300-500 words)
   - Theoretical implications
   - Practical applications
   - Policy recommendations
   - Future directions

4. **Conclusions** (200-300 words)
   - Summary of main points
   - Take-home messages
   - Call to action or next steps

### Example Output Structure

```markdown
# [Presentation Title]

## Overview

### Topic
[Brief introduction to the topic...]

### Key Questions
- [Question 1]
- [Question 2]
- [Question 3]

### Objectives
By the end of this presentation, you will understand:
- [Objective 1]
- [Objective 2]
- [Objective 3]

---

## Key Findings

### Finding 1: [Title]

**Main Point**: [One-sentence summary]

**Evidence**:
- [Evidence point 1]
- [Evidence point 2]
- [Evidence point 3]

**Visual**: [Description of chart/graph showing this finding]

### Finding 2: [Title]

**Main Point**: [One-sentence summary]

**Evidence**:
- [Evidence point 1]
- [Evidence point 2]

**Visual**: [Description of supporting visual]

### Finding 3: [Title]

[Similar structure...]

---

## Implications

### For Theory
- [Theoretical implication 1]
- [Theoretical implication 2]

### For Practice
- [Practical application 1]
- [Practical application 2]
- [Practical application 3]

### For Policy
- [Policy recommendation 1]
- [Policy recommendation 2]

---

## Conclusions

### Key Takeaways
1. [Main takeaway 1]
2. [Main takeaway 2]
3. [Main takeaway 3]

### Next Steps
- [Next step 1]
- [Next step 2]

### Questions?
[Contact information or discussion prompts]
```

### Typical Word Count

- **Default**: 1,500 words
- **Range**: 1,000-2,000 words
- **Slide equivalent**: 15-25 slides worth of content

### Best Used For

- Academic conference presentations
- Seminar talks
- Teaching materials
- Webinars
- Workshop content
- Stakeholder briefings

### Key Features

- **Bullet-point format**: Easy to scan and present
- **Clear headings**: Organized for visual slides
- **Concise language**: Suitable for spoken delivery
- **Visual descriptions**: Suggests charts/graphs
- **Actionable takeaways**: Clear conclusions
- **Minimal citations**: Only key references

---

## Format Comparison

### Structural Comparison

| Element | Paper | Review | Proposal | Abstract | Presentation |
|---------|-------|--------|----------|----------|--------------|
| **Abstract** | ✓ | ✓ | ✗ | ✓ (only) | ✗ |
| **Introduction** | ✓ | ✓ | ✗ | ✗ | ✓ (Overview) |
| **Literature Review** | ✓ | ✓ (main) | ✓ | ✗ | ✗ |
| **Methodology** | ✓ | ✗ | ✓ (proposed) | ✓ (brief) | ✗ |
| **Findings/Results** | ✓ | ✗ | ✗ | ✓ | ✓ |
| **Discussion** | ✓ | ✗ | ✗ | ✗ | ✓ (Implications) |
| **Research Gaps** | ✗ | ✓ | ✓ | ✗ | ✗ |
| **Future Directions** | ✓ (brief) | ✓ | ✓ (timeline) | ✗ | ✓ |
| **References** | ✓ | ✓ | ✓ | ✗ | ✓ (minimal) |

### Length Comparison

```
Abstract:       ▓ (250-500 words)
Presentation:   ▓▓▓ (1,000-2,000 words)
Proposal:       ▓▓▓▓▓ (3,000-8,000 words)
Review:         ▓▓▓▓▓▓▓ (5,000-10,000 words)
Paper:          ▓▓▓▓▓▓▓▓ (6,000-12,000 words)
```

### Purpose Comparison

| Format | Primary Purpose | Time Orientation | Audience |
|--------|----------------|------------------|----------|
| **Paper** | Report completed research | Past/Present | Academic peers |
| **Review** | Synthesize existing knowledge | Past | Researchers, students |
| **Proposal** | Plan future research | Future | Funders, committees |
| **Abstract** | Summarize research briefly | Past/Present | Conference attendees |
| **Presentation** | Communicate key findings | Present | General academic audience |

---

## Usage Examples

### Example 1: Journal Article

**Scenario**: Writing a full research paper for journal submission

```bash
python -m gazzali.gazzali --academic \
    --output-format paper \
    --discipline stem \
    --citation-style ieee \
    --word-count 8000 \
    "Machine learning approaches to protein structure prediction"
```

**Output**: 8,000-word research paper with full sections, IEEE citations, STEM terminology

---

### Example 2: Dissertation Literature Review

**Scenario**: Comprehensive literature review for dissertation chapter

```bash
python -m gazzali.gazzali --academic \
    --output-format review \
    --discipline social \
    --citation-style apa \
    --word-count 12000 \
    --export-bib \
    "Social media effects on adolescent mental health"
```

**Output**: 12,000-word literature review with thematic analysis, APA citations, bibliography export

---

### Example 3: Grant Proposal

**Scenario**: Research proposal for NSF grant application

```bash
python -m gazzali.gazzali --academic \
    --output-format proposal \
    --discipline stem \
    --citation-style apa \
    --word-count 6000 \
    --refine \
    "Novel quantum computing algorithms for optimization problems"
```

**Output**: 6,000-word research proposal with refined questions, methodology, timeline

---

### Example 4: Conference Abstract

**Scenario**: Abstract for academic conference submission

```bash
python -m gazzali.gazzali --academic \
    --output-format abstract \
    --discipline humanities \
    --citation-style mla \
    --word-count 300 \
    "Postcolonial perspectives in contemporary African literature"
```

**Output**: 300-word structured abstract suitable for conference submission

---

### Example 5: Seminar Presentation

**Scenario**: Content for academic seminar talk

```bash
python -m gazzali.gazzali --academic \
    --output-format presentation \
    --discipline medical \
    --citation-style apa \
    --word-count 1500 \
    "Recent advances in immunotherapy for cancer treatment"
```

**Output**: 1,500-word presentation content with bullet points, key findings, implications

---

## Customization Options

### Word Count Adjustment

Adjust target word count for any format:

```bash
python -m gazzali.gazzali --academic \
    --output-format paper \
    --word-count 10000 \
    "Your research question"
```

**Recommended Ranges**:
- Abstract: 250-500 words
- Presentation: 1,000-2,500 words
- Proposal: 3,000-10,000 words
- Review: 5,000-15,000 words
- Paper: 6,000-15,000 words

### Section Customization

Control which sections are included:

```bash
# Environment variables
export INCLUDE_ABSTRACT=true
export INCLUDE_METHODOLOGY=true

python -m gazzali.gazzali --academic --output-format paper "Your question"
```

### Discipline-Specific Formatting

Each format adapts to discipline conventions:

```bash
# STEM paper: Emphasizes methodology, data, reproducibility
python -m gazzali.gazzali --academic --output-format paper --discipline stem "Your question"

# Humanities review: Emphasizes interpretation, theory, textual analysis
python -m gazzali.gazzali --academic --output-format review --discipline humanities "Your question"

# Medical proposal: Follows clinical research guidelines
python -m gazzali.gazzali --academic --output-format proposal --discipline medical "Your question"
```

### Citation Style Integration

All formats support multiple citation styles:

```bash
# APA style (default)
--citation-style apa

# MLA style
--citation-style mla

# Chicago style
--citation-style chicago

# IEEE style
--citation-style ieee
```

See [Citation Styles Guide](CITATION_STYLES.md) for detailed formatting examples.

---

## Best Practices

### Choosing the Right Format

**Use Paper format when**:
- Submitting to academic journals
- Writing dissertation/thesis chapters
- Creating comprehensive research reports
- Need full documentation of methods and findings

**Use Review format when**:
- Conducting systematic literature reviews
- Writing state-of-the-art surveys
- Synthesizing existing research
- Identifying research gaps for future work

**Use Proposal format when**:
- Applying for research grants
- Planning dissertation research
- Seeking project approval
- Outlining future research directions

**Use Abstract format when**:
- Submitting to conferences
- Creating brief summaries
- Indexing research in databases
- Providing quick overviews

**Use Presentation format when**:
- Preparing conference talks
- Creating teaching materials
- Briefing stakeholders
- Developing seminar content

### Optimizing Word Count

**For shorter outputs**:
- Use `--word-count` to specify target
- Choose abstract or presentation format
- Focus research question narrowly
- Use `--refine` to scope appropriately

**For longer outputs**:
- Increase word count target
- Use paper or review format
- Broaden research question scope
- Request comprehensive coverage

### Combining with Other Features

**Question refinement**:
```bash
python -m gazzali.gazzali --academic \
    --output-format proposal \
    --refine \
    "Broad research topic"
```

**Bibliography export**:
```bash
python -m gazzali.gazzali --academic \
    --output-format paper \
    --export-bib \
    "Your research question"
```

**Discipline-specific**:
```bash
python -m gazzali.gazzali --academic \
    --output-format review \
    --discipline medical \
    --citation-style apa \
    "Your research question"
```

### Format-Specific Tips

**Paper Format**:
- Ensure methodology section is detailed enough for replication
- Include limitations discussion
- Balance literature review with original contribution
- Use tables/figures for complex data

**Review Format**:
- Organize thematically rather than chronologically
- Explicitly identify research gaps
- Synthesize rather than summarize
- Include sufficient sources (30+ for comprehensive review)

**Proposal Format**:
- Emphasize feasibility and significance
- Include realistic timeline
- Address potential challenges
- Demonstrate knowledge of field

**Abstract Format**:
- Include specific results, not just "results will be discussed"
- Make self-contained (understandable without full paper)
- Follow conference word limits strictly
- Include keywords for indexing

**Presentation Format**:
- Use clear, scannable bullet points
- Emphasize key takeaways
- Minimize technical jargon
- Include visual descriptions

### Quality Assurance

**Before finalizing**:
1. Verify format matches intended use
2. Check word count meets requirements
3. Ensure all required sections present
4. Validate citations are complete
5. Review for discipline-appropriate terminology
6. Confirm structure follows conventions

**After generation**:
1. Review and edit for clarity
2. Add your own analysis and insights
3. Verify citations are accurate
4. Check formatting consistency
5. Proofread for errors
6. Ensure arguments are well-supported

---

## See Also

- [Academic Mode Guide](ACADEMIC_MODE.md) — Complete academic features overview
- [Citation Styles Guide](CITATION_STYLES.md) — Detailed citation formatting
- [Discipline Settings](DISCIPLINE_SETTINGS.md) — Discipline-specific conventions
- [Workflow Configuration](WORKFLOW_CONFIGURATION.md) — Workflow templates
- [CLI Interface](CLI_INTERFACE.md) — Command-line reference

---

## Frequently Asked Questions

### Q: Can I mix elements from different formats?

**A**: While each format has a standard structure, you can customize sections using environment variables. However, it's generally best to choose the format that most closely matches your needs and make minor adjustments rather than mixing formats.

### Q: How do I convert between formats?

**A**: Generate the research in one format, then regenerate with a different format flag. The underlying research remains the same, but the structure and emphasis will change.

### Q: Can I create custom formats?

**A**: Currently, the five standard formats cover most academic needs. For custom requirements, choose the closest format and manually adjust the output, or modify the `academic_config.py` file to add custom formats.

### Q: Which format is best for my dissertation?

**A**: 
- **Literature review chapter**: Use `review` format
- **Methodology chapter**: Use `paper` format with emphasis on methodology
- **Results chapters**: Use `paper` format
- **Proposal**: Use `proposal` format

### Q: How do formats handle citations?

**A**: All formats (except abstract) include full citations and bibliography. The citation style is independent of output format and can be configured separately.

### Q: Can I generate multiple formats from the same research?

**A**: Yes! Run the research once, then regenerate with different format flags to create multiple versions (e.g., full paper + conference abstract).

---

**Last Updated**: January 2024  
**Version**: 1.0.0
