# Workflow Templates Documentation

## Overview

Gazzali Research provides preset workflow templates for common academic research tasks. Each template automatically configures prompts, search strategies, output formats, and quality criteria optimized for specific research types.

## Available Workflows

### 1. Literature Review

**Purpose**: Comprehensive synthesis of existing research on a topic

**Best For**:
- Understanding the current state of research
- Identifying major themes and trends
- Finding research gaps
- Exploring a new research area

**Configuration**:
- Output Format: Literature Review
- Word Count: 5,000-8,000 words
- Minimum Sources: 10 peer-reviewed
- Quality Threshold: 7/10

**Key Features**:
- Thematic organization of literature
- Chronological development tracking
- Identification of consensus and controversy
- Research gap analysis
- Future directions

**Example Questions**:
- "What are the current approaches to explainable AI in healthcare?"
- "How has research on remote work productivity evolved since 2020?"
- "What methodologies are used to study social media's impact on mental health?"

**Usage**:
```bash
python -m gazzali.gazzali --academic --workflow literature_review \
    "What are the current approaches to explainable AI in healthcare?"
```

---

### 2. Systematic Review

**Purpose**: Structured, protocol-driven review following systematic methodology

**Best For**:
- Evidence-based decision making
- Clinical or policy questions
- Rigorous synthesis of intervention studies
- Meta-analysis preparation

**Configuration**:
- Output Format: Literature Review (with methodology)
- Word Count: 7,000-12,000 words
- Minimum Sources: 15 peer-reviewed
- Quality Threshold: 8/10

**Key Features**:
- PRISMA compliance
- Explicit inclusion/exclusion criteria
- Quality assessment of studies
- Systematic data extraction
- Publication bias assessment
- PICO framework

**Example Questions**:
- "What is the effectiveness of cognitive behavioral therapy for treating anxiety disorders?"
- "How do different machine learning algorithms compare for medical image classification?"
- "What interventions are effective for reducing workplace burnout?"

**Usage**:
```bash
python -m gazzali.gazzali --academic --workflow systematic_review \
    "What is the effectiveness of CBT for anxiety disorders?"
```

---

### 3. Methodology Comparison

**Purpose**: Comparative analysis of different research methodologies

**Best For**:
- Methodology selection for new research
- Understanding methodological trade-offs
- Designing mixed-methods studies
- Methodological education

**Configuration**:
- Output Format: Research Paper
- Word Count: 6,000-9,000 words
- Minimum Sources: 12 peer-reviewed
- Quality Threshold: 7/10

**Key Features**:
- Detailed methodology descriptions
- Systematic comparison across dimensions
- Strengths and limitations analysis
- Selection framework
- Case studies and examples
- Resource requirement analysis

**Example Questions**:
- "How do different methodologies compare for studying user experience in mobile apps?"
- "What are the strengths and limitations of various approaches to measuring organizational culture?"
- "How do qualitative and quantitative methods differ in studying climate change adaptation?"

**Usage**:
```bash
python -m gazzali.gazzali --academic --workflow methodology_comparison \
    "How do different methodologies compare for studying UX in mobile apps?"
```

---

### 4. Theoretical Analysis

**Purpose**: Deep analysis of theoretical frameworks and conceptual approaches

**Best For**:
- Understanding theoretical foundations
- Theoretical development
- Conceptual papers
- Philosophical analysis

**Configuration**:
- Output Format: Research Paper
- Word Count: 7,000-10,000 words
- Minimum Sources: 15 peer-reviewed
- Quality Threshold: 8/10

**Key Features**:
- Core concept explication
- Historical development tracking
- Theoretical assumption analysis
- Empirical application discussion
- Theoretical critique and debate
- Framework comparison
- Integration possibilities

**Example Questions**:
- "What are the major theoretical frameworks for understanding human motivation?"
- "How have theories of organizational learning evolved and what are their core differences?"
- "What theoretical approaches exist for explaining technology adoption and diffusion?"

**Usage**:
```bash
python -m gazzali.gazzali --academic --workflow theoretical_analysis \
    "What are the major theoretical frameworks for understanding human motivation?"
```

---

## Using Workflow Templates

### Command-Line Interface

```bash
# Use a workflow template
python -m gazzali.gazzali --academic --workflow <workflow_type> "Your question"

# List available workflows
python -m gazzali.gazzali --list-workflows

# Override workflow settings
python -m gazzali.gazzali --academic --workflow literature_review \
    --word-count 10000 --citation-style apa "Your question"
```

### Python API

```python
from gazzali.workflows import get_workflow_template, WorkflowType

# Get a workflow template
template = get_workflow_template(WorkflowType.LITERATURE_REVIEW)

# Access configuration
config = template.academic_config
print(f"Output format: {config.output_format}")
print(f"Word count: {config.word_count_target}")

# Get prompt additions
research_prompt = template.get_research_prompt_additions()
synthesis_prompt = template.get_synthesis_prompt_additions()

# Validate configuration
issues = template.validate_config()
if issues:
    print("Configuration issues:", issues)
```

### Creating Custom Workflows

```python
from gazzali.workflows import create_custom_workflow, WorkflowType

# Create custom workflow based on template
custom = create_custom_workflow(
    name="Short Literature Review",
    description="Condensed literature review for quick overview",
    base_template=WorkflowType.LITERATURE_REVIEW,
    word_count_target=3000,
    min_peer_reviewed=5,
)

# Create workflow from scratch
custom = create_custom_workflow(
    name="Custom Research",
    description="My custom research workflow",
    output_format="paper",
    word_count_target=5000,
    citation_style="apa",
)
```

## Workflow Components

### Search Strategy

Each workflow defines an optimized search strategy:

- **Literature Review**: Comprehensive search across time periods, emphasis on recent work
- **Systematic Review**: Protocol-driven search with explicit criteria
- **Methodology Comparison**: Focus on methodological papers and diverse approaches
- **Theoretical Analysis**: Prioritize theoretical papers, seminal works, and critiques

### Prompt Additions

Workflows add specific instructions to research and synthesis prompts:

- **Research Phase**: What to extract, how to organize, what to prioritize
- **Synthesis Phase**: How to structure, what to emphasize, writing style

### Required Sections

Each workflow specifies required report sections:

```python
# Literature Review sections
["Abstract", "Introduction", "Thematic Analysis", "Research Gaps", 
 "Future Directions", "Conclusion", "References"]

# Systematic Review sections
["Abstract", "Introduction", "Methodology", "Search Strategy", 
 "Study Selection", "Quality Assessment", "Results", "Discussion", 
 "Limitations", "Conclusion", "References"]
```

### Quality Criteria

Workflows define quality assessment criteria:

- Minimum number of sources
- Source quality requirements
- Coverage expectations
- Methodological rigor
- Analysis depth

## Workflow Selection Guide

### Choose Literature Review When:
- ✅ You need a broad overview of a research area
- ✅ You want to identify themes and trends
- ✅ You're exploring a new topic
- ✅ You need to find research gaps
- ❌ You need rigorous evidence synthesis (use Systematic Review)
- ❌ You're comparing methodologies (use Methodology Comparison)

### Choose Systematic Review When:
- ✅ You need evidence-based conclusions
- ✅ You're answering a specific clinical/policy question
- ✅ You need to assess study quality rigorously
- ✅ You're preparing for meta-analysis
- ❌ You need a broad exploratory review (use Literature Review)
- ❌ Time/resources are limited (Systematic Reviews are intensive)

### Choose Methodology Comparison When:
- ✅ You're designing a new study
- ✅ You need to justify methodology choices
- ✅ You want to understand methodological trade-offs
- ✅ You're teaching research methods
- ❌ You need substantive findings (use Literature Review)
- ❌ You need theoretical analysis (use Theoretical Analysis)

### Choose Theoretical Analysis When:
- ✅ You're developing theoretical understanding
- ✅ You need to compare theoretical frameworks
- ✅ You're writing a conceptual paper
- ✅ You need philosophical depth
- ❌ You need empirical findings (use Literature Review)
- ❌ You need practical methodology guidance (use Methodology Comparison)

## Advanced Features

### Workflow Validation

Templates include validation to ensure appropriate configuration:

```python
template = get_workflow_template(WorkflowType.SYSTEMATIC_REVIEW)
issues = template.validate_config()

# Example issues:
# - "Word count target (2000) is below recommended minimum (7000)"
# - "Minimum peer-reviewed sources should be at least 15"
```

### Workflow Customization

Override specific settings while keeping workflow structure:

```bash
# Use systematic review workflow but adjust word count
python -m gazzali.gazzali --academic --workflow systematic_review \
    --word-count 15000 --min-sources 20 "Your question"
```

### Combining with Other Features

Workflows work with all Gazzali features:

```bash
# Workflow + Question refinement
python -m gazzali.gazzali --academic --workflow literature_review \
    --refine "Broad topic"

# Workflow + Specific discipline
python -m gazzali.gazzali --academic --workflow theoretical_analysis \
    --discipline social "Your question"

# Workflow + Bibliography export
python -m gazzali.gazzali --academic --workflow systematic_review \
    --export-bib "Your question"
```

## Best Practices

### 1. Match Workflow to Research Goal
- Use the workflow selection guide above
- Consider your audience and purpose
- Think about time and resource constraints

### 2. Adjust Word Count Appropriately
- Stay within recommended ranges
- Consider journal/conference requirements
- Balance depth with readability

### 3. Set Appropriate Quality Thresholds
- Higher thresholds for systematic reviews
- Moderate thresholds for exploratory reviews
- Consider field-specific norms

### 4. Refine Questions for Workflows
- Systematic reviews need specific PICO questions
- Literature reviews can handle broader topics
- Methodology comparisons need clear scope
- Theoretical analyses need focused frameworks

### 5. Review and Iterate
- Check generated reports against quality criteria
- Adjust configuration based on results
- Refine search strategy if needed

## Troubleshooting

### "Not enough peer-reviewed sources found"
- **Solution**: Lower `min_peer_reviewed` or broaden search terms
- **Prevention**: Use Scholar-priority mode, check topic specificity

### "Word count significantly below/above target"
- **Solution**: Adjust `word_count_target` or topic scope
- **Prevention**: Match question breadth to word count

### "Missing required sections"
- **Solution**: Check synthesis prompt, may need manual editing
- **Prevention**: Ensure question matches workflow type

### "Quality criteria not met"
- **Solution**: Review quality criteria, adjust configuration
- **Prevention**: Validate configuration before starting

## Examples

### Example 1: Literature Review in STEM

```bash
python -m gazzali.gazzali --academic \
    --workflow literature_review \
    --discipline stem \
    --citation-style ieee \
    "What are the current approaches to quantum error correction?"
```

### Example 2: Systematic Review in Medical

```bash
python -m gazzali.gazzali --academic \
    --workflow systematic_review \
    --discipline medical \
    --citation-style apa \
    --word-count 10000 \
    "What is the effectiveness of mindfulness interventions for chronic pain?"
```

### Example 3: Methodology Comparison in Social Sciences

```bash
python -m gazzali.gazzali --academic \
    --workflow methodology_comparison \
    --discipline social \
    --citation-style apa \
    "How do survey and interview methods compare for studying workplace satisfaction?"
```

### Example 4: Theoretical Analysis in Humanities

```bash
python -m gazzali.gazzali --academic \
    --workflow theoretical_analysis \
    --discipline humanities \
    --citation-style mla \
    "What are the major theoretical frameworks for understanding narrative identity?"
```

## API Reference

### WorkflowTemplate Class

```python
@dataclass
class WorkflowTemplate:
    name: str
    workflow_type: WorkflowType
    description: str
    academic_config: AcademicConfig
    search_strategy: str
    prompt_additions: Dict[str, str]
    required_sections: List[str]
    recommended_word_count: tuple[int, int]
    quality_criteria: List[str]
    example_questions: List[str]
    
    def get_research_prompt_additions() -> str
    def get_synthesis_prompt_additions() -> str
    def get_search_strategy_prompt() -> str
    def validate_config() -> List[str]
    def to_dict() -> Dict[str, Any]
```

### Functions

```python
# Get workflow by type
get_workflow_template(workflow_type: WorkflowType) -> WorkflowTemplate

# List all workflows
list_available_workflows() -> List[Dict[str, str]]

# Get workflow by name
get_workflow_by_name(name: str) -> Optional[WorkflowTemplate]

# Create custom workflow
create_custom_workflow(
    name: str,
    description: str,
    base_template: Optional[WorkflowType] = None,
    **config_overrides
) -> WorkflowTemplate
```

## See Also

- [Academic Configuration](ACADEMIC_CONFIG.md) - Configuration options
- [Citation Styles](CITATION_STYLES.md) - Citation formatting
- [Output Formats](OUTPUT_FORMATS.md) - Report formats
- [Discipline Settings](DISCIPLINE_SETTINGS.md) - Discipline-specific features
