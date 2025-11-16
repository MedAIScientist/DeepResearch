#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Statistical Analysis Parser for Gazzali Research

This module provides tools for extracting, interpreting, and analyzing statistical
information from academic papers. It supports identification of statistical tests,
extraction of key measures, and interpretation of statistical significance.

Requirements addressed:
- 9.1: Extract key statistical measures (means, SDs, CIs, p-values, effect sizes)
- 9.2: Interpret statistical and practical significance
- 9.3: Identify statistical tests and explain appropriateness
- 9.4: Perform meta-analysis calculations and effect size conversions

Features:
- Statistical measure extraction from text
- Statistical test identification and classification
- Significance interpretation (statistical and practical)
- Effect size calculations and conversions
- Meta-analysis support
- Integration with Python Interpreter for calculations
"""

import re
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum


class StatisticalTest(Enum):
    """Enumeration of common statistical tests."""
    T_TEST = "t-test"
    ANOVA = "ANOVA"
    CHI_SQUARE = "chi-square"
    REGRESSION = "regression"
    CORRELATION = "correlation"
    MANN_WHITNEY = "Mann-Whitney U"
    WILCOXON = "Wilcoxon"
    KRUSKAL_WALLIS = "Kruskal-Wallis"
    ANCOVA = "ANCOVA"
    MANOVA = "MANOVA"
    FACTOR_ANALYSIS = "factor analysis"
    SEM = "structural equation modeling"
    META_ANALYSIS = "meta-analysis"
    UNKNOWN = "unknown"


class EffectSizeType(Enum):
    """Enumeration of effect size measures."""
    COHENS_D = "Cohen's d"
    HEDGES_G = "Hedges' g"
    GLASS_DELTA = "Glass's delta"
    COHENS_F = "Cohen's f"
    ETA_SQUARED = "eta-squared"
    PARTIAL_ETA_SQUARED = "partial eta-squared"
    OMEGA_SQUARED = "omega-squared"
    R_SQUARED = "R-squared"
    CORRELATION_R = "correlation r"
    ODDS_RATIO = "odds ratio"
    RISK_RATIO = "risk ratio"
    CRAMERS_V = "Cramer's V"
    UNKNOWN = "unknown"


@dataclass
class StatisticalMeasure:
    """Represents a statistical measure extracted from text."""
    measure_type: str  # e.g., "mean", "SD", "p-value", "CI"
    value: float
    unit: Optional[str] = None
    context: Optional[str] = None  # Surrounding text for context
    variable: Optional[str] = None  # What variable this measure describes
    
    def __str__(self) -> str:
        """String representation of the measure."""
        parts = [f"{self.measure_type} = {self.value}"]
        if self.unit:
            parts.append(self.unit)
        if self.variable:
            parts = [f"{self.variable}: {parts[0]}"]
        return ' '.join(parts)


@dataclass
class EffectSize:
    """Represents an effect size measure."""
    effect_type: EffectSizeType
    value: float
    interpretation: str  # "small", "medium", "large"
    confidence_interval: Optional[Tuple[float, float]] = None
    
    def __str__(self) -> str:
        """String representation of effect size."""
        ci_str = ""
        if self.confidence_interval:
            ci_str = f", 95% CI [{self.confidence_interval[0]:.3f}, {self.confidence_interval[1]:.3f}]"
        return f"{self.effect_type.value} = {self.value:.3f} ({self.interpretation}){ci_str}"


@dataclass
class StatisticalResult:
    """Represents a complete statistical result from a test."""
    test_type: StatisticalTest
    test_statistic: Optional[float] = None
    p_value: Optional[float] = None
    degrees_of_freedom: Optional[Tuple[int, ...]] = None
    effect_size: Optional[EffectSize] = None
    sample_size: Optional[int] = None
    is_significant: Optional[bool] = None
    alpha_level: float = 0.05
    interpretation: Optional[str] = None
    appropriateness_notes: Optional[str] = None
    
    def __post_init__(self):
        """Calculate significance if p-value is available."""
        if self.p_value is not None and self.is_significant is None:
            self.is_significant = self.p_value < self.alpha_level
    
    def __str__(self) -> str:
        """String representation of statistical result."""
        parts = [f"{self.test_type.value}"]
        
        if self.test_statistic is not None:
            parts.append(f"statistic = {self.test_statistic:.3f}")
        
        if self.degrees_of_freedom:
            df_str = ', '.join(map(str, self.degrees_of_freedom))
            parts.append(f"df = {df_str}")
        
        if self.p_value is not None:
            sig_marker = "*" if self.is_significant else "ns"
            parts.append(f"p = {self.p_value:.4f} ({sig_marker})")
        
        if self.effect_size:
            parts.append(str(self.effect_size))
        
        return ', '.join(parts)


@dataclass
class StatisticalSummary:
    """Summary of all statistical information extracted from text."""
    measures: List[StatisticalMeasure] = field(default_factory=list)
    results: List[StatisticalResult] = field(default_factory=list)
    tests_identified: List[StatisticalTest] = field(default_factory=list)
    effect_sizes: List[EffectSize] = field(default_factory=list)
    sample_sizes: List[int] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            'measures': [str(m) for m in self.measures],
            'results': [str(r) for r in self.results],
            'tests_identified': [t.value for t in self.tests_identified],
            'effect_sizes': [str(e) for e in self.effect_sizes],
            'sample_sizes': self.sample_sizes,
            'total_measures': len(self.measures),
            'total_results': len(self.results),
        }


class StatisticalParser:
    """
    Parser for extracting and interpreting statistical information from text.
    
    This class provides methods to:
    - Extract statistical measures (means, SDs, p-values, etc.)
    - Identify statistical tests used
    - Interpret statistical significance
    - Calculate and convert effect sizes
    - Assess appropriateness of statistical methods
    """
    
    def __init__(self, alpha_level: float = 0.05):
        """
        Initialize the statistical parser.
        
        Args:
            alpha_level: Significance threshold (default: 0.05)
        """
        self.alpha_level = alpha_level
        
        # Regex patterns for statistical measures
        self.patterns = {
            'mean': [
                r'M\s*=\s*([\d.]+)',
                r'mean\s*=\s*([\d.]+)',
                r'μ\s*=\s*([\d.]+)',
                r'average\s*=\s*([\d.]+)',
            ],
            'sd': [
                r'SD\s*=\s*([\d.]+)',
                r'std\s*=\s*([\d.]+)',
                r'σ\s*=\s*([\d.]+)',
                r'standard deviation\s*=\s*([\d.]+)',
            ],
            'p_value': [
                r'p\s*[=<>]\s*([\d.]+)',
                r'p-value\s*[=<>]\s*([\d.]+)',
                r'P\s*[=<>]\s*([\d.]+)',
            ],
            'confidence_interval': [
                r'95%\s*CI\s*[:\[]\s*([\d.]+)\s*[,;]\s*([\d.]+)\s*[\]]',
                r'CI\s*=\s*\[\s*([\d.]+)\s*,\s*([\d.]+)\s*\]',
            ],
            'effect_size': [
                r'd\s*=\s*([\d.]+)',
                r"Cohen's d\s*=\s*([\d.]+)",
                r'η²\s*=\s*([\d.]+)',
                r'eta-squared\s*=\s*([\d.]+)',
                r'r\s*=\s*([\d.]+)',
            ],
            'sample_size': [
                r'[Nn]\s*=\s*(\d+)',
                r'sample size\s*=\s*(\d+)',
                r'participants\s*=\s*(\d+)',
            ],
        }
        
        # Test identification patterns
        self.test_patterns = {
            StatisticalTest.T_TEST: [
                r't-test', r't test', r"Student's t", r'paired t',
                r'independent t', r't\(\d+\)\s*='
            ],
            StatisticalTest.ANOVA: [
                r'ANOVA', r'analysis of variance', r'F\(\d+,\s*\d+\)\s*='
            ],
            StatisticalTest.CHI_SQUARE: [
                r'chi-square', r'χ²', r'chi square', r'χ2'
            ],
            StatisticalTest.REGRESSION: [
                r'regression', r'linear model', r'multiple regression',
                r'logistic regression', r'hierarchical regression'
            ],
            StatisticalTest.CORRELATION: [
                r'correlation', r"Pearson's r", r"Spearman's rho",
                r'correlational analysis'
            ],
            StatisticalTest.MANN_WHITNEY: [
                r'Mann-Whitney', r'Mann Whitney U', r'Wilcoxon rank-sum'
            ],
            StatisticalTest.WILCOXON: [
                r'Wilcoxon signed-rank', r'Wilcoxon test'
            ],
            StatisticalTest.KRUSKAL_WALLIS: [
                r'Kruskal-Wallis', r'Kruskal Wallis'
            ],
            StatisticalTest.ANCOVA: [
                r'ANCOVA', r'analysis of covariance'
            ],
            StatisticalTest.MANOVA: [
                r'MANOVA', r'multivariate analysis of variance'
            ],
            StatisticalTest.FACTOR_ANALYSIS: [
                r'factor analysis', r'principal component', r'PCA',
                r'exploratory factor', r'confirmatory factor'
            ],
            StatisticalTest.SEM: [
                r'structural equation', r'SEM', r'path analysis'
            ],
            StatisticalTest.META_ANALYSIS: [
                r'meta-analysis', r'meta analysis', r'systematic review'
            ],
        }
    
    def extract_statistical_measures(self, text: str) -> List[StatisticalMeasure]:
        """
        Extract statistical measures from text.
        
        Args:
            text: Text to extract measures from
        
        Returns:
            List of StatisticalMeasure objects
        """
        measures = []
        
        for measure_type, patterns in self.patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, text, re.IGNORECASE)
                for match in matches:
                    try:
                        if measure_type == 'confidence_interval':
                            # CI has two values
                            lower = float(match.group(1))
                            upper = float(match.group(2))
                            measures.append(StatisticalMeasure(
                                measure_type='CI_lower',
                                value=lower,
                                context=match.group(0)
                            ))
                            measures.append(StatisticalMeasure(
                                measure_type='CI_upper',
                                value=upper,
                                context=match.group(0)
                            ))
                        else:
                            value = float(match.group(1))
                            measures.append(StatisticalMeasure(
                                measure_type=measure_type,
                                value=value,
                                context=match.group(0)
                            ))
                    except (ValueError, IndexError):
                        continue
        
        return measures
    
    def identify_statistical_tests(self, text: str) -> List[StatisticalTest]:
        """
        Identify statistical tests mentioned in text.
        
        Args:
            text: Text to analyze
        
        Returns:
            List of identified StatisticalTest enums
        """
        identified_tests = []
        
        for test_type, patterns in self.test_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    if test_type not in identified_tests:
                        identified_tests.append(test_type)
                    break
        
        return identified_tests if identified_tests else [StatisticalTest.UNKNOWN]
    
    def interpret_p_value(self, p_value: float, alpha: Optional[float] = None) -> Dict[str, Any]:
        """
        Interpret a p-value for statistical and practical significance.
        
        Args:
            p_value: The p-value to interpret
            alpha: Significance threshold (uses instance default if None)
        
        Returns:
            Dictionary with interpretation details
        """
        if alpha is None:
            alpha = self.alpha_level
        
        is_significant = p_value < alpha
        
        # Determine strength of evidence
        if p_value < 0.001:
            strength = "very strong"
            stars = "***"
        elif p_value < 0.01:
            strength = "strong"
            stars = "**"
        elif p_value < 0.05:
            strength = "moderate"
            stars = "*"
        elif p_value < 0.10:
            strength = "weak (marginal)"
            stars = "†"
        else:
            strength = "insufficient"
            stars = "ns"
        
        interpretation = {
            'p_value': p_value,
            'alpha': alpha,
            'is_significant': is_significant,
            'strength': strength,
            'notation': stars,
            'interpretation': (
                f"The p-value of {p_value:.4f} indicates {strength} evidence "
                f"against the null hypothesis (α = {alpha}). "
                f"{'The result is statistically significant.' if is_significant else 'The result is not statistically significant.'}"
            )
        }
        
        return interpretation
    
    def calculate_cohens_d(self, mean1: float, mean2: float, sd_pooled: float) -> EffectSize:
        """
        Calculate Cohen's d effect size.
        
        Args:
            mean1: Mean of group 1
            mean2: Mean of group 2
            sd_pooled: Pooled standard deviation
        
        Returns:
            EffectSize object with Cohen's d
        """
        d = abs(mean1 - mean2) / sd_pooled
        
        # Interpret effect size (Cohen's conventions)
        if d < 0.2:
            interpretation = "negligible"
        elif d < 0.5:
            interpretation = "small"
        elif d < 0.8:
            interpretation = "medium"
        else:
            interpretation = "large"
        
        return EffectSize(
            effect_type=EffectSizeType.COHENS_D,
            value=d,
            interpretation=interpretation
        )
    
    def convert_r_to_d(self, r: float) -> float:
        """
        Convert correlation coefficient r to Cohen's d.
        
        Args:
            r: Correlation coefficient
        
        Returns:
            Cohen's d value
        """
        # Formula: d = 2r / sqrt(1 - r²)
        return (2 * r) / ((1 - r**2) ** 0.5)
    
    def convert_d_to_r(self, d: float) -> float:
        """
        Convert Cohen's d to correlation coefficient r.
        
        Args:
            d: Cohen's d value
        
        Returns:
            Correlation coefficient r
        """
        # Formula: r = d / sqrt(d² + 4)
        return d / ((d**2 + 4) ** 0.5)
    
    def interpret_effect_size(self, effect_size: float, effect_type: EffectSizeType) -> str:
        """
        Interpret an effect size value.
        
        Args:
            effect_size: The effect size value
            effect_type: Type of effect size measure
        
        Returns:
            Interpretation string
        """
        # Cohen's d, Hedges' g, Glass's delta
        if effect_type in [EffectSizeType.COHENS_D, EffectSizeType.HEDGES_G, EffectSizeType.GLASS_DELTA]:
            if abs(effect_size) < 0.2:
                return "negligible"
            elif abs(effect_size) < 0.5:
                return "small"
            elif abs(effect_size) < 0.8:
                return "medium"
            else:
                return "large"
        
        # Correlation r
        elif effect_type == EffectSizeType.CORRELATION_R:
            if abs(effect_size) < 0.1:
                return "negligible"
            elif abs(effect_size) < 0.3:
                return "small"
            elif abs(effect_size) < 0.5:
                return "medium"
            else:
                return "large"
        
        # Eta-squared, R-squared
        elif effect_type in [EffectSizeType.ETA_SQUARED, EffectSizeType.R_SQUARED]:
            if effect_size < 0.01:
                return "negligible"
            elif effect_size < 0.06:
                return "small"
            elif effect_size < 0.14:
                return "medium"
            else:
                return "large"
        
        # Odds ratio
        elif effect_type == EffectSizeType.ODDS_RATIO:
            if 0.9 <= effect_size <= 1.1:
                return "negligible"
            elif 0.7 <= effect_size < 0.9 or 1.1 < effect_size <= 1.5:
                return "small"
            elif 0.5 <= effect_size < 0.7 or 1.5 < effect_size <= 2.5:
                return "medium"
            else:
                return "large"
        
        return "unknown"
    
    def assess_test_appropriateness(self, test_type: StatisticalTest, 
                                   context: Dict[str, Any]) -> str:
        """
        Assess the appropriateness of a statistical test for given context.
        
        Args:
            test_type: The statistical test used
            context: Dictionary with context info (data_type, sample_size, etc.)
        
        Returns:
            Assessment string explaining appropriateness
        """
        data_type = context.get('data_type', 'unknown')
        sample_size = context.get('sample_size', None)
        groups = context.get('groups', 2)
        
        assessments = []
        
        # T-test appropriateness
        if test_type == StatisticalTest.T_TEST:
            if data_type == 'continuous':
                assessments.append("✓ Appropriate for continuous data")
            if sample_size and sample_size < 30:
                assessments.append("⚠ Small sample size; normality assumption critical")
            if groups == 2:
                assessments.append("✓ Appropriate for comparing two groups")
            else:
                assessments.append("✗ Not appropriate for more than two groups; consider ANOVA")
        
        # ANOVA appropriateness
        elif test_type == StatisticalTest.ANOVA:
            if data_type == 'continuous':
                assessments.append("✓ Appropriate for continuous dependent variable")
            if groups > 2:
                assessments.append("✓ Appropriate for comparing multiple groups")
            else:
                assessments.append("⚠ For two groups, t-test may be simpler")
        
        # Chi-square appropriateness
        elif test_type == StatisticalTest.CHI_SQUARE:
            if data_type == 'categorical':
                assessments.append("✓ Appropriate for categorical data")
            if sample_size and sample_size < 20:
                assessments.append("⚠ Small sample; Fisher's exact test may be better")
        
        # Regression appropriateness
        elif test_type == StatisticalTest.REGRESSION:
            if data_type == 'continuous':
                assessments.append("✓ Appropriate for continuous outcome")
            if sample_size and sample_size < 100:
                assessments.append("⚠ Consider sample size relative to number of predictors")
        
        # Non-parametric tests
        elif test_type in [StatisticalTest.MANN_WHITNEY, StatisticalTest.WILCOXON]:
            assessments.append("✓ Appropriate when normality assumptions violated")
            assessments.append("✓ Robust to outliers")
        
        if not assessments:
            return "Assessment requires more context about the research design and data characteristics."
        
        return " | ".join(assessments)
    
    def parse_statistical_result(self, text: str) -> Optional[StatisticalResult]:
        """
        Parse a complete statistical result from text.
        
        Args:
            text: Text containing statistical result
        
        Returns:
            StatisticalResult object or None
        """
        # Identify test type
        tests = self.identify_statistical_tests(text)
        if not tests or tests[0] == StatisticalTest.UNKNOWN:
            return None
        
        test_type = tests[0]
        
        # Extract measures
        measures = self.extract_statistical_measures(text)
        
        # Extract p-value
        p_value = None
        for measure in measures:
            if measure.measure_type == 'p_value':
                p_value = measure.value
                break
        
        # Extract sample size
        sample_size = None
        for measure in measures:
            if measure.measure_type == 'sample_size':
                sample_size = int(measure.value)
                break
        
        # Create result
        result = StatisticalResult(
            test_type=test_type,
            p_value=p_value,
            sample_size=sample_size,
            alpha_level=self.alpha_level
        )
        
        # Add interpretation
        if p_value is not None:
            interp = self.interpret_p_value(p_value)
            result.interpretation = interp['interpretation']
        
        return result
    
    def extract_all_statistics(self, text: str) -> StatisticalSummary:
        """
        Extract all statistical information from text.
        
        Args:
            text: Text to analyze
        
        Returns:
            StatisticalSummary object with all extracted information
        """
        summary = StatisticalSummary()
        
        # Extract measures
        summary.measures = self.extract_statistical_measures(text)
        
        # Identify tests
        summary.tests_identified = self.identify_statistical_tests(text)
        
        # Extract sample sizes
        for measure in summary.measures:
            if measure.measure_type == 'sample_size':
                summary.sample_sizes.append(int(measure.value))
        
        # Try to parse complete results
        # Split text into sentences and try to parse each
        sentences = re.split(r'[.!?]\s+', text)
        for sentence in sentences:
            result = self.parse_statistical_result(sentence)
            if result:
                summary.results.append(result)
        
        return summary
    
    def generate_meta_analysis_code(self, effect_sizes: List[float], 
                                   sample_sizes: List[int]) -> str:
        """
        Generate Python code for meta-analysis calculations.
        
        Args:
            effect_sizes: List of effect sizes from studies
            sample_sizes: List of sample sizes from studies
        
        Returns:
            Python code string for meta-analysis
        """
        code = f"""
# Meta-analysis calculation
import numpy as np

# Study data
effect_sizes = {effect_sizes}
sample_sizes = {sample_sizes}

# Calculate weights (inverse variance weighting)
weights = np.array(sample_sizes)
weights = weights / np.sum(weights)

# Calculate pooled effect size
pooled_effect = np.sum(np.array(effect_sizes) * weights)

# Calculate standard error
se = np.sqrt(1 / np.sum(sample_sizes))

# Calculate 95% confidence interval
ci_lower = pooled_effect - 1.96 * se
ci_upper = pooled_effect + 1.96 * se

print(f"Pooled effect size: {{pooled_effect:.3f}}")
print(f"95% CI: [{{ci_lower:.3f}}, {{ci_upper:.3f}}]")
print(f"Standard error: {{se:.3f}}")

# Heterogeneity (I²)
# Note: This is a simplified calculation
q_statistic = np.sum(weights * (np.array(effect_sizes) - pooled_effect)**2)
df = len(effect_sizes) - 1
i_squared = max(0, (q_statistic - df) / q_statistic * 100)
print(f"I² (heterogeneity): {{i_squared:.1f}}%")
"""
        return code


def create_statistical_table(results: List[StatisticalResult]) -> str:
    """
    Create a formatted table of statistical results.
    
    Args:
        results: List of StatisticalResult objects
    
    Returns:
        Markdown-formatted table string
    """
    if not results:
        return "No statistical results to display."
    
    lines = []
    lines.append("| Test | Statistic | df | p-value | Effect Size | Significant |")
    lines.append("|------|-----------|----|---------| ------------|-------------|")
    
    for result in results:
        test = result.test_type.value
        stat = f"{result.test_statistic:.3f}" if result.test_statistic else "—"
        df = ', '.join(map(str, result.degrees_of_freedom)) if result.degrees_of_freedom else "—"
        p = f"{result.p_value:.4f}" if result.p_value else "—"
        effect = str(result.effect_size) if result.effect_size else "—"
        sig = "Yes*" if result.is_significant else "No"
        
        lines.append(f"| {test} | {stat} | {df} | {p} | {effect} | {sig} |")
    
    return '\n'.join(lines)
