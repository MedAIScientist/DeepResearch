#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Enhanced Google Scholar Tool for Gazzali Research

This module provides an enhanced Google Scholar search tool with comprehensive
metadata extraction, citation tracking, and academic-specific features.

Requirements addressed:
- 1.3: Extract and preserve bibliographic metadata
- 14.1: Optimized Scholar queries with academic operators
- 14.2: Extract citation counts and publication venues
- 14.3: Identify highly cited papers and seminal works

Enhancements over base Scholar tool:
- Structured JSON output with full bibliographic data
- Citation count extraction and tracking
- Abstract text extraction
- Paper type identification (empirical, review, theoretical)
- Methodology information extraction
- Open access version identification
- Integration with CitationManager
"""

import os
import json
import re
import requests
from typing import Union, List, Dict, Any, Optional
from qwen_agent.tools.base import BaseTool, register_tool
from concurrent.futures import ThreadPoolExecutor
import http.client

try:
    from gazzali.config import get_env
    from gazzali.citation_manager import CitationManager, Citation, VenueType
except Exception:  # pragma: no cover
    def get_env(name: str, default=None):
        return os.getenv(name, default)
    CitationManager = None
    Citation = None
    VenueType = None


SERPER_KEY = get_env("SERPER_API_KEY") or os.environ.get("SERPER_KEY_ID")


@register_tool("google_scholar", allow_overwrite=True)
class Scholar(BaseTool):
    """
    Enhanced Google Scholar search tool with comprehensive metadata extraction.
    
    This tool searches Google Scholar and returns structured academic metadata
    including bibliographic information, citation counts, abstracts, and more.
    """
    
    name = "google_scholar"
    description = (
        "Search Google Scholar for academic publications with comprehensive metadata extraction. "
        "Returns structured information including authors, publication details, citation counts, "
        "abstracts, paper types, and open access links. Prioritize this tool for academic research."
    )
    parameters = {
        "type": "object",
        "properties": {
            "query": {
                "type": "array",
                "items": {"type": "string", "description": "The search query."},
                "minItems": 1,
                "description": "The list of search queries for Google Scholar."
            },
        },
        "required": ["query"],
    }
    
    def __init__(self, cfg: Optional[Dict] = None):
        """
        Initialize Scholar tool.
        
        Args:
            cfg: Optional configuration dictionary
        """
        super().__init__(cfg)
        self.citation_manager = CitationManager() if CitationManager else None
    
    def google_scholar_with_serp(self, query: str) -> str:
        """
        Search Google Scholar using Serper API with enhanced metadata extraction.
        
        Args:
            query: Search query string
        
        Returns:
            Formatted string with search results and metadata
        """
        conn = http.client.HTTPSConnection("google.serper.dev")
        payload = json.dumps({"q": query})
        headers = {
            'X-API-KEY': SERPER_KEY,
            'Content-Type': 'application/json'
        }
        
        # Retry logic with exponential backoff
        for i in range(5):
            try:
                conn.request("POST", "/scholar", payload, headers)
                res = conn.getresponse()
                break
            except Exception as e:
                print(f"Scholar API request error: {e}")
                if i == 4:
                    return f"Google Scholar Timeout, return None. Please try again later."
                continue
        
        data = res.read()
        results = json.loads(data.decode("utf-8"))
        
        try:
            if "organic" not in results:
                raise Exception(f"No results found for query: '{query}'. Use a less specific query.")
            
            # Extract and structure results
            structured_results = []
            web_snippets = []
            
            for idx, page in enumerate(results.get("organic", []), 1):
                # Extract comprehensive metadata
                metadata = self._extract_metadata(page, idx)
                structured_results.append(metadata)
                
                # Create citation if CitationManager available
                if self.citation_manager and Citation:
                    citation = self._create_citation_from_result(metadata)
                    if citation:
                        self.citation_manager.add_citation(citation)
                
                # Format for display
                snippet = self._format_result(metadata, idx)
                web_snippets.append(snippet)
            
            # Create comprehensive response
            content = self._format_response(query, web_snippets, structured_results)
            return content
            
        except Exception as e:
            return f"No results found for '{query}'. Try with a more general query. Error: {str(e)}"
    
    def _extract_metadata(self, page: Dict[str, Any], idx: int) -> Dict[str, Any]:
        """
        Extract comprehensive metadata from a Scholar search result.
        
        Args:
            page: Raw result dictionary from Serper API
            idx: Result index number
        
        Returns:
            Dictionary with structured metadata
        """
        metadata = {
            'index': idx,
            'title': page.get('title', ''),
            'authors': self._extract_authors(page),
            'year': self._extract_year(page),
            'venue': self._extract_venue(page),
            'venue_type': self._identify_venue_type(page),
            'citation_count': page.get('citedBy', 0),
            'abstract': page.get('snippet', ''),
            'url': page.get('link', ''),
            'pdf_url': page.get('pdfUrl', None),
            'is_open_access': bool(page.get('pdfUrl')),
            'publication_info': page.get('publicationInfo', ''),
            'paper_type': self._identify_paper_type(page),
            'methodology': self._extract_methodology(page),
            'is_highly_cited': self._is_highly_cited(page.get('citedBy', 0)),
            'related_url': page.get('relatedUrl', None),
        }
        
        return metadata
    
    def _extract_authors(self, page: Dict[str, Any]) -> List[str]:
        """
        Extract author names from result.
        
        Args:
            page: Raw result dictionary
        
        Returns:
            List of author names
        """
        # Try publicationInfo field first
        pub_info = page.get('publicationInfo', '')
        if pub_info:
            # Pattern: "Author1, Author2, Author3 - Journal, Year"
            match = re.match(r'^([^-]+?)\s*-', pub_info)
            if match:
                authors_str = match.group(1).strip()
                # Split by comma and clean
                authors = [a.strip() for a in authors_str.split(',') if a.strip()]
                if authors:
                    return authors
        
        # Try snippet for author patterns
        snippet = page.get('snippet', '')
        if snippet:
            # Look for "by Author" pattern
            match = re.search(r'by\s+([A-Z][^.]+?)(?:\.|$)', snippet)
            if match:
                authors_str = match.group(1).strip()
                authors = [a.strip() for a in authors_str.split(',') if a.strip()]
                if authors:
                    return authors
        
        return []
    
    def _extract_year(self, page: Dict[str, Any]) -> Optional[int]:
        """
        Extract publication year from result.
        
        Args:
            page: Raw result dictionary
        
        Returns:
            Publication year or None
        """
        # Direct year field
        if 'year' in page:
            try:
                return int(page['year'])
            except (ValueError, TypeError):
                pass
        
        # Extract from publicationInfo
        pub_info = page.get('publicationInfo', '')
        if pub_info:
            # Look for 4-digit year
            match = re.search(r'\b(19\d{2}|20\d{2})\b', pub_info)
            if match:
                try:
                    return int(match.group(1))
                except ValueError:
                    pass
        
        return None
    
    def _extract_venue(self, page: Dict[str, Any]) -> str:
        """
        Extract publication venue from result.
        
        Args:
            page: Raw result dictionary
        
        Returns:
            Venue name
        """
        pub_info = page.get('publicationInfo', '')
        if pub_info:
            # Pattern: "Authors - Venue, Year"
            match = re.search(r'-\s*([^,]+?)(?:,\s*\d{4})?$', pub_info)
            if match:
                venue = match.group(1).strip()
                # Remove author names if they leaked through
                if not any(word in venue.lower() for word in ['journal', 'conference', 'proceedings', 'arxiv']):
                    # Might be authors, try another pattern
                    pass
                else:
                    return venue
        
        # Fallback to full publicationInfo
        return pub_info
    
    def _identify_venue_type(self, page: Dict[str, Any]) -> str:
        """
        Identify the type of publication venue.
        
        Args:
            page: Raw result dictionary
        
        Returns:
            Venue type string
        """
        pub_info = page.get('publicationInfo', '').lower()
        venue = self._extract_venue(page).lower()
        
        if 'journal' in pub_info or 'journal' in venue:
            return 'journal'
        elif any(word in pub_info or word in venue for word in ['conference', 'proceedings', 'symposium', 'workshop']):
            return 'conference'
        elif 'arxiv' in pub_info or 'arxiv' in venue or 'preprint' in pub_info:
            return 'preprint'
        elif 'book' in pub_info or 'book' in venue:
            return 'book'
        elif 'thesis' in pub_info or 'dissertation' in pub_info:
            return 'thesis'
        else:
            return 'other'
    
    def _identify_paper_type(self, page: Dict[str, Any]) -> str:
        """
        Identify the type of paper (empirical, review, theoretical).
        
        Args:
            page: Raw result dictionary
        
        Returns:
            Paper type string
        """
        title = page.get('title', '').lower()
        snippet = page.get('snippet', '').lower()
        combined = f"{title} {snippet}"
        
        # Review paper indicators
        review_keywords = [
            'review', 'survey', 'meta-analysis', 'systematic review',
            'literature review', 'state of the art', 'overview'
        ]
        if any(keyword in combined for keyword in review_keywords):
            return 'review'
        
        # Theoretical paper indicators
        theoretical_keywords = [
            'theory', 'theoretical', 'framework', 'model', 'conceptual',
            'perspective', 'paradigm'
        ]
        if any(keyword in combined for keyword in theoretical_keywords):
            # Check if it's also empirical
            empirical_keywords = [
                'study', 'experiment', 'data', 'analysis', 'results',
                'findings', 'evidence', 'sample', 'participants'
            ]
            if not any(keyword in combined for keyword in empirical_keywords):
                return 'theoretical'
        
        # Empirical paper indicators
        empirical_keywords = [
            'study', 'experiment', 'empirical', 'data', 'analysis',
            'results', 'findings', 'evidence', 'sample', 'participants',
            'survey', 'case study', 'observation'
        ]
        if any(keyword in combined for keyword in empirical_keywords):
            return 'empirical'
        
        return 'unknown'
    
    def _extract_methodology(self, page: Dict[str, Any]) -> Optional[str]:
        """
        Extract methodology information from result.
        
        Args:
            page: Raw result dictionary
        
        Returns:
            Methodology description or None
        """
        snippet = page.get('snippet', '').lower()
        
        # Common methodology keywords
        methodologies = {
            'qualitative': ['qualitative', 'interview', 'ethnography', 'case study', 'grounded theory'],
            'quantitative': ['quantitative', 'survey', 'experiment', 'statistical', 'regression', 'correlation'],
            'mixed-methods': ['mixed methods', 'mixed-method', 'triangulation'],
            'meta-analysis': ['meta-analysis', 'systematic review'],
            'computational': ['simulation', 'computational', 'algorithm', 'machine learning', 'deep learning'],
            'experimental': ['experiment', 'randomized', 'controlled trial', 'rct'],
        }
        
        found_methods = []
        for method_type, keywords in methodologies.items():
            if any(keyword in snippet for keyword in keywords):
                found_methods.append(method_type)
        
        if found_methods:
            return ', '.join(found_methods)
        
        return None
    
    def _is_highly_cited(self, citation_count: int) -> bool:
        """
        Determine if a paper is highly cited.
        
        Args:
            citation_count: Number of citations
        
        Returns:
            True if highly cited, False otherwise
        """
        # Threshold for "highly cited" - can be adjusted
        return citation_count >= 100
    
    def _create_citation_from_result(self, metadata: Dict[str, Any]) -> Optional[Citation]:
        """
        Create a Citation object from extracted metadata.
        
        Args:
            metadata: Structured metadata dictionary
        
        Returns:
            Citation object or None
        """
        if not Citation or not VenueType:
            return None
        
        try:
            # Map venue type string to enum
            venue_type_map = {
                'journal': VenueType.JOURNAL,
                'conference': VenueType.CONFERENCE,
                'book': VenueType.BOOK,
                'preprint': VenueType.PREPRINT,
                'thesis': VenueType.THESIS,
                'other': VenueType.OTHER,
            }
            venue_type = venue_type_map.get(metadata['venue_type'], VenueType.OTHER)
            
            # Create citation using CitationManager
            citation = self.citation_manager.create_citation_from_metadata(
                title=metadata['title'],
                authors=metadata['authors'],
                year=metadata['year'],
                venue=metadata['venue'],
                url=metadata['url'],
                venue_type=venue_type,
                citation_count=metadata['citation_count'],
                abstract=metadata['abstract'],
                pdf_url=metadata['pdf_url'],
                is_open_access=metadata['is_open_access'],
            )
            
            return citation
        
        except Exception as e:
            print(f"Error creating citation from result: {e}")
            return None
    
    def _format_result(self, metadata: Dict[str, Any], idx: int) -> str:
        """
        Format a single result for display.
        
        Args:
            metadata: Structured metadata dictionary
            idx: Result index
        
        Returns:
            Formatted result string
        """
        lines = []
        
        # Title with link
        title = metadata['title']
        url = metadata['url']
        pdf_url = metadata['pdf_url']
        
        if pdf_url:
            link_info = f"PDF: {pdf_url}"
        elif url:
            link_info = url
        else:
            link_info = "no available link"
        
        lines.append(f"{idx}. [{title}]({link_info})")
        
        # Authors
        if metadata['authors']:
            authors_str = ', '.join(metadata['authors'][:3])
            if len(metadata['authors']) > 3:
                authors_str += ' et al.'
            lines.append(f"   Authors: {authors_str}")
        
        # Publication info
        pub_parts = []
        if metadata['venue']:
            pub_parts.append(metadata['venue'])
        if metadata['year']:
            pub_parts.append(str(metadata['year']))
        if pub_parts:
            lines.append(f"   Publication: {', '.join(pub_parts)}")
        
        # Citation count
        if metadata['citation_count']:
            cited_str = f"Cited by: {metadata['citation_count']}"
            if metadata['is_highly_cited']:
                cited_str += " [HIGHLY CITED]"
            lines.append(f"   {cited_str}")
        
        # Paper type and methodology
        meta_info = []
        if metadata['paper_type'] != 'unknown':
            meta_info.append(f"Type: {metadata['paper_type']}")
        if metadata['methodology']:
            meta_info.append(f"Methods: {metadata['methodology']}")
        if meta_info:
            lines.append(f"   {' | '.join(meta_info)}")
        
        # Open access indicator
        if metadata['is_open_access']:
            lines.append(f"   [OPEN ACCESS]")
        
        # Abstract/snippet
        if metadata['abstract']:
            abstract = metadata['abstract'].replace("Your browser can't play this video.", "").strip()
            if abstract:
                lines.append(f"   {abstract}")
        
        return '\n'.join(lines)
    
    def _format_response(self, query: str, web_snippets: List[str], structured_results: List[Dict]) -> str:
        """
        Format the complete response with summary statistics.
        
        Args:
            query: Original search query
            web_snippets: List of formatted result strings
            structured_results: List of structured metadata dictionaries
        
        Returns:
            Formatted response string
        """
        lines = []
        
        # Header
        lines.append(f"Google Scholar search for '{query}' found {len(web_snippets)} results:")
        lines.append("")
        
        # Summary statistics
        total_citations = sum(r['citation_count'] for r in structured_results if r['citation_count'])
        highly_cited = sum(1 for r in structured_results if r['is_highly_cited'])
        open_access = sum(1 for r in structured_results if r['is_open_access'])
        
        # Paper type distribution
        paper_types = {}
        for r in structured_results:
            ptype = r['paper_type']
            paper_types[ptype] = paper_types.get(ptype, 0) + 1
        
        lines.append("## Summary")
        lines.append(f"- Total results: {len(structured_results)}")
        lines.append(f"- Highly cited papers (100+ citations): {highly_cited}")
        lines.append(f"- Open access papers: {open_access}")
        lines.append(f"- Total citations: {total_citations}")
        
        if paper_types:
            type_str = ', '.join([f"{k}: {v}" for k, v in paper_types.items() if k != 'unknown'])
            if type_str:
                lines.append(f"- Paper types: {type_str}")
        
        lines.append("")
        lines.append("## Scholar Results")
        lines.append("")
        
        # Results
        lines.extend(web_snippets)
        
        return '\n'.join(lines)
    
    def call(self, params: Union[str, dict], **kwargs) -> str:
        """
        Execute Scholar search with given parameters.
        
        Args:
            params: Query parameters (string or dict with 'query' field)
            **kwargs: Additional arguments
        
        Returns:
            Formatted search results
        """
        try:
            params = self._verify_json_format_args(params)
            query = params["query"]
        except Exception:
            return "[google_scholar] Invalid request format: Input must be a JSON object containing 'query' field"
        
        if isinstance(query, str):
            response = self.google_scholar_with_serp(query)
        else:
            assert isinstance(query, list)
            with ThreadPoolExecutor(max_workers=3) as executor:
                response = list(executor.map(self.google_scholar_with_serp, query))
            response = "\n=======\n".join(response)
        
        return response
    
    def get_citation_manager(self) -> Optional[CitationManager]:
        """
        Get the citation manager instance.
        
        Returns:
            CitationManager instance or None
        """
        return self.citation_manager
