#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Academic Configuration Module for Gazzali Research

This module provides configuration management for academic research features,
including citation styles, output formats, discipline-specific settings,
and report structure generation.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, List, Dict, Any

# Import config helpers for consistent environment variable parsing
from . import config


class CitationStyle(str, Enum):
    """Supported academic citation styles"""
    APA = "apa"
    MLA = "mla"
    CHICAGO = "chicago"
    IEEE = "ieee"


class OutputFormat(str, Enum):
    """Supported output document formats"""
    PAPER = "paper"
    REVIEW = "review"
    PROPOSAL = "proposal"
    ABSTRACT = "abstract"
    PRESENTATION = "presentation"


class Discipline(str, Enum):
    """Academic disciplines with specific conventions"""
    GENERAL = "general"
    STEM = "stem"
    SOCIAL = "social"
    HUMANITIES = "humanities"
    MEDICAL = "medical"


@dataclass
class AcademicConfig:
    """
    Configuration for academic research features.
    
    Attributes:
        citation_style: Citation format (APA, MLA, Chicago, IEEE)
        output_format: Document format (paper, review, proposal, abstract, presentation)
        discipline: Academic discipline for terminology and conventions
        word_count_target: Target word count for generated reports
        include_abstract: Whether to include an abstract section
        include_methodology: Whether to include a methodology section
        scholar_priority: Prioritize Scholar tool over general search
        export_bibliography: Export bibliography to separate file
        min_peer_reviewed: Minimum number of peer-reviewed sources
        source_quality_threshold: Minimum quality score for sources (0-10)
    """
    
    citation_style: CitationStyle = CitationStyle.APA
    output_format: OutputFormat = OutputFormat.PAPER
    discipline: Discipline = Discipline.GENERAL
    word_count_target: int = 8000
    include_abstract: bool = True
    include_methodology: bool = True
    scholar_priority: bool = True
    export_bibliography: bool = False
    min_peer_reviewed: int = 5
    source_quality_threshold: int = 7
    
    @classmethod
    def from_env(cls) -> 'AcademicConfig':
        """
        Load configuration from environment variables.
        
        Uses helper functions from config module for consistent parsing.
        
        Environment variables:
            CITATION_STYLE: Citation format (apa, mla, chicago, ieee)
            OUTPUT_FORMAT: Output format (paper, review, proposal, abstract, presentation)
            DISCIPLINE: Academic discipline (general, stem, social, humanities, medical)
            WORD_COUNT_TARGET: Target word count (integer)
            INCLUDE_ABSTRACT: Include abstract (true/false)
            INCLUDE_METHODOLOGY: Include methodology (true/false)
            SCHOLAR_PRIORITY: Prioritize Scholar tool (true/false)
            EXPORT_BIBLIOGRAPHY: Export bibliography file (true/false)
            MIN_PEER_REVIEWED_SOURCES: Minimum peer-reviewed sources (integer)
            SOURCE_QUALITY_THRESHOLD: Quality threshold 0-10 (integer)
        
        Returns:
            AcademicConfig instance with values from environment or defaults
        """
        def get_enum(key: str, enum_class, default):
            """Parse enum from environment variable"""
            value = os.getenv(key, "").lower()
            try:
                return enum_class(value)
            except ValueError:
                return default
        
        return cls(
            citation_style=get_enum("CITATION_STYLE", CitationStyle, CitationStyle.APA),
            output_format=get_enum("OUTPUT_FORMAT", OutputFormat, OutputFormat.PAPER),
            discipline=get_enum("DISCIPLINE", Discipline, Discipline.GENERAL),
            word_count_target=config.get_word_count_target(),
            include_abstract=config.get_include_abstract(),
            include_methodology=config.get_include_methodology(),
            scholar_priority=config.get_scholar_priority(),
            export_bibliography=config.get_export_bibliography(),
            min_peer_reviewed=config.get_min_peer_reviewed_sources(),
            source_quality_threshold=config.get_source_quality_threshold(),
        )
    
    @classmethod
    def from_args(cls, args) -> 'AcademicConfig':
        """
        Load configuration from command-line arguments.
        
        Args:
            args: argparse.Namespace or object with attributes:
                - citation_style: str (optional)
                - output_format: str (optional)
                - discipline: str (optional)
                - word_count: int (optional)
                - export_bib: bool (optional)
        
        Returns:
            AcademicConfig instance with values from args or defaults
        """
        # Start with defaults
        config = cls()
        
        # Override with provided arguments
        if hasattr(args, 'citation_style') and args.citation_style:
            try:
                config.citation_style = CitationStyle(args.citation_style.lower())
            except ValueError:
                pass
        
        if hasattr(args, 'output_format') and args.output_format:
            try:
                config.output_format = OutputFormat(args.output_format.lower())
            except ValueError:
                pass
        
        if hasattr(args, 'discipline') and args.discipline:
            try:
                config.discipline = Discipline(args.discipline.lower())
            except ValueError:
                pass
        
        if hasattr(args, 'word_count') and args.word_count:
            config.word_count_target = args.word_count
        
        if hasattr(args, 'export_bib'):
            config.export_bibliography = args.export_bib
        
        return config

    
    def get_prompt_modifiers(self) -> Dict[str, str]:
        """
        Generate prompt modifiers based on discipline and output format.
        
        Returns:
            Dictionary with keys: terminology, methodology_focus, structure, depth,
            source_priorities, analysis_approach, writing_conventions
        """
        modifiers = {
            "terminology": "",
            "methodology_focus": "",
            "structure": "",
            "depth": "",
            "source_priorities": "",
            "analysis_approach": "",
            "writing_conventions": ""
        }
        
        # Discipline-specific modifiers
        if self.discipline == Discipline.STEM:
            modifiers["terminology"] = (
                "Use technical and scientific terminology appropriate for STEM fields. "
                "Include mathematical notation, chemical formulas, equations, and technical specifications where relevant. "
                "Use SI units and standard scientific nomenclature. "
                "Define specialized terms on first use."
            )
            modifiers["methodology_focus"] = (
                "Focus on experimental design, quantitative methods, statistical analysis, "
                "reproducibility, and empirical validation. Emphasize data-driven approaches, "
                "hypothesis testing, control groups, and statistical significance. "
                "Document experimental procedures, equipment, measurement precision, and error analysis. "
                "Prioritize replicability and falsifiability of findings."
            )
            modifiers["source_priorities"] = (
                "Prioritize peer-reviewed journals in relevant STEM fields (e.g., Nature, Science, IEEE, ACM). "
                "Value experimental studies, systematic reviews, and meta-analyses. "
                "Include preprints from arXiv, bioRxiv when discussing cutting-edge research. "
                "Consider technical reports from research institutions and standards organizations."
            )
            modifiers["analysis_approach"] = (
                "Emphasize quantitative analysis, statistical rigor, and empirical evidence. "
                "Evaluate effect sizes, confidence intervals, and statistical power. "
                "Assess reproducibility and replication studies. "
                "Consider computational complexity, scalability, and performance metrics. "
                "Analyze data quality, measurement validity, and experimental controls."
            )
            modifiers["writing_conventions"] = (
                "Use passive voice when describing methods ('The solution was heated to 100°C'). "
                "Present results objectively with precise numerical data. "
                "Use figures, tables, and equations to present complex information. "
                "Follow discipline-specific formatting (e.g., chemical notation, mathematical proofs). "
                "Include detailed methodology sufficient for replication."
            )
        
        elif self.discipline == Discipline.SOCIAL:
            modifiers["terminology"] = (
                "Use social science terminology including theoretical frameworks, "
                "constructs, and discipline-specific concepts from psychology, sociology, "
                "economics, anthropology, or political science. "
                "Define key constructs operationally. "
                "Use appropriate statistical and methodological terminology (e.g., validity, reliability, generalizability)."
            )
            modifiers["methodology_focus"] = (
                "Focus on qualitative and quantitative social research methods including "
                "surveys, interviews, focus groups, ethnography, participant observation, "
                "statistical modeling, and mixed-methods approaches. "
                "Emphasize internal validity, external validity, construct validity, and reliability. "
                "Consider sampling strategies, response rates, and representativeness. "
                "Address ethical considerations for human subjects research including informed consent and confidentiality."
            )
            modifiers["source_priorities"] = (
                "Prioritize peer-reviewed social science journals (e.g., American Sociological Review, "
                "Psychological Science, American Economic Review). "
                "Value longitudinal studies, randomized controlled trials, and large-scale surveys. "
                "Include working papers from research institutions and policy organizations. "
                "Consider government statistics and demographic data sources."
            )
            modifiers["analysis_approach"] = (
                "Emphasize both quantitative and qualitative analysis as appropriate. "
                "Evaluate theoretical frameworks and their empirical support. "
                "Consider cultural context, social dynamics, and human behavior complexity. "
                "Assess generalizability across populations and settings. "
                "Analyze potential confounds, mediators, and moderators. "
                "Consider practical significance alongside statistical significance."
            )
            modifiers["writing_conventions"] = (
                "Balance theoretical discussion with empirical evidence. "
                "Integrate participant quotes in qualitative research. "
                "Present demographic characteristics of samples. "
                "Discuss implications for policy, practice, and social understanding. "
                "Address limitations related to sampling, measurement, and generalizability. "
                "Consider ethical implications and social justice perspectives."
            )
        
        elif self.discipline == Discipline.HUMANITIES:
            modifiers["terminology"] = (
                "Use humanities terminology including critical theory, hermeneutics, "
                "textual analysis, discourse analysis, and philosophical concepts. "
                "Emphasize interpretive frameworks, rhetorical analysis, and cultural criticism. "
                "Use discipline-specific terms from literary theory, philosophy, history, or cultural studies. "
                "Define theoretical concepts and their intellectual genealogy."
            )
            modifiers["methodology_focus"] = (
                "Focus on textual analysis, close reading, historical methods, archival research, "
                "critical interpretation, comparative analysis, and theoretical frameworks. "
                "Emphasize contextual understanding, historical situatedness, and interpretive depth. "
                "Consider primary sources, archival materials, and original texts. "
                "Engage with scholarly debates and multiple interpretive perspectives. "
                "Analyze rhetoric, narrative structure, symbolism, and meaning-making."
            )
            modifiers["source_priorities"] = (
                "Prioritize peer-reviewed humanities journals and university press publications. "
                "Value primary sources, original texts, and archival materials. "
                "Include scholarly monographs and edited collections. "
                "Consider historical documents, literary works, and cultural artifacts. "
                "Engage with canonical works and contemporary scholarship."
            )
            modifiers["analysis_approach"] = (
                "Emphasize interpretive analysis, critical reading, and theoretical engagement. "
                "Consider multiple interpretive frameworks and scholarly perspectives. "
                "Analyze historical context, cultural significance, and philosophical implications. "
                "Evaluate arguments for logical coherence and textual support. "
                "Engage with theoretical debates and intellectual traditions. "
                "Consider aesthetic, ethical, and political dimensions of texts and artifacts."
            )
            modifiers["writing_conventions"] = (
                "Develop sustained arguments with careful textual evidence. "
                "Integrate quotations smoothly with analysis. "
                "Engage with scholarly conversations and theoretical debates. "
                "Use sophisticated vocabulary and complex sentence structures appropriately. "
                "Balance close reading with broader theoretical claims. "
                "Consider multiple interpretive possibilities and their implications."
            )
        
        elif self.discipline == Discipline.MEDICAL:
            modifiers["terminology"] = (
                "Use medical and clinical terminology including anatomical terms, "
                "diagnostic criteria, treatment protocols, pharmacological nomenclature, "
                "and evidence-based medicine concepts. "
                "Use standard medical abbreviations appropriately (define on first use). "
                "Include ICD codes, drug names (generic and brand), and clinical classifications. "
                "Use precise medical language for conditions, procedures, and outcomes."
            )
            modifiers["methodology_focus"] = (
                "Focus on clinical trials (RCTs), systematic reviews, meta-analyses, cohort studies, "
                "case-control studies, and case reports following evidence hierarchy. "
                "Emphasize evidence-based practice, patient outcomes, safety, efficacy, "
                "and clinical significance. "
                "Document inclusion/exclusion criteria, intervention protocols, and outcome measures. "
                "Address ethical considerations including informed consent, patient safety, and IRB approval. "
                "Consider number needed to treat (NNT), relative risk, and odds ratios."
            )
            modifiers["source_priorities"] = (
                "Prioritize high-impact medical journals (e.g., NEJM, Lancet, JAMA, BMJ). "
                "Value systematic reviews and meta-analyses from Cochrane Library. "
                "Include clinical practice guidelines from professional organizations. "
                "Consider FDA/EMA reports and drug safety databases. "
                "Reference clinical trial registries (ClinicalTrials.gov) for ongoing research."
            )
            modifiers["analysis_approach"] = (
                "Emphasize clinical significance alongside statistical significance. "
                "Evaluate evidence quality using GRADE or similar frameworks. "
                "Assess patient-centered outcomes (mortality, morbidity, quality of life). "
                "Consider adverse effects, contraindications, and safety profiles. "
                "Analyze cost-effectiveness and healthcare resource implications. "
                "Evaluate applicability to different patient populations and clinical settings. "
                "Consider comorbidities, drug interactions, and individual patient factors."
            )
            modifiers["writing_conventions"] = (
                "Follow CONSORT, PRISMA, or other reporting guidelines as appropriate. "
                "Present patient characteristics and baseline data clearly. "
                "Report outcomes with confidence intervals and p-values. "
                "Discuss clinical implications and practice recommendations. "
                "Address limitations including sample size, follow-up duration, and generalizability. "
                "Consider patient safety, ethical considerations, and informed decision-making. "
                "Use tables for presenting clinical data and treatment comparisons."
            )
        
        else:  # GENERAL
            modifiers["terminology"] = (
                "Use clear, accessible academic language appropriate for interdisciplinary audiences. "
                "Define specialized terms from any discipline on first use. "
                "Balance technical precision with readability."
            )
            modifiers["methodology_focus"] = (
                "Focus on research methods appropriate to the topic, including both "
                "qualitative and quantitative approaches as relevant. "
                "Adapt methodology discussion to the specific research domain. "
                "Emphasize rigor and appropriateness of methods for research questions."
            )
            modifiers["source_priorities"] = (
                "Prioritize peer-reviewed academic sources across disciplines. "
                "Value high-quality research regardless of specific field. "
                "Include interdisciplinary perspectives when relevant."
            )
            modifiers["analysis_approach"] = (
                "Adapt analytical approach to the research topic and available evidence. "
                "Consider multiple disciplinary perspectives. "
                "Emphasize critical thinking and evidence-based reasoning."
            )
            modifiers["writing_conventions"] = (
                "Follow general academic writing conventions. "
                "Maintain formal, objective tone. "
                "Structure arguments clearly with appropriate evidence. "
                "Make content accessible to readers from various academic backgrounds."
            )
        
        # Output format-specific modifiers
        if self.output_format == OutputFormat.PAPER:
            modifiers["structure"] = (
                "Structure as a full research paper with: Abstract, Introduction, "
                "Literature Review, Methodology, Findings, Discussion, Conclusion, and References."
            )
            modifiers["depth"] = (
                "Provide comprehensive, in-depth analysis with detailed evidence, "
                "extensive citations, and thorough discussion of implications and limitations."
            )
        
        elif self.output_format == OutputFormat.REVIEW:
            modifiers["structure"] = (
                "Structure as a Literature review with: Abstract, Introduction, "
                "Thematic Analysis (organized by themes or chronologically), "
                "Research Gaps, Future Directions, and References."
            )
            modifiers["depth"] = (
                "Provide systematic synthesis of existing literature, identifying patterns, "
                "contradictions, and gaps. Focus on comprehensive coverage of the field."
            )
        
        elif self.output_format == OutputFormat.PROPOSAL:
            modifiers["structure"] = (
                "Structure as a research proposal with: Background, Research Questions, "
                "Literature Review, Proposed Methodology, Expected Outcomes, Timeline, "
                "and References."
            )
            modifiers["depth"] = (
                "Provide forward-looking analysis justifying the proposed research. "
                "Emphasize feasibility, significance, and potential contributions."
            )
        
        elif self.output_format == OutputFormat.ABSTRACT:
            modifiers["structure"] = (
                "Structure as a conference abstract (250-300 words) with: "
                "Background, Methods, Results, and Conclusions in a single paragraph or short sections."
            )
            modifiers["depth"] = (
                "Provide concise summary of key findings and significance. "
                "Focus on the most important results and implications only."
            )
        
        elif self.output_format == OutputFormat.PRESENTATION:
            modifiers["structure"] = (
                "Structure for presentation with: Key Points, Main Findings, "
                "Visual Summaries, and Takeaways. Use bullet points and clear headings."
            )
            modifiers["depth"] = (
                "Provide clear, accessible summary suitable for oral presentation. "
                "Focus on main ideas and practical implications."
            )
        
        return modifiers
    
    def get_discipline_prompt_text(self) -> str:
        """
        Get formatted discipline-specific prompt text for integration into research prompts.
        
        Returns:
            Formatted string with all discipline-specific guidelines
        """
        modifiers = self.get_prompt_modifiers()
        
        if self.discipline == Discipline.GENERAL:
            return ""  # No specific modifiers for general discipline
        
        discipline_name = self.discipline.value.upper()
        
        prompt_text = f"\n## {discipline_name} Discipline Guidelines\n\n"
        
        if modifiers["terminology"]:
            prompt_text += f"**Terminology**: {modifiers['terminology']}\n\n"
        
        if modifiers["methodology_focus"]:
            prompt_text += f"**Methodology Focus**: {modifiers['methodology_focus']}\n\n"
        
        if modifiers["source_priorities"]:
            prompt_text += f"**Source Priorities**: {modifiers['source_priorities']}\n\n"
        
        if modifiers["analysis_approach"]:
            prompt_text += f"**Analysis Approach**: {modifiers['analysis_approach']}\n\n"
        
        if modifiers["writing_conventions"]:
            prompt_text += f"**Writing Conventions**: {modifiers['writing_conventions']}\n\n"
        
        return prompt_text
    
    def get_report_structure(self) -> List[str]:
        """
        Get the required sections for the specified output format.
        
        Returns:
            List of section names in order
        """
        if self.output_format == OutputFormat.PAPER:
            sections = []
            if self.include_abstract:
                sections.append("Abstract")
            sections.extend([
                "Introduction",
                "Literature Review"
            ])
            if self.include_methodology:
                sections.append("Methodology")
            sections.extend([
                "Findings",
                "Discussion",
                "Conclusion",
                "References"
            ])
            return sections
        
        elif self.output_format == OutputFormat.REVIEW:
            sections = []
            if self.include_abstract:
                sections.append("Abstract")
            sections.extend([
                "Introduction",
                "Thematic Analysis",
                "Research Gaps",
                "Future Directions",
                "References"
            ])
            return sections
        
        elif self.output_format == OutputFormat.PROPOSAL:
            sections = [
                "Background",
                "Research Questions",
                "Literature Review",
                "Proposed Methodology",
                "Expected Outcomes",
                "Timeline",
                "References"
            ]
            return sections
        
        elif self.output_format == OutputFormat.ABSTRACT:
            return ["Abstract"]
        
        elif self.output_format == OutputFormat.PRESENTATION:
            return [
                "Overview",
                "Key Findings",
                "Implications",
                "Conclusions"
            ]
        
        return ["Introduction", "Body", "Conclusion", "References"]
    
    def validate(self) -> List[str]:
        """
        Validate configuration values and return list of issues.
        
        Returns:
            List of validation issue messages (empty if valid)
        """
        issues = []
        
        # Validate word count
        if self.word_count_target < 500:
            issues.append(
                f"Word count target ({self.word_count_target}) is very low. "
                "Consider at least 500 words for meaningful academic content."
            )
        elif self.word_count_target > 50000:
            issues.append(
                f"Word count target ({self.word_count_target}) is very high. "
                "Consider breaking into multiple documents or reducing scope."
            )
        
        # Validate abstract format word count
        if self.output_format == OutputFormat.ABSTRACT and self.word_count_target > 500:
            issues.append(
                f"Abstract format typically requires 250-500 words, but target is {self.word_count_target}. "
                "Consider reducing word count target."
            )
        
        # Validate minimum peer-reviewed sources
        if self.min_peer_reviewed < 0:
            issues.append(
                f"Minimum peer-reviewed sources cannot be negative ({self.min_peer_reviewed})."
            )
        
        # Validate quality threshold
        if self.source_quality_threshold < 0 or self.source_quality_threshold > 10:
            issues.append(
                f"Source quality threshold must be between 0 and 10 (got {self.source_quality_threshold})."
            )
        
        return issues
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert configuration to dictionary.
        
        Returns:
            Dictionary representation of configuration
        """
        return {
            "citation_style": self.citation_style.value,
            "output_format": self.output_format.value,
            "discipline": self.discipline.value,
            "word_count_target": self.word_count_target,
            "include_abstract": self.include_abstract,
            "include_methodology": self.include_methodology,
            "scholar_priority": self.scholar_priority,
            "export_bibliography": self.export_bibliography,
            "min_peer_reviewed": self.min_peer_reviewed,
            "source_quality_threshold": self.source_quality_threshold,
        }
    
    def __str__(self) -> str:
        """String representation of configuration"""
        return (
            f"AcademicConfig(\n"
            f"  Citation Style: {self.citation_style.value}\n"
            f"  Output Format: {self.output_format.value}\n"
            f"  Discipline: {self.discipline.value}\n"
            f"  Word Count Target: {self.word_count_target}\n"
            f"  Scholar Priority: {self.scholar_priority}\n"
            f"  Export Bibliography: {self.export_bibliography}\n"
            f")"
        )


def get_default_config() -> AcademicConfig:
    """
    Get default academic configuration.
    
    Returns:
        AcademicConfig with default values
    """
    return AcademicConfig()
