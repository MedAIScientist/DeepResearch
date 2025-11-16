# Methodology and Theory Extraction

This document describes the methodology and theory extraction features in Gazzali Research, which automatically identify and categorize research methodologies and theoretical frameworks from academic papers.

## Overview

Gazzali Research includes advanced extraction capabilities that analyze academic content to identify:

- **Research Methodologies**: The research methods and approaches used in studies
- **Theoretical Frameworks**: The theories and conceptual models that guide research

This information is automatically extracted from paper abstracts and content during the research process and stored in the research metadata.

## Methodology Extraction

### Supported Methodology Types

The system can identify and categorize the following methodology types:

1. **Qualitative**: Interview-based, ethnographic, case study, grounded theory approaches
2. **Quantitative**: Survey-based, experimental, statistical analysis approaches
3. **Mixed-Methods**: Combined qualitative and quantitative approaches
4. **Meta-Analysis**: Systematic synthesis of multiple studies
5. **Computational**: Simulation, algorithm-based, machine learning approaches
6. **Experimental**: Controlled experiments, randomized trials
7. **Case Study**: Single or multiple case analysis
8. **Systematic Review**: Structured literature review with defined protocols

### Extracted Information

For each methodology, the system extracts:

- **Methodology Type**: Primary classification (qualitative, quantitative, etc.)
- **Specific Methods**: Detailed methods used (e.g., "interviews", "surveys", "regression")
- **Data Collection**: Description of how data was gathered
- **Analysis Techniques**: Statistical or analytical methods applied
- **Sample Information**: Details about participants or data sources
- **Limitations**: Identified methodological constraints or weaknesses
- **Confidence Score**: Reliability of the extraction (0-1)

### Example

```python
from gazzali.methodology_extractor import MethodologyExtractor

extractor = MethodologyExtractor()

content = """
This qualitative study employed semi-structured interviews with 25 participants.
Data were analyzed using thematic analysis to identify key patterns.
Limitations include the small sample size and geographic restriction.
"""

methodology = extractor.extract_methodology(content)

print(f"Type: {methodology.methodology_type}")  # qualitative
print(f"Methods: {methodology.specific_methods}")  # ['Interviews', 'Thematic']
print(f"Confidence: {methodology.confidence}")  # 0.7
```

## Theory Extraction

### Supported Theory Types

The system can identify theories across multiple disciplines:

- **Psychological**: Cognitive, behavioral, social, developmental theories
- **Sociological**: Social, structural, institutional, cultural theories
- **Economic**: Market, rational choice, game theory
- **Organizational**: Management, leadership, strategic theories
- **Communication**: Media, information, communication theories
- **Educational**: Learning, pedagogical, instructional theories
- **Computational**: Information processing, algorithmic theories

### Extracted Information

For each theory, the system extracts:

- **Theory Name**: Name of the theoretical framework
- **Theory Type**: Disciplinary classification
- **Key Constructs**: Important concepts within the theory
- **Definitions**: Definitions of key constructs (when available)
- **Applications**: How the theory is applied in the research
- **Citations**: References to original theory papers
- **Confidence Score**: Reliability of the extraction (0-1)

### Example

```python
from gazzali.methodology_extractor import TheoryExtractor

extractor = TheoryExtractor()

content = """
This study applies Social Cognitive Theory to understand learning behaviors.
The theory's key constructs include self-efficacy, outcome expectations,
and observational learning. Self-efficacy refers to an individual's belief
in their capability to perform specific tasks.
"""

theories = extractor.extract_theories(content)

for theory in theories:
    print(f"Theory: {theory.theory_name}")  # Social Cognitive Theory
    print(f"Type: {theory.theory_type}")  # psychological
    print(f"Constructs: {theory.key_constructs}")  # ['Self-efficacy', ...]
```

## Integration with Scholar Tool

The methodology and theory extraction is automatically integrated with the Google Scholar tool. When searching for academic papers, the system:

1. Extracts the paper's abstract
2. Analyzes the abstract for methodology indicators
3. Identifies theoretical frameworks mentioned
4. Stores this information in the search results metadata

### Scholar Results with Methodology

When you search Google Scholar in academic mode, results include methodology information:

```
1. [Paper Title](url)
   Authors: Smith et al.
   Publication: Journal of Research, 2023
   Cited by: 45 [PEER-REVIEWED]
   Quality: 8.5/10 (high)
   Type: empirical | Methodology: quantitative
   Theories: Social Cognitive Theory, Self-Determination Theory
   
   Abstract text here...
```

## Storage in Research Metadata

Extracted methodology and theory information is stored in the `ResearchMetadata` object:

```python
from gazzali.report_models import ResearchMetadata

metadata = ResearchMetadata(
    question="What factors influence student motivation?",
    methodologies_found=["quantitative", "qualitative", "mixed-methods"],
    key_theories=["Self-Determination Theory", "Achievement Goal Theory"],
    methodology_details={
        "methodology_type": "mixed-methods",
        "specific_methods": ["Surveys", "Interviews"],
        "analysis_techniques": ["Regression", "Thematic"],
        "confidence": 0.8
    },
    theory_details=[
        {
            "theory_name": "Self-Determination Theory",
            "theory_type": "psychological",
            "key_constructs": ["Autonomy", "Competence", "Relatedness"],
            "confidence": 0.9
        }
    ]
)
```

## Use in Report Generation

The extracted methodology and theory information enhances academic reports by:

1. **Methodology Section**: Automatically populating methodology descriptions
2. **Theoretical Framework Section**: Identifying and explaining relevant theories
3. **Literature Review**: Organizing papers by methodology type
4. **Discussion**: Comparing methodological approaches across studies

## Confidence Scores

All extractions include a confidence score (0-1) indicating reliability:

- **0.9-1.0**: Very high confidence (multiple strong indicators)
- **0.7-0.9**: High confidence (clear indicators present)
- **0.5-0.7**: Moderate confidence (some indicators present)
- **0.3-0.5**: Low confidence (weak or ambiguous indicators)
- **0.0-0.3**: Very low confidence (minimal evidence)

Use confidence scores to assess the reliability of extracted information.

## Limitations

### Methodology Extraction Limitations

- **Abstract-Only Analysis**: Extraction is based on abstracts, which may not contain full methodological details
- **Keyword-Based**: Uses pattern matching, which may miss novel or unconventional methodologies
- **Ambiguity**: Some papers use multiple methodologies, making classification challenging
- **Incomplete Information**: Abstracts may not mention all methodological details

### Theory Extraction Limitations

- **Implicit Theories**: Theories that are applied but not explicitly named may be missed
- **Discipline-Specific Terminology**: May not recognize theories from highly specialized fields
- **Theory Variants**: Different versions or extensions of theories may not be distinguished
- **Context Dependency**: Theory identification depends on how theories are mentioned in text

## Best Practices

### For Researchers

1. **Review Extracted Information**: Always verify extracted methodology and theory information
2. **Check Confidence Scores**: Pay attention to confidence scores when using extracted data
3. **Supplement with Manual Review**: Use extraction as a starting point, not a replacement for reading papers
4. **Provide Context**: When possible, provide full paper content rather than just abstracts

### For Developers

1. **Update Patterns**: Regularly update keyword patterns to capture new methodologies and theories
2. **Validate Extractions**: Test extraction accuracy on diverse paper samples
3. **Handle Edge Cases**: Implement fallbacks for ambiguous or missing information
4. **Document Limitations**: Clearly communicate extraction limitations to users

## Future Enhancements

Planned improvements to methodology and theory extraction:

1. **Full-Text Analysis**: Extract from complete papers, not just abstracts
2. **Machine Learning Models**: Use trained models for more accurate classification
3. **Relationship Extraction**: Identify relationships between theories and methodologies
4. **Temporal Analysis**: Track evolution of methodologies and theories over time
5. **Cross-Reference Validation**: Validate extractions against citation networks
6. **Discipline-Specific Models**: Specialized extractors for different academic fields

## API Reference

### MethodologyExtractor

```python
class MethodologyExtractor:
    def extract_methodology(
        self,
        content: str,
        title: str = ""
    ) -> MethodologyInfo:
        """
        Extract methodology information from content.
        
        Args:
            content: Text content to analyze
            title: Optional paper title for context
        
        Returns:
            MethodologyInfo object with extracted information
        """
```

### TheoryExtractor

```python
class TheoryExtractor:
    def extract_theories(
        self,
        content: str,
        title: str = ""
    ) -> List[TheoryInfo]:
        """
        Extract theoretical frameworks from content.
        
        Args:
            content: Text content to analyze
            title: Optional paper title for context
        
        Returns:
            List of TheoryInfo objects
        """
```

### Convenience Function

```python
def extract_methodology_and_theories(
    content: str,
    title: str = ""
) -> Dict[str, Any]:
    """
    Extract both methodology and theories in one call.
    
    Args:
        content: Text content to analyze
        title: Optional paper title
    
    Returns:
        Dictionary with 'methodology' and 'theories' keys
    """
```

## Related Documentation

- [Academic Mode Guide](ACADEMIC_MODE.md) - Overview of academic research features
- [Scholar Tool Documentation](SCHOLAR_TOOL.md) - Google Scholar integration details
- [Report Generation](ACADEMIC_REPORT_GENERATION.md) - How extracted data is used in reports
- [Source Credibility](SOURCE_CREDIBILITY.md) - Quality assessment of sources

## Support

For questions or issues with methodology and theory extraction:

1. Check the confidence scores in extracted data
2. Review the limitations section above
3. Examine the source content for clarity
4. Report persistent issues or false positives

---

*Generated by Gazzali Research - Academic AI Assistant*
