#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Workflow Templates for Gazzali Research

This module provides preset workflow templates for common academic research tasks.
Each template configures prompts, search strategies, output formats, and other
settings optimized for specific research types.

Templates support:
- Literature Review: Comprehensive synthesis of existing research
- Systematic Review: Structured, protocol-driven literature analysis
- Methodology Comparison: Comparative analysis of research methods
- Theoretical Analysis: Deep dive into theoretical frameworks
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Any

from ..academic_config import AcademicConfig, OutputFormat, Discipline


class WorkflowType(str, Enum):
    """Types of research workflows"""
    LITERATURE_REVIEW = "literature_review"
    SYSTEMATIC_REVIEW = "systematic_review"
    METHODOLOGY_COMPARISON = "methodology_comparison"
    THEORETICAL_ANALYSIS = "theoretical_analysis"


@dataclass
class WorkflowTemplate:
    """
    Template for a research workflow.
    
    Attributes:
        name: Human-readable workflow name
        workflow_type: Type of workflow
        description: Brief description of the workflow
        academic_config: Academic configuration settings
        search_strategy: Search strategy description
        prompt_additions: Additional prompt instructions
        required_sections: Required report sections
        recommended_word_count: Recommended word count range
        quality_criteria: Quality assessment criteria
        example_questions: Example research questions for this workflow
    """
    
    name: str
    workflow_type: WorkflowType
    description: str
    academic_config: AcademicConfig
    search_strategy: str
    prompt_additions: Dict[str, str] = field(default_factory=dict)
    required_sections: List[str] = field(default_factory=list)
    recommended_word_count: tuple[int, int] = (5000, 10000)
    quality_criteria: List[str] = field(default_factory=list)
    example_questions: List[str] = field(default_factory=list)
    
    def get_research_prompt_additions(self) -> str:
        """
        Get additional prompt text for research agent.
        
        Returns:
            Formatted prompt additions for research phase
        """
        if not self.prompt_additions.get('research'):
            return ""
        
        return f"\n## Workflow-Specific Instructions\n\n{self.prompt_additions['research']}\n"
    
    def get_synthesis_prompt_additions(self) -> str:
        """
        Get additional prompt text for synthesis model.
        
        Returns:
            Formatted prompt additions for synthesis phase
        """
        if not self.prompt_additions.get('synthesis'):
            return ""
        
        return f"\n## Workflow-Specific Instructions\n\n{self.prompt_additions['synthesis']}\n"
    
    def get_search_strategy_prompt(self) -> str:
        """
        Get search strategy prompt text.
        
        Returns:
            Formatted search strategy instructions
        """
        return f"\n## Search Strategy\n\n{self.search_strategy}\n"
    
    def validate_config(self) -> List[str]:
        """
        Validate workflow configuration.
        
        Returns:
            List of validation issues (empty if valid)
        """
        issues = []
        
        # Validate academic config
        config_issues = self.academic_config.validate()
        issues.extend(config_issues)
        
        # Validate word count against recommendations
        target = self.academic_config.word_count_target
        min_rec, max_rec = self.recommended_word_count
        
        if target < min_rec:
            issues.append(
                f"Word count target ({target}) is below recommended minimum ({min_rec}) "
                f"for {self.name} workflow"
            )
        elif target > max_rec:
            issues.append(
                f"Word count target ({target}) exceeds recommended maximum ({max_rec}) "
                f"for {self.name} workflow"
            )
        
        return issues
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert template to dictionary.
        
        Returns:
            Dictionary representation
        """
        return {
            "name": self.name,
            "workflow_type": self.workflow_type.value,
            "description": self.description,
            "academic_config": self.academic_config.to_dict(),
            "search_strategy": self.search_strategy,
            "prompt_additions": self.prompt_additions,
            "required_sections": self.required_sections,
            "recommended_word_count": self.recommended_word_count,
            "quality_criteria": self.quality_criteria,
            "example_questions": self.example_questions,
        }


# ============================================================================
# LITERATURE REVIEW TEMPLATE
# ============================================================================

LITERATURE_REVIEW_TEMPLATE = WorkflowTemplate(
    name="Literature Review",
    workflow_type=WorkflowType.LITERATURE_REVIEW,
    description=(
        "Comprehensive synthesis of existing research on a topic. "
        "Identifies major themes, trends, gaps, and future directions."
    ),
    academic_config=AcademicConfig(
        output_format=OutputFormat.REVIEW,
        word_count_target=6000,
        include_abstract=True,
        include_methodology=False,
        scholar_priority=True,
        min_peer_reviewed=10,
        source_quality_threshold=7,
    ),
    search_strategy=(
        "Conduct comprehensive literature search across multiple time periods. "
        "Prioritize recent publications (last 5 years) but include seminal works. "
        "Search for review articles, meta-analyses, and highly-cited papers first. "
        "Use Scholar tool to identify key authors and citation networks. "
        "Include both theoretical and empirical papers. "
        "Search across related disciplines for interdisciplinary perspectives."
    ),
    prompt_additions={
        "research": (
            "Focus on identifying:\n"
            "- Major research themes and how they evolved over time\n"
            "- Consensus areas where multiple studies agree\n"
            "- Controversial areas with conflicting findings\n"
            "- Methodological approaches used across studies\n"
            "- Theoretical frameworks employed\n"
            "- Research gaps and unanswered questions\n"
            "- Future research directions suggested by authors\n\n"
            "Organize findings thematically rather than paper-by-paper. "
            "Track publication dates to show chronological development. "
            "Note highly-cited papers and influential authors."
        ),
        "synthesis": (
            "Structure the literature review thematically, not chronologically. "
            "Begin each theme with an overview, then discuss key studies. "
            "Compare and contrast different approaches and findings. "
            "Explicitly identify areas of consensus and controversy. "
            "Dedicate a section to research gaps and limitations. "
            "Conclude with future research directions. "
            "Use transition sentences to connect themes. "
            "Maintain critical, analytical tone throughout."
        ),
    },
    required_sections=[
        "Abstract",
        "Introduction",
        "Thematic Analysis",
        "Research Gaps",
        "Future Directions",
        "Conclusion",
        "References"
    ],
    recommended_word_count=(5000, 8000),
    quality_criteria=[
        "Comprehensive coverage of major research streams",
        "Clear thematic organization",
        "Critical analysis of methodologies and findings",
        "Identification of research gaps",
        "Synthesis across multiple sources",
        "Balanced representation of different perspectives",
        "Minimum 10 peer-reviewed sources",
        "Recent publications (majority within 5 years)",
    ],
    example_questions=[
        "What are the current approaches to explainable AI in healthcare?",
        "How has research on remote work productivity evolved since 2020?",
        "What methodologies are used to study social media's impact on mental health?",
        "What are the major theoretical frameworks for understanding organizational change?",
    ],
)


# ============================================================================
# SYSTEMATIC REVIEW TEMPLATE
# ============================================================================

SYSTEMATIC_REVIEW_TEMPLATE = WorkflowTemplate(
    name="Systematic Review",
    workflow_type=WorkflowType.SYSTEMATIC_REVIEW,
    description=(
        "Structured, protocol-driven review following systematic methodology. "
        "Includes explicit search strategy, inclusion/exclusion criteria, "
        "and quality assessment of studies."
    ),
    academic_config=AcademicConfig(
        output_format=OutputFormat.REVIEW,
        word_count_target=8000,
        include_abstract=True,
        include_methodology=True,
        scholar_priority=True,
        min_peer_reviewed=15,
        source_quality_threshold=8,
    ),
    search_strategy=(
        "Follow systematic review protocol:\n"
        "1. Define clear research question using PICO framework (Population, Intervention, Comparison, Outcome)\n"
        "2. Establish explicit inclusion/exclusion criteria\n"
        "3. Search multiple databases (Scholar, PubMed, discipline-specific)\n"
        "4. Use structured search terms with Boolean operators\n"
        "5. Document search process and results\n"
        "6. Screen titles and abstracts against criteria\n"
        "7. Assess quality of included studies\n"
        "8. Extract data systematically\n"
        "Priority: Randomized controlled trials, cohort studies, case-control studies. "
        "Minimum quality threshold: peer-reviewed, adequate methodology, clear outcomes."
    ),
    prompt_additions={
        "research": (
            "Follow systematic review methodology:\n"
            "- Document all search terms and databases used\n"
            "- Apply inclusion/exclusion criteria consistently\n"
            "- Extract key data: study design, sample size, methods, outcomes, limitations\n"
            "- Assess study quality using appropriate framework (e.g., GRADE, Cochrane Risk of Bias)\n"
            "- Note any conflicts of interest or funding sources\n"
            "- Track reasons for excluding studies\n"
            "- Identify potential publication bias\n\n"
            "For each included study, document:\n"
            "- Study design and methodology\n"
            "- Sample characteristics and size\n"
            "- Intervention/exposure details\n"
            "- Outcome measures and results\n"
            "- Statistical analysis methods\n"
            "- Limitations and biases\n"
            "- Quality assessment score"
        ),
        "synthesis": (
            "Follow PRISMA reporting guidelines for systematic reviews:\n"
            "- Include detailed methodology section describing search strategy\n"
            "- Present PRISMA flow diagram showing study selection process\n"
            "- Provide characteristics table for included studies\n"
            "- Present quality assessment results\n"
            "- Synthesize findings systematically (narrative or meta-analysis)\n"
            "- Discuss heterogeneity across studies\n"
            "- Address publication bias and limitations\n"
            "- Provide evidence-based conclusions\n"
            "- Use tables to present study characteristics and outcomes\n"
            "- Maintain objective, evidence-focused tone"
        ),
    },
    required_sections=[
        "Abstract",
        "Introduction",
        "Methodology",
        "Search Strategy",
        "Study Selection",
        "Quality Assessment",
        "Results",
        "Discussion",
        "Limitations",
        "Conclusion",
        "References"
    ],
    recommended_word_count=(7000, 12000),
    quality_criteria=[
        "Explicit research question (PICO format)",
        "Documented search strategy",
        "Clear inclusion/exclusion criteria",
        "Quality assessment of studies",
        "Systematic data extraction",
        "PRISMA compliance",
        "Minimum 15 peer-reviewed studies",
        "Assessment of publication bias",
        "Discussion of heterogeneity",
        "Evidence-based conclusions",
    ],
    example_questions=[
        "What is the effectiveness of cognitive behavioral therapy for treating anxiety disorders?",
        "How do different machine learning algorithms compare for medical image classification?",
        "What interventions are effective for reducing workplace burnout?",
        "What is the impact of early childhood education on long-term academic outcomes?",
    ],
)


# ============================================================================
# METHODOLOGY COMPARISON TEMPLATE
# ============================================================================

METHODOLOGY_COMPARISON_TEMPLATE = WorkflowTemplate(
    name="Methodology Comparison",
    workflow_type=WorkflowType.METHODOLOGY_COMPARISON,
    description=(
        "Comparative analysis of different research methodologies used to study a topic. "
        "Evaluates strengths, limitations, and appropriateness of various approaches."
    ),
    academic_config=AcademicConfig(
        output_format=OutputFormat.PAPER,
        word_count_target=7000,
        include_abstract=True,
        include_methodology=True,
        scholar_priority=True,
        min_peer_reviewed=12,
        source_quality_threshold=7,
    ),
    search_strategy=(
        "Search for papers using diverse methodological approaches to study the same or similar topics. "
        "Include both qualitative and quantitative studies. "
        "Prioritize methodological papers and studies with detailed methods sections. "
        "Search for: experimental studies, surveys, case studies, ethnographies, mixed-methods, "
        "meta-analyses, systematic reviews, computational models, simulations. "
        "Look for papers that explicitly compare methodologies or discuss methodological choices. "
        "Include methodological critiques and debates."
    ),
    prompt_additions={
        "research": (
            "For each methodology encountered, extract:\n"
            "- Methodology type and specific approach\n"
            "- Research questions it addresses well\n"
            "- Data collection methods\n"
            "- Analysis techniques\n"
            "- Sample size and characteristics\n"
            "- Strengths and advantages\n"
            "- Limitations and constraints\n"
            "- Resource requirements (time, cost, expertise)\n"
            "- Validity and reliability considerations\n"
            "- Ethical considerations\n"
            "- Examples of successful applications\n\n"
            "Compare methodologies across dimensions:\n"
            "- Internal vs. external validity\n"
            "- Depth vs. breadth of insights\n"
            "- Generalizability\n"
            "- Feasibility and practicality\n"
            "- Appropriateness for different research questions"
        ),
        "synthesis": (
            "Structure comparison systematically:\n"
            "- Begin with overview of methodological landscape\n"
            "- Describe each methodology in detail with examples\n"
            "- Create comparison tables highlighting key dimensions\n"
            "- Discuss trade-offs between approaches\n"
            "- Provide decision framework for methodology selection\n"
            "- Include case studies showing methodology in practice\n"
            "- Address common methodological challenges\n"
            "- Discuss mixed-methods and triangulation approaches\n"
            "- Provide recommendations based on research context\n"
            "- Use tables and figures to visualize comparisons"
        ),
    },
    required_sections=[
        "Abstract",
        "Introduction",
        "Methodological Overview",
        "Methodology Descriptions",
        "Comparative Analysis",
        "Strengths and Limitations",
        "Selection Framework",
        "Case Studies",
        "Recommendations",
        "Conclusion",
        "References"
    ],
    recommended_word_count=(6000, 9000),
    quality_criteria=[
        "Coverage of multiple methodological approaches",
        "Detailed description of each methodology",
        "Systematic comparison across dimensions",
        "Discussion of trade-offs",
        "Practical selection guidance",
        "Real-world examples and case studies",
        "Balanced assessment of strengths and limitations",
        "Consideration of resource constraints",
        "Minimum 12 peer-reviewed sources",
        "Representation of diverse methodological traditions",
    ],
    example_questions=[
        "How do different methodologies compare for studying user experience in mobile apps?",
        "What are the strengths and limitations of various approaches to measuring organizational culture?",
        "How do qualitative and quantitative methods differ in studying climate change adaptation?",
        "What methodologies are most appropriate for evaluating educational interventions?",
    ],
)


# ============================================================================
# THEORETICAL ANALYSIS TEMPLATE
# ============================================================================

THEORETICAL_ANALYSIS_TEMPLATE = WorkflowTemplate(
    name="Theoretical Analysis",
    workflow_type=WorkflowType.THEORETICAL_ANALYSIS,
    description=(
        "Deep analysis of theoretical frameworks, models, and conceptual approaches. "
        "Examines theoretical foundations, development, applications, and critiques."
    ),
    academic_config=AcademicConfig(
        output_format=OutputFormat.PAPER,
        word_count_target=8000,
        include_abstract=True,
        include_methodology=False,
        scholar_priority=True,
        min_peer_reviewed=15,
        source_quality_threshold=8,
    ),
    search_strategy=(
        "Search for theoretical and conceptual papers, not just empirical studies. "
        "Prioritize: original theoretical papers, theoretical reviews, conceptual frameworks, "
        "theoretical critiques, philosophical analyses, model development papers. "
        "Include seminal works that introduced theories (even if older). "
        "Search for papers that apply, test, extend, or critique the theories. "
        "Look for theoretical debates and competing frameworks. "
        "Include interdisciplinary theoretical perspectives. "
        "Search for meta-theoretical discussions and paradigm analyses."
    ),
    prompt_additions={
        "research": (
            "For each theoretical framework, extract:\n"
            "- Core concepts and constructs\n"
            "- Key propositions and relationships\n"
            "- Theoretical assumptions and foundations\n"
            "- Historical development and origins\n"
            "- Intellectual genealogy and influences\n"
            "- Scope and boundary conditions\n"
            "- Operationalization in empirical research\n"
            "- Empirical support and evidence\n"
            "- Theoretical critiques and limitations\n"
            "- Extensions and refinements\n"
            "- Competing or alternative theories\n"
            "- Practical applications and implications\n\n"
            "Analyze theoretical relationships:\n"
            "- How theories relate to each other\n"
            "- Areas of convergence and divergence\n"
            "- Complementary vs. competing perspectives\n"
            "- Integration possibilities\n"
            "- Paradigmatic differences"
        ),
        "synthesis": (
            "Structure theoretical analysis comprehensively:\n"
            "- Begin with theoretical landscape overview\n"
            "- Present each theory's core elements systematically\n"
            "- Trace historical development and evolution\n"
            "- Analyze theoretical assumptions and logic\n"
            "- Discuss empirical applications and tests\n"
            "- Present theoretical critiques and debates\n"
            "- Compare and contrast different frameworks\n"
            "- Identify theoretical gaps and opportunities\n"
            "- Discuss implications for research and practice\n"
            "- Propose theoretical integration or synthesis where appropriate\n"
            "- Use conceptual diagrams to illustrate relationships\n"
            "- Maintain philosophical and analytical depth\n"
            "- Engage with theoretical debates substantively"
        ),
    },
    required_sections=[
        "Abstract",
        "Introduction",
        "Theoretical Background",
        "Core Theoretical Frameworks",
        "Theoretical Development",
        "Empirical Applications",
        "Theoretical Critiques",
        "Comparative Analysis",
        "Theoretical Integration",
        "Implications",
        "Future Directions",
        "Conclusion",
        "References"
    ],
    recommended_word_count=(7000, 10000),
    quality_criteria=[
        "Deep engagement with theoretical literature",
        "Clear explication of theoretical concepts",
        "Historical and intellectual context",
        "Analysis of theoretical assumptions",
        "Discussion of empirical support",
        "Engagement with theoretical debates",
        "Comparison of competing frameworks",
        "Philosophical and conceptual depth",
        "Minimum 15 peer-reviewed sources",
        "Balance of classic and contemporary works",
        "Interdisciplinary theoretical perspectives",
    ],
    example_questions=[
        "What are the major theoretical frameworks for understanding human motivation?",
        "How have theories of organizational learning evolved and what are their core differences?",
        "What theoretical approaches exist for explaining technology adoption and diffusion?",
        "How do different theories conceptualize the relationship between structure and agency?",
    ],
)


# ============================================================================
# TEMPLATE REGISTRY AND UTILITIES
# ============================================================================

_WORKFLOW_REGISTRY: Dict[WorkflowType, WorkflowTemplate] = {
    WorkflowType.LITERATURE_REVIEW: LITERATURE_REVIEW_TEMPLATE,
    WorkflowType.SYSTEMATIC_REVIEW: SYSTEMATIC_REVIEW_TEMPLATE,
    WorkflowType.METHODOLOGY_COMPARISON: METHODOLOGY_COMPARISON_TEMPLATE,
    WorkflowType.THEORETICAL_ANALYSIS: THEORETICAL_ANALYSIS_TEMPLATE,
}


def get_workflow_template(workflow_type: WorkflowType) -> WorkflowTemplate:
    """
    Get a workflow template by type.
    
    Args:
        workflow_type: Type of workflow
    
    Returns:
        WorkflowTemplate instance
    
    Raises:
        KeyError: If workflow type not found
    """
    if workflow_type not in _WORKFLOW_REGISTRY:
        raise KeyError(f"Unknown workflow type: {workflow_type}")
    
    return _WORKFLOW_REGISTRY[workflow_type]


def list_available_workflows() -> List[Dict[str, str]]:
    """
    List all available workflow templates.
    
    Returns:
        List of dictionaries with workflow information
    """
    workflows = []
    for workflow_type, template in _WORKFLOW_REGISTRY.items():
        workflows.append({
            "type": workflow_type.value,
            "name": template.name,
            "description": template.description,
            "word_count_range": f"{template.recommended_word_count[0]}-{template.recommended_word_count[1]}",
            "min_sources": str(template.academic_config.min_peer_reviewed),
        })
    return workflows


def get_workflow_by_name(name: str) -> Optional[WorkflowTemplate]:
    """
    Get a workflow template by name (case-insensitive).
    
    Args:
        name: Workflow name
    
    Returns:
        WorkflowTemplate instance or None if not found
    """
    name_lower = name.lower().replace(" ", "_").replace("-", "_")
    
    for workflow_type, template in _WORKFLOW_REGISTRY.items():
        if workflow_type.value == name_lower or template.name.lower() == name.lower():
            return template
    
    return None


def create_custom_workflow(
    name: str,
    description: str,
    base_template: Optional[WorkflowType] = None,
    **config_overrides
) -> WorkflowTemplate:
    """
    Create a custom workflow based on a template with overrides.
    
    Args:
        name: Custom workflow name
        description: Custom workflow description
        base_template: Base template to start from (optional)
        **config_overrides: Configuration overrides
    
    Returns:
        Custom WorkflowTemplate instance
    """
    # Start with base template or default
    if base_template:
        base = get_workflow_template(base_template)
        config = AcademicConfig(**{**base.academic_config.to_dict(), **config_overrides})
        
        return WorkflowTemplate(
            name=name,
            workflow_type=base.workflow_type,
            description=description,
            academic_config=config,
            search_strategy=base.search_strategy,
            prompt_additions=base.prompt_additions.copy(),
            required_sections=base.required_sections.copy(),
            recommended_word_count=base.recommended_word_count,
            quality_criteria=base.quality_criteria.copy(),
            example_questions=[],
        )
    else:
        # Create from scratch
        config = AcademicConfig(**config_overrides)
        
        return WorkflowTemplate(
            name=name,
            workflow_type=WorkflowType.LITERATURE_REVIEW,  # Default
            description=description,
            academic_config=config,
            search_strategy="Conduct comprehensive academic research.",
            prompt_additions={},
            required_sections=config.get_report_structure(),
            recommended_word_count=(5000, 10000),
            quality_criteria=[],
            example_questions=[],
        )
