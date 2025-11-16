# Statistical Analysis Support

## Overview

The Statistical Analysis Parser (`stats_parser.py`) provides comprehensive tools for extracting, interpreting, and analyzing statistical information from academic papers. This module addresses Requirements 9.1-9.4 by enabling automated extraction of statistical measures, identification of statistical tests, interpretation of significance, and support for meta-analysis calculations.

## Features

### 1. Statistical Measure Extraction (Requirement 9.1)

The parser can automatically extract key statistical measures from text:

- **Descriptive Statistics**: means (M, μ), standard deviations (SD, σ), medians
- **Inferential Statistics**: p-values, confidence intervals (CI), test statistics
- **Effect Sizes**: Cohen's d, eta-squared (η²), correlation coefficients (r)
- **Sample Information**: sample sizes (N), participant counts

**Example Usage:**

```python
from gazzali.tools.stats_parser import StatisticalParser

parser = StatisticalParser()
text = "The treatment group (M = 45.3, SD = 8.2, N = 120) showed significantly higher scores than the control group (M = 38.7, SD = 7.9, N = 115), t(233) = 5.67, p < .001, d = 0.84."

measures = parser.extract_statistical_measures(text)
for measure in measures:
    print(measure)
# Output:
# mean = 45.3
# SD = 8.2
# sample_size = 120
# mean = 38.7
# SD = 7.9
# sample_size = 115
# p_value = 0.001
# effect_size = 0.84
```

### 2. Statistical Significance Interpretation (Requirement 9.2)

The parser interprets both statistical and practical significance:

**Statistical Significance:**
- Compares p-values against alpha threshold (default: 0.05)
- Provides strength of evidence ratings (very strong, strong, moderate, weak)
- Uses standard notation (*** p < .001, ** p < .01, * p < .05, † p < .10, ns)

**Practical Significance:**
- Interprets effect sizes using established conventions
- Distinguishes between statistical significance and practical importance
- Provides context-appropriate interpretations

**Example Usage:**

```python
# Interpret a p-value
interpretation = parser.interpret_p_value(0.003)
print(interpretation['interpretation'])
# Output: "The p-value of 0.0030 indicates strong evidence against the null 
# hypothesis (α = 0.05). The result is statistically significant."

# Interpret effect size
effect_size = parser.calculate_cohens_d(mean1=45.3, mean2=38.7, sd_pooled=8.05)
print(effect_size)
# Output: "Cohen's d = 0.820 (large)"
```

### 3. Statistical Test Identification (Requirement 9.3)

The parser identifies and explains the appropriateness of statistical tests:

**Supported Tests:**
- **Parametric**: t-test, ANOVA, ANCOVA, MANOVA, regression
- **Non-parametric**: Mann-Whitney U, Wilcoxon, Kruskal-Wallis
- **Categorical**: Chi-square, Fisher's exact
- **Multivariate**: Factor analysis, SEM, PCA
- **Meta-analysis**: Systematic review methods

**Example Usage:**

```python
# Identify tests in text
text = "We conducted a one-way ANOVA to compare the three groups, F(2, 147) = 8.45, p < .001, η² = 0.103."

tests = parser.identify_statistical_tests(text)
print(tests)
# Output: [StatisticalTest.ANOVA]

# Assess appropriateness
context = {
    'data_type': 'continuous',
    'sample_size': 150,
    'groups': 3
}
assessment = parser.assess_test_appropriateness(StatisticalTest.ANOVA, context)
print(assessment)
# Output: "✓ Appropriate for continuous dependent variable | ✓ Appropriate for comparing multiple groups"
```

### 4. Meta-Analysis Support (Requirement 9.4)

The parser supports meta-analysis calculations and effect size conversions:

**Effect Size Conversions:**
- Cohen's d ↔ correlation r
- Various effect size standardizations
- Confidence interval calculations

**Meta-Analysis Calculations:**
- Pooled effect sizes with inverse variance weighting
- Heterogeneity assessment (I² statistic)
- Forest plot data preparation
- Python code generation for complex calculations

**Example Usage:**

```python
# Convert between effect sizes
r = 0.40
d = parser.convert_r_to_d(r)
print(f"r = {r:.3f} → d = {d:.3f}")
# Output: "r = 0.400 → d = 0.873"

# Generate meta-analysis code
effect_sizes = [0.45, 0.62, 0.38, 0.51]
sample_sizes = [120, 95, 150, 110]
code = parser.generate_meta_analysis_code(effect_sizes, sample_sizes)

# Execute with Python Interpreter tool
# The code calculates pooled effect size, CI, and heterogeneity
```

## Data Structures

### StatisticalMeasure

Represents a single statistical measure extracted from text:

```python
@dataclass
class StatisticalMeasure:
    measure_type: str      # "mean", "SD", "p_value", "CI", etc.
    value: float           # Numerical value
    unit: Optional[str]    # Unit of measurement
    context: Optional[str] # Surrounding text
    variable: Optional[str] # Variable name
```

### StatisticalResult

Represents a complete statistical test result:

```python
@dataclass
class StatisticalResult:
    test_type: StatisticalTest
    test_statistic: Optional[float]
    p_value: Optional[float]
    degrees_of_freedom: Optional[Tuple[int, ...]]
    effect_size: Optional[EffectSize]
    sample_size: Optional[int]
    is_significant: Optional[bool]
    alpha_level: float = 0.05
    interpretation: Optional[str]
    appropriateness_notes: Optional[str]
```

### EffectSize

Represents an effect size measure with interpretation:

```python
@dataclass
class EffectSize:
    effect_type: EffectSizeType  # Cohen's d, eta-squared, etc.
    value: float
    interpretation: str          # "small", "medium", "large"
    confidence_interval: Optional[Tuple[float, float]]
```

### StatisticalSummary

Comprehensive summary of all statistical information:

```python
@dataclass
class StatisticalSummary:
    measures: List[StatisticalMeasure]
    results: List[StatisticalResult]
    tests_identified: List[StatisticalTest]
    effect_sizes: List[EffectSize]
    sample_sizes: List[int]
```

## Integration with Research Agent

The Statistical Parser integrates with the research agent workflow:

1. **During Research**: Extract statistics from paper abstracts and results sections
2. **During Synthesis**: Include statistical summaries in generated reports
3. **For Meta-Analysis**: Aggregate effect sizes across multiple studies
4. **With Python Interpreter**: Execute complex statistical calculations

**Example Integration:**

```python
# In research agent workflow
from gazzali.tools.stats_parser import StatisticalParser

parser = StatisticalParser()

# Extract statistics from paper
paper_text = """
Results showed significant differences between groups, 
F(2, 147) = 8.45, p < .001, η² = 0.103. Post-hoc tests 
revealed that Group A (M = 45.3, SD = 8.2) scored 
significantly higher than Group B (M = 38.7, SD = 7.9), 
t(233) = 5.67, p < .001, d = 0.84.
"""

summary = parser.extract_all_statistics(paper_text)

# Generate formatted output for report
print(f"Statistical Tests Identified: {[t.value for t in summary.tests_identified]}")
print(f"Total Measures Extracted: {len(summary.measures)}")
print(f"Significant Results: {sum(1 for r in summary.results if r.is_significant)}")
```

## Effect Size Interpretation Guidelines

### Cohen's d (Standardized Mean Difference)

- **Negligible**: |d| < 0.20
- **Small**: 0.20 ≤ |d| < 0.50
- **Medium**: 0.50 ≤ |d| < 0.80
- **Large**: |d| ≥ 0.80

### Correlation (r)

- **Negligible**: |r| < 0.10
- **Small**: 0.10 ≤ |r| < 0.30
- **Medium**: 0.30 ≤ |r| < 0.50
- **Large**: |r| ≥ 0.50

### Eta-squared (η²) and R-squared (R²)

- **Negligible**: < 0.01 (< 1% variance explained)
- **Small**: 0.01 ≤ value < 0.06 (1-6% variance)
- **Medium**: 0.06 ≤ value < 0.14 (6-14% variance)
- **Large**: ≥ 0.14 (≥ 14% variance)

### Odds Ratio (OR)

- **Negligible**: 0.90 ≤ OR ≤ 1.10
- **Small**: 0.70 ≤ OR < 0.90 or 1.10 < OR ≤ 1.50
- **Medium**: 0.50 ≤ OR < 0.70 or 1.50 < OR ≤ 2.50
- **Large**: OR < 0.50 or OR > 2.50

## Statistical Test Appropriateness Guidelines

### T-test

**Appropriate when:**
- Comparing means of two groups
- Dependent variable is continuous
- Data approximately normally distributed (or N > 30)
- Equal variances (or use Welch's correction)

**Not appropriate when:**
- More than two groups (use ANOVA)
- Dependent variable is categorical (use chi-square)
- Severe violations of normality (use Mann-Whitney U)

### ANOVA

**Appropriate when:**
- Comparing means of three or more groups
- Dependent variable is continuous
- Homogeneity of variance across groups
- Independent observations

**Not appropriate when:**
- Only two groups (t-test is simpler)
- Dependent variable is categorical
- Severe violations of assumptions (use Kruskal-Wallis)

### Chi-square

**Appropriate when:**
- Both variables are categorical
- Expected frequencies ≥ 5 in all cells
- Independent observations

**Not appropriate when:**
- Expected frequencies < 5 (use Fisher's exact)
- Variables are continuous (use correlation/regression)
- Paired/matched data (use McNemar's test)

### Regression

**Appropriate when:**
- Predicting continuous outcome from one or more predictors
- Linear relationship between variables
- Adequate sample size (N > 100 + number of predictors)
- No severe multicollinearity

**Not appropriate when:**
- Outcome is categorical (use logistic regression)
- Non-linear relationships (use polynomial/non-linear regression)
- Severe violations of assumptions

## Generating Statistical Tables

The module includes utilities for creating formatted statistical tables:

```python
from gazzali.tools.stats_parser import create_statistical_table

# Create table from results
table = create_statistical_table(summary.results)
print(table)
```

**Output:**

| Test | Statistic | df | p-value | Effect Size | Significant |
|------|-----------|----|---------| ------------|-------------|
| ANOVA | 8.450 | 2, 147 | 0.0001 | η² = 0.103 (medium) | Yes* |
| t-test | 5.670 | 233 | 0.0001 | d = 0.840 (large) | Yes* |

## Best Practices

1. **Always report effect sizes**: Statistical significance alone is insufficient
2. **Consider practical significance**: Large samples can yield significant but trivial effects
3. **Report confidence intervals**: Provide precision estimates for effect sizes
4. **Check assumptions**: Verify that statistical tests are appropriate for the data
5. **Correct for multiple comparisons**: Use Bonferroni or FDR correction when needed
6. **Report complete statistics**: Include test statistic, df, p-value, and effect size

## Limitations

- **Pattern-based extraction**: May miss non-standard statistical reporting formats
- **Context sensitivity**: Cannot always determine which statistics belong together
- **Assumption checking**: Cannot verify that statistical assumptions were met
- **Complex designs**: May not fully capture factorial or nested designs
- **Bayesian statistics**: Primarily focused on frequentist approaches

## Future Enhancements

- Bayesian statistics support (Bayes factors, credible intervals)
- Power analysis calculations
- Sample size determination
- Advanced meta-analysis (publication bias, sensitivity analysis)
- Integration with statistical software output (SPSS, R, SAS)
- Automated assumption checking recommendations
- Interactive statistical visualizations

## References

- Cohen, J. (1988). Statistical power analysis for the behavioral sciences (2nd ed.)
- American Psychological Association (2020). Publication Manual (7th ed.)
- Cumming, G. (2012). Understanding the new statistics: Effect sizes, confidence intervals, and meta-analysis
- Lakens, D. (2013). Calculating and reporting effect sizes to facilitate cumulative science

## Related Documentation

- [Academic Prompts](ACADEMIC_PROMPTS.md) - Integration with research agent
- [Report Generation](ACADEMIC_REPORT_GENERATION.md) - Including statistics in reports
- [Methodology Extraction](METHODOLOGY_THEORY_EXTRACTION.md) - Identifying research methods
