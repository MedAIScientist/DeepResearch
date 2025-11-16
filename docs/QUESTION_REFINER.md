# Question Refiner Documentation

## Overview

The Question Refiner module helps academic researchers transform broad research topics into specific, answerable research questions. It uses the FINER criteria (Feasible, Interesting, Novel, Ethical, Relevant) to ensure questions meet academic standards.

## Features

- **Automatic Question Refinement**: Converts broad topics into 3-5 specific research questions
- **FINER Criteria Assessment**: Evaluates questions using established academic quality criteria
- **Question Type Classification**: Identifies whether questions are descriptive, comparative, relationship-based, or causal
- **Variable Identification**: Extracts key variables, populations, and contexts
- **Scope Assessment**: Determines if questions are too broad, too narrow, or appropriately scoped
- **Feasibility Analysis**: Provides practical considerations for conducting the research

## FINER Criteria

The FINER framework ensures research questions are high quality:

- **Feasible**: Can be investigated with available resources, time, and methods
- **Interesting**: Engages researchers and has potential impact
- **Novel**: Addresses a gap in knowledge or provides new insights
- **Ethical**: Can be conducted ethically without harm
- **Relevant**: Has significance for theory, practice, or policy

## Usage

### Basic Question Refinement

```python
from gazzali.question_refiner import QuestionRefiner

# Initialize the refiner
refiner = QuestionRefiner(api_key="your-api-key")

# Refine a broad topic
broad_topic = "artificial intelligence in education"
refined = refiner.refine_question(broad_topic)

# Access refined questions
print(f"Original: {refined.original_topic}")
print(f"Best question: {refined.get_best_question()}")
print(f"Question type: {refined.question_type}")
print(f"Key variables: {', '.join(refined.key_variables)}")
```

### With Discipline Context

```python
# Refine with discipline-specific guidance
refined = refiner.refine_question(
    broad_topic="machine learning in healthcare",
    discipline="medical",
    context="Focus on diagnostic applications"
)

# View all refined questions
for i, question in enumerate(refined.refined_questions, 1):
    print(f"{i}. {question}")
```

### Quality Assessment

```python
# Assess an existing research question
question = "How does social media use affect adolescent mental health?"
assessment = refiner.assess_question_quality(question, discipline="social")

# Check quality metrics
print(f"Is specific: {assessment.is_specific}")
print(f"Is answerable: {assessment.is_answerable}")
print(f"Scope: {assessment.scope}")
print(f"Overall quality: {assessment.overall_quality()}")

# View FINER scores
for criterion, score in assessment.finer_scores.items():
    print(f"{criterion.capitalize()}: {score}/10")

# Get improvement suggestions
for suggestion in assessment.suggestions:
    print(f"- {suggestion}")
```

## Data Classes

### RefinedQuestion

Represents a refined research question with metadata:

```python
@dataclass
class RefinedQuestion:
    original_topic: str              # Original broad topic
    refined_questions: list[str]     # 3-5 specific questions
    question_type: str               # Question classification
    key_variables: list[str]         # Variables to investigate
    key_populations: list[str]       # Target populations
    contexts: list[str]              # Relevant settings
    scope_assessment: str            # Scope evaluation
    feasibility_notes: str           # Practical considerations
    quality_assessment: QualityAssessment  # FINER assessment
```

### QualityAssessment

Evaluates question quality using FINER criteria:

```python
@dataclass
class QualityAssessment:
    is_specific: bool                # Question is focused
    is_answerable: bool              # Can be researched
    is_novel: bool                   # Addresses knowledge gap
    scope: str                       # 'too_broad', 'appropriate', 'too_narrow'
    suggestions: list[str]           # Improvement recommendations
    finer_scores: dict[str, int]     # Scores for each criterion (0-10)
```

## Question Types

The refiner classifies questions into five types:

1. **Descriptive**: Describes characteristics, prevalence, or patterns
   - Example: "What are the common features of successful online learning platforms?"

2. **Comparative**: Compares two or more groups, interventions, or conditions
   - Example: "How do student outcomes differ between synchronous and asynchronous online courses?"

3. **Relationship**: Examines associations or correlations between variables
   - Example: "What is the relationship between student engagement and course completion rates?"

4. **Causal**: Investigates cause-and-effect relationships
   - Example: "Does gamification in online courses improve student motivation?"

5. **Mixed**: Combines multiple question types
   - Example: "How do different teaching methods affect student performance, and what factors mediate this relationship?"

## Scope Assessment

Questions are evaluated for appropriate scope:

- **too_broad**: Question covers too much ground, needs narrowing
  - Example: "How does technology affect society?"
  - Suggestion: Focus on specific technology, population, and outcome

- **appropriate**: Question is well-scoped for research
  - Example: "How does smartphone use during lectures affect undergraduate students' note-taking quality?"

- **too_narrow**: Question is overly specific, may limit findings
  - Example: "What is the effect of 15-minute meditation sessions on test anxiety in first-year biology students at University X?"
  - Suggestion: Broaden population or generalize intervention

## Integration with CLI

The question refiner can be used with the `--refine` flag:

```bash
# Refine question before research
python -m gazzali.ask "AI in education" --refine --academic

# With discipline specification
python -m gazzali.ask "machine learning diagnostics" \
    --refine --discipline medical --academic
```

## Best Practices

### 1. Start Broad, Refine Iteratively

```python
# First refinement
refined1 = refiner.refine_question("climate change")

# Assess the best question
assessment = refiner.assess_question_quality(refined1.get_best_question())

# Refine further if needed
if assessment.scope == "too_broad":
    refined2 = refiner.refine_question(
        refined1.get_best_question(),
        context="Focus on coastal communities"
    )
```

### 2. Use Discipline Context

Provide discipline information for better refinement:

```python
# STEM research
refined = refiner.refine_question(
    "quantum computing applications",
    discipline="stem"
)

# Social sciences
refined = refiner.refine_question(
    "social media influence",
    discipline="social"
)

# Humanities
refined = refiner.refine_question(
    "narrative structures in literature",
    discipline="humanities"
)
```

### 3. Review Multiple Options

The refiner provides 3-5 questions - review all options:

```python
refined = refiner.refine_question("renewable energy adoption")

print("Choose the best question for your research:")
for i, question in enumerate(refined.refined_questions, 1):
    print(f"\n{i}. {question}")
    print(f"   Variables: {', '.join(refined.key_variables)}")
    print(f"   Population: {', '.join(refined.key_populations)}")
```

### 4. Check Feasibility

Always review feasibility notes:

```python
refined = refiner.refine_question("global education systems")

print(f"Feasibility: {refined.feasibility_notes}")
print(f"Scope: {refined.scope_assessment}")

if refined.quality_assessment:
    print(f"Overall quality: {refined.quality_assessment.overall_quality()}")
```

## Error Handling

The refiner includes robust error handling:

```python
try:
    refined = refiner.refine_question(broad_topic)
except ValueError as e:
    print(f"Refinement failed: {e}")
    # Fallback: use original topic
    refined_questions = [broad_topic]
```

## Configuration

### Environment Variables

```bash
# API configuration (uses same as main research tool)
OPENROUTER_API_KEY=your-key-here

# Optional: Custom model for refinement
QUESTION_REFINER_MODEL=grok-beta
```

### Custom Models

Use different models for refinement:

```python
# Use a specific model
refiner = QuestionRefiner(
    api_key="your-key",
    model="gpt-4",
    base_url="https://api.openai.com/v1"
)

# Or use OpenRouter
refiner = QuestionRefiner(
    api_key="your-key",
    model="anthropic/claude-3-opus",
    base_url="https://openrouter.ai/api/v1"
)
```

## Examples

### Example 1: Education Research

```python
refiner = QuestionRefiner(api_key="key")

refined = refiner.refine_question(
    "online learning effectiveness",
    discipline="social",
    context="K-12 education during pandemic"
)

# Output:
# 1. How did emergency remote teaching during COVID-19 affect K-12 student 
#    learning outcomes compared to traditional in-person instruction?
# 2. What factors predicted successful adaptation to online learning among 
#    K-12 students during the pandemic?
# 3. How did teacher preparedness for online instruction influence student 
#    engagement in K-12 remote learning?
```

### Example 2: Medical Research

```python
refined = refiner.refine_question(
    "AI in medical diagnosis",
    discipline="medical",
    context="Focus on radiology and imaging"
)

# Output:
# 1. What is the diagnostic accuracy of AI-assisted radiology systems 
#    compared to human radiologists for detecting lung cancer in CT scans?
# 2. How does AI integration in radiology workflows affect diagnostic 
#    turnaround time and radiologist workload?
# 3. What factors influence radiologist trust and adoption of AI diagnostic 
#    support tools in clinical practice?
```

### Example 3: Computer Science Research

```python
refined = refiner.refine_question(
    "blockchain security",
    discipline="stem",
    context="Smart contract vulnerabilities"
)

# Output:
# 1. What are the most common vulnerability patterns in Ethereum smart 
#    contracts and their exploitation frequencies?
# 2. How effective are automated static analysis tools in detecting 
#    security vulnerabilities in smart contracts?
# 3. What development practices correlate with lower vulnerability rates 
#    in production smart contracts?
```

## Troubleshooting

### Issue: Questions Still Too Broad

**Solution**: Provide more specific context

```python
refined = refiner.refine_question(
    "machine learning",
    context="Focus on natural language processing for sentiment analysis in social media posts"
)
```

### Issue: Questions Too Technical

**Solution**: Specify target audience in context

```python
refined = refiner.refine_question(
    "quantum entanglement",
    context="Suitable for undergraduate physics research project"
)
```

### Issue: Low FINER Scores

**Solution**: Iterate on the best question

```python
# First attempt
refined1 = refiner.refine_question("social media")

# Assess quality
assessment = refiner.assess_question_quality(refined1.get_best_question())

# If scores are low, refine with suggestions
if assessment.overall_quality() in ['needs_improvement', 'poor']:
    context = "; ".join(assessment.suggestions)
    refined2 = refiner.refine_question(refined1.get_best_question(), context=context)
```

## API Reference

### QuestionRefiner Class

```python
class QuestionRefiner:
    def __init__(self, api_key: str, model: str = "grok-beta", 
                 base_url: str = "https://api.x.ai/v1")
    
    def refine_question(self, broad_topic: str, discipline: Optional[str] = None,
                       context: Optional[str] = None) -> RefinedQuestion
    
    def assess_question_quality(self, question: str, 
                               discipline: Optional[str] = None) -> QualityAssessment
```

### Constants

```python
QuestionRefiner.QUESTION_TYPES = {
    'descriptive': 'Describes characteristics, prevalence, or patterns',
    'comparative': 'Compares two or more groups, interventions, or conditions',
    'relationship': 'Examines associations or correlations between variables',
    'causal': 'Investigates cause-and-effect relationships',
    'mixed': 'Combines multiple question types'
}

QuestionRefiner.FINER_CRITERIA = {
    'feasible': 'Can be investigated with available resources, time, and methods',
    'interesting': 'Engages researchers and has potential impact',
    'novel': 'Addresses a gap in knowledge or provides new insights',
    'ethical': 'Can be conducted ethically without harm',
    'relevant': 'Has significance for theory, practice, or policy'
}
```

## Related Documentation

- [Academic Mode Guide](ACADEMIC_MODE.md) - Overview of academic features
- [Academic Configuration](ACADEMIC_CONFIG.md) - Configuration options
- [Academic Prompts](ACADEMIC_PROMPTS.md) - Prompt engineering for academic research

## References

- Hulley, S. B., et al. (2013). *Designing Clinical Research*. Lippincott Williams & Wilkins.
- Creswell, J. W., & Creswell, J. D. (2017). *Research Design: Qualitative, Quantitative, and Mixed Methods Approaches*. SAGE Publications.
