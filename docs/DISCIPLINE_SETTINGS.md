# Discipline Settings Documentation

## Overview

Gazzali Research supports discipline-specific configurations that adapt the research process, terminology, methodology focus, source priorities, and writing conventions to match the standards and expectations of different academic fields. This document describes the settings and conventions for each supported discipline.

## Supported Disciplines

Gazzali Research currently supports five discipline categories:

1. **General** - Interdisciplinary or non-specialized research
2. **STEM** - Science, Technology, Engineering, and Mathematics
3. **Social Sciences** - Psychology, Sociology, Economics, Political Science, etc.
4. **Humanities** - Literature, Philosophy, History, Cultural Studies, etc.
5. **Medical/Health Sciences** - Clinical research, public health, biomedical sciences

## Configuring Discipline Settings

### Command-Line Configuration

Use the `--discipline` flag when running Gazzali Research:

```bash
# STEM research
python -m gazzali.gazzali "quantum computing algorithms" --academic --discipline stem

# Social sciences research
python -m gazzali.gazzali "social media impact on mental health" --academic --discipline social

# Humanities research
python -m gazzali.gazzali "postcolonial literature analysis" --academic --discipline humanities

# Medical research
python -m gazzali.gazzali "diabetes treatment efficacy" --academic --discipline medical
```

### Environment Variable Configuration

Set the `DISCIPLINE` environment variable in your `.env` file:

```bash
DISCIPLINE=stem
```

### Programmatic Configuration

```python
from gazzali.academic_config import AcademicConfig, Discipline

config = AcademicConfig(
    discipline=Discipline.STEM,
    citation_style="apa",
    output_format="paper"
)
```

## Discipline-Specific Settings

### 1. General Discipline

**Use Case**: Interdisciplinary research, exploratory topics, or when no specific discipline applies.

#### Terminology
- Clear, accessible academic language appropriate for interdisciplinary audiences
- Specialized terms from any discipline defined on first use
- Balance between technical precision and readability
- Avoids overly specialized jargon without explanation

#### Methodology Focus
- Adapts to research methods appropriate for the topic
- Includes both qualitative and quantitative approaches as relevant
- Emphasizes rigor and appropriateness of methods for research questions
- Flexible methodology discussion based on research domain

#### Source Priorities
- Peer-reviewed academic sources across all disciplines
- High-quality research regardless of specific field
- Interdisciplinary perspectives when relevant
- Balanced representation of different scholarly traditions

#### Analysis Approach
- Adapts analytical approach to research topic and available evidence
- Considers multiple disciplinary perspectives
- Emphasizes critical thinking and evidence-based reasoning
- Integrates insights from various fields when appropriate

#### Writing Conventions
- General academic writing standards
- Formal, objective tone
- Clear argument structure with appropriate evidence
- Accessible to readers from various academic backgrounds
- Third-person perspective
- Proper citation and attribution

**Best For**: 
- Exploratory research across multiple fields
- Topics that don't fit neatly into one discipline
- Undergraduate-level research
- General audience academic writing

---

### 2. STEM Discipline

**Use Case**: Science, Technology, Engineering, Mathematics, Computer Science, Physics, Chemistry, Biology, etc.

#### Terminology
- Technical and scientific terminology appropriate for STEM fields
- Mathematical notation, chemical formulas, equations, and technical specifications
- SI units and standard scientific nomenclature
- Specialized terms defined on first use
- Precise technical language for measurements and procedures

**Examples**:
- "The algorithm achieves O(n log n) time complexity"
- "The solution was titrated to pH 7.4 ± 0.1"
- "The neural network architecture consists of 12 transformer layers"

#### Methodology Focus
- **Experimental design**: Control groups, randomization, blinding
- **Quantitative methods**: Statistical analysis, measurement precision
- **Reproducibility**: Detailed procedures for replication
- **Empirical validation**: Hypothesis testing, falsifiability
- **Data-driven approaches**: Large datasets, computational analysis
- **Statistical significance**: p-values, confidence intervals, effect sizes
- **Error analysis**: Measurement uncertainty, systematic errors
- **Equipment and materials**: Specific instruments, software versions

**Key Methodological Considerations**:
- Sample size calculations and statistical power
- Experimental controls and variables
- Data collection protocols
- Measurement instruments and calibration
- Computational methods and algorithms
- Validation and verification procedures

#### Source Priorities
1. **Top-tier journals**: Nature, Science, Cell, PNAS
2. **Field-specific journals**: IEEE Transactions, ACM journals, Physical Review
3. **Preprint servers**: arXiv, bioRxiv (for cutting-edge research)
4. **Conference proceedings**: Major conferences (NeurIPS, ICML, CVPR, etc.)
5. **Technical reports**: Research institutions, standards organizations
6. **Systematic reviews and meta-analyses**: Cochrane-style reviews

**Quality Indicators**:
- High citation counts
- Impact factor of journals
- Replication studies
- Open data and code availability

#### Analysis Approach
- Quantitative analysis with statistical rigor
- Effect sizes, confidence intervals, statistical power
- Reproducibility and replication assessment
- Computational complexity and scalability analysis
- Performance metrics and benchmarking
- Data quality and measurement validity
- Experimental controls and confounding variables
- Sensitivity analysis and robustness checks

#### Writing Conventions
- **Passive voice for methods**: "The solution was heated to 100°C"
- **Active voice for results**: "The algorithm outperformed baseline methods"
- Precise numerical data with appropriate significant figures
- Figures, tables, and equations for complex information
- Detailed methodology sufficient for replication
- Results presented objectively without interpretation in results section
- Discussion separates findings from interpretation
- Limitations clearly stated

**Report Structure**:
- Abstract (structured: Background, Methods, Results, Conclusions)
- Introduction (with clear hypothesis or research questions)
- Materials and Methods (highly detailed)
- Results (objective presentation with figures/tables)
- Discussion (interpretation, comparison with literature)
- Conclusion
- References

**Best For**:
- Experimental research
- Computational studies
- Engineering design and optimization
- Mathematical proofs and theorems
- Scientific investigations

---

### 3. Social Sciences Discipline

**Use Case**: Psychology, Sociology, Economics, Anthropology, Political Science, Education, Communication Studies, etc.

#### Terminology
- Social science theoretical frameworks and constructs
- Discipline-specific concepts (e.g., social capital, cognitive dissonance, market equilibrium)
- Operational definitions of key constructs
- Statistical and methodological terminology (validity, reliability, generalizability)
- Population and demographic terminology

**Examples**:
- "Social capital, defined as networks of relationships among people"
- "The construct validity of the measure was established through..."
- "Participants exhibited confirmation bias when..."

#### Methodology Focus
- **Qualitative methods**: Interviews, focus groups, ethnography, participant observation, grounded theory
- **Quantitative methods**: Surveys, experiments, statistical modeling, regression analysis
- **Mixed methods**: Integration of qualitative and quantitative approaches
- **Validity types**: Internal, external, construct, and statistical conclusion validity
- **Reliability**: Inter-rater reliability, test-retest reliability, internal consistency
- **Sampling**: Probability sampling, stratified sampling, representativeness
- **Ethics**: Informed consent, confidentiality, IRB approval, vulnerable populations

**Key Methodological Considerations**:
- Sample characteristics and demographics
- Response rates and non-response bias
- Measurement instruments and psychometric properties
- Data collection procedures
- Coding schemes for qualitative data
- Statistical assumptions and diagnostics
- Generalizability and external validity

#### Source Priorities
1. **Top-tier journals**: American Sociological Review, Psychological Science, American Economic Review, American Political Science Review
2. **Field-specific journals**: Journal of Personality and Social Psychology, Social Forces, Econometrica
3. **Longitudinal studies**: Panel studies, cohort studies
4. **Randomized controlled trials**: Experimental interventions
5. **Large-scale surveys**: National surveys, census data
6. **Working papers**: NBER, research institutions
7. **Government statistics**: Census Bureau, Bureau of Labor Statistics

**Quality Indicators**:
- Sample size and representativeness
- Methodological rigor
- Longitudinal vs. cross-sectional design
- Replication studies

#### Analysis Approach
- Both quantitative and qualitative analysis as appropriate
- Theoretical frameworks and empirical support
- Cultural context and social dynamics
- Generalizability across populations and settings
- Confounds, mediators, and moderators
- Practical significance alongside statistical significance
- Alternative explanations and rival hypotheses
- Contextual factors and boundary conditions

#### Writing Conventions
- Balance theoretical discussion with empirical evidence
- Integrate participant quotes in qualitative research (with context)
- Present demographic characteristics of samples in tables
- Discuss implications for policy, practice, and social understanding
- Address limitations (sampling, measurement, generalizability)
- Consider ethical implications and social justice perspectives
- Use APA style typically (though varies by subfield)
- Acknowledge researcher positionality in qualitative work

**Report Structure**:
- Abstract
- Introduction (with theoretical framework)
- Literature Review (organized thematically or chronologically)
- Methods (participants, measures, procedures, analysis)
- Results (organized by research question or theme)
- Discussion (interpretation, implications, limitations)
- Conclusion
- References

**Best For**:
- Human behavior research
- Social phenomena investigation
- Policy analysis
- Educational research
- Market research and consumer behavior

---

### 4. Humanities Discipline

**Use Case**: Literature, Philosophy, History, Art History, Religious Studies, Cultural Studies, Linguistics, etc.

#### Terminology
- Critical theory and philosophical concepts
- Hermeneutics and textual analysis terminology
- Discourse analysis and rhetorical concepts
- Literary theory (structuralism, post-structuralism, feminism, etc.)
- Historical periodization and historiography
- Aesthetic and interpretive terminology

**Examples**:
- "The text exhibits characteristics of magical realism"
- "Through a Foucauldian lens, the discourse reveals..."
- "The hermeneutic circle illuminates the relationship between..."

#### Methodology Focus
- **Textual analysis**: Close reading, literary criticism, rhetorical analysis
- **Historical methods**: Archival research, historiography, periodization
- **Critical interpretation**: Multiple theoretical frameworks
- **Comparative analysis**: Cross-cultural, cross-temporal comparisons
- **Philosophical inquiry**: Conceptual analysis, logical argumentation
- **Contextual understanding**: Historical, cultural, and social context
- **Primary sources**: Original texts, manuscripts, artifacts

**Key Methodological Considerations**:
- Selection and justification of texts/artifacts
- Theoretical framework and interpretive lens
- Historical and cultural contextualization
- Engagement with scholarly debates
- Multiple interpretive possibilities
- Textual evidence and close reading
- Archival research methods

#### Source Priorities
1. **Primary sources**: Original texts, historical documents, literary works, cultural artifacts
2. **Scholarly monographs**: University press publications
3. **Peer-reviewed journals**: PMLA, Critical Inquiry, American Historical Review
4. **Edited collections**: Essay collections on specific topics
5. **Canonical works**: Foundational texts in the field
6. **Contemporary scholarship**: Recent theoretical developments
7. **Archival materials**: Manuscripts, letters, unpublished documents

**Quality Indicators**:
- Scholarly reputation and peer review
- Engagement with primary sources
- Theoretical sophistication
- Contribution to scholarly conversation

#### Analysis Approach
- Interpretive analysis and critical reading
- Multiple interpretive frameworks and perspectives
- Historical context and cultural significance
- Philosophical implications and ethical dimensions
- Logical coherence and textual support
- Engagement with theoretical debates
- Aesthetic, ethical, and political dimensions
- Intertextual connections and influences

#### Writing Conventions
- Sustained arguments with careful textual evidence
- Smooth integration of quotations with analysis
- Engagement with scholarly conversations and debates
- Sophisticated vocabulary and complex sentence structures (when appropriate)
- Balance close reading with broader theoretical claims
- Multiple interpretive possibilities acknowledged
- Footnotes or endnotes for additional context (Chicago style common)
- First-person acceptable in some contexts (reflective essays)

**Report Structure**:
- Introduction (with thesis statement and theoretical framework)
- Body sections (organized thematically or chronologically)
  - Close readings of primary texts
  - Engagement with secondary scholarship
  - Theoretical analysis
- Conclusion (synthesis and broader implications)
- Bibliography or Works Cited

**Best For**:
- Literary analysis
- Philosophical inquiry
- Historical research
- Cultural criticism
- Textual interpretation

---

### 5. Medical/Health Sciences Discipline

**Use Case**: Clinical medicine, public health, nursing, pharmacy, biomedical research, epidemiology, health policy, etc.

#### Terminology
- Medical and clinical terminology (anatomical, diagnostic, therapeutic)
- Pharmacological nomenclature (generic and brand names)
- Evidence-based medicine concepts
- Clinical classifications (ICD codes, DSM criteria)
- Epidemiological terminology (incidence, prevalence, risk ratios)
- Standard medical abbreviations (defined on first use)

**Examples**:
- "Patients with type 2 diabetes mellitus (T2DM) and HbA1c >7.0%"
- "The intervention group received metformin 500mg BID"
- "The number needed to treat (NNT) was 12 (95% CI: 8-20)"

#### Methodology Focus
- **Evidence hierarchy**: Systematic reviews > RCTs > cohort studies > case-control > case series
- **Clinical trials**: Randomized controlled trials, blinding, allocation concealment
- **Systematic reviews**: PRISMA guidelines, meta-analysis
- **Observational studies**: Cohort, case-control, cross-sectional designs
- **Outcome measures**: Mortality, morbidity, quality of life, patient-reported outcomes
- **Safety and efficacy**: Adverse events, contraindications, drug interactions
- **Ethics**: Informed consent, IRB approval, patient safety, equipoise

**Key Methodological Considerations**:
- Inclusion/exclusion criteria for participants
- Intervention protocols and dosing
- Outcome measures (primary and secondary)
- Follow-up duration and loss to follow-up
- Intention-to-treat vs. per-protocol analysis
- Adverse event monitoring and reporting
- Statistical analysis plan (pre-specified)
- Clinical trial registration

#### Source Priorities
1. **High-impact medical journals**: New England Journal of Medicine (NEJM), The Lancet, JAMA, BMJ
2. **Specialty journals**: JACC, Annals of Internal Medicine, Circulation
3. **Systematic reviews**: Cochrane Library, systematic reviews with meta-analysis
4. **Clinical guidelines**: Professional organizations (AHA, ADA, WHO, etc.)
5. **Regulatory documents**: FDA/EMA approvals, drug safety communications
6. **Clinical trial registries**: ClinicalTrials.gov for ongoing research
7. **Public health data**: CDC, WHO, national health statistics

**Quality Indicators**:
- Level of evidence (systematic reviews and RCTs highest)
- Sample size and statistical power
- Methodological quality (Cochrane risk of bias tool)
- Clinical relevance and applicability
- Conflict of interest disclosures

#### Analysis Approach
- Clinical significance alongside statistical significance
- Evidence quality assessment (GRADE framework)
- Patient-centered outcomes (mortality, morbidity, quality of life)
- Adverse effects and safety profiles
- Cost-effectiveness and healthcare resource implications
- Applicability to different patient populations
- Comorbidities and individual patient factors
- Number needed to treat (NNT) and number needed to harm (NNH)
- Absolute vs. relative risk reduction

#### Writing Conventions
- Follow reporting guidelines: CONSORT (RCTs), PRISMA (systematic reviews), STROBE (observational studies)
- Present patient characteristics and baseline data in tables
- Report outcomes with confidence intervals and p-values
- Discuss clinical implications and practice recommendations
- Address limitations (sample size, follow-up, generalizability)
- Consider patient safety and informed decision-making
- Use tables for clinical data and treatment comparisons
- Include conflict of interest statements
- Structured abstracts (Background, Methods, Results, Conclusions)

**Report Structure**:
- Structured Abstract
- Introduction (clinical background and rationale)
- Methods
  - Study design
  - Participants (inclusion/exclusion criteria)
  - Interventions
  - Outcomes
  - Statistical analysis
- Results
  - Participant flow (CONSORT diagram)
  - Baseline characteristics
  - Primary outcomes
  - Secondary outcomes
  - Adverse events
- Discussion
  - Interpretation in clinical context
  - Comparison with existing evidence
  - Clinical implications
  - Limitations
- Conclusion
- References

**Best For**:
- Clinical research
- Public health studies
- Treatment efficacy research
- Epidemiological investigations
- Health policy analysis

---

## Discipline-Specific Prompt Modifiers

When you select a discipline, Gazzali Research automatically applies prompt modifiers that guide the AI research agent and synthesis model. These modifiers affect:

1. **Terminology**: Vocabulary and technical language used
2. **Methodology Focus**: Types of research methods prioritized
3. **Source Priorities**: Which types of sources are valued most
4. **Analysis Approach**: How evidence is evaluated and synthesized
5. **Writing Conventions**: Style, structure, and formatting expectations

### Accessing Prompt Modifiers Programmatically

```python
from gazzali.academic_config import AcademicConfig, Discipline

config = AcademicConfig(discipline=Discipline.STEM)
modifiers = config.get_prompt_modifiers()

print(modifiers["terminology"])
print(modifiers["methodology_focus"])
print(modifiers["source_priorities"])
print(modifiers["analysis_approach"])
print(modifiers["writing_conventions"])
```

### Getting Formatted Discipline Prompt Text

```python
config = AcademicConfig(discipline=Discipline.MEDICAL)
discipline_prompt = config.get_discipline_prompt_text()
# Returns formatted text ready for inclusion in research prompts
```

## Combining Discipline with Other Settings

Discipline settings work in combination with other academic configuration options:

### Discipline + Citation Style

```bash
# STEM research with IEEE citations (common in engineering)
python -m gazzali.gazzali "machine learning optimization" --academic --discipline stem --citation-style ieee

# Humanities research with MLA citations (common in literature)
python -m gazzali.gazzali "Shakespeare's sonnets" --academic --discipline humanities --citation-style mla

# Medical research with AMA citations
python -m gazzali.gazzali "hypertension treatment" --academic --discipline medical --citation-style apa
```

### Discipline + Output Format

```bash
# STEM literature review
python -m gazzali.gazzali "quantum computing" --academic --discipline stem --output-format review

# Social sciences research proposal
python -m gazzali.gazzali "social media effects" --academic --discipline social --output-format proposal

# Medical systematic review
python -m gazzali.gazzali "diabetes interventions" --academic --discipline medical --output-format review
```

## Customizing Discipline Settings

While Gazzali Research provides five predefined disciplines, you can customize the behavior by:

1. **Modifying the academic_config.py file**: Add custom discipline-specific modifiers
2. **Using environment variables**: Override specific settings
3. **Creating custom prompts**: Develop discipline-specific prompt templates

### Example: Adding a Custom Discipline

To add a new discipline (e.g., "Law"), you would:

1. Add to the `Discipline` enum in `academic_config.py`
2. Add discipline-specific modifiers in `get_prompt_modifiers()`
3. Update documentation

## Best Practices

### Choosing the Right Discipline

- **Use STEM for**: Hard sciences, engineering, computer science, mathematics
- **Use Social Sciences for**: Psychology, sociology, economics, education, political science
- **Use Humanities for**: Literature, philosophy, history, art, cultural studies
- **Use Medical for**: Clinical research, public health, biomedical sciences
- **Use General for**: Interdisciplinary topics, exploratory research, or when unsure

### Discipline-Specific Tips

#### STEM Research
- Emphasize reproducibility and provide detailed methods
- Include statistical analysis and effect sizes
- Use figures and tables extensively
- Cite preprints for cutting-edge topics
- Focus on quantitative evidence

#### Social Sciences Research
- Balance theory with empirical evidence
- Discuss generalizability and limitations
- Consider cultural and contextual factors
- Address ethical considerations
- Include both qualitative and quantitative evidence

#### Humanities Research
- Engage deeply with primary sources
- Develop sustained interpretive arguments
- Consider multiple theoretical perspectives
- Integrate scholarly conversations
- Balance close reading with broader claims

#### Medical Research
- Follow reporting guidelines (CONSORT, PRISMA, etc.)
- Emphasize clinical significance
- Discuss patient safety and ethics
- Consider applicability to practice
- Report adverse events and limitations

## Troubleshooting

### Issue: Results don't match discipline expectations

**Solution**: 
- Verify discipline is set correctly with `--discipline` flag
- Check that academic mode is enabled with `--academic` flag
- Review the generated prompt modifiers to ensure they're applied

### Issue: Terminology too technical or not technical enough

**Solution**:
- Adjust the discipline setting to better match your needs
- Use "general" for more accessible language
- Use specific disciplines for technical depth

### Issue: Wrong types of sources being prioritized

**Solution**:
- Ensure Scholar priority is enabled for academic sources
- Check that the discipline matches your field
- Adjust source quality threshold if needed

## Related Documentation

- [Academic Mode Guide](ACADEMIC_MODE.md) - Overview of academic features
- [Citation Styles](CITATION_STYLES.md) - Citation formatting details
- [Output Formats](OUTPUT_FORMATS.md) - Report structure options
- [Configuration Guide](ENVIRONMENT_SETUP.md) - Environment setup

## Examples

### Example 1: STEM Research

```bash
python -m gazzali.gazzali \
  "deep learning for protein folding prediction" \
  --academic \
  --discipline stem \
  --citation-style ieee \
  --output-format paper \
  --word-count 8000
```

**Expected Output**:
- Technical terminology (neural networks, amino acid sequences)
- Focus on computational methods and algorithms
- IEEE-style citations [1], [2], [3]
- Emphasis on reproducibility and performance metrics
- Detailed methodology section

### Example 2: Social Sciences Research

```bash
python -m gazzali.gazzali \
  "impact of remote work on employee well-being" \
  --academic \
  --discipline social \
  --citation-style apa \
  --output-format paper \
  --word-count 6000
```

**Expected Output**:
- Social science terminology (well-being, work-life balance)
- Mixed methods discussion
- APA-style citations (Author, Year)
- Consideration of cultural and contextual factors
- Discussion of practical and policy implications

### Example 3: Humanities Research

```bash
python -m gazzali.gazzali \
  "postmodern elements in contemporary fiction" \
  --academic \
  --discipline humanities \
  --citation-style mla \
  --output-format paper \
  --word-count 5000
```

**Expected Output**:
- Literary and critical theory terminology
- Close reading and textual analysis
- MLA-style citations (Author Page)
- Engagement with primary texts and secondary scholarship
- Interpretive depth and theoretical sophistication

### Example 4: Medical Research

```bash
python -m gazzali.gazzali \
  "effectiveness of SGLT2 inhibitors in heart failure" \
  --academic \
  --discipline medical \
  --citation-style apa \
  --output-format review \
  --word-count 7000
```

**Expected Output**:
- Medical terminology (SGLT2 inhibitors, ejection fraction)
- Focus on RCTs and systematic reviews
- Clinical outcomes and safety data
- PRISMA-style systematic review structure
- Discussion of clinical implications and guidelines

## Conclusion

Discipline settings in Gazzali Research ensure that your research output matches the conventions, expectations, and standards of your academic field. By selecting the appropriate discipline, you enable the AI to:

- Use field-appropriate terminology
- Prioritize relevant methodologies
- Focus on discipline-specific sources
- Apply appropriate analytical frameworks
- Follow field-specific writing conventions

Choose your discipline carefully to get the most relevant and high-quality academic research output.
