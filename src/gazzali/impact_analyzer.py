#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Research Impact Analysis Module for Gazzali Research

This module provides functionality for analyzing research impact through:
- Citation count tracking and analysis
- Identification of highly cited papers
- Extraction of research implications
- Generation of implications sections
- Identification of future research directions

Requirements addressed:
- 12.1: Generate implications section with theoretical and practical applications
- 12.2: Identify how research contributes to or challenges existing theories
- 12.3: Discuss practical applications for practitioners and policymakers
- 12.4: Identify future research directions
- 12.5: Document impact and influence of highly cited papers
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Tuple
from enum import Enum

from .citation_manager import Citation, CitationManager


class ImpactLevel(str, Enum):
    """Classification of research impact levels"""
    HIGHLY_CITED = "highly_cited"  # Top 10% by citation count
    WELL_CITED = "well_cited"      # Top 25% by citation count
    MODERATELY_CITED = "moderately_cited"  # Top 50% by citation count
    EMERGING = "emerging"          # Recent papers with growing citations
    FOUNDATIONAL = "foundational"  # Older papers with sustained citations


class ImplicationType(str, Enum):
    """Types of research implications"""
    THEORETICAL = "theoretical"
    PRACTICAL = "practical"
    METHODOLOGICAL = "methodological"
    POLICY = "policy"
    EDUCATIONAL = "educational"


@dataclass
class ResearchImplication:
    """
    Represents a specific research implication.
    
    Attributes:
        implication_type: Type of implication (theoretical, practical, etc.)
        description: Description of the implication
        stakeholders: Who benefits from this implication
        evidence: Supporting evidence or citations
        confidence: Confidence level (high, medium, low)
    """
    implication_type: ImplicationType
    description: str
    stakeholders: List[str] = field(default_factory=list)
    evidence: List[str] = field(default_factory=list)
    confidence: str = "medium"  # high, medium, low
    
    def to_text(self) -> str:
        """Convert implication to formatted text"""
        text_parts = [self.description]
        
        if self.stakeholders:
            stakeholders_str = ", ".join(self.stakeholders)
            text_parts.append(f"This has implications for {stakeholders_str}.")
        
        return " ".join(text_parts)


@dataclass
class FutureDirection:
    """
    Represents a future research direction.
    
    Attributes:
        direction: Description of the research direction
        rationale: Why this direction is important
        methodology_suggestions: Suggested methodological approaches
        priority: Priority level (high, medium, low)
        related_gaps: Research gaps this direction addresses
    """
    direction: str
    rationale: str
    methodology_suggestions: List[str] = field(default_factory=list)
    priority: str = "medium"  # high, medium, low
    related_gaps: List[str] = field(default_factory=list)
    
    def to_text(self) -> str:
        """Convert future direction to formatted text"""
        text_parts = [self.direction, self.rationale]
        
        if self.methodology_suggestions:
            methods_str = ", ".join(self.methodology_suggestions)
            text_parts.append(f"Potential methodological approaches include {methods_str}.")
        
        return " ".join(text_parts)


@dataclass
class ImpactAnalysis:
    """
    Complete impact analysis for a research topic.
    
    Attributes:
        highly_cited_papers: List of highly cited papers with analysis
        citation_statistics: Overall citation statistics
        theoretical_implications: Theoretical implications identified
        practical_implications: Practical implications identified
        policy_implications: Policy implications identified
        future_directions: Identified future research directions
        knowledge_contributions: How research contributes to knowledge
        challenges_to_theory: How research challenges existing theories
    """
    highly_cited_papers: List[Tuple[Citation, ImpactLevel]] = field(default_factory=list)
    citation_statistics: Dict[str, Any] = field(default_factory=dict)
    theoretical_implications: List[ResearchImplication] = field(default_factory=list)
    practical_implications: List[ResearchImplication] = field(default_factory=list)
    policy_implications: List[ResearchImplication] = field(default_factory=list)
    future_directions: List[FutureDirection] = field(default_factory=list)
    knowledge_contributions: List[str] = field(default_factory=list)
    challenges_to_theory: List[str] = field(default_factory=list)
    
    def get_summary(self) -> str:
        """Generate a summary of the impact analysis"""
        parts = []
        
        if self.highly_cited_papers:
            parts.append(f"Identified {len(self.highly_cited_papers)} highly influential papers.")
        
        total_implications = (
            len(self.theoretical_implications) +
            len(self.practical_implications) +
            len(self.policy_implications)
        )
        if total_implications > 0:
            parts.append(f"Found {total_implications} key implications across theoretical, practical, and policy domains.")
        
        if self.future_directions:
            parts.append(f"Identified {len(self.future_directions)} promising future research directions.")
        
        return " ".join(parts) if parts else "No impact analysis available."


class ImpactAnalyzer:
    """
    Analyzes research impact through citation analysis and implication extraction.
    
    This class provides methods to:
    - Track and analyze citation counts
    - Identify highly cited papers
    - Extract research implications from content
    - Generate implications sections for reports
    - Identify future research directions
    
    Requirements addressed:
    - 12.1: Generate implications section
    - 12.2: Identify contributions to theory
    - 12.3: Discuss practical applications
    - 12.4: Identify future research directions
    - 12.5: Document impact of highly cited papers
    """
    
    def __init__(self, citation_manager: CitationManager):
        """
        Initialize the impact analyzer.
        
        Args:
            citation_manager: Citation manager containing research sources
        """
        self.citation_manager = citation_manager
        self.impact_analysis: Optional[ImpactAnalysis] = None
    
    def analyze_impact(self, research_content: str = "") -> ImpactAnalysis:
        """
        Perform complete impact analysis.
        
        This method:
        1. Analyzes citation counts and identifies highly cited papers
        2. Extracts implications from research content
        3. Identifies future research directions
        4. Compiles comprehensive impact analysis
        
        Args:
            research_content: Research findings text to analyze for implications
        
        Returns:
            Complete ImpactAnalysis object
        
        Requirements:
            - 12.1: Generate implications section
            - 12.5: Document impact of highly cited papers
        """
        analysis = ImpactAnalysis()
        
        # Analyze citations and identify highly cited papers
        analysis.highly_cited_papers = self.identify_highly_cited_papers()
        analysis.citation_statistics = self.calculate_citation_statistics()
        
        # Extract implications from research content if provided
        if research_content:
            implications = self.extract_implications(research_content)
            analysis.theoretical_implications = implications.get('theoretical', [])
            analysis.practical_implications = implications.get('practical', [])
            analysis.policy_implications = implications.get('policy', [])
            
            # Extract future directions
            analysis.future_directions = self.extract_future_directions(research_content)
            
            # Extract knowledge contributions and challenges
            analysis.knowledge_contributions = self.extract_knowledge_contributions(research_content)
            analysis.challenges_to_theory = self.extract_theoretical_challenges(research_content)
        
        self.impact_analysis = analysis
        return analysis
    
    def identify_highly_cited_papers(self) -> List[Tuple[Citation, ImpactLevel]]:
        """
        Identify highly cited papers from the citation collection.
        
        Classifies papers into impact levels based on citation counts:
        - Highly cited: Top 10% or >100 citations
        - Well cited: Top 25% or >50 citations
        - Moderately cited: Top 50% or >20 citations
        - Emerging: Recent papers (<3 years) with >10 citations
        - Foundational: Older papers (>10 years) with sustained citations
        
        Returns:
            List of (Citation, ImpactLevel) tuples sorted by citation count
        
        Requirements:
            - 14.3: Identify highly cited papers based on citation metrics
            - 12.5: Document impact and influence of highly cited work
        """
        # Get all citations with citation counts
        citations_with_counts = [
            c for c in self.citation_manager.citations.values()
            if c.citation_count is not None and c.citation_count > 0
        ]
        
        if not citations_with_counts:
            return []
        
        # Sort by citation count
        citations_with_counts.sort(key=lambda c: c.citation_count or 0, reverse=True)
        
        # Calculate percentile thresholds
        total_count = len(citations_with_counts)
        top_10_threshold = max(100, citations_with_counts[min(int(total_count * 0.1), total_count - 1)].citation_count or 0)
        top_25_threshold = max(50, citations_with_counts[min(int(total_count * 0.25), total_count - 1)].citation_count or 0)
        top_50_threshold = max(20, citations_with_counts[min(int(total_count * 0.50), total_count - 1)].citation_count or 0)
        
        # Classify papers
        classified_papers = []
        current_year = 2025  # From system context
        
        for citation in citations_with_counts:
            count = citation.citation_count or 0
            age = current_year - citation.year if citation.year else 0
            
            # Determine impact level
            if count >= top_10_threshold or count >= 100:
                level = ImpactLevel.HIGHLY_CITED
            elif count >= top_25_threshold or count >= 50:
                level = ImpactLevel.WELL_CITED
            elif count >= top_50_threshold or count >= 20:
                level = ImpactLevel.MODERATELY_CITED
            elif age <= 3 and count >= 10:
                level = ImpactLevel.EMERGING
            elif age >= 10 and count >= 30:
                level = ImpactLevel.FOUNDATIONAL
            else:
                continue  # Skip papers that don't meet any threshold
            
            classified_papers.append((citation, level))
        
        return classified_papers
    
    def calculate_citation_statistics(self) -> Dict[str, Any]:
        """
        Calculate overall citation statistics for the research collection.
        
        Returns:
            Dictionary with citation statistics including:
            - total_papers: Total number of papers
            - papers_with_citations: Papers with citation data
            - total_citations: Sum of all citations
            - mean_citations: Average citations per paper
            - median_citations: Median citation count
            - highly_cited_count: Number of highly cited papers
            - citation_range: Min and max citation counts
        
        Requirements:
            - 12.5: Track citation counts and analyze impact
        """
        citations = list(self.citation_manager.citations.values())
        citations_with_counts = [
            c for c in citations
            if c.citation_count is not None and c.citation_count > 0
        ]
        
        if not citations_with_counts:
            return {
                'total_papers': len(citations),
                'papers_with_citations': 0,
                'total_citations': 0,
                'mean_citations': 0,
                'median_citations': 0,
                'highly_cited_count': 0,
                'citation_range': (0, 0),
            }
        
        # Calculate statistics
        citation_counts = [c.citation_count or 0 for c in citations_with_counts]
        citation_counts.sort()
        
        total_citations = sum(citation_counts)
        mean_citations = total_citations / len(citation_counts)
        median_citations = citation_counts[len(citation_counts) // 2]
        highly_cited_count = sum(1 for c in citation_counts if c >= 100)
        
        return {
            'total_papers': len(citations),
            'papers_with_citations': len(citations_with_counts),
            'total_citations': total_citations,
            'mean_citations': round(mean_citations, 1),
            'median_citations': median_citations,
            'highly_cited_count': highly_cited_count,
            'citation_range': (min(citation_counts), max(citation_counts)),
        }
    
    def extract_implications(self, research_content: str) -> Dict[str, List[ResearchImplication]]:
        """
        Extract research implications from content.
        
        Identifies implications by looking for:
        - Theoretical implications: Theory development, conceptual advances
        - Practical implications: Applications, interventions, tools
        - Policy implications: Policy recommendations, regulatory guidance
        
        Args:
            research_content: Research findings text
        
        Returns:
            Dictionary mapping implication types to lists of implications
        
        Requirements:
            - 12.1: Generate implications section
            - 12.2: Identify theoretical implications
            - 12.3: Discuss practical applications
        """
        implications = {
            'theoretical': [],
            'practical': [],
            'policy': [],
        }
        
        # Split content into sentences for analysis
        import re
        sentences = re.split(r'[.!?]+\s+', research_content)
        
        # Keywords for identifying different types of implications
        theoretical_keywords = [
            'theory', 'theoretical', 'conceptual', 'framework', 'model',
            'understanding', 'knowledge', 'contributes to', 'advances',
            'challenges', 'supports', 'extends', 'refines'
        ]
        
        practical_keywords = [
            'practical', 'application', 'practice', 'practitioners',
            'implementation', 'intervention', 'tool', 'technique',
            'method', 'approach', 'strategy', 'can be used',
            'useful for', 'helps', 'enables', 'facilitates'
        ]
        
        policy_keywords = [
            'policy', 'policymakers', 'regulation', 'regulatory',
            'government', 'legislation', 'guidelines', 'standards',
            'should', 'recommend', 'suggest', 'advocate', 'propose'
        ]
        
        # Analyze sentences for implications
        for sentence in sentences:
            sentence_lower = sentence.lower()
            
            # Skip very short sentences
            if len(sentence.split()) < 5:
                continue
            
            # Check for implication indicators
            has_implication_indicator = any(
                indicator in sentence_lower
                for indicator in ['implication', 'implications', 'suggests', 'indicates',
                                'demonstrates', 'shows', 'reveals', 'highlights']
            )
            
            if not has_implication_indicator:
                continue
            
            # Classify implication type
            theoretical_score = sum(1 for kw in theoretical_keywords if kw in sentence_lower)
            practical_score = sum(1 for kw in practical_keywords if kw in sentence_lower)
            policy_score = sum(1 for kw in policy_keywords if kw in sentence_lower)
            
            # Determine primary type
            if theoretical_score > practical_score and theoretical_score > policy_score:
                implication_type = ImplicationType.THEORETICAL
                category = 'theoretical'
                stakeholders = ['researchers', 'theorists', 'academics']
            elif practical_score > policy_score:
                implication_type = ImplicationType.PRACTICAL
                category = 'practical'
                stakeholders = ['practitioners', 'professionals', 'organizations']
            elif policy_score > 0:
                implication_type = ImplicationType.POLICY
                category = 'policy'
                stakeholders = ['policymakers', 'regulators', 'government agencies']
            else:
                continue  # Skip if no clear type
            
            # Create implication object
            implication = ResearchImplication(
                implication_type=implication_type,
                description=sentence.strip(),
                stakeholders=stakeholders,
                confidence="medium",
            )
            
            implications[category].append(implication)
        
        return implications
    
    def extract_future_directions(self, research_content: str) -> List[FutureDirection]:
        """
        Extract future research directions from content.
        
        Identifies future directions by looking for:
        - Explicit mentions of "future research"
        - Research gaps and limitations
        - Unanswered questions
        - Suggested next steps
        
        Args:
            research_content: Research findings text
        
        Returns:
            List of FutureDirection objects
        
        Requirements:
            - 12.4: Identify future research directions based on findings and gaps
        """
        directions = []
        
        # Split content into sentences
        import re
        sentences = re.split(r'[.!?]+\s+', research_content)
        
        # Keywords for identifying future directions
        future_keywords = [
            'future research', 'future studies', 'future work',
            'further research', 'further investigation', 'further study',
            'should investigate', 'should explore', 'should examine',
            'warrants', 'needed', 'necessary', 'important to',
            'remains to be', 'yet to be', 'unclear', 'unknown'
        ]
        
        gap_keywords = [
            'gap', 'limitation', 'limited', 'lack of', 'absence of',
            'insufficient', 'not yet', 'remains unclear', 'unknown',
            'unanswered', 'unexplored', 'understudied'
        ]
        
        # Analyze sentences for future directions
        for i, sentence in enumerate(sentences):
            sentence_lower = sentence.lower()
            
            # Skip very short sentences
            if len(sentence.split()) < 5:
                continue
            
            # Check for future direction indicators
            has_future_indicator = any(kw in sentence_lower for kw in future_keywords)
            has_gap_indicator = any(kw in sentence_lower for kw in gap_keywords)
            
            if not (has_future_indicator or has_gap_indicator):
                continue
            
            # Extract rationale from context (next sentence if available)
            rationale = ""
            if i + 1 < len(sentences):
                next_sentence = sentences[i + 1].strip()
                if len(next_sentence.split()) >= 5:
                    rationale = next_sentence
            
            # Determine priority based on keywords
            priority = "medium"
            if any(kw in sentence_lower for kw in ['critical', 'essential', 'crucial', 'important']):
                priority = "high"
            elif any(kw in sentence_lower for kw in ['may', 'could', 'might', 'potentially']):
                priority = "low"
            
            # Create future direction object
            direction = FutureDirection(
                direction=sentence.strip(),
                rationale=rationale,
                priority=priority,
            )
            
            directions.append(direction)
        
        # Limit to most relevant directions
        return directions[:10]
    
    def extract_knowledge_contributions(self, research_content: str) -> List[str]:
        """
        Extract how research contributes to existing knowledge.
        
        Identifies contributions by looking for:
        - Novel findings or discoveries
        - Extensions of existing theories
        - New methodological approaches
        - Synthesis of disparate findings
        
        Args:
            research_content: Research findings text
        
        Returns:
            List of knowledge contribution statements
        
        Requirements:
            - 12.2: Identify how research contributes to existing theories and knowledge
        """
        contributions = []
        
        # Split content into sentences
        import re
        sentences = re.split(r'[.!?]+\s+', research_content)
        
        # Keywords for identifying contributions
        contribution_keywords = [
            'contributes', 'contribution', 'advances', 'extends',
            'builds on', 'adds to', 'enhances', 'improves',
            'novel', 'new', 'first', 'original', 'innovative',
            'demonstrates', 'shows', 'reveals', 'establishes',
            'provides evidence', 'supports', 'confirms'
        ]
        
        # Analyze sentences for contributions
        for sentence in sentences:
            sentence_lower = sentence.lower()
            
            # Skip very short sentences
            if len(sentence.split()) < 5:
                continue
            
            # Check for contribution indicators
            has_contribution = any(kw in sentence_lower for kw in contribution_keywords)
            
            if has_contribution:
                contributions.append(sentence.strip())
        
        # Limit to most relevant contributions
        return contributions[:8]
    
    def extract_theoretical_challenges(self, research_content: str) -> List[str]:
        """
        Extract how research challenges existing theories.
        
        Identifies challenges by looking for:
        - Contradictions with existing theories
        - Limitations of current frameworks
        - Alternative explanations
        - Paradigm shifts
        
        Args:
            research_content: Research findings text
        
        Returns:
            List of theoretical challenge statements
        
        Requirements:
            - 12.2: Identify how research challenges existing theories
        """
        challenges = []
        
        # Split content into sentences
        import re
        sentences = re.split(r'[.!?]+\s+', research_content)
        
        # Keywords for identifying challenges
        challenge_keywords = [
            'challenges', 'contradicts', 'contrary to', 'inconsistent with',
            'questions', 'disputes', 'refutes', 'opposes',
            'alternative', 'different from', 'diverges from',
            'limitation of', 'weakness of', 'fails to',
            'however', 'but', 'although', 'despite'
        ]
        
        # Analyze sentences for challenges
        for sentence in sentences:
            sentence_lower = sentence.lower()
            
            # Skip very short sentences
            if len(sentence.split()) < 5:
                continue
            
            # Check for challenge indicators
            has_challenge = any(kw in sentence_lower for kw in challenge_keywords)
            
            # Also check for theory-related terms
            has_theory_mention = any(
                term in sentence_lower
                for term in ['theory', 'theoretical', 'framework', 'model', 'paradigm']
            )
            
            if has_challenge and has_theory_mention:
                challenges.append(sentence.strip())
        
        # Limit to most relevant challenges
        return challenges[:6]
    
    def generate_implications_section(
        self,
        analysis: Optional[ImpactAnalysis] = None,
        include_future_directions: bool = True,
    ) -> str:
        """
        Generate a formatted implications section for academic reports.
        
        This method creates a comprehensive implications section that includes:
        - Theoretical implications
        - Practical implications
        - Policy implications
        - Future research directions (optional)
        
        Args:
            analysis: ImpactAnalysis object (uses self.impact_analysis if None)
            include_future_directions: Whether to include future directions
        
        Returns:
            Formatted implications section text
        
        Requirements:
            - 12.1: Generate implications section with theoretical and practical applications
            - 12.3: Discuss practical applications for stakeholders
            - 12.4: Identify future research directions
        """
        if analysis is None:
            analysis = self.impact_analysis
        
        if analysis is None:
            return "No impact analysis available. Please run analyze_impact() first."
        
        sections = []
        
        # Introduction
        sections.append(
            "This research has significant implications across theoretical, practical, "
            "and policy domains. The findings contribute to existing knowledge while "
            "also suggesting new directions for future investigation."
        )
        sections.append("")
        
        # Theoretical implications
        if analysis.theoretical_implications:
            sections.append("### Theoretical Implications")
            sections.append("")
            sections.append(
                "The research makes several important theoretical contributions. "
            )
            for i, impl in enumerate(analysis.theoretical_implications[:5], 1):
                sections.append(f"{i}. {impl.to_text()}")
            sections.append("")
        
        # Knowledge contributions
        if analysis.knowledge_contributions:
            sections.append(
                "These findings contribute to existing knowledge by "
                + " ".join(analysis.knowledge_contributions[:3])
            )
            sections.append("")
        
        # Theoretical challenges
        if analysis.challenges_to_theory:
            sections.append(
                "The research also challenges some existing theoretical assumptions. "
                + " ".join(analysis.challenges_to_theory[:2])
            )
            sections.append("")
        
        # Practical implications
        if analysis.practical_implications:
            sections.append("### Practical Implications")
            sections.append("")
            sections.append(
                "The findings have important practical applications for various stakeholders. "
            )
            for i, impl in enumerate(analysis.practical_implications[:5], 1):
                sections.append(f"{i}. {impl.to_text()}")
            sections.append("")
        
        # Policy implications
        if analysis.policy_implications:
            sections.append("### Policy Implications")
            sections.append("")
            sections.append(
                "The research has several implications for policy and regulation. "
            )
            for i, impl in enumerate(analysis.policy_implications[:5], 1):
                sections.append(f"{i}. {impl.to_text()}")
            sections.append("")
        
        # Future research directions
        if include_future_directions and analysis.future_directions:
            sections.append("### Future Research Directions")
            sections.append("")
            sections.append(
                "Based on the findings and identified gaps, several promising "
                "directions for future research emerge:"
            )
            sections.append("")
            for i, direction in enumerate(analysis.future_directions[:6], 1):
                sections.append(f"{i}. {direction.to_text()}")
            sections.append("")
        
        # Conclusion
        sections.append(
            "These implications highlight the multifaceted impact of this research "
            "and underscore the importance of continued investigation in this area."
        )
        
        return "\n".join(sections)
    
    def generate_highly_cited_summary(
        self,
        analysis: Optional[ImpactAnalysis] = None,
        max_papers: int = 10,
    ) -> str:
        """
        Generate a summary of highly cited papers.
        
        Args:
            analysis: ImpactAnalysis object (uses self.impact_analysis if None)
            max_papers: Maximum number of papers to include
        
        Returns:
            Formatted summary of highly cited papers
        
        Requirements:
            - 12.5: Document impact and influence of highly cited papers
        """
        if analysis is None:
            analysis = self.impact_analysis
        
        if analysis is None or not analysis.highly_cited_papers:
            return "No highly cited papers identified."
        
        sections = []
        sections.append("### Highly Cited and Influential Papers")
        sections.append("")
        sections.append(
            "The following papers have demonstrated significant impact in the field, "
            "as evidenced by their citation counts and influence on subsequent research:"
        )
        sections.append("")
        
        for i, (citation, level) in enumerate(analysis.highly_cited_papers[:max_papers], 1):
            # Format citation info
            authors_str = citation.authors[0] if citation.authors else "Unknown"
            if len(citation.authors) > 1:
                authors_str += " et al."
            
            year_str = str(citation.year) if citation.year else "n.d."
            count_str = f"{citation.citation_count} citations" if citation.citation_count else "citation count unavailable"
            
            # Impact level description
            level_desc = {
                ImpactLevel.HIGHLY_CITED: "highly influential",
                ImpactLevel.WELL_CITED: "well-cited",
                ImpactLevel.MODERATELY_CITED: "moderately cited",
                ImpactLevel.EMERGING: "emerging influence",
                ImpactLevel.FOUNDATIONAL: "foundational work",
            }.get(level, "influential")
            
            sections.append(
                f"{i}. **{authors_str} ({year_str})**: *{citation.title}*. "
                f"This {level_desc} paper has received {count_str}."
            )
        
        sections.append("")
        sections.append(
            f"These {len(analysis.highly_cited_papers[:max_papers])} papers represent "
            "key contributions that have shaped the field and influenced subsequent research directions."
        )
        
        return "\n".join(sections)


def analyze_research_impact(
    citation_manager: CitationManager,
    research_content: str = "",
) -> ImpactAnalysis:
    """
    Convenience function to perform research impact analysis.
    
    Args:
        citation_manager: Citation manager with research sources
        research_content: Research findings text to analyze
    
    Returns:
        Complete ImpactAnalysis object
    
    Example:
        >>> from gazzali.citation_manager import CitationManager
        >>> from gazzali.impact_analyzer import analyze_research_impact
        >>> 
        >>> citation_mgr = CitationManager()
        >>> # ... add citations ...
        >>> 
        >>> analysis = analyze_research_impact(citation_mgr, research_text)
        >>> print(analysis.get_summary())
    """
    analyzer = ImpactAnalyzer(citation_manager)
    return analyzer.analyze_impact(research_content)
