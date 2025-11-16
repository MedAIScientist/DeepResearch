# Research Impact Analysis

## Overview

The Research Impact Analysis module provides comprehensive tools for analyzing the impact and influence of academic research. It tracks citation counts, identifies highly cited papers, extracts research implications, and generates detailed implications sections for academic reports.

## Features

### 1. Citation Count Tracking and Analysis

The impact analyzer automatically tracks citation counts from Google Scholar results and calculates comprehensive statistics:

- **Total citations**: Sum of all citations across papers
- **Mean citations**: Average citations per paper
- **Median citations**: Median citation count
- **Citation range**: Minimum and maximum citation counts
- **Highly cited count**: Number of papers with >100 citations

### 2. Highly Cited Paper Identification

Papers are automatically classified into impact levels based on citation counts and age:

- **Highly Cited**: Top 10% by citations or >100 citations
- **Well Cited**: Top 25% by citations or >50 citations
- **Moderately Cited**: Top 50% by citations or >20 citations
- **Emerging**: Recent papers (<3 years) with >10 citations
- **Foundational**: Older papers (>10 years) with sustained citations

### 3. Research Implications Extraction

The analyzer automatically extracts three types of implications from research content:

#### Theoretical Implications
- Theory development and conceptual advances
- Extensions of existing frameworks
- Challenges to current paradigms
- Contributions to theoretical knowledge

#### Practical Implications
- Applications for practitioners
- Implementation strategies
- Tools and techniques
- Real-world interventions

#### Policy Implications
- Policy recommendations
- Regulatory guidance
- Government and institutional applications
- Standards and guidelines

### 4. Future Research Directions

The analyzer identifies promising future research directions by analyzing:

- Explicit mentions of "future research"
- Research gaps and limitations
- Unanswered questions
- Suggested next steps

Each direction includes:
- Description of the research direction
- Rationale for its importance
- Suggested methodological approaches
- Priority level (high, medium, low)

### 5. Knowledge Contributions and Theoretical Challenges

The analyzer extracts:

- **Knowledge Contributions**: How research advances existing knowledge
- **Theoretical Challenges**: How research questions or contradicts existing theories

## Usage

### Basic Usage

```python
from gazzali.citation_manager import CitationManager
from gazzali.impact_analyzer import ImpactAnalyzer

# Initialize citation manager and add citations
citation_mgr = CitationManager()
# ... add citations from research ...

# Create impact analyzer
analyzer = ImpactAnalyzer(citation_mgr)

# Perform complete impact analysis
analysis = analyzer.analyze_impact(research_content="[research findings text]")

# Access results
print(f"Highly cited papers: {len(analysis.highly_cited_papers)}")
print(f"Theoretical implications: {len(analysis.theoretical_implications)}")
print(f"Future directions: {len(analysis.future_directions)}")
```

### Generating Implications Section

```python
# Generate formatted implications section for report
implications_text = analyzer.generate_implications_section(
    analysis=analysis,
    include_future_directions=True
)

# Add to academic report
print(implications_text)
```

### Generating Highly Cited Papers Summary

```python
# Generate summary of highly cited papers
summary = analyzer.generate_highly_cited_summary(
    analysis=analysis,
    max_papers=10
)

print(summary)
```

### Convenience Function

```python
from gazzali.impact_analyzer import analyze_research_impact

# One-line impact analysis
analysis = analyze_research_impact(
    citation_manager=citation_mgr,
    research_content=research_text
)

print(analysis.get_summary())
```

## Data Models

### ImpactAnalysis

Complete impact analysis results:

```python
@dataclass
class ImpactAnalysis:
    highly_cited_papers: List[Tuple[Citation, ImpactLevel]]
    citation_statistics: Dict[str, Any]
    theoretical_implications: List[ResearchImplication]
    practical_implications: List[ResearchImplication]
    policy_implications: List[ResearchImplication]
    future_directions: List[FutureDirection]
    knowledge_contributions: List[str]
    challenges_to_theory: List[str]
```

### ResearchImplication

Individual research implication:

```python
@dataclass
class ResearchImplication:
    implication_type: ImplicationType  # theoretical, practical, policy
    description: str
    stakeholders: List[str]
    evidence: List[str]
    confidence: str  # high, medium, low
```

### FutureDirection

Future research direction:

```python
@dataclass
class FutureDirection:
    direction: str
    rationale: str
    methodology_suggestions: List[str]
    priority: str  # high, medium, low
    related_gaps: List[str]
```

## Integration with Academic Reports

The impact analyzer integrates seamlessly with the academic report generator:

```python
from gazzali.academic_config import AcademicConfig
from gazzali.citation_manager import CitationManager
from gazzali.impact_analyzer import ImpactAnalyzer
from gazzali.report_generator import AcademicReportGenerator

# Setup
config = AcademicConfig(output_format="paper")
citation_mgr = CitationManager()
impact_analyzer = ImpactAnalyzer(citation_mgr)

# Perform research and collect citations
# ... research process ...

# Analyze impact
analysis = impact_analyzer.analyze_impact(research_results)

# Generate report with implications section
report_generator = AcademicReportGenerator(config, citation_mgr)
report = report_generator.generate_report(
    question=research_question,
    research_results=research_results,
    api_key=api_key
)

# Add impact analysis sections
implications_section = impact_analyzer.generate_implications_section(analysis)
highly_cited_summary = impact_analyzer.generate_highly_cited_summary(analysis)

# Include in report
report.sections['Implications'] = implications_section
report.sections['Influential Papers'] = highly_cited_summary
```

## Citation Statistics

The analyzer provides detailed citation statistics:

```python
stats = analysis.citation_statistics

print(f"Total papers: {stats['total_papers']}")
print(f"Papers with citations: {stats['papers_with_citations']}")
print(f"Total citations: {stats['total_citations']}")
print(f"Mean citations: {stats['mean_citations']}")
print(f"Median citations: {stats['median_citations']}")
print(f"Highly cited papers: {stats['highly_cited_count']}")
print(f"Citation range: {stats['citation_range']}")
```

## Impact Levels

Papers are classified into five impact levels:

### Highly Cited
- Top 10% by citation count
- OR >100 citations
- Represents seminal and highly influential work

### Well Cited
- Top 25% by citation count
- OR >50 citations
- Represents important contributions to the field

### Moderately Cited
- Top 50% by citation count
- OR >20 citations
- Represents solid contributions with moderate impact

### Emerging
- Recent papers (<3 years old)
- >10 citations
- Represents new work gaining traction

### Foundational
- Older papers (>10 years old)
- >30 citations
- Represents classic work with sustained influence

## Implication Types

### Theoretical Implications

Identified by keywords:
- theory, theoretical, conceptual, framework, model
- understanding, knowledge, contributes to, advances
- challenges, supports, extends, refines

Stakeholders:
- Researchers
- Theorists
- Academics

### Practical Implications

Identified by keywords:
- practical, application, practice, practitioners
- implementation, intervention, tool, technique
- can be used, useful for, helps, enables

Stakeholders:
- Practitioners
- Professionals
- Organizations

### Policy Implications

Identified by keywords:
- policy, policymakers, regulation, regulatory
- government, legislation, guidelines, standards
- should, recommend, suggest, advocate

Stakeholders:
- Policymakers
- Regulators
- Government agencies

## Future Direction Identification

Future directions are identified by analyzing:

### Explicit Future Research Mentions
- "future research", "future studies", "future work"
- "further research", "further investigation"
- "should investigate", "should explore"

### Research Gaps
- "gap", "limitation", "limited"
- "lack of", "absence of", "insufficient"
- "not yet", "remains unclear", "unknown"

### Priority Assignment
- **High priority**: Contains "critical", "essential", "crucial", "important"
- **Medium priority**: Default
- **Low priority**: Contains "may", "could", "might", "potentially"

## Best Practices

### 1. Ensure Citation Data Quality

Make sure citations include citation counts:

```python
citation = Citation(
    citation_id="smith_2020_abc123",
    authors=["Smith, J.", "Jones, M."],
    year=2020,
    title="Important Research",
    venue="Journal of Science",
    citation_count=150,  # Important for impact analysis
    # ... other fields ...
)
```

### 2. Provide Rich Research Content

For best implication extraction, provide comprehensive research content:

```python
# Good: Detailed research findings
research_content = """
The findings suggest several theoretical implications for understanding...
This research contributes to existing knowledge by demonstrating...
Practical applications include interventions for practitioners...
Future research should investigate the long-term effects...
"""

# Less effective: Minimal content
research_content = "The research found significant results."
```

### 3. Review and Refine Extracted Implications

The analyzer provides automated extraction, but review results:

```python
analysis = analyzer.analyze_impact(research_content)

# Review implications
for impl in analysis.theoretical_implications:
    print(f"Type: {impl.implication_type}")
    print(f"Description: {impl.description}")
    print(f"Confidence: {impl.confidence}")
    print()
```

### 4. Customize Output Sections

Tailor the implications section to your needs:

```python
# Include only specific types
implications_text = []

if analysis.theoretical_implications:
    implications_text.append("### Theoretical Implications")
    for impl in analysis.theoretical_implications[:3]:
        implications_text.append(impl.to_text())

if analysis.practical_implications:
    implications_text.append("### Practical Implications")
    for impl in analysis.practical_implications[:3]:
        implications_text.append(impl.to_text())

custom_section = "\n\n".join(implications_text)
```

## Requirements Addressed

This module addresses the following requirements from the academic research assistant specification:

- **12.1**: Generate implications section with theoretical and practical applications
- **12.2**: Identify how research contributes to or challenges existing theories
- **12.3**: Discuss practical applications for practitioners, policymakers, and stakeholders
- **12.4**: Identify future research directions based on findings and gaps
- **12.5**: Document impact and influence of highly cited papers

## Examples

### Example 1: Complete Impact Analysis

```python
from gazzali.citation_manager import CitationManager, Citation
from gazzali.impact_analyzer import ImpactAnalyzer

# Create citation manager with sample citations
citation_mgr = CitationManager()

# Add highly cited paper
citation1 = Citation(
    citation_id="smith_2015_abc",
    authors=["Smith, J."],
    year=2015,
    title="Foundational Theory of X",
    venue="Nature",
    citation_count=250,
    venue_type="journal"
)
citation_mgr.add_citation(citation1)

# Add emerging paper
citation2 = Citation(
    citation_id="jones_2023_def",
    authors=["Jones, M."],
    year=2023,
    title="Novel Approach to Y",
    venue="Science",
    citation_count=15,
    venue_type="journal"
)
citation_mgr.add_citation(citation2)

# Research content with implications
research_content = """
This research contributes to existing theory by extending the framework
of Smith (2015) to include new dimensions. The findings suggest that
the theoretical model should be refined to account for contextual factors.

Practical implications include the development of new interventions for
practitioners working in clinical settings. These tools can be used to
improve outcomes and facilitate better decision-making.

Future research should investigate the long-term effects of these
interventions and explore their applicability across different populations.
"""

# Analyze impact
analyzer = ImpactAnalyzer(citation_mgr)
analysis = analyzer.analyze_impact(research_content)

# Print results
print(analysis.get_summary())
print(f"\nHighly cited papers: {len(analysis.highly_cited_papers)}")
print(f"Theoretical implications: {len(analysis.theoretical_implications)}")
print(f"Practical implications: {len(analysis.practical_implications)}")
print(f"Future directions: {len(analysis.future_directions)}")

# Generate sections
print("\n" + analyzer.generate_implications_section(analysis))
print("\n" + analyzer.generate_highly_cited_summary(analysis))
```

### Example 2: Integration with Report Generation

```python
from gazzali.academic_config import AcademicConfig
from gazzali.citation_manager import CitationManager
from gazzali.impact_analyzer import ImpactAnalyzer
from gazzali.report_generator import generate_academic_report

# Setup
config = AcademicConfig(
    citation_style="apa",
    output_format="paper",
    discipline="stem"
)

citation_mgr = CitationManager()
# ... populate with citations from research ...

# Analyze impact
analyzer = ImpactAnalyzer(citation_mgr)
analysis = analyzer.analyze_impact(research_results)

# Generate report
report = generate_academic_report(
    question="What are the effects of climate change on biodiversity?",
    research_results=research_results,
    api_key=api_key,
    config=config,
    citation_manager=citation_mgr
)

# Add impact analysis sections
report.sections['Research Implications'] = analyzer.generate_implications_section(
    analysis,
    include_future_directions=True
)

report.sections['Influential Research'] = analyzer.generate_highly_cited_summary(
    analysis,
    max_papers=8
)

# Save report
report.save("climate_biodiversity_report.md", format="markdown")
```

## Troubleshooting

### No Highly Cited Papers Identified

**Problem**: `analysis.highly_cited_papers` is empty

**Solutions**:
1. Ensure citations have `citation_count` values
2. Check that citation counts are reasonable (>0)
3. Lower thresholds by modifying the analyzer logic if needed

### Few Implications Extracted

**Problem**: Very few implications found in research content

**Solutions**:
1. Provide more comprehensive research content
2. Ensure content includes explicit implication statements
3. Include sections discussing theoretical and practical applications
4. Use keywords like "implications", "suggests", "demonstrates"

### Future Directions Not Identified

**Problem**: No future directions extracted

**Solutions**:
1. Include explicit "future research" sections in content
2. Discuss research gaps and limitations
3. Mention unanswered questions
4. Use phrases like "should investigate", "warrants further study"

## Performance Considerations

### Large Citation Collections

For large citation collections (>1000 papers):

```python
# Analyze only papers with citation data
citations_with_counts = [
    c for c in citation_mgr.citations.values()
    if c.citation_count is not None
]

# Create temporary citation manager
temp_mgr = CitationManager()
for citation in citations_with_counts:
    temp_mgr.add_citation(citation)

# Analyze with filtered set
analyzer = ImpactAnalyzer(temp_mgr)
analysis = analyzer.analyze_impact(research_content)
```

### Long Research Content

For very long research content (>50,000 words):

```python
# Extract key sections for analysis
key_sections = [
    discussion_section,
    implications_section,
    conclusion_section,
    limitations_section
]

combined_content = "\n\n".join(key_sections)

# Analyze focused content
analysis = analyzer.analyze_impact(combined_content)
```

## See Also

- [Citation Manager Documentation](CITATION_MANAGER.md)
- [Academic Report Generation](ACADEMIC_REPORT_GENERATION.md)
- [Scholar Tool Integration](SCHOLAR_TOOL.md)
- [Academic Configuration](ACADEMIC_CONFIG.md)
