#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Source Credibility Evaluation Module for Gazzali Research

This module provides source credibility assessment, quality scoring, and
tracking for academic research. It evaluates sources based on publication
type, venue reputation, and academic indicators.

Requirements addressed:
- 1.4: Source credibility evaluation by prioritizing recognized publishers
- 7.1: Quality of evidence evaluation using established frameworks
"""

from __future__ import annotations

import re
import logging
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from enum import Enum


# Configure logging
logger = logging.getLogger(__name__)


class SourceType(str, Enum):
    """Types of sources with associated credibility levels"""
    PEER_REVIEWED_JOURNAL = "peer_reviewed_journal"
    CONFERENCE_PROCEEDINGS = "conference_proceedings"
    ACADEMIC_BOOK = "academic_book"
    INSTITUTIONAL_PUBLICATION = "institutional_publication"
    PREPRINT = "preprint"
    THESIS_DISSERTATION = "thesis_dissertation"
    GOVERNMENT_REPORT = "government_report"
    PROFESSIONAL_PUBLICATION = "professional_publication"
    GENERAL_WEB = "general_web"
    UNKNOWN = "unknown"


@dataclass
class CredibilityScore:
    """
    Represents the credibility assessment of a source.
    
    Attributes:
        score: Numerical credibility score (0-10)
        source_type: Type of source
        is_peer_reviewed: Whether the source is peer-reviewed
        is_open_access: Whether the source is openly accessible
        venue_reputation: Reputation score of the publication venue (0-10)
        citation_count: Number of citations (if available)
        recency_score: Score based on publication recency (0-10)
        overall_quality: Overall quality assessment
        warnings: List of quality warnings or concerns
        strengths: List of source strengths
    """
    score: float
    source_type: SourceType
    is_peer_reviewed: bool = False
    is_open_access: bool = False
    venue_reputation: float = 0.0
    citation_count: Optional[int] = None
    recency_score: float = 5.0
    overall_quality: str = "moderate"
    warnings: List[str] = field(default_factory=list)
    strengths: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation"""
        return {
            "score": self.score,
            "source_type": self.source_type.value,
            "is_peer_reviewed": self.is_peer_reviewed,
            "is_open_access": self.is_open_access,
            "venue_reputation": self.venue_reputation,
            "citation_count": self.citation_count,
            "recency_score": self.recency_score,
            "overall_quality": self.overall_quality,
            "warnings": self.warnings,
            "strengths": self.strengths,
        }


class SourceCredibilityEvaluator:
    """
    Evaluates source credibility and tracks quality metrics.
    
    This class provides methods to:
    - Score sources based on type and characteristics
    - Identify peer-reviewed sources
    - Assess venue reputation
    - Track source quality statistics
    - Generate quality warnings
    """
    
    # Base scores for different source types
    SOURCE_TYPE_SCORES = {
        SourceType.PEER_REVIEWED_JOURNAL: 10,
        SourceType.CONFERENCE_PROCEEDINGS: 9,
        SourceType.ACADEMIC_BOOK: 9,
        SourceType.INSTITUTIONAL_PUBLICATION: 7,
        SourceType.THESIS_DISSERTATION: 7,
        SourceType.GOVERNMENT_REPORT: 7,
        SourceType.PREPRINT: 6,
        SourceType.PROFESSIONAL_PUBLICATION: 5,
        SourceType.GENERAL_WEB: 3,
        SourceType.UNKNOWN: 2,
    }
    
    # High-reputation journal patterns
    HIGH_REPUTATION_JOURNALS = [
        r'\bnature\b',
        r'\bscience\b',
        r'\bcell\b',
        r'\blancet\b',
        r'\bnejm\b',
        r'\bnew england journal',
        r'\bjama\b',
        r'\bbmj\b',
        r'\bpnas\b',
        r'\bproceedings of the national academy',
        r'\bacm\b',
        r'\bieee\b',
        r'\bplos\b',
    ]
    
    # Institutional domains indicating academic sources
    ACADEMIC_DOMAINS = [
        r'\.edu$',
        r'\.ac\.uk$',
        r'\.edu\.au$',
        r'\.edu\.cn$',
        r'arxiv\.org',
        r'biorxiv\.org',
        r'ssrn\.com',
        r'researchgate\.net',
        r'scholar\.google',
        r'pubmed\.ncbi',
        r'doi\.org',
        r'springer\.com',
        r'sciencedirect\.com',
        r'wiley\.com',
        r'tandfonline\.com',
        r'sagepub\.com',
        r'jstor\.org',
    ]
    
    # Government and institutional domains
    INSTITUTIONAL_DOMAINS = [
        r'\.gov$',
        r'\.gov\.uk$',
        r'\.gc\.ca$',
        r'who\.int',
        r'worldbank\.org',
        r'oecd\.org',
        r'un\.org',
        r'europa\.eu',
    ]
    
    def __init__(self, min_quality_threshold: float = 7.0):
        """
        Initialize source credibility evaluator.
        
        Args:
            min_quality_threshold: Minimum quality score for sources (0-10)
        """
        self.min_quality_threshold = min_quality_threshold
        self.evaluated_sources: List[CredibilityScore] = []
        self._peer_reviewed_count = 0
        self._total_count = 0
    
    def evaluate_source(
        self,
        title: str,
        venue: str = "",
        url: str = "",
        venue_type: str = "other",
        citation_count: Optional[int] = None,
        year: Optional[int] = None,
        is_open_access: bool = False,
        abstract: str = "",
    ) -> CredibilityScore:
        """
        Evaluate the credibility of a source.
        
        Args:
            title: Source title
            venue: Publication venue
            url: Source URL
            venue_type: Type of venue (journal, conference, book, etc.)
            citation_count: Number of citations
            year: Publication year
            is_open_access: Whether source is open access
            abstract: Abstract text
        
        Returns:
            CredibilityScore object with assessment
        """
        # Determine source type
        source_type = self._identify_source_type(venue, url, venue_type)
        
        # Get base score
        base_score = self.SOURCE_TYPE_SCORES.get(source_type, 2.0)
        
        # Check if peer-reviewed
        is_peer_reviewed = self._is_peer_reviewed(source_type, venue, url)
        
        # Assess venue reputation
        venue_reputation = self._assess_venue_reputation(venue, url)
        
        # Calculate recency score
        recency_score = self._calculate_recency_score(year)
        
        # Calculate final score with adjustments
        final_score = self._calculate_final_score(
            base_score=base_score,
            venue_reputation=venue_reputation,
            citation_count=citation_count,
            recency_score=recency_score,
            is_open_access=is_open_access,
        )
        
        # Determine overall quality
        overall_quality = self._determine_quality_level(final_score)
        
        # Generate warnings and strengths
        warnings = self._generate_warnings(
            source_type=source_type,
            final_score=final_score,
            citation_count=citation_count,
            year=year,
            venue=venue,
        )
        
        strengths = self._generate_strengths(
            source_type=source_type,
            is_peer_reviewed=is_peer_reviewed,
            venue_reputation=venue_reputation,
            citation_count=citation_count,
            is_open_access=is_open_access,
        )
        
        # Create credibility score
        credibility = CredibilityScore(
            score=final_score,
            source_type=source_type,
            is_peer_reviewed=is_peer_reviewed,
            is_open_access=is_open_access,
            venue_reputation=venue_reputation,
            citation_count=citation_count,
            recency_score=recency_score,
            overall_quality=overall_quality,
            warnings=warnings,
            strengths=strengths,
        )
        
        # Track statistics
        self.evaluated_sources.append(credibility)
        self._total_count += 1
        if is_peer_reviewed:
            self._peer_reviewed_count += 1
        
        # Log warnings if score is below threshold
        if final_score < self.min_quality_threshold:
            logger.warning(
                f"Source quality below threshold ({final_score:.1f} < {self.min_quality_threshold}): "
                f"{title[:50]}... ({source_type.value})"
            )
        
        return credibility
    
    def _identify_source_type(self, venue: str, url: str, venue_type: str) -> SourceType:
        """
        Identify the type of source based on venue, URL, and metadata.
        
        Args:
            venue: Publication venue
            url: Source URL
            venue_type: Venue type from metadata
        
        Returns:
            SourceType enum value
        """
        venue_lower = venue.lower()
        url_lower = url.lower()
        
        # Check for preprints
        if any(pattern in url_lower for pattern in ['arxiv', 'biorxiv', 'medrxiv', 'ssrn']):
            return SourceType.PREPRINT
        
        if 'preprint' in venue_lower:
            return SourceType.PREPRINT
        
        # Check for thesis/dissertation
        if any(term in venue_lower for term in ['thesis', 'dissertation', 'phd', 'master']):
            return SourceType.THESIS_DISSERTATION
        
        # Check for government reports
        if any(pattern in url_lower for pattern in ['.gov', 'who.int', 'worldbank', 'oecd']):
            return SourceType.GOVERNMENT_REPORT
        
        # Check for academic books
        if venue_type == 'book' or 'book' in venue_lower:
            # Check if from academic publisher
            if any(pub in venue_lower for pub in ['springer', 'cambridge', 'oxford', 'wiley', 'elsevier']):
                return SourceType.ACADEMIC_BOOK
        
        # Check for conference proceedings
        if venue_type == 'conference' or any(term in venue_lower for term in ['conference', 'proceedings', 'symposium', 'workshop']):
            return SourceType.CONFERENCE_PROCEEDINGS
        
        # Check for peer-reviewed journals
        if venue_type == 'journal' or 'journal' in venue_lower:
            return SourceType.PEER_REVIEWED_JOURNAL
        
        # Check for institutional publications
        if any(re.search(pattern, url_lower) for pattern in self.INSTITUTIONAL_DOMAINS):
            return SourceType.INSTITUTIONAL_PUBLICATION
        
        # Check for academic domains
        if any(re.search(pattern, url_lower) for pattern in self.ACADEMIC_DOMAINS):
            # Could be various academic types, default to institutional
            return SourceType.INSTITUTIONAL_PUBLICATION
        
        # Check for professional publications
        if any(term in venue_lower for term in ['magazine', 'newsletter', 'bulletin', 'report']):
            return SourceType.PROFESSIONAL_PUBLICATION
        
        # Default to general web if no academic indicators
        if url and not any(re.search(pattern, url_lower) for pattern in self.ACADEMIC_DOMAINS):
            return SourceType.GENERAL_WEB
        
        return SourceType.UNKNOWN
    
    def _is_peer_reviewed(self, source_type: SourceType, venue: str, url: str) -> bool:
        """
        Determine if a source is peer-reviewed.
        
        Args:
            source_type: Type of source
            venue: Publication venue
            url: Source URL
        
        Returns:
            True if peer-reviewed, False otherwise
        """
        # Peer-reviewed source types
        if source_type in [
            SourceType.PEER_REVIEWED_JOURNAL,
            SourceType.CONFERENCE_PROCEEDINGS,
            SourceType.ACADEMIC_BOOK,
        ]:
            return True
        
        # Check venue for peer-review indicators
        venue_lower = venue.lower()
        if any(term in venue_lower for term in ['journal', 'proceedings', 'transactions']):
            # Exclude predatory or non-peer-reviewed journals
            if not any(term in venue_lower for term in ['blog', 'magazine', 'news']):
                return True
        
        # Check URL for academic publishers (usually peer-reviewed)
        url_lower = url.lower()
        academic_publishers = [
            'springer', 'elsevier', 'wiley', 'sage', 'taylor', 'oxford',
            'cambridge', 'ieee', 'acm', 'nature', 'science', 'cell',
            'plos', 'frontiers', 'mdpi', 'hindawi'
        ]
        
        if any(pub in url_lower for pub in academic_publishers):
            return True
        
        return False
    
    def _assess_venue_reputation(self, venue: str, url: str) -> float:
        """
        Assess the reputation of the publication venue.
        
        Args:
            venue: Publication venue
            url: Source URL
        
        Returns:
            Reputation score (0-10)
        """
        venue_lower = venue.lower()
        url_lower = url.lower()
        
        # Check for high-reputation journals
        for pattern in self.HIGH_REPUTATION_JOURNALS:
            if re.search(pattern, venue_lower, re.IGNORECASE):
                return 10.0
        
        # Check for well-known academic publishers
        high_reputation_publishers = {
            'nature': 10.0,
            'science': 10.0,
            'cell': 10.0,
            'lancet': 10.0,
            'nejm': 10.0,
            'jama': 10.0,
            'bmj': 10.0,
            'pnas': 9.5,
            'ieee': 9.0,
            'acm': 9.0,
            'springer': 8.0,
            'elsevier': 8.0,
            'wiley': 8.0,
            'oxford': 8.5,
            'cambridge': 8.5,
            'sage': 7.5,
            'taylor': 7.5,
        }
        
        for publisher, score in high_reputation_publishers.items():
            if publisher in venue_lower or publisher in url_lower:
                return score
        
        # Default reputation scores by source indicators
        if any(term in venue_lower for term in ['journal', 'proceedings']):
            return 7.0  # Moderate reputation for unidentified journals
        
        if any(re.search(pattern, url_lower) for pattern in self.ACADEMIC_DOMAINS):
            return 6.0  # Academic domain but unknown venue
        
        return 3.0  # Low reputation for general sources
    
    def _calculate_recency_score(self, year: Optional[int]) -> float:
        """
        Calculate recency score based on publication year.
        
        More recent publications get higher scores.
        
        Args:
            year: Publication year
        
        Returns:
            Recency score (0-10)
        """
        if not year:
            return 5.0  # Neutral score if year unknown
        
        from datetime import datetime
        current_year = datetime.now().year
        age = current_year - year
        
        if age < 0:
            return 5.0  # Future date, neutral score
        elif age <= 2:
            return 10.0  # Very recent
        elif age <= 5:
            return 9.0  # Recent
        elif age <= 10:
            return 7.0  # Moderately recent
        elif age <= 20:
            return 5.0  # Older but still relevant
        else:
            return 3.0  # Old, may be outdated
    
    def _calculate_final_score(
        self,
        base_score: float,
        venue_reputation: float,
        citation_count: Optional[int],
        recency_score: float,
        is_open_access: bool,
    ) -> float:
        """
        Calculate final credibility score with adjustments.
        
        Args:
            base_score: Base score from source type
            venue_reputation: Venue reputation score
            citation_count: Number of citations
            recency_score: Recency score
            is_open_access: Whether source is open access
        
        Returns:
            Final credibility score (0-10)
        """
        # Start with base score
        score = base_score
        
        # Adjust for venue reputation (weighted 30%)
        score = score * 0.7 + venue_reputation * 0.3
        
        # Adjust for citation count (bonus up to +1.0)
        if citation_count is not None:
            if citation_count >= 1000:
                score += 1.0
            elif citation_count >= 500:
                score += 0.8
            elif citation_count >= 100:
                score += 0.6
            elif citation_count >= 50:
                score += 0.4
            elif citation_count >= 10:
                score += 0.2
        
        # Adjust for recency (weighted 10%)
        score = score * 0.9 + recency_score * 0.1
        
        # Small bonus for open access (promotes accessibility)
        if is_open_access:
            score += 0.2
        
        # Ensure score is within bounds
        return min(10.0, max(0.0, score))
    
    def _determine_quality_level(self, score: float) -> str:
        """
        Determine overall quality level from score.
        
        Args:
            score: Credibility score
        
        Returns:
            Quality level string
        """
        if score >= 9.0:
            return "excellent"
        elif score >= 7.5:
            return "high"
        elif score >= 6.0:
            return "good"
        elif score >= 4.0:
            return "moderate"
        elif score >= 2.0:
            return "low"
        else:
            return "very_low"
    
    def _generate_warnings(
        self,
        source_type: SourceType,
        final_score: float,
        citation_count: Optional[int],
        year: Optional[int],
        venue: str,
    ) -> List[str]:
        """
        Generate quality warnings for the source.
        
        Args:
            source_type: Type of source
            final_score: Final credibility score
            citation_count: Number of citations
            year: Publication year
            venue: Publication venue
        
        Returns:
            List of warning messages
        """
        warnings = []
        
        # Low overall score
        if final_score < 4.0:
            warnings.append("Low credibility score - verify information with additional sources")
        
        # Non-peer-reviewed sources
        if source_type in [SourceType.GENERAL_WEB, SourceType.UNKNOWN]:
            warnings.append("Non-academic source - may lack peer review")
        
        if source_type == SourceType.PREPRINT:
            warnings.append("Preprint - not yet peer-reviewed")
        
        # Low citation count
        if citation_count is not None and citation_count < 5:
            warnings.append("Low citation count - limited validation by research community")
        
        # Old publication
        if year:
            from datetime import datetime
            age = datetime.now().year - year
            if age > 20:
                warnings.append(f"Published {age} years ago - findings may be outdated")
        
        # Missing venue information
        if not venue or venue.strip() == "":
            warnings.append("Publication venue unknown - difficult to assess credibility")
        
        return warnings
    
    def _generate_strengths(
        self,
        source_type: SourceType,
        is_peer_reviewed: bool,
        venue_reputation: float,
        citation_count: Optional[int],
        is_open_access: bool,
    ) -> List[str]:
        """
        Generate strength indicators for the source.
        
        Args:
            source_type: Type of source
            is_peer_reviewed: Whether source is peer-reviewed
            venue_reputation: Venue reputation score
            citation_count: Number of citations
            is_open_access: Whether source is open access
        
        Returns:
            List of strength messages
        """
        strengths = []
        
        # Peer-reviewed
        if is_peer_reviewed:
            strengths.append("Peer-reviewed publication")
        
        # High-reputation venue
        if venue_reputation >= 9.0:
            strengths.append("Published in high-impact venue")
        elif venue_reputation >= 7.5:
            strengths.append("Published in reputable venue")
        
        # High citation count
        if citation_count is not None:
            if citation_count >= 1000:
                strengths.append(f"Highly cited ({citation_count:,} citations)")
            elif citation_count >= 100:
                strengths.append(f"Well-cited ({citation_count} citations)")
        
        # Open access
        if is_open_access:
            strengths.append("Open access - freely available")
        
        # Academic source types
        if source_type in [SourceType.PEER_REVIEWED_JOURNAL, SourceType.CONFERENCE_PROCEEDINGS]:
            strengths.append("Academic publication")
        
        return strengths
    
    def get_peer_reviewed_percentage(self) -> float:
        """
        Get percentage of peer-reviewed sources.
        
        Returns:
            Percentage (0-100)
        """
        if self._total_count == 0:
            return 0.0
        return (self._peer_reviewed_count / self._total_count) * 100
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about evaluated sources.
        
        Returns:
            Dictionary with statistics
        """
        if not self.evaluated_sources:
            return {
                "total_sources": 0,
                "peer_reviewed_count": 0,
                "peer_reviewed_percentage": 0.0,
                "average_score": 0.0,
                "high_quality_count": 0,
                "low_quality_count": 0,
                "source_type_distribution": {},
            }
        
        # Calculate statistics
        total = len(self.evaluated_sources)
        peer_reviewed = sum(1 for s in self.evaluated_sources if s.is_peer_reviewed)
        average_score = sum(s.score for s in self.evaluated_sources) / total
        high_quality = sum(1 for s in self.evaluated_sources if s.score >= self.min_quality_threshold)
        low_quality = sum(1 for s in self.evaluated_sources if s.score < 4.0)
        
        # Source type distribution
        type_dist = {}
        for source in self.evaluated_sources:
            stype = source.source_type.value
            type_dist[stype] = type_dist.get(stype, 0) + 1
        
        return {
            "total_sources": total,
            "peer_reviewed_count": peer_reviewed,
            "peer_reviewed_percentage": (peer_reviewed / total) * 100,
            "average_score": average_score,
            "high_quality_count": high_quality,
            "low_quality_count": low_quality,
            "source_type_distribution": type_dist,
            "quality_threshold": self.min_quality_threshold,
        }
    
    def log_quality_summary(self):
        """Log a summary of source quality statistics"""
        stats = self.get_statistics()
        
        logger.info("=" * 60)
        logger.info("SOURCE QUALITY SUMMARY")
        logger.info("=" * 60)
        logger.info(f"Total sources evaluated: {stats['total_sources']}")
        logger.info(f"Peer-reviewed sources: {stats['peer_reviewed_count']} ({stats['peer_reviewed_percentage']:.1f}%)")
        logger.info(f"Average quality score: {stats['average_score']:.2f}/10")
        logger.info(f"High-quality sources (≥{stats['quality_threshold']}): {stats['high_quality_count']}")
        logger.info(f"Low-quality sources (<4.0): {stats['low_quality_count']}")
        
        if stats['source_type_distribution']:
            logger.info("\nSource type distribution:")
            for stype, count in sorted(stats['source_type_distribution'].items(), key=lambda x: x[1], reverse=True):
                logger.info(f"  - {stype}: {count}")
        
        logger.info("=" * 60)
    
    def filter_low_quality_sources(self, sources: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Filter out sources below quality threshold.
        
        Args:
            sources: List of source dictionaries
        
        Returns:
            Filtered list of sources
        """
        filtered = []
        
        for source in sources:
            # Evaluate source
            credibility = self.evaluate_source(
                title=source.get('title', ''),
                venue=source.get('venue', ''),
                url=source.get('url', ''),
                venue_type=source.get('venue_type', 'other'),
                citation_count=source.get('citation_count'),
                year=source.get('year'),
                is_open_access=source.get('is_open_access', False),
            )
            
            # Include if above threshold
            if credibility.score >= self.min_quality_threshold:
                # Add credibility info to source
                source['credibility_score'] = credibility.score
                source['credibility_assessment'] = credibility.to_dict()
                filtered.append(source)
            else:
                logger.info(
                    f"Filtered out low-quality source (score: {credibility.score:.1f}): "
                    f"{source.get('title', 'Unknown')[:50]}..."
                )
        
        return filtered
