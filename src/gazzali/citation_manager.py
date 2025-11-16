#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Citation Manager Module for Gazzali Research

This module provides citation tracking, formatting, and bibliography generation
for academic research. It supports multiple citation styles (APA, MLA, Chicago, IEEE)
and handles citation extraction from various sources.

Requirements addressed:
- 2.1: Automatic citation capture for all sources
- 2.2: Citation formatting in multiple academic styles
- 2.5: Citation deduplication and tracking
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum


class CitationStyle(str, Enum):
    """Supported citation styles"""
    APA = "apa"
    MLA = "mla"
    CHICAGO = "chicago"
    IEEE = "ieee"


class VenueType(str, Enum):
    """Types of publication venues"""
    JOURNAL = "journal"
    CONFERENCE = "conference"
    BOOK = "book"
    PREPRINT = "preprint"
    THESIS = "thesis"
    WEB = "web"
    OTHER = "other"


@dataclass
class Citation:
    """
    Represents a single academic citation with bibliographic metadata.
    
    Attributes:
        citation_id: Unique identifier for this citation
        authors: List of author names
        year: Publication year
        title: Publication title
        venue: Publication venue (journal, conference, book name)
        venue_type: Type of publication venue
        volume: Volume number (for journals)
        issue: Issue number (for journals)
        pages: Page numbers or range
        doi: Digital Object Identifier
        url: Web URL for the source
        pdf_url: Direct link to PDF if available
        citation_count: Number of citations (from Scholar)
        abstract: Abstract text
        keywords: List of keywords or tags
        access_date: Date the source was accessed
        is_open_access: Whether the source is freely available
        is_incomplete: Flag for citations with missing metadata
    """
    citation_id: str
    authors: List[str]
    year: int
    title: str
    venue: str
    venue_type: VenueType = VenueType.OTHER
    volume: Optional[str] = None
    issue: Optional[str] = None
    pages: Optional[str] = None
    doi: Optional[str] = None
    url: str = ""
    pdf_url: Optional[str] = None
    citation_count: Optional[int] = None
    abstract: Optional[str] = None
    keywords: List[str] = field(default_factory=list)
    access_date: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d"))
    is_open_access: bool = False
    is_incomplete: bool = False
    
    def format(self, style: CitationStyle = CitationStyle.APA) -> str:
        """
        Format citation in the specified style.
        
        Args:
            style: Citation style to use (APA, MLA, Chicago, IEEE)
        
        Returns:
            Formatted citation string
        """
        if style == CitationStyle.APA:
            return self._format_apa()
        elif style == CitationStyle.MLA:
            return self._format_mla()
        elif style == CitationStyle.CHICAGO:
            return self._format_chicago()
        elif style == CitationStyle.IEEE:
            return self._format_ieee()
        else:
            return self._format_apa()  # Default to APA
    
    def _format_apa(self) -> str:
        """Format citation in APA 7th edition style"""
        # Authors (Last, F. M.)
        if not self.authors:
            author_str = "[No author]"
        elif len(self.authors) == 1:
            author_str = self._format_author_apa(self.authors[0])
        elif len(self.authors) == 2:
            author_str = f"{self._format_author_apa(self.authors[0])}, & {self._format_author_apa(self.authors[1])}"
        elif len(self.authors) <= 20:
            authors_formatted = [self._format_author_apa(a) for a in self.authors[:-1]]
            author_str = ", ".join(authors_formatted) + f", & {self._format_author_apa(self.authors[-1])}"
        else:
            # More than 20 authors: list first 19, then "...", then last
            authors_formatted = [self._format_author_apa(a) for a in self.authors[:19]]
            author_str = ", ".join(authors_formatted) + f", ... {self._format_author_apa(self.authors[-1])}"
        
        # Year
        year_str = f"({self.year})" if self.year else "(n.d.)"
        
        # Title (sentence case for articles, title case for books)
        title_str = self.title
        if not title_str.endswith('.'):
            title_str += '.'
        
        # Venue information
        venue_str = ""
        if self.venue_type == VenueType.JOURNAL:
            venue_str = f"{self.venue}"
            if self.volume:
                venue_str += f", {self.volume}"
            if self.issue:
                venue_str += f"({self.issue})"
            if self.pages:
                venue_str += f", {self.pages}"
            venue_str += "."
        elif self.venue_type == VenueType.BOOK:
            venue_str = f"{self.venue}."
        elif self.venue_type == VenueType.CONFERENCE:
            venue_str = f"In {self.venue}"
            if self.pages:
                venue_str += f" (pp. {self.pages})"
            venue_str += "."
        else:
            venue_str = f"{self.venue}." if self.venue else ""
        
        # DOI or URL
        link_str = ""
        if self.doi:
            link_str = f" https://doi.org/{self.doi}"
        elif self.url:
            link_str = f" {self.url}"
        
        # Combine all parts
        citation = f"{author_str} {year_str}. {title_str} {venue_str}{link_str}"
        
        # Add incomplete flag if needed
        if self.is_incomplete:
            citation += " [Incomplete citation]"
        
        return citation.strip()
    
    def _format_mla(self) -> str:
        """Format citation in MLA 9th edition style"""
        # Authors (Last, First)
        if not self.authors:
            author_str = "[No author]"
        elif len(self.authors) == 1:
            author_str = self._format_author_mla(self.authors[0])
        elif len(self.authors) == 2:
            author_str = f"{self._format_author_mla(self.authors[0])}, and {self._format_author_mla(self.authors[1])}"
        else:
            author_str = f"{self._format_author_mla(self.authors[0])}, et al"
        
        # Title (in quotes for articles, italics for books)
        if self.venue_type in [VenueType.JOURNAL, VenueType.CONFERENCE]:
            title_str = f'"{self.title}."'
        else:
            title_str = f"{self.title}."
        
        # Venue
        venue_str = f"{self.venue}," if self.venue else ""
        
        # Volume and issue
        vol_issue = ""
        if self.volume:
            vol_issue = f" vol. {self.volume},"
        if self.issue:
            vol_issue += f" no. {self.issue},"
        
        # Year
        year_str = f" {self.year}," if self.year else ""
        
        # Pages
        pages_str = f" pp. {self.pages}." if self.pages else "."
        
        # URL or DOI
        link_str = ""
        if self.doi:
            link_str = f" https://doi.org/{self.doi}."
        elif self.url:
            link_str = f" {self.url}. Accessed {self.access_date}."
        
        citation = f"{author_str} {title_str} {venue_str}{vol_issue}{year_str}{pages_str}{link_str}"
        
        if self.is_incomplete:
            citation += " [Incomplete citation]"
        
        return citation.strip()
    
    def _format_chicago(self) -> str:
        """Format citation in Chicago 17th edition style (author-date)"""
        # Authors (Last, First)
        if not self.authors:
            author_str = "[No author]"
        elif len(self.authors) == 1:
            author_str = self._format_author_chicago(self.authors[0])
        elif len(self.authors) == 2:
            author_str = f"{self._format_author_chicago(self.authors[0])}, and {self._format_author_chicago(self.authors[1])}"
        elif len(self.authors) == 3:
            author_str = f"{self._format_author_chicago(self.authors[0])}, {self._format_author_chicago(self.authors[1])}, and {self._format_author_chicago(self.authors[2])}"
        else:
            author_str = f"{self._format_author_chicago(self.authors[0])} et al."
        
        # Year
        year_str = f" {self.year}." if self.year else " n.d."
        
        # Title
        title_str = f' "{self.title}."' if self.venue_type in [VenueType.JOURNAL, VenueType.CONFERENCE] else f" {self.title}."
        
        # Venue
        venue_str = f" {self.venue}" if self.venue else ""
        
        # Volume, issue, pages
        if self.volume:
            venue_str += f" {self.volume}"
        if self.issue:
            venue_str += f", no. {self.issue}"
        if self.pages:
            venue_str += f": {self.pages}"
        venue_str += "."
        
        # DOI or URL
        link_str = ""
        if self.doi:
            link_str = f" https://doi.org/{self.doi}."
        elif self.url:
            link_str = f" {self.url}."
        
        citation = f"{author_str}.{year_str}{title_str}{venue_str}{link_str}"
        
        if self.is_incomplete:
            citation += " [Incomplete citation]"
        
        return citation.strip()
    
    def _format_ieee(self) -> str:
        """Format citation in IEEE style"""
        # Authors (F. M. Last)
        if not self.authors:
            author_str = "[No author]"
        elif len(self.authors) <= 6:
            authors_formatted = [self._format_author_ieee(a) for a in self.authors]
            author_str = ", ".join(authors_formatted)
        else:
            # More than 6: list first author and "et al."
            author_str = f"{self._format_author_ieee(self.authors[0])} et al."
        
        # Title
        title_str = f'"{self.title},"'
        
        # Venue
        venue_str = f" {self.venue}," if self.venue else ""
        
        # Volume, issue, pages, year
        details = []
        if self.volume:
            details.append(f"vol. {self.volume}")
        if self.issue:
            details.append(f"no. {self.issue}")
        if self.pages:
            details.append(f"pp. {self.pages}")
        if self.year:
            details.append(str(self.year))
        
        details_str = ", ".join(details) + "." if details else ""
        
        # DOI or URL
        link_str = ""
        if self.doi:
            link_str = f" doi: {self.doi}."
        elif self.url:
            link_str = f" [Online]. Available: {self.url}"
        
        citation = f"{author_str}, {title_str}{venue_str} {details_str}{link_str}"
        
        if self.is_incomplete:
            citation += " [Incomplete citation]"
        
        return citation.strip()
    
    def _format_author_apa(self, author: str) -> str:
        """Format author name for APA style (Last, F. M.)"""
        author = author.strip()
        if not author:
            return ""
        
        # Check if already in "Last, First" format
        if ',' in author:
            parts = author.split(',', 1)
            last = parts[0].strip()
            first = parts[1].strip() if len(parts) > 1 else ""
            if first:
                # Extract initials from first name
                first_parts = first.split()
                initials = " ".join([f"{p[0]}." for p in first_parts if p])
                return f"{last}, {initials}"
            return last
        else:
            # Assume "First Last" format
            parts = author.split()
            if len(parts) == 0:
                return ""
            elif len(parts) == 1:
                return parts[0]
            else:
                # Last name is last part, rest are first/middle names
                last = parts[-1]
                initials = " ".join([f"{p[0]}." for p in parts[:-1] if p])
                return f"{last}, {initials}"
    
    def _format_author_mla(self, author: str) -> str:
        """Format author name for MLA style (Last, First)"""
        author = author.strip()
        if not author:
            return ""
        
        # Check if already in "Last, First" format
        if ',' in author:
            return author  # Already in correct format
        else:
            # Assume "First Last" format
            parts = author.split()
            if len(parts) == 0:
                return ""
            elif len(parts) == 1:
                return parts[0]
            else:
                last = parts[-1]
                first = " ".join(parts[:-1])
                return f"{last}, {first}"
    
    def _format_author_chicago(self, author: str) -> str:
        """Format author name for Chicago style (Last, First)"""
        return self._format_author_mla(author)
    
    def _format_author_ieee(self, author: str) -> str:
        """Format author name for IEEE style (F. M. Last)"""
        author = author.strip()
        if not author:
            return ""
        
        # Check if in "Last, First" format
        if ',' in author:
            parts = author.split(',', 1)
            last = parts[0].strip()
            first = parts[1].strip() if len(parts) > 1 else ""
            if first:
                # Extract initials from first name
                first_parts = first.split()
                initials = " ".join([f"{p[0]}." for p in first_parts if p])
                return f"{initials} {last}"
            return last
        else:
            # Assume "First Last" format
            parts = author.split()
            if len(parts) == 0:
                return ""
            elif len(parts) == 1:
                return parts[0]
            else:
                last = parts[-1]
                initials = " ".join([f"{p[0]}." for p in parts[:-1] if p])
                return f"{initials} {last}"
    
    def get_inline_citation(self, style: CitationStyle = CitationStyle.APA, page: Optional[str] = None) -> str:
        """
        Generate inline citation for use in text.
        
        Args:
            style: Citation style to use
            page: Optional page number for the citation
        
        Returns:
            Inline citation string (e.g., "(Smith, 2020)" for APA)
        """
        def extract_last_name(author: str) -> str:
            """Extract last name from author string"""
            author = author.strip()
            if ',' in author:
                # "Last, First" format
                return author.split(',')[0].strip()
            else:
                # "First Last" format
                return author.split()[-1] if author.split() else author
        
        if style == CitationStyle.APA or style == CitationStyle.CHICAGO:
            # (Author, Year) or (Author, Year, p. X)
            if not self.authors:
                author = "[No author]"
            elif len(self.authors) == 1:
                author = extract_last_name(self.authors[0])
            elif len(self.authors) == 2:
                author = f"{extract_last_name(self.authors[0])} & {extract_last_name(self.authors[1])}"
            else:
                author = f"{extract_last_name(self.authors[0])} et al."
            
            year = self.year if self.year else "n.d."
            citation = f"({author}, {year}"
            if page:
                citation += f", p. {page}"
            citation += ")"
            return citation
        
        elif style == CitationStyle.MLA:
            # (Author Page) or (Author)
            if not self.authors:
                author = "[No author]"
            elif len(self.authors) == 1:
                author = extract_last_name(self.authors[0])
            else:
                author = f"{extract_last_name(self.authors[0])} et al."
            
            if page:
                return f"({author} {page})"
            else:
                return f"({author})"
        
        elif style == CitationStyle.IEEE:
            # [Number] - requires citation manager to assign numbers
            return f"[{self.citation_id}]"
        
        return f"({self.citation_id})"
    
    def to_bibtex(self) -> str:
        """
        Export citation in BibTeX format.
        
        Returns:
            BibTeX entry string
        """
        # Determine entry type
        if self.venue_type == VenueType.JOURNAL:
            entry_type = "article"
        elif self.venue_type == VenueType.CONFERENCE:
            entry_type = "inproceedings"
        elif self.venue_type == VenueType.BOOK:
            entry_type = "book"
        elif self.venue_type == VenueType.THESIS:
            entry_type = "phdthesis"
        else:
            entry_type = "misc"
        
        # Build BibTeX entry
        lines = [f"@{entry_type}{{{self.citation_id},"]
        
        # Authors
        if self.authors:
            authors_str = " and ".join(self.authors)
            lines.append(f'  author = {{{authors_str}}},')
        
        # Title
        lines.append(f'  title = {{{self.title}}},')
        
        # Year
        if self.year:
            lines.append(f'  year = {{{self.year}}},')
        
        # Venue-specific fields
        if self.venue_type == VenueType.JOURNAL:
            lines.append(f'  journal = {{{self.venue}}},')
            if self.volume:
                lines.append(f'  volume = {{{self.volume}}},')
            if self.issue:
                lines.append(f'  number = {{{self.issue}}},')
        elif self.venue_type == VenueType.CONFERENCE:
            lines.append(f'  booktitle = {{{self.venue}}},')
        elif self.venue_type == VenueType.BOOK:
            lines.append(f'  publisher = {{{self.venue}}},')
        
        # Pages
        if self.pages:
            lines.append(f'  pages = {{{self.pages}}},')
        
        # DOI
        if self.doi:
            lines.append(f'  doi = {{{self.doi}}},')
        
        # URL
        if self.url:
            lines.append(f'  url = {{{self.url}}},')
        
        lines.append("}")
        return "\n".join(lines)
    
    def to_ris(self) -> str:
        """
        Export citation in RIS format.
        
        Returns:
            RIS entry string
        """
        # Determine type
        if self.venue_type == VenueType.JOURNAL:
            type_code = "JOUR"
        elif self.venue_type == VenueType.CONFERENCE:
            type_code = "CONF"
        elif self.venue_type == VenueType.BOOK:
            type_code = "BOOK"
        elif self.venue_type == VenueType.THESIS:
            type_code = "THES"
        else:
            type_code = "GEN"
        
        lines = [f"TY  - {type_code}"]
        
        # Authors
        for author in self.authors:
            lines.append(f"AU  - {author}")
        
        # Title
        lines.append(f"TI  - {self.title}")
        
        # Venue
        if self.venue:
            if self.venue_type == VenueType.JOURNAL:
                lines.append(f"JO  - {self.venue}")
            else:
                lines.append(f"T2  - {self.venue}")
        
        # Year
        if self.year:
            lines.append(f"PY  - {self.year}")
        
        # Volume
        if self.volume:
            lines.append(f"VL  - {self.volume}")
        
        # Issue
        if self.issue:
            lines.append(f"IS  - {self.issue}")
        
        # Pages
        if self.pages:
            lines.append(f"SP  - {self.pages}")
        
        # DOI
        if self.doi:
            lines.append(f"DO  - {self.doi}")
        
        # URL
        if self.url:
            lines.append(f"UR  - {self.url}")
        
        lines.append("ER  -")
        return "\n".join(lines)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert citation to dictionary.
        
        Returns:
            Dictionary representation of citation
        """
        return {
            "citation_id": self.citation_id,
            "authors": self.authors,
            "year": self.year,
            "title": self.title,
            "venue": self.venue,
            "venue_type": self.venue_type.value,
            "volume": self.volume,
            "issue": self.issue,
            "pages": self.pages,
            "doi": self.doi,
            "url": self.url,
            "pdf_url": self.pdf_url,
            "citation_count": self.citation_count,
            "abstract": self.abstract,
            "keywords": self.keywords,
            "access_date": self.access_date,
            "is_open_access": self.is_open_access,
            "is_incomplete": self.is_incomplete,
        }



class CitationManager:
    """
    Manages a collection of citations with tracking, formatting, and export capabilities.
    
    This class handles:
    - Citation storage and retrieval
    - Automatic deduplication
    - Bibliography generation in multiple styles
    - Citation export (BibTeX, RIS)
    - Citation extraction from various sources
    
    Requirements addressed:
    - 2.1: Automatic citation capture
    - 2.2: Multi-style citation formatting
    - 2.3: Bibliography generation
    - 2.5: Citation deduplication
    """
    
    def __init__(self):
        """Initialize empty citation manager"""
        self.citations: Dict[str, Citation] = {}
        self._citation_counter = 0
    
    def add_citation(self, citation: Citation) -> str:
        """
        Add a citation to the manager.
        
        Automatically checks for duplicates based on title and authors.
        If duplicate found, returns existing citation_id.
        
        Args:
            citation: Citation object to add
        
        Returns:
            citation_id of the added or existing citation
        """
        # Check for duplicates
        existing_id = self._find_duplicate(citation)
        if existing_id:
            return existing_id
        
        # Add new citation
        self.citations[citation.citation_id] = citation
        return citation.citation_id
    
    def _find_duplicate(self, citation: Citation) -> Optional[str]:
        """
        Find duplicate citation based on title and authors.
        
        Args:
            citation: Citation to check
        
        Returns:
            citation_id of duplicate if found, None otherwise
        """
        # Normalize title for comparison
        title_normalized = citation.title.lower().strip()
        
        for cid, existing in self.citations.items():
            existing_title = existing.title.lower().strip()
            
            # Check title similarity
            if title_normalized == existing_title:
                # Check if authors match
                if set(citation.authors) == set(existing.authors):
                    return cid
        
        return None
    
    def get_citation(self, citation_id: str) -> Optional[Citation]:
        """
        Retrieve a citation by ID.
        
        Args:
            citation_id: Unique citation identifier
        
        Returns:
            Citation object if found, None otherwise
        """
        return self.citations.get(citation_id)
    
    def get_inline_citation(self, citation_id: str, style: CitationStyle = CitationStyle.APA, page: Optional[str] = None) -> str:
        """
        Generate inline citation for a given citation ID.
        
        Args:
            citation_id: Citation identifier
            style: Citation style to use
            page: Optional page number
        
        Returns:
            Inline citation string or error message if not found
        """
        citation = self.get_citation(citation_id)
        if not citation:
            return f"[Citation {citation_id} not found]"
        
        return citation.get_inline_citation(style, page)
    
    def generate_bibliography(self, style: CitationStyle = CitationStyle.APA, sort_by_author: bool = True) -> str:
        """
        Generate a formatted bibliography of all citations.
        
        Args:
            style: Citation style to use
            sort_by_author: Whether to sort by author surname (default: True)
        
        Returns:
            Formatted bibliography string
        """
        if not self.citations:
            return ""
        
        # Get all citations
        citation_list = list(self.citations.values())
        
        # Sort by author surname if requested
        if sort_by_author:
            citation_list.sort(key=lambda c: self._get_sort_key(c))
        
        # Format each citation
        formatted_citations = []
        for i, citation in enumerate(citation_list, 1):
            if style == CitationStyle.IEEE:
                # IEEE uses numbered references
                formatted = f"[{i}] {citation.format(style)}"
            else:
                formatted = citation.format(style)
            formatted_citations.append(formatted)
        
        return "\n\n".join(formatted_citations)
    
    def _get_sort_key(self, citation: Citation) -> str:
        """
        Get sort key for citation (author surname + year + title).
        
        Args:
            citation: Citation to get sort key for
        
        Returns:
            Sort key string
        """
        if not citation.authors:
            author_key = "zzz"  # Sort no-author citations last
        else:
            # Use last name of first author
            author = citation.authors[0].strip()
            if ',' in author:
                # "Last, First" format
                author_key = author.split(',')[0].strip().lower()
            else:
                # "First Last" format
                author_key = author.split()[-1].lower() if author.split() else author.lower()
        
        year_key = str(citation.year) if citation.year else "9999"
        title_key = citation.title.lower()
        
        return f"{author_key}_{year_key}_{title_key}"
    
    def export_bibtex(self, filepath: str) -> None:
        """
        Export all citations to a BibTeX file.
        
        Args:
            filepath: Path to output .bib file
        """
        with open(filepath, 'w', encoding='utf-8') as f:
            for citation in self.citations.values():
                f.write(citation.to_bibtex())
                f.write("\n\n")
    
    def export_ris(self, filepath: str) -> None:
        """
        Export all citations to an RIS file.
        
        Args:
            filepath: Path to output .ris file
        """
        with open(filepath, 'w', encoding='utf-8') as f:
            for citation in self.citations.values():
                f.write(citation.to_ris())
                f.write("\n\n")
    
    def create_citation_from_metadata(
        self,
        title: str,
        authors: List[str],
        year: Optional[int] = None,
        venue: str = "",
        url: str = "",
        **kwargs
    ) -> Citation:
        """
        Create a Citation object from metadata and generate unique ID.
        
        Args:
            title: Publication title
            authors: List of author names
            year: Publication year
            venue: Publication venue
            url: Source URL
            **kwargs: Additional citation fields
        
        Returns:
            Citation object with generated ID
        """
        # Generate citation ID
        citation_id = self._generate_citation_id(title, authors, year)
        
        # Check if citation is incomplete
        is_incomplete = not (title and authors and year)
        
        # Create citation
        citation = Citation(
            citation_id=citation_id,
            title=title,
            authors=authors,
            year=year or 0,
            venue=venue,
            url=url,
            is_incomplete=is_incomplete,
            **kwargs
        )
        
        return citation
    
    def _generate_citation_id(self, title: str, authors: List[str], year: Optional[int]) -> str:
        """
        Generate unique citation ID from metadata.
        
        Uses hash of title + first author + year for uniqueness.
        
        Args:
            title: Publication title
            authors: List of authors
            year: Publication year
        
        Returns:
            Unique citation ID string
        """
        # Create hash from key fields
        hash_input = f"{title}_{authors[0] if authors else 'noauthor'}_{year or 0}"
        hash_obj = hashlib.md5(hash_input.encode('utf-8'))
        hash_str = hash_obj.hexdigest()[:8]
        
        # Create readable ID
        if authors:
            author = authors[0].strip()
            if ',' in author:
                # "Last, First" format
                author_part = author.split(',')[0].strip().lower()[:10]
            else:
                # "First Last" format
                author_part = author.split()[-1].lower()[:10] if author.split() else author.lower()[:10]
        else:
            author_part = "noauthor"
        
        year_part = str(year) if year else "nodate"
        
        citation_id = f"{author_part}_{year_part}_{hash_str}"
        
        return citation_id
    
    def extract_from_scholar_result(self, result: Dict[str, Any]) -> Optional[Citation]:
        """
        Extract citation from Google Scholar search result.
        
        Expected result format:
        {
            'title': str,
            'authors': str (comma-separated),
            'year': str or int,
            'venue': str,
            'citation_count': int,
            'url': str,
            'abstract': str (optional),
            ...
        }
        
        Args:
            result: Dictionary containing Scholar result data
        
        Returns:
            Citation object or None if extraction fails
        """
        try:
            # Extract title
            title = result.get('title', '').strip()
            if not title:
                return None
            
            # Extract and parse authors
            authors_str = result.get('authors', '')
            if isinstance(authors_str, str):
                authors = [a.strip() for a in authors_str.split(',') if a.strip()]
            elif isinstance(authors_str, list):
                authors = authors_str
            else:
                authors = []
            
            # Extract year
            year_raw = result.get('year', 0)
            try:
                year = int(year_raw) if year_raw else 0
            except (ValueError, TypeError):
                year = 0
            
            # Extract venue
            venue = result.get('venue', '').strip()
            
            # Determine venue type
            venue_type = VenueType.OTHER
            if 'journal' in venue.lower():
                venue_type = VenueType.JOURNAL
            elif 'conference' in venue.lower() or 'proceedings' in venue.lower():
                venue_type = VenueType.CONFERENCE
            elif 'arxiv' in venue.lower() or 'preprint' in venue.lower():
                venue_type = VenueType.PREPRINT
            
            # Extract other fields
            url = result.get('url', '')
            citation_count = result.get('citation_count', None)
            abstract = result.get('abstract', None)
            doi = result.get('doi', None)
            pdf_url = result.get('pdf_url', None)
            
            # Create citation
            citation = self.create_citation_from_metadata(
                title=title,
                authors=authors,
                year=year,
                venue=venue,
                url=url,
                venue_type=venue_type,
                citation_count=citation_count,
                abstract=abstract,
                doi=doi,
                pdf_url=pdf_url,
            )
            
            return citation
        
        except Exception as e:
            # Log error and return None
            print(f"Error extracting citation from Scholar result: {e}")
            return None
    
    def extract_from_webpage(self, content: str, url: str) -> Optional[Citation]:
        """
        Extract citation metadata from webpage content using heuristics.
        
        Attempts to find:
        - Title (from <title>, <h1>, or meta tags)
        - Authors (from meta tags or common patterns)
        - Date (from meta tags or content)
        - DOI (from content or meta tags)
        
        Args:
            content: HTML or text content of webpage
            url: URL of the webpage
        
        Returns:
            Citation object or None if extraction fails
        """
        try:
            # Extract title
            title = self._extract_title_from_html(content)
            if not title:
                title = url  # Fallback to URL
            
            # Extract authors
            authors = self._extract_authors_from_html(content)
            
            # Extract year
            year = self._extract_year_from_html(content)
            
            # Extract DOI if present
            doi = self._extract_doi_from_content(content)
            
            # Extract venue (domain name)
            venue = self._extract_domain(url)
            
            # Create citation
            citation = self.create_citation_from_metadata(
                title=title,
                authors=authors,
                year=year,
                venue=venue,
                url=url,
                doi=doi,
                venue_type=VenueType.WEB,
            )
            
            return citation
        
        except Exception as e:
            print(f"Error extracting citation from webpage: {e}")
            return None
    
    def _extract_title_from_html(self, content: str) -> str:
        """Extract title from HTML content using multiple strategies"""
        # Try citation_title meta tag (academic papers)
        match = re.search(r'<meta[^>]*name=["\']citation_title["\'][^>]*content=["\']([^"\']+)["\']', content, re.IGNORECASE)
        if match:
            return match.group(1).strip()
        
        # Try DC.Title meta tag (Dublin Core)
        match = re.search(r'<meta[^>]*name=["\']DC\.Title["\'][^>]*content=["\']([^"\']+)["\']', content, re.IGNORECASE)
        if match:
            return match.group(1).strip()
        
        # Try og:title meta tag (Open Graph)
        match = re.search(r'<meta[^>]*property=["\']og:title["\'][^>]*content=["\']([^"\']+)["\']', content, re.IGNORECASE)
        if match:
            return match.group(1).strip()
        
        # Try twitter:title meta tag
        match = re.search(r'<meta[^>]*name=["\']twitter:title["\'][^>]*content=["\']([^"\']+)["\']', content, re.IGNORECASE)
        if match:
            return match.group(1).strip()
        
        # Try <title> tag
        match = re.search(r'<title[^>]*>([^<]+)</title>', content, re.IGNORECASE)
        if match:
            title = match.group(1).strip()
            # Clean up common title suffixes
            title = re.sub(r'\s*[\|\-]\s*[^|]*$', '', title)
            return title.strip()
        
        # Try <h1> tag
        match = re.search(r'<h1[^>]*>([^<]+)</h1>', content, re.IGNORECASE)
        if match:
            return match.group(1).strip()
        
        return ""
    
    def _extract_authors_from_html(self, content: str) -> List[str]:
        """Extract authors from HTML content using multiple strategies"""
        authors = []
        
        # Try citation_author meta tags (can be multiple)
        matches = re.findall(r'<meta[^>]*name=["\']citation_author["\'][^>]*content=["\']([^"\']+)["\']', content, re.IGNORECASE)
        if matches:
            return [m.strip() for m in matches if m.strip()]
        
        # Try DC.Creator meta tag (Dublin Core)
        match = re.search(r'<meta[^>]*name=["\']DC\.Creator["\'][^>]*content=["\']([^"\']+)["\']', content, re.IGNORECASE)
        if match:
            author_str = match.group(1).strip()
            authors = [a.strip() for a in author_str.split(';') if a.strip()]
            if authors:
                return authors
        
        # Try standard author meta tag
        match = re.search(r'<meta[^>]*name=["\']author["\'][^>]*content=["\']([^"\']+)["\']', content, re.IGNORECASE)
        if match:
            author_str = match.group(1).strip()
            # Try different separators
            for sep in [',', ';', ' and ', '&']:
                if sep in author_str:
                    authors = [a.strip() for a in author_str.split(sep) if a.strip()]
                    if authors:
                        return authors
            # Single author
            if author_str:
                return [author_str]
        
        return authors
    
    def _extract_year_from_html(self, content: str) -> Optional[int]:
        """Extract publication year from HTML content using multiple strategies"""
        # Try citation_publication_date meta tag (academic papers)
        match = re.search(r'<meta[^>]*name=["\']citation_publication_date["\'][^>]*content=["\'](\d{4})', content, re.IGNORECASE)
        if match:
            try:
                year = int(match.group(1))
                if 1900 <= year <= 2100:
                    return year
            except ValueError:
                pass
        
        # Try citation_year meta tag
        match = re.search(r'<meta[^>]*name=["\']citation_year["\'][^>]*content=["\'](\d{4})["\']', content, re.IGNORECASE)
        if match:
            try:
                year = int(match.group(1))
                if 1900 <= year <= 2100:
                    return year
            except ValueError:
                pass
        
        # Try DC.Date meta tag (Dublin Core)
        match = re.search(r'<meta[^>]*name=["\']DC\.Date["\'][^>]*content=["\'](\d{4})', content, re.IGNORECASE)
        if match:
            try:
                year = int(match.group(1))
                if 1900 <= year <= 2100:
                    return year
            except ValueError:
                pass
        
        # Try article:published_time meta tag
        match = re.search(r'<meta[^>]*property=["\']article:published_time["\'][^>]*content=["\'](\d{4})', content, re.IGNORECASE)
        if match:
            try:
                year = int(match.group(1))
                if 1900 <= year <= 2100:
                    return year
            except ValueError:
                pass
        
        # Try standard date meta tag
        match = re.search(r'<meta[^>]*name=["\']date["\'][^>]*content=["\'](\d{4})', content, re.IGNORECASE)
        if match:
            try:
                year = int(match.group(1))
                if 1900 <= year <= 2100:
                    return year
            except ValueError:
                pass
        
        # Try time tag with datetime attribute
        match = re.search(r'<time[^>]*datetime=["\'](\d{4})', content, re.IGNORECASE)
        if match:
            try:
                year = int(match.group(1))
                if 1900 <= year <= 2100:
                    return year
            except ValueError:
                pass
        
        return None
    
    def _extract_domain(self, url: str) -> str:
        """Extract domain name from URL"""
        match = re.search(r'https?://(?:www\.)?([^/]+)', url)
        if match:
            return match.group(1)
        return url
    
    def _extract_doi_from_content(self, content: str) -> Optional[str]:
        """
        Extract DOI from content using regex patterns.
        
        Args:
            content: HTML or text content
        
        Returns:
            DOI string if found, None otherwise
        """
        # Common DOI patterns
        patterns = [
            r'doi:\s*(10\.\d{4,}/[^\s<>"]+)',
            r'https?://doi\.org/(10\.\d{4,}/[^\s<>"]+)',
            r'https?://dx\.doi\.org/(10\.\d{4,}/[^\s<>"]+)',
            r'<meta[^>]*name=["\']citation_doi["\'][^>]*content=["\']([^"\']+)["\']',
            r'<meta[^>]*name=["\']DC\.Identifier["\'][^>]*content=["\']doi:(10\.\d{4,}/[^\s<>"]+)["\']',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                doi = match.group(1).strip()
                # Clean up DOI (remove trailing punctuation)
                doi = re.sub(r'[.,;:)\]]+$', '', doi)
                return doi
        
        return None
    
    def extract_from_text(self, text: str, url: str = "") -> Optional[Citation]:
        """
        Extract citation from plain text using regex patterns.
        
        This is a fallback method that attempts to extract citation information
        from unstructured text using common citation patterns.
        
        Args:
            text: Plain text containing citation information
            url: Optional URL associated with the citation
        
        Returns:
            Citation object or None if extraction fails
        """
        try:
            # Try to extract title (usually in quotes or after common patterns)
            title = self._extract_title_from_text(text)
            
            # Try to extract authors
            authors = self._extract_authors_from_text(text)
            
            # Try to extract year
            year = self._extract_year_from_text(text)
            
            # Try to extract DOI
            doi = self._extract_doi_from_content(text)
            
            # If we have at least a title, create citation
            if title:
                citation = self.create_citation_from_metadata(
                    title=title,
                    authors=authors,
                    year=year,
                    venue="",
                    url=url,
                    doi=doi,
                    venue_type=VenueType.OTHER,
                )
                return citation
            
            return None
        
        except Exception as e:
            print(f"Error extracting citation from text: {e}")
            return None
    
    def _extract_title_from_text(self, text: str) -> str:
        """
        Extract title from plain text.
        
        Looks for titles in quotes or after common patterns.
        """
        # Try quoted text (common in citations)
        patterns = [
            r'"([^"]{10,200})"',  # Text in double quotes
            r"'([^']{10,200})'",  # Text in single quotes
            r'Title:\s*([^\n]{10,200})',  # After "Title:"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        # Fallback: take first substantial line
        lines = text.split('\n')
        for line in lines:
            line = line.strip()
            if len(line) > 10 and not line.startswith('http'):
                return line
        
        return ""
    
    def _extract_authors_from_text(self, text: str) -> List[str]:
        """
        Extract authors from plain text.
        
        Looks for author patterns like "Last, First" or "First Last".
        """
        authors = []
        
        # Pattern for "Last, First" format
        pattern1 = r'\b([A-Z][a-z]+),\s+([A-Z][a-z]+(?:\s+[A-Z]\.)?)\b'
        matches = re.findall(pattern1, text)
        for match in matches[:5]:  # Limit to first 5 matches
            authors.append(f"{match[0]}, {match[1]}")
        
        if authors:
            return authors
        
        # Pattern for "First Last" format (after "by" or "Author:")
        pattern2 = r'(?:by|Author[s]?:)\s+([A-Z][a-z]+\s+[A-Z][a-z]+(?:,\s+[A-Z][a-z]+\s+[A-Z][a-z]+)*)'
        match = re.search(pattern2, text, re.IGNORECASE)
        if match:
            author_str = match.group(1)
            authors = [a.strip() for a in author_str.split(',') if a.strip()]
        
        return authors
    
    def _extract_year_from_text(self, text: str) -> Optional[int]:
        """
        Extract publication year from plain text.
        
        Looks for 4-digit years in common contexts.
        """
        # Look for year in parentheses (common in citations)
        match = re.search(r'\((\d{4})\)', text)
        if match:
            try:
                year = int(match.group(1))
                if 1900 <= year <= 2100:
                    return year
            except ValueError:
                pass
        
        # Look for year after common patterns
        patterns = [
            r'(?:published|year|date):\s*(\d{4})',
            r'\b(19\d{2}|20\d{2})\b',  # Any year 1900-2099
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                try:
                    year = int(match.group(1))
                    if 1900 <= year <= 2100:
                        return year
                except ValueError:
                    pass
        
        return None
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about the citation collection.
        
        Returns:
            Dictionary with statistics
        """
        total = len(self.citations)
        incomplete = sum(1 for c in self.citations.values() if c.is_incomplete)
        with_doi = sum(1 for c in self.citations.values() if c.doi)
        open_access = sum(1 for c in self.citations.values() if c.is_open_access)
        
        # Count by venue type
        venue_counts = {}
        for citation in self.citations.values():
            vtype = citation.venue_type.value
            venue_counts[vtype] = venue_counts.get(vtype, 0) + 1
        
        return {
            'total_citations': total,
            'incomplete_citations': incomplete,
            'citations_with_doi': with_doi,
            'open_access_citations': open_access,
            'venue_type_counts': venue_counts,
        }
    
    def __len__(self) -> int:
        """Return number of citations"""
        return len(self.citations)
    
    def __contains__(self, citation_id: str) -> bool:
        """Check if citation ID exists"""
        return citation_id in self.citations
    
    def __iter__(self):
        """Iterate over citations"""
        return iter(self.citations.values())


# Convenience functions for creating citations

def create_citation(
    title: str,
    authors: List[str],
    year: int,
    venue: str = "",
    **kwargs
) -> Citation:
    """
    Convenience function to create a Citation object.
    
    Args:
        title: Publication title
        authors: List of author names
        year: Publication year
        venue: Publication venue
        **kwargs: Additional citation fields
    
    Returns:
        Citation object with generated ID
    """
    manager = CitationManager()
    return manager.create_citation_from_metadata(title, authors, year, venue, **kwargs)
