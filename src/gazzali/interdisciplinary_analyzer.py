#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Interdisciplinary Research Analyzer for Gazzali Research

This module provides functionality for analyzing research across multiple academic
disciplines, identifying disciplinary perspectives, highlighting convergence and
divergence, and translating discipline-specific terminology.

Supports Requirements 8.1, 8.2, 8.3, 8.4, 8.5 for interdisciplinary research.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Dict, Set, Optional, Tuple
from enum import Enum
import re


class AcademicDiscipline(str, Enum):
    """Major academic disciplines for interdisciplinary analysis"""
    PSYCHOLOGY = "psychology"
    SOCIOLOGY = "sociology"
    ECONOMICS = "economics"
    COMPUTER_SCIENCE = "computer_science"
    BIOLOGY = "biology"
    PHYSICS = "physics"
    CHEMISTRY = "chemistry"
    MEDICINE = "medicine"
    EDUCATION = "education"
    POLITICAL_SCIENCE = "political_science"
    ANTHROPOLOGY = "anthropology"
    PHILOSOPHY = "philosophy"
    HISTORY = "history"
    LITERATURE = "literature"
    LINGUISTICS = "linguistics"
    ENGINEERING = "engineering"
    MATHEMATICS = "mathematics"
    ENVIRONMENTAL_SCIENCE = "environmental_science"
    NEUROSCIENCE = "neuroscience"
    PUBLIC_HEALTH = "public_health"


@dataclass
class DisciplinaryPerspective:
    """
    Represents a disciplinary perspective on a research topic.
    
    Attributes:
        discipline: The academic discipline
        key_concepts: Main concepts used in this discipline
        theoretical_frameworks: Theories applied from this discipline
        methodologies: Research methods typical of this discipline
        terminology: Discipline-specific terms and their definitions
        key_findings: Main findings from this disciplinary perspective
        sources: List of source citations from this discipline
    """
    discipline: AcademicDiscipline
    key_concepts: List[str] = field(default_factory=list)
    theoretical_frameworks: List[str] = field(default_factory=list)
    methodologies: List[str] = field(default_factory=list)
    terminology: Dict[str, str] = field(default_factory=dict)  # term -> definition
    key_findings: List[str] = field(default_factory=list)
    sources: List[str] = field(default_factory=list)
    
    def add_concept(self, concept: str) -> None:
        """Add a key concept if not already present"""
        if concept and concept not in self.key_concepts:
            self.key_concepts.append(concept)
    
    def add_framework(self, framework: str) -> None:
        """Add a theoretical framework if not already present"""
        if framework and framework not in self.theoretical_frameworks:
            self.theoretical_frameworks.append(framework)
    
    def add_methodology(self, methodology: str) -> None:
        """Add a methodology if not already present"""
        if methodology and methodology not in self.methodologies:
            self.methodologies.append(methodology)
    
    def add_terminology(self, term: str, definition: str) -> None:
        """Add or update a term definition"""
        if term and definition:
            self.terminology[term] = definition
    
    def add_finding(self, finding: str) -> None:
        """Add a key finding if not already present"""
        if finding and finding not in self.key_findings:
            self.key_findings.append(finding)
    
    def add_source(self, source: str) -> None:
        """Add a source citation if not already present"""
        if source and source not in self.sources:
            self.sources.append(source)


@dataclass
class InterdisciplinaryInsight:
    """
    Represents insights from interdisciplinary analysis.
    
    Attributes:
        convergence_areas: Topics where disciplines agree
        divergence_areas: Topics where disciplines disagree
        complementary_insights: How disciplines complement each other
        integrated_understanding: Synthesized cross-disciplinary understanding
        translation_map: Mapping of equivalent terms across disciplines
    """
    convergence_areas: List[str] = field(default_factory=list)
    divergence_areas: List[str] = field(default_factory=list)
    complementary_insights: List[str] = field(default_factory=list)
    integrated_understanding: str = ""
    translation_map: Dict[str, Dict[str, str]] = field(default_factory=dict)  # concept -> {discipline -> term}


class InterdisciplinaryAnalyzer:
    """
    Analyzer for interdisciplinary research that identifies disciplinary perspectives,
    highlights convergence and divergence, and translates terminology.
    """
    
    # Discipline indicators - keywords that suggest a particular discipline
    DISCIPLINE_INDICATORS = {
        AcademicDiscipline.PSYCHOLOGY: [
            "cognitive", "behavioral", "psychological", "mental", "emotion", "perception",
            "personality", "motivation", "learning", "memory", "attention", "consciousness",
            "psychotherapy", "clinical psychology", "developmental psychology"
        ],
        AcademicDiscipline.SOCIOLOGY: [
            "social", "society", "cultural", "community", "inequality", "stratification",
            "socialization", "institutions", "norms", "values", "social structure",
            "social change", "social movements", "social capital"
        ],
        AcademicDiscipline.ECONOMICS: [
            "economic", "market", "price", "demand", "supply", "utility", "cost",
            "efficiency", "trade", "investment", "monetary", "fiscal", "macroeconomic",
            "microeconomic", "elasticity", "equilibrium"
        ],
        AcademicDiscipline.COMPUTER_SCIENCE: [
            "algorithm", "computational", "software", "hardware", "programming",
            "data structure", "machine learning", "artificial intelligence", "network",
            "database", "cybersecurity", "computer vision", "natural language processing"
        ],
        AcademicDiscipline.BIOLOGY: [
            "biological", "organism", "cell", "gene", "evolution", "ecology",
            "molecular", "genetic", "species", "population", "ecosystem", "biodiversity",
            "physiology", "anatomy", "metabolism"
        ],
        AcademicDiscipline.PHYSICS: [
            "physical", "force", "energy", "matter", "quantum", "particle",
            "wave", "thermodynamics", "mechanics", "electromagnetic", "relativity",
            "atomic", "nuclear", "optics"
        ],
        AcademicDiscipline.CHEMISTRY: [
            "chemical", "molecule", "compound", "reaction", "element", "bond",
            "synthesis", "catalyst", "organic", "inorganic", "analytical", "biochemical",
            "stoichiometry", "equilibrium"
        ],
        AcademicDiscipline.MEDICINE: [
            "medical", "clinical", "patient", "disease", "treatment", "diagnosis",
            "therapy", "pharmaceutical", "surgical", "pathology", "epidemiology",
            "healthcare", "symptom", "prognosis"
        ],
        AcademicDiscipline.EDUCATION: [
            "educational", "pedagogy", "curriculum", "teaching", "learning",
            "instruction", "assessment", "classroom", "student", "teacher",
            "educational psychology", "educational technology"
        ],
        AcademicDiscipline.POLITICAL_SCIENCE: [
            "political", "government", "policy", "democracy", "power", "governance",
            "legislation", "electoral", "public administration", "international relations",
            "political theory", "comparative politics"
        ],
        AcademicDiscipline.ANTHROPOLOGY: [
            "anthropological", "ethnographic", "cultural anthropology", "archaeology",
            "human evolution", "kinship", "ritual", "symbolic", "cross-cultural",
            "indigenous", "ethnography"
        ],
        AcademicDiscipline.PHILOSOPHY: [
            "philosophical", "epistemology", "ontology", "ethics", "metaphysics",
            "logic", "phenomenology", "existential", "normative", "analytical philosophy",
            "continental philosophy"
        ],
        AcademicDiscipline.NEUROSCIENCE: [
            "neural", "brain", "neuron", "synaptic", "neurological", "cognitive neuroscience",
            "neuroimaging", "neurotransmitter", "cortex", "neuroplasticity"
        ],
        AcademicDiscipline.PUBLIC_HEALTH: [
            "public health", "epidemiological", "health promotion", "disease prevention",
            "health policy", "population health", "health disparities", "health systems"
        ]
    }
    
    # Common terminology translations across disciplines
    TERMINOLOGY_TRANSLATIONS = {
        "behavior": {
            AcademicDiscipline.PSYCHOLOGY: "observable actions and responses",
            AcademicDiscipline.SOCIOLOGY: "social actions and interactions",
            AcademicDiscipline.ECONOMICS: "economic decision-making and choices",
            AcademicDiscipline.BIOLOGY: "organism responses to stimuli"
        },
        "system": {
            AcademicDiscipline.COMPUTER_SCIENCE: "integrated software/hardware components",
            AcademicDiscipline.BIOLOGY: "interconnected biological components",
            AcademicDiscipline.SOCIOLOGY: "social structures and institutions",
            AcademicDiscipline.ENGINEERING: "engineered components working together"
        },
        "network": {
            AcademicDiscipline.COMPUTER_SCIENCE: "connected computing nodes",
            AcademicDiscipline.SOCIOLOGY: "social connections and relationships",
            AcademicDiscipline.NEUROSCIENCE: "interconnected neurons",
            AcademicDiscipline.ECONOMICS: "trade and exchange relationships"
        },
        "model": {
            AcademicDiscipline.MATHEMATICS: "mathematical representation",
            AcademicDiscipline.COMPUTER_SCIENCE: "computational simulation",
            AcademicDiscipline.ECONOMICS: "economic theory representation",
            AcademicDiscipline.PSYCHOLOGY: "theoretical framework"
        },
        "adaptation": {
            AcademicDiscipline.BIOLOGY: "evolutionary change for survival",
            AcademicDiscipline.PSYCHOLOGY: "behavioral adjustment to environment",
            AcademicDiscipline.SOCIOLOGY: "cultural adjustment to change",
            AcademicDiscipline.COMPUTER_SCIENCE: "algorithm adjustment to data"
        }
    }
    
    def __init__(self):
        """Initialize the interdisciplinary analyzer"""
        self.perspectives: Dict[AcademicDiscipline, DisciplinaryPerspective] = {}
        self.insights: InterdisciplinaryInsight = InterdisciplinaryInsight()
    
    def identify_disciplines(self, text: str) -> List[AcademicDiscipline]:
        """
        Identify which academic disciplines are represented in the text.
        
        Args:
            text: Text content to analyze
        
        Returns:
            List of identified disciplines, sorted by relevance
        """
        text_lower = text.lower()
        discipline_scores: Dict[AcademicDiscipline, int] = {}
        
        for discipline, indicators in self.DISCIPLINE_INDICATORS.items():
            score = 0
            for indicator in indicators:
                # Count occurrences of each indicator
                score += len(re.findall(r'\b' + re.escape(indicator) + r'\b', text_lower))
            
            if score > 0:
                discipline_scores[discipline] = score
        
        # Sort by score (descending) and return disciplines
        sorted_disciplines = sorted(
            discipline_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        return [disc for disc, score in sorted_disciplines if score >= 2]  # Threshold of 2 mentions
    
    def add_perspective(
        self,
        discipline: AcademicDiscipline,
        content: str,
        source: Optional[str] = None
    ) -> DisciplinaryPerspective:
        """
        Add or update a disciplinary perspective based on content.
        
        Args:
            discipline: The academic discipline
            content: Content representing this disciplinary perspective
            source: Optional source citation
        
        Returns:
            The updated DisciplinaryPerspective
        """
        if discipline not in self.perspectives:
            self.perspectives[discipline] = DisciplinaryPerspective(discipline=discipline)
        
        perspective = self.perspectives[discipline]
        
        if source:
            perspective.add_source(source)
        
        # Extract key concepts (simplified - looks for capitalized phrases)
        concepts = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', content)
        for concept in set(concepts):
            if len(concept.split()) <= 4:  # Limit to 4-word phrases
                perspective.add_concept(concept)
        
        return perspective
    
    def analyze_convergence_divergence(self) -> InterdisciplinaryInsight:
        """
        Analyze where disciplines converge and diverge in their perspectives.
        
        Returns:
            InterdisciplinaryInsight with convergence and divergence analysis
        """
        if len(self.perspectives) < 2:
            return self.insights
        
        # Analyze concept overlap (convergence)
        all_concepts: Dict[str, Set[AcademicDiscipline]] = {}
        for discipline, perspective in self.perspectives.items():
            for concept in perspective.key_concepts:
                concept_lower = concept.lower()
                if concept_lower not in all_concepts:
                    all_concepts[concept_lower] = set()
                all_concepts[concept_lower].add(discipline)
        
        # Concepts mentioned by multiple disciplines indicate convergence
        for concept, disciplines in all_concepts.items():
            if len(disciplines) >= 2:
                disc_names = ", ".join([d.value.replace("_", " ").title() for d in disciplines])
                self.insights.convergence_areas.append(
                    f"{concept.title()} (addressed in {disc_names})"
                )
        
        # Analyze methodology differences (potential divergence)
        methodology_by_discipline: Dict[str, List[AcademicDiscipline]] = {}
        for discipline, perspective in self.perspectives.items():
            for methodology in perspective.methodologies:
                method_lower = methodology.lower()
                if method_lower not in methodology_by_discipline:
                    methodology_by_discipline[method_lower] = []
                methodology_by_discipline[method_lower].append(discipline)
        
        # Unique methodologies indicate disciplinary differences
        unique_methods = {
            method: discs[0] for method, discs in methodology_by_discipline.items()
            if len(discs) == 1
        }
        
        if unique_methods:
            for method, discipline in list(unique_methods.items())[:5]:  # Limit to 5
                self.insights.divergence_areas.append(
                    f"{discipline.value.replace('_', ' ').title()} uses {method}"
                )
        
        return self.insights
    
    def translate_terminology(
        self,
        term: str,
        from_discipline: Optional[AcademicDiscipline] = None,
        to_discipline: Optional[AcademicDiscipline] = None
    ) -> Dict[AcademicDiscipline, str]:
        """
        Translate a term across disciplines or provide all discipline-specific meanings.
        
        Args:
            term: The term to translate
            from_discipline: Source discipline (optional)
            to_discipline: Target discipline (optional)
        
        Returns:
            Dictionary mapping disciplines to their interpretation of the term
        """
        term_lower = term.lower()
        
        # Check if we have predefined translations
        if term_lower in self.TERMINOLOGY_TRANSLATIONS:
            translations = self.TERMINOLOGY_TRANSLATIONS[term_lower]
            
            if to_discipline and to_discipline in translations:
                return {to_discipline: translations[to_discipline]}
            elif from_discipline:
                # Return all except source discipline
                return {
                    disc: meaning for disc, meaning in translations.items()
                    if disc != from_discipline
                }
            else:
                return translations
        
        # Check perspectives for custom terminology
        custom_translations = {}
        for discipline, perspective in self.perspectives.items():
            if term in perspective.terminology:
                custom_translations[discipline] = perspective.terminology[term]
            elif term.lower() in [t.lower() for t in perspective.terminology.keys()]:
                # Case-insensitive match
                for t, definition in perspective.terminology.items():
                    if t.lower() == term_lower:
                        custom_translations[discipline] = definition
                        break
        
        return custom_translations
    
    def generate_synthesis(self) -> str:
        """
        Generate an integrated synthesis across all disciplinary perspectives.
        
        Returns:
            Synthesized understanding integrating multiple disciplines
        """
        if not self.perspectives:
            return ""
        
        synthesis_parts = []
        
        # Introduction
        discipline_names = [
            d.value.replace("_", " ").title() for d in self.perspectives.keys()
        ]
        if len(discipline_names) == 1:
            synthesis_parts.append(
                f"This research draws primarily from {discipline_names[0]}."
            )
        elif len(discipline_names) == 2:
            synthesis_parts.append(
                f"This research integrates perspectives from {discipline_names[0]} and {discipline_names[1]}."
            )
        else:
            disciplines_str = ", ".join(discipline_names[:-1]) + f", and {discipline_names[-1]}"
            synthesis_parts.append(
                f"This research integrates perspectives from multiple disciplines including {disciplines_str}."
            )
        
        # Convergence areas
        if self.insights.convergence_areas:
            synthesis_parts.append(
                "\n\nAcross disciplines, there is convergence on several key concepts: " +
                "; ".join(self.insights.convergence_areas[:5]) + "."
            )
        
        # Disciplinary contributions
        synthesis_parts.append("\n\nEach discipline contributes unique insights:")
        for discipline, perspective in self.perspectives.items():
            disc_name = discipline.value.replace("_", " ").title()
            if perspective.key_findings:
                finding = perspective.key_findings[0]  # First finding
                synthesis_parts.append(f"\n- {disc_name} emphasizes {finding}")
            elif perspective.theoretical_frameworks:
                framework = perspective.theoretical_frameworks[0]
                synthesis_parts.append(f"\n- {disc_name} applies {framework}")
        
        # Complementary insights
        if len(self.perspectives) >= 2:
            synthesis_parts.append(
                "\n\nThese disciplinary perspectives are complementary rather than contradictory, "
                "each illuminating different aspects of the phenomenon under investigation."
            )
        
        self.insights.integrated_understanding = "".join(synthesis_parts)
        return self.insights.integrated_understanding
    
    def get_search_queries_for_disciplines(
        self,
        base_query: str,
        disciplines: Optional[List[AcademicDiscipline]] = None
    ) -> List[str]:
        """
        Generate discipline-specific search queries for comprehensive coverage.
        
        Args:
            base_query: The base research question or topic
            disciplines: List of disciplines to target (if None, uses common disciplines)
        
        Returns:
            List of discipline-specific search queries
        """
        if disciplines is None:
            # Default to common interdisciplinary set
            disciplines = [
                AcademicDiscipline.PSYCHOLOGY,
                AcademicDiscipline.SOCIOLOGY,
                AcademicDiscipline.ECONOMICS,
                AcademicDiscipline.COMPUTER_SCIENCE,
                AcademicDiscipline.BIOLOGY,
                AcademicDiscipline.MEDICINE
            ]
        
        queries = [base_query]  # Always include base query
        
        for discipline in disciplines:
            disc_name = discipline.value.replace("_", " ")
            # Add discipline-specific query
            queries.append(f"{base_query} {disc_name}")
            queries.append(f"{disc_name} perspective on {base_query}")
        
        return queries
    
    def format_interdisciplinary_report_section(self) -> str:
        """
        Format a report section summarizing interdisciplinary analysis.
        
        Returns:
            Formatted markdown section for inclusion in academic reports
        """
        if not self.perspectives:
            return ""
        
        sections = []
        
        # Header
        sections.append("## Interdisciplinary Perspectives\n")
        
        # Overview
        discipline_names = [
            d.value.replace("_", " ").title() for d in self.perspectives.keys()
        ]
        sections.append(
            f"This analysis integrates insights from {len(discipline_names)} disciplines: " +
            ", ".join(discipline_names) + ".\n"
        )
        
        # Individual perspectives
        sections.append("\n### Disciplinary Contributions\n")
        for discipline, perspective in self.perspectives.items():
            disc_name = discipline.value.replace("_", " ").title()
            sections.append(f"\n**{disc_name}**:\n")
            
            if perspective.theoretical_frameworks:
                sections.append(
                    f"- Theoretical frameworks: {', '.join(perspective.theoretical_frameworks[:3])}\n"
                )
            
            if perspective.methodologies:
                sections.append(
                    f"- Methodologies: {', '.join(perspective.methodologies[:3])}\n"
                )
            
            if perspective.key_findings:
                sections.append(f"- Key insights: {perspective.key_findings[0]}\n")
        
        # Convergence and divergence
        if self.insights.convergence_areas or self.insights.divergence_areas:
            sections.append("\n### Cross-Disciplinary Analysis\n")
            
            if self.insights.convergence_areas:
                sections.append("\n**Areas of Convergence**:\n")
                for area in self.insights.convergence_areas[:5]:
                    sections.append(f"- {area}\n")
            
            if self.insights.divergence_areas:
                sections.append("\n**Disciplinary Differences**:\n")
                for area in self.insights.divergence_areas[:5]:
                    sections.append(f"- {area}\n")
        
        # Integrated synthesis
        if self.insights.integrated_understanding:
            sections.append("\n### Integrated Understanding\n")
            sections.append(f"\n{self.insights.integrated_understanding}\n")
        
        return "".join(sections)
    
    def get_terminology_glossary(self) -> Dict[str, Dict[str, str]]:
        """
        Generate a glossary of terms with discipline-specific definitions.
        
        Returns:
            Dictionary mapping terms to discipline-specific definitions
        """
        glossary: Dict[str, Dict[str, str]] = {}
        
        # Add predefined translations
        for term, translations in self.TERMINOLOGY_TRANSLATIONS.items():
            glossary[term] = {
                disc.value.replace("_", " ").title(): definition
                for disc, definition in translations.items()
            }
        
        # Add custom terminology from perspectives
        for discipline, perspective in self.perspectives.items():
            disc_name = discipline.value.replace("_", " ").title()
            for term, definition in perspective.terminology.items():
                if term not in glossary:
                    glossary[term] = {}
                glossary[term][disc_name] = definition
        
        return glossary
    
    def clear(self) -> None:
        """Clear all stored perspectives and insights"""
        self.perspectives.clear()
        self.insights = InterdisciplinaryInsight()


def create_interdisciplinary_prompt_addition() -> str:
    """
    Create prompt text to add to research agent for interdisciplinary support.
    
    Returns:
        Formatted prompt text for interdisciplinary research
    """
    return """
## Interdisciplinary Research Guidelines

When conducting research on topics that span multiple academic disciplines:

**1. Multi-Discipline Search Strategy**:
- Conduct searches across multiple relevant disciplines
- Use discipline-specific terminology in queries
- Search for "[topic] + [discipline]" (e.g., "decision making psychology", "decision making economics")
- Look for interdisciplinary journals and cross-disciplinary research

**2. Identify Disciplinary Perspectives**:
- Explicitly note which discipline each source represents
- Identify discipline-specific theoretical frameworks and methodologies
- Document how different disciplines conceptualize the same phenomenon
- Note discipline-specific terminology and definitions

**3. Analyze Convergence and Divergence**:
- **Convergence**: Identify where disciplines agree on findings or concepts
- **Divergence**: Note where disciplines have different interpretations or contradictory findings
- **Complementarity**: Recognize how disciplines provide different but compatible insights
- Explain reasons for differences (methodology, focus, assumptions)

**4. Translate Discipline-Specific Terminology**:
- Define technical terms from each discipline
- Identify equivalent concepts across disciplines (e.g., "utility" in economics vs "satisfaction" in psychology)
- Explain how the same term may have different meanings in different fields
- Create a terminology bridge for interdisciplinary understanding

**5. Integrate Cross-Disciplinary Insights**:
- Synthesize findings across disciplines into coherent understanding
- Show how different disciplinary perspectives complement each other
- Build integrated theoretical frameworks drawing from multiple fields
- Avoid simply listing disciplinary findings separately - create true synthesis
- Highlight unique contributions from each discipline

**Example Interdisciplinary Analysis**:
Topic: "Social Media and Mental Health"
- Psychology: Examines individual cognitive and emotional effects
- Sociology: Analyzes social network structures and group dynamics
- Computer Science: Studies algorithms, design patterns, and user interfaces
- Public Health: Investigates population-level health outcomes
- Convergence: All disciplines recognize significant impacts on well-being
- Divergence: Different levels of analysis (individual vs. societal)
- Integration: Comprehensive understanding requires combining individual psychological effects with social structures and technological design
"""
