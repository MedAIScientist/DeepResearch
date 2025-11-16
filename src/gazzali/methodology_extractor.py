#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Methodology and Theory Extraction Module for Gazzali Research

This module provides functionality to extract and categorize research methodologies
and theoretical frameworks from academic papers and research content.

Requirements addressed:
- 4.1: Extract and document research methodologies from papers
- 4.2: Categorize methodologies (qualitative, quantitative, mixed-methods)
- 11.1: Identify theoretical frameworks and models
- 11.2: Extract definitions of key theoretical constructs

Components:
- MethodologyExtractor: Extracts and categorizes research methodologies
- TheoryExtractor: Identifies and extracts theoretical frameworks
- MethodologyInfo: Data class for methodology information
- TheoryInfo: Data class for theoretical framework information
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Set
from enum import Enum


class MethodologyType(str, Enum):
    """Types of research methodologies"""
    QUALITATIVE = "qualitative"
    QUANTITATIVE = "quantitative"
    MIXED_METHODS = "mixed-methods"
    THEORETICAL = "theoretical"
    COMPUTATIONAL = "computational"
    EXPERIMENTAL = "experimental"
    META_ANALYSIS = "meta-analysis"
    SYSTEMATIC_REVIEW = "systematic-review"
    CASE_STUDY = "case-study"
    UNKNOWN = "unknown"


@dataclass
class MethodologyInfo:
    """
    Information about a research methodology.
    
    Attributes:
        methodology_type: Primary type of methodology
        specific_methods: List of specific methods used (e.g., "interviews", "surveys")
        data_collection: Description of data collection approach
        analysis_techniques: List of analysis techniques used
        sample_info: Information about sample/participants
        limitations: Identified limitations of the methodology
        confidence: Confidence score (0-1) in the extraction
    """
    methodology_type: MethodologyType
    specific_methods: List[str] = field(default_factory=list)
    data_collection: str = ""
    analysis_techniques: List[str] = field(default_factory=list)
    sample_info: str = ""
    limitations: List[str] = field(default_factory=list)
    confidence: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "methodology_type": self.methodology_type.value,
            "specific_methods": self.specific_methods,
            "data_collection": self.data_collection,
            "analysis_techniques": self.analysis_techniques,
            "sample_info": self.sample_info,
            "limitations": self.limitations,
            "confidence": self.confidence,
        }
    
    def __str__(self) -> str:
        """String representation"""
        parts = [f"{self.methodology_type.value}"]
        if self.specific_methods:
            parts.append(f"({', '.join(self.specific_methods[:3])})")
        return " ".join(parts)


@dataclass
class TheoryInfo:
    """
    Information about a theoretical framework.
    
    Attributes:
        theory_name: Name of the theory or framework
        theory_type: Type of theory (e.g., "psychological", "economic")
        key_constructs: List of key theoretical constructs
        definitions: Dictionary mapping constructs to definitions
        applications: How the theory is applied in the research
        citations: References to original theory papers
        confidence: Confidence score (0-1) in the extraction
    """
    theory_name: str
    theory_type: str = ""
    key_constructs: List[str] = field(default_factory=list)
    definitions: Dict[str, str] = field(default_factory=dict)
    applications: str = ""
    citations: List[str] = field(default_factory=list)
    confidence: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "theory_name": self.theory_name,
            "theory_type": self.theory_type,
            "key_constructs": self.key_constructs,
            "definitions": self.definitions,
            "applications": self.applications,
            "citations": self.citations,
            "confidence": self.confidence,
        }
    
    def __str__(self) -> str:
        """String representation"""
        return f"{self.theory_name} ({self.theory_type})" if self.theory_type else self.theory_name


class MethodologyExtractor:
    """
    Extracts and categorizes research methodologies from academic content.
    
    This class analyzes text to identify:
    - Primary methodology type (qualitative, quantitative, mixed-methods, etc.)
    - Specific research methods used
    - Data collection approaches
    - Analysis techniques
    - Sample/participant information
    - Methodological limitations
    """
    
    # Keyword patterns for methodology identification
    METHODOLOGY_PATTERNS = {
        MethodologyType.QUALITATIVE: [
            r'\bqualitative\b', r'\bethnograph', r'\bphenomenolog',
            r'\bgrounded theory\b', r'\bcase study\b', r'\bcase studies\b',
            r'\binterviews?\b', r'\bfocus groups?\b', r'\bobservation',
            r'\bthematic analysis\b', r'\bcontent analysis\b',
            r'\bnarrative analysis\b', r'\bdiscourse analysis\b',
        ],
        MethodologyType.QUANTITATIVE: [
            r'\bquantitative\b', r'\bsurvey', r'\bquestionnaire',
            r'\bstatistical\b', r'\bregression\b', r'\bcorrelation',
            r'\banova\b', r'\bt-test\b', r'\bchi-square\b',
            r'\bexperiment', r'\brandomized\b', r'\bcontrol group\b',
            r'\bsample size\b', r'\bn\s*=\s*\d+', r'\bp\s*[<>=]',
        ],
        MethodologyType.MIXED_METHODS: [
            r'\bmixed[- ]methods?\b', r'\bmixed[- ]method\b',
            r'\btriangulation\b', r'\bsequential\b.*\bdesign\b',
            r'\bconcurrent\b.*\bdesign\b', r'\bconvergent\b',
        ],
        MethodologyType.META_ANALYSIS: [
            r'\bmeta[- ]analysis\b', r'\bmeta[- ]analytic\b',
            r'\bsystematic review\b', r'\beffect size', r'\bforest plot\b',
            r'\bheterogeneity\b', r'\bpublication bias\b',
        ],
        MethodologyType.COMPUTATIONAL: [
            r'\bcomputational\b', r'\bsimulation', r'\balgorithm',
            r'\bmachine learning\b', r'\bdeep learning\b', r'\bneural network',
            r'\bdata mining\b', r'\bartificial intelligence\b',
            r'\bmodeling\b', r'\bcomputational model',
        ],
        MethodologyType.EXPERIMENTAL: [
            r'\bexperiment', r'\brandomized controlled trial\b', r'\brct\b',
            r'\btreatment group\b', r'\bcontrol group\b', r'\bintervention',
            r'\bpre-test\b', r'\bpost-test\b', r'\bwithin[- ]subjects\b',
            r'\bbetween[- ]subjects\b',
        ],
        MethodologyType.CASE_STUDY: [
            r'\bcase study\b', r'\bcase studies\b', r'\bsingle case\b',
            r'\bmultiple case\b', r'\bcase analysis\b',
        ],
        MethodologyType.SYSTEMATIC_REVIEW: [
            r'\bsystematic review\b', r'\bsystematic literature review\b',
            r'\bprisma\b', r'\binclusion criteria\b', r'\bexclusion criteria\b',
            r'\bsearch strategy\b', r'\bquality assessment\b',
        ],
    }
    
    # Specific method keywords
    SPECIFIC_METHODS = {
        'interviews': [r'\binterview', r'\bsemi[- ]structured interview'],
        'surveys': [r'\bsurvey', r'\bquestionnaire'],
        'observations': [r'\bobservation', r'\bethnograph'],
        'focus_groups': [r'\bfocus group'],
        'experiments': [r'\bexperiment', r'\blaboratory study\b'],
        'archival_analysis': [r'\barchival', r'\bdocument analysis\b'],
        'regression': [r'\bregression\b', r'\blinear regression\b', r'\blogistic regression\b'],
        'anova': [r'\banova\b', r'\banalysis of variance\b'],
        'factor_analysis': [r'\bfactor analysis\b', r'\bprincipal component'],
        'structural_equation': [r'\bstructural equation\b', r'\bsem\b'],
        'thematic_coding': [r'\bthematic\b.*\bcoding\b', r'\bthematic analysis\b'],
        'content_analysis': [r'\bcontent analysis\b'],
    }
    
    # Analysis technique keywords
    ANALYSIS_TECHNIQUES = {
        'statistical': [r'\bstatistical\b', r'\bstatistics\b'],
        'descriptive': [r'\bdescriptive\b.*\bstatistics\b', r'\bmean\b', r'\bstandard deviation\b'],
        'inferential': [r'\binferential\b', r'\bhypothesis test', r'\bsignificance test'],
        'regression': [r'\bregression\b'],
        'correlation': [r'\bcorrelation\b'],
        'anova': [r'\banova\b'],
        'thematic': [r'\bthematic\b.*\banalysis\b'],
        'content': [r'\bcontent\b.*\banalysis\b'],
        'discourse': [r'\bdiscourse\b.*\banalysis\b'],
        'grounded_theory': [r'\bgrounded theory\b'],
        'machine_learning': [r'\bmachine learning\b', r'\bdeep learning\b'],
    }
    
    def __init__(self):
        """Initialize the methodology extractor"""
        pass
    
    def extract_methodology(self, content: str, title: str = "") -> MethodologyInfo:
        """
        Extract methodology information from content.
        
        Args:
            content: Text content to analyze (abstract, methodology section, or full paper)
            title: Optional paper title for additional context
        
        Returns:
            MethodologyInfo object with extracted information
        
        Requirements:
            - 4.1: Extract and document research methodologies
            - 4.2: Categorize methodologies
        """
        content_lower = content.lower()
        combined_text = f"{title} {content}".lower()
        
        # Identify primary methodology type
        methodology_type, confidence = self._identify_methodology_type(combined_text)
        
        # Extract specific methods
        specific_methods = self._extract_specific_methods(content_lower)
        
        # Extract data collection information
        data_collection = self._extract_data_collection(content)
        
        # Extract analysis techniques
        analysis_techniques = self._extract_analysis_techniques(content_lower)
        
        # Extract sample information
        sample_info = self._extract_sample_info(content)
        
        # Extract limitations
        limitations = self._extract_limitations(content)
        
        return MethodologyInfo(
            methodology_type=methodology_type,
            specific_methods=specific_methods,
            data_collection=data_collection,
            analysis_techniques=analysis_techniques,
            sample_info=sample_info,
            limitations=limitations,
            confidence=confidence,
        )
    
    def _identify_methodology_type(self, text: str) -> tuple[MethodologyType, float]:
        """
        Identify the primary methodology type.
        
        Args:
            text: Text to analyze
        
        Returns:
            Tuple of (MethodologyType, confidence_score)
        """
        scores = {}
        
        # Count matches for each methodology type
        for method_type, patterns in self.METHODOLOGY_PATTERNS.items():
            count = 0
            for pattern in patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                count += len(matches)
            scores[method_type] = count
        
        # Find type with highest score
        if not scores or max(scores.values()) == 0:
            return MethodologyType.UNKNOWN, 0.0
        
        max_type = max(scores, key=scores.get)
        max_score = scores[max_type]
        
        # Calculate confidence based on score
        total_matches = sum(scores.values())
        confidence = min(max_score / max(total_matches, 1), 1.0)
        
        # Boost confidence if multiple strong indicators
        if max_score >= 3:
            confidence = min(confidence + 0.2, 1.0)
        
        return max_type, confidence
    
    def _extract_specific_methods(self, text: str) -> List[str]:
        """
        Extract specific research methods mentioned.
        
        Args:
            text: Text to analyze
        
        Returns:
            List of specific method names
        """
        found_methods = []
        
        for method_name, patterns in self.SPECIFIC_METHODS.items():
            for pattern in patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    # Convert method_name to readable format
                    readable_name = method_name.replace('_', ' ').title()
                    if readable_name not in found_methods:
                        found_methods.append(readable_name)
                    break
        
        return found_methods
    
    def _extract_data_collection(self, content: str) -> str:
        """
        Extract data collection approach description.
        
        Args:
            content: Content to analyze
        
        Returns:
            Description of data collection approach
        """
        # Look for sentences containing data collection keywords
        data_keywords = [
            'data collection', 'data gathering', 'data were collected',
            'data was collected', 'participants were recruited',
            'sampling', 'sample was', 'recruited from'
        ]
        
        sentences = re.split(r'[.!?]+', content)
        relevant_sentences = []
        
        for sentence in sentences:
            sentence_lower = sentence.lower()
            if any(keyword in sentence_lower for keyword in data_keywords):
                relevant_sentences.append(sentence.strip())
                if len(relevant_sentences) >= 2:  # Limit to 2 sentences
                    break
        
        return '. '.join(relevant_sentences) + '.' if relevant_sentences else ""
    
    def _extract_analysis_techniques(self, text: str) -> List[str]:
        """
        Extract analysis techniques mentioned.
        
        Args:
            text: Text to analyze
        
        Returns:
            List of analysis technique names
        """
        found_techniques = []
        
        for technique_name, patterns in self.ANALYSIS_TECHNIQUES.items():
            for pattern in patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    # Convert technique_name to readable format
                    readable_name = technique_name.replace('_', ' ').title()
                    if readable_name not in found_techniques:
                        found_techniques.append(readable_name)
                    break
        
        return found_techniques
    
    def _extract_sample_info(self, content: str) -> str:
        """
        Extract sample/participant information.
        
        Args:
            content: Content to analyze
        
        Returns:
            Description of sample
        """
        # Look for sample size patterns
        sample_patterns = [
            r'n\s*=\s*(\d+)',
            r'sample\s+(?:of|size|consisted)\s+(?:of\s+)?(\d+)',
            r'(\d+)\s+participants?',
            r'(\d+)\s+subjects?',
        ]
        
        sample_info_parts = []
        
        for pattern in sample_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                sample_size = match.group(1)
                sample_info_parts.append(f"N={sample_size}")
                break
        
        # Look for demographic information
        demo_keywords = [
            'participants', 'subjects', 'respondents', 'sample',
            'age', 'gender', 'male', 'female'
        ]
        
        sentences = re.split(r'[.!?]+', content)
        for sentence in sentences:
            sentence_lower = sentence.lower()
            if any(keyword in sentence_lower for keyword in demo_keywords):
                if 'age' in sentence_lower or 'gender' in sentence_lower:
                    sample_info_parts.append(sentence.strip())
                    break
        
        return '; '.join(sample_info_parts) if sample_info_parts else ""
    
    def _extract_limitations(self, content: str) -> List[str]:
        """
        Extract methodological limitations.
        
        Args:
            content: Content to analyze
        
        Returns:
            List of limitation descriptions
        """
        limitations = []
        
        # Look for limitation section or keywords
        limitation_keywords = [
            'limitation', 'constraint', 'weakness', 'caveat',
            'restricted', 'limited by', 'could not'
        ]
        
        sentences = re.split(r'[.!?]+', content)
        for sentence in sentences:
            sentence_lower = sentence.lower()
            if any(keyword in sentence_lower for keyword in limitation_keywords):
                limitations.append(sentence.strip())
                if len(limitations) >= 3:  # Limit to 3 limitations
                    break
        
        return limitations


class TheoryExtractor:
    """
    Extracts theoretical frameworks and constructs from academic content.
    
    This class analyzes text to identify:
    - Theoretical frameworks and models
    - Key theoretical constructs
    - Definitions of constructs
    - Applications of theories
    - Citations to original theory papers
    """
    
    # Common theory keywords and patterns
    THEORY_PATTERNS = [
        r'\b(\w+(?:\s+\w+){0,3})\s+theory\b',
        r'\b(\w+(?:\s+\w+){0,3})\s+model\b',
        r'\b(\w+(?:\s+\w+){0,3})\s+framework\b',
        r'\b(\w+(?:\s+\w+){0,3})\s+paradigm\b',
        r'\btheory\s+of\s+(\w+(?:\s+\w+){0,3})\b',
        r'\bmodel\s+of\s+(\w+(?:\s+\w+){0,3})\b',
    ]
    
    # Theory type indicators
    THEORY_TYPES = {
        'psychological': ['cognitive', 'behavioral', 'social', 'developmental', 'personality'],
        'sociological': ['social', 'structural', 'institutional', 'cultural'],
        'economic': ['economic', 'market', 'rational', 'game'],
        'organizational': ['organizational', 'management', 'leadership', 'strategic'],
        'communication': ['communication', 'media', 'information'],
        'educational': ['learning', 'pedagogical', 'instructional', 'educational'],
        'computational': ['computational', 'algorithmic', 'information processing'],
    }
    
    def __init__(self):
        """Initialize the theory extractor"""
        pass
    
    def extract_theories(self, content: str, title: str = "") -> List[TheoryInfo]:
        """
        Extract theoretical frameworks from content.
        
        Args:
            content: Text content to analyze
            title: Optional paper title for additional context
        
        Returns:
            List of TheoryInfo objects
        
        Requirements:
            - 11.1: Identify theoretical frameworks and models
            - 11.2: Extract definitions of key constructs
        """
        combined_text = f"{title} {content}"
        
        # Extract theory names
        theory_names = self._extract_theory_names(combined_text)
        
        # Create TheoryInfo objects for each theory
        theories = []
        for theory_name in theory_names:
            theory_info = self._extract_theory_details(
                theory_name,
                content,
                combined_text
            )
            theories.append(theory_info)
        
        return theories
    
    def _extract_theory_names(self, text: str) -> Set[str]:
        """
        Extract theory names from text.
        
        Args:
            text: Text to analyze
        
        Returns:
            Set of theory names
        """
        theory_names = set()
        
        for pattern in self.THEORY_PATTERNS:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                # Clean up the match
                theory_name = match.strip()
                
                # Filter out common false positives
                if len(theory_name) < 3:
                    continue
                if theory_name.lower() in ['the', 'this', 'that', 'these', 'those']:
                    continue
                
                # Capitalize properly
                theory_name = ' '.join(word.capitalize() for word in theory_name.split())
                
                theory_names.add(theory_name)
        
        return theory_names
    
    def _extract_theory_details(
        self,
        theory_name: str,
        content: str,
        full_text: str
    ) -> TheoryInfo:
        """
        Extract detailed information about a specific theory.
        
        Args:
            theory_name: Name of the theory
            content: Content to analyze
            full_text: Full text including title
        
        Returns:
            TheoryInfo object with details
        """
        # Identify theory type
        theory_type = self._identify_theory_type(theory_name, full_text)
        
        # Extract key constructs
        key_constructs = self._extract_constructs(theory_name, content)
        
        # Extract definitions
        definitions = self._extract_definitions(key_constructs, content)
        
        # Extract applications
        applications = self._extract_applications(theory_name, content)
        
        # Calculate confidence
        confidence = self._calculate_confidence(theory_name, content)
        
        return TheoryInfo(
            theory_name=theory_name,
            theory_type=theory_type,
            key_constructs=key_constructs,
            definitions=definitions,
            applications=applications,
            confidence=confidence,
        )
    
    def _identify_theory_type(self, theory_name: str, text: str) -> str:
        """
        Identify the type of theory.
        
        Args:
            theory_name: Name of the theory
            text: Text to analyze
        
        Returns:
            Theory type string
        """
        theory_lower = theory_name.lower()
        text_lower = text.lower()
        
        # Check theory name for type indicators
        for theory_type, keywords in self.THEORY_TYPES.items():
            if any(keyword in theory_lower for keyword in keywords):
                return theory_type
        
        # Check surrounding context
        # Look for sentences mentioning the theory
        sentences = re.split(r'[.!?]+', text)
        relevant_sentences = []
        for sentence in sentences:
            if theory_name.lower() in sentence.lower():
                relevant_sentences.append(sentence.lower())
        
        context = ' '.join(relevant_sentences)
        
        for theory_type, keywords in self.THEORY_TYPES.items():
            if any(keyword in context for keyword in keywords):
                return theory_type
        
        return "general"
    
    def _extract_constructs(self, theory_name: str, content: str) -> List[str]:
        """
        Extract key theoretical constructs.
        
        Args:
            theory_name: Name of the theory
            content: Content to analyze
        
        Returns:
            List of construct names
        """
        constructs = []
        
        # Look for construct-related keywords near theory mentions
        construct_keywords = [
            'construct', 'concept', 'dimension', 'component',
            'factor', 'element', 'variable', 'aspect'
        ]
        
        sentences = re.split(r'[.!?]+', content)
        for sentence in sentences:
            sentence_lower = sentence.lower()
            
            # Check if sentence mentions the theory
            if theory_name.lower() in sentence_lower:
                # Look for construct keywords
                if any(keyword in sentence_lower for keyword in construct_keywords):
                    # Extract capitalized terms (likely construct names)
                    words = sentence.split()
                    for i, word in enumerate(words):
                        if word[0].isupper() and len(word) > 3:
                            if word not in constructs and word != theory_name:
                                constructs.append(word)
        
        return constructs[:5]  # Limit to 5 constructs
    
    def _extract_definitions(
        self,
        constructs: List[str],
        content: str
    ) -> Dict[str, str]:
        """
        Extract definitions for constructs.
        
        Args:
            constructs: List of construct names
            content: Content to analyze
        
        Returns:
            Dictionary mapping constructs to definitions
        """
        definitions = {}
        
        # Look for definition patterns
        definition_patterns = [
            r'{construct}\s+(?:is|refers to|means|represents)\s+([^.!?]+)',
            r'{construct}\s+(?:can be )?defined as\s+([^.!?]+)',
            r'(?:the|a)\s+{construct}\s+(?:is|refers to)\s+([^.!?]+)',
        ]
        
        for construct in constructs:
            for pattern_template in definition_patterns:
                pattern = pattern_template.replace('{construct}', re.escape(construct))
                match = re.search(pattern, content, re.IGNORECASE)
                if match:
                    definition = match.group(1).strip()
                    definitions[construct] = definition
                    break
        
        return definitions
    
    def _extract_applications(self, theory_name: str, content: str) -> str:
        """
        Extract how the theory is applied.
        
        Args:
            theory_name: Name of the theory
            content: Content to analyze
        
        Returns:
            Description of applications
        """
        # Look for application keywords near theory mentions
        application_keywords = [
            'applied', 'application', 'used to', 'employed',
            'utilized', 'implemented', 'operationalized'
        ]
        
        sentences = re.split(r'[.!?]+', content)
        application_sentences = []
        
        for sentence in sentences:
            sentence_lower = sentence.lower()
            if theory_name.lower() in sentence_lower:
                if any(keyword in sentence_lower for keyword in application_keywords):
                    application_sentences.append(sentence.strip())
                    if len(application_sentences) >= 2:
                        break
        
        return '. '.join(application_sentences) + '.' if application_sentences else ""
    
    def _calculate_confidence(self, theory_name: str, content: str) -> float:
        """
        Calculate confidence in theory extraction.
        
        Args:
            theory_name: Name of the theory
            content: Content to analyze
        
        Returns:
            Confidence score (0-1)
        """
        # Count mentions of the theory
        mentions = len(re.findall(re.escape(theory_name), content, re.IGNORECASE))
        
        # Base confidence on number of mentions
        if mentions >= 5:
            confidence = 0.9
        elif mentions >= 3:
            confidence = 0.7
        elif mentions >= 2:
            confidence = 0.5
        else:
            confidence = 0.3
        
        return confidence


def extract_methodology_and_theories(
    content: str,
    title: str = ""
) -> Dict[str, Any]:
    """
    Convenience function to extract both methodology and theories.
    
    Args:
        content: Text content to analyze
        title: Optional paper title
    
    Returns:
        Dictionary with 'methodology' and 'theories' keys
    
    Example:
        >>> content = "This qualitative study used interviews..."
        >>> result = extract_methodology_and_theories(content)
        >>> print(result['methodology'].methodology_type)
        qualitative
    """
    methodology_extractor = MethodologyExtractor()
    theory_extractor = TheoryExtractor()
    
    methodology = methodology_extractor.extract_methodology(content, title)
    theories = theory_extractor.extract_theories(content, title)
    
    return {
        'methodology': methodology,
        'theories': theories,
    }
