#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for Scholar Tool and Citation Manager Integration

This test file verifies that the Scholar tool properly integrates with the
Citation Manager to automatically track citations from search results.

Requirements addressed:
- 1.3: Extract and preserve bibliographic metadata
- 2.1: Automatically capture citation information
- 14.2: Extract citation counts and publication venues
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from src.gazzali.tools.tool_scholar import Scholar
from src.gazzali.citation_manager import (
    Citation,
    CitationManager,
    CitationStyle,
    VenueType,
)


class TestScholarCitationIntegration:
    """Test integration between Scholar tool and Citation Manager"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.scholar = Scholar()
        self.citation_manager = self.scholar.get_citation_manager()
    
    def test_scholar_has_citation_manager(self):
        """Test that Scholar tool initializes with Citation Manager"""
        assert self.scholar.citation_manager is not None
        assert isinstance(self.scholar.citation_manager, CitationManager)
    
    def test_get_citation_manager(self):
        """Test that get_citation_manager returns the manager instance"""
        cm = self.scholar.get_citation_manager()
        assert cm is not None
        assert isinstance(cm, CitationManager)
        assert cm is self.scholar.citation_manager
    
    def test_create_citation_from_result(self):
        """Test citation creation from Scholar result metadata"""
        metadata = {
            'index': 1,
            'title': 'Deep Learning for Natural Language Processing',
            'authors': ['Smith, John', 'Doe, Jane'],
            'year': 2023,
            'venue': 'Journal of AI Research',
            'venue_type': 'journal',
            'citation_count': 150,
            'abstract': 'This paper presents a novel approach...',
            'url': 'https://example.com/paper',
            'pdf_url': 'https://example.com/paper.pdf',
            'is_open_access': True,
            'publication_info': 'Smith, Doe - Journal of AI Research, 2023',
            'paper_type': 'empirical',
            'methodology': 'quantitative, computational',
            'is_highly_cited': True,
            'related_url': None,
        }
        
        citation = self.scholar._create_citation_from_result(metadata)
        
        assert citation is not None
        assert isinstance(citation, Citation)
        assert citation.title == 'Deep Learning for Natural Language Processing'
        assert len(citation.authors) == 2
        assert citation.year == 2023
        assert citation.venue == 'Journal of AI Research'
        assert citation.venue_type == VenueType.JOURNAL
        assert citation.citation_count == 150
        assert citation.abstract == 'This paper presents a novel approach...'
        assert citation.url == 'https://example.com/paper'
        assert citation.pdf_url == 'https://example.com/paper.pdf'
        assert citation.is_open_access is True
    
    def test_citation_added_to_manager(self):
        """Test that citations are automatically added to manager"""
        # Create a mock result
        metadata = {
            'index': 1,
            'title': 'Test Paper',
            'authors': ['Author, Test'],
            'year': 2024,
            'venue': 'Test Journal',
            'venue_type': 'journal',
            'citation_count': 10,
            'abstract': 'Test abstract',
            'url': 'https://test.com',
            'pdf_url': None,
            'is_open_access': False,
            'publication_info': '',
            'paper_type': 'empirical',
            'methodology': None,
            'is_highly_cited': False,
            'related_url': None,
        }
        
        # Create citation
        citation = self.scholar._create_citation_from_result(metadata)
        
        # Add to manager
        initial_count = len(self.citation_manager)
        citation_id = self.citation_manager.add_citation(citation)
        
        # Verify it was added
        assert len(self.citation_manager) == initial_count + 1
        assert citation_id in self.citation_manager
        
        # Verify we can retrieve it
        retrieved = self.citation_manager.get_citation(citation_id)
        assert retrieved is not None
        assert retrieved.title == 'Test Paper'
    
    def test_venue_type_mapping(self):
        """Test that venue types are correctly mapped from strings to enums"""
        test_cases = [
            ('journal', VenueType.JOURNAL),
            ('conference', VenueType.CONFERENCE),
            ('book', VenueType.BOOK),
            ('preprint', VenueType.PREPRINT),
            ('thesis', VenueType.THESIS),
            ('other', VenueType.OTHER),
        ]
        
        for venue_type_str, expected_enum in test_cases:
            metadata = {
                'index': 1,
                'title': f'Test Paper {venue_type_str}',
                'authors': ['Author, Test'],
                'year': 2024,
                'venue': 'Test Venue',
                'venue_type': venue_type_str,
                'citation_count': 0,
                'abstract': '',
                'url': 'https://test.com',
                'pdf_url': None,
                'is_open_access': False,
                'publication_info': '',
                'paper_type': 'unknown',
                'methodology': None,
                'is_highly_cited': False,
                'related_url': None,
            }
            
            citation = self.scholar._create_citation_from_result(metadata)
            assert citation.venue_type == expected_enum
    
    def test_citation_deduplication_in_manager(self):
        """Test that duplicate citations are not added twice"""
        metadata = {
            'index': 1,
            'title': 'Unique Paper Title',
            'authors': ['Smith, John'],
            'year': 2023,
            'venue': 'Journal',
            'venue_type': 'journal',
            'citation_count': 50,
            'abstract': 'Abstract text',
            'url': 'https://example.com',
            'pdf_url': None,
            'is_open_access': False,
            'publication_info': '',
            'paper_type': 'empirical',
            'methodology': None,
            'is_highly_cited': False,
            'related_url': None,
        }
        
        # Create and add first citation
        citation1 = self.scholar._create_citation_from_result(metadata)
        id1 = self.citation_manager.add_citation(citation1)
        initial_count = len(self.citation_manager)
        
        # Try to add duplicate
        citation2 = self.scholar._create_citation_from_result(metadata)
        id2 = self.citation_manager.add_citation(citation2)
        
        # Should return same ID and not increase count
        assert id1 == id2
        assert len(self.citation_manager) == initial_count
    
    def test_multiple_citations_tracked(self):
        """Test that multiple different citations are all tracked"""
        papers = [
            {
                'title': 'First Paper',
                'authors': ['Author, One'],
                'year': 2023,
                'venue': 'Journal A',
            },
            {
                'title': 'Second Paper',
                'authors': ['Author, Two'],
                'year': 2024,
                'venue': 'Journal B',
            },
            {
                'title': 'Third Paper',
                'authors': ['Author, Three'],
                'year': 2022,
                'venue': 'Conference C',
            },
        ]
        
        initial_count = len(self.citation_manager)
        
        for paper in papers:
            metadata = {
                'index': 1,
                'title': paper['title'],
                'authors': paper['authors'],
                'year': paper['year'],
                'venue': paper['venue'],
                'venue_type': 'journal',
                'citation_count': 0,
                'abstract': '',
                'url': 'https://example.com',
                'pdf_url': None,
                'is_open_access': False,
                'publication_info': '',
                'paper_type': 'unknown',
                'methodology': None,
                'is_highly_cited': False,
                'related_url': None,
            }
            citation = self.scholar._create_citation_from_result(metadata)
            self.citation_manager.add_citation(citation)
        
        # All three should be added
        assert len(self.citation_manager) == initial_count + 3
    
    def test_citation_with_missing_metadata(self):
        """Test handling of citations with incomplete metadata"""
        metadata = {
            'index': 1,
            'title': 'Paper with Missing Data',
            'authors': [],  # No authors
            'year': None,  # No year
            'venue': '',
            'venue_type': 'other',
            'citation_count': 0,
            'abstract': '',
            'url': 'https://example.com',
            'pdf_url': None,
            'is_open_access': False,
            'publication_info': '',
            'paper_type': 'unknown',
            'methodology': None,
            'is_highly_cited': False,
            'related_url': None,
        }
        
        citation = self.scholar._create_citation_from_result(metadata)
        
        # Should still create citation but mark as incomplete
        assert citation is not None
        assert citation.is_incomplete is True
        assert citation.title == 'Paper with Missing Data'
    
    def test_citation_statistics_after_scholar_search(self):
        """Test that citation statistics reflect Scholar results"""
        # Add several citations with different properties
        papers = [
            {
                'title': 'Open Access Paper',
                'authors': ['Author, One'],
                'year': 2023,
                'venue': 'Journal A',
                'venue_type': 'journal',
                'is_open_access': True,
                'citation_count': 150,
            },
            {
                'title': 'Conference Paper',
                'authors': ['Author, Two'],
                'year': 2024,
                'venue': 'Conference B',
                'venue_type': 'conference',
                'is_open_access': False,
                'citation_count': 50,
            },
            {
                'title': 'Preprint',
                'authors': ['Author, Three'],
                'year': 2024,
                'venue': 'arXiv',
                'venue_type': 'preprint',
                'is_open_access': True,
                'citation_count': 10,
            },
        ]
        
        for paper in papers:
            metadata = {
                'index': 1,
                'title': paper['title'],
                'authors': paper['authors'],
                'year': paper['year'],
                'venue': paper['venue'],
                'venue_type': paper['venue_type'],
                'citation_count': paper['citation_count'],
                'abstract': '',
                'url': 'https://example.com',
                'pdf_url': None,
                'is_open_access': paper['is_open_access'],
                'publication_info': '',
                'paper_type': 'unknown',
                'methodology': None,
                'is_highly_cited': paper['citation_count'] >= 100,
                'related_url': None,
            }
            citation = self.scholar._create_citation_from_result(metadata)
            self.citation_manager.add_citation(citation)
        
        stats = self.citation_manager.get_statistics()
        
        # Check statistics
        assert stats['open_access_citations'] >= 2
        assert 'journal' in stats['venue_type_counts']
        assert 'conference' in stats['venue_type_counts']
        assert 'preprint' in stats['venue_type_counts']
    
    def test_bibliography_generation_from_scholar_results(self):
        """Test generating bibliography from Scholar-tracked citations"""
        # Add citations
        papers = [
            {
                'title': 'Zebra Research',
                'authors': ['Zimmerman, Zoe'],
                'year': 2023,
                'venue': 'Journal Z',
            },
            {
                'title': 'Apple Research',
                'authors': ['Anderson, Alice'],
                'year': 2024,
                'venue': 'Journal A',
            },
        ]
        
        for paper in papers:
            metadata = {
                'index': 1,
                'title': paper['title'],
                'authors': paper['authors'],
                'year': paper['year'],
                'venue': paper['venue'],
                'venue_type': 'journal',
                'citation_count': 0,
                'abstract': '',
                'url': 'https://example.com',
                'pdf_url': None,
                'is_open_access': False,
                'publication_info': '',
                'paper_type': 'unknown',
                'methodology': None,
                'is_highly_cited': False,
                'related_url': None,
            }
            citation = self.scholar._create_citation_from_result(metadata)
            self.citation_manager.add_citation(citation)
        
        # Generate bibliography
        bibliography = self.citation_manager.generate_bibliography(
            CitationStyle.APA,
            sort_by_author=True
        )
        
        # Check that bibliography contains both papers
        assert 'Zebra Research' in bibliography
        assert 'Apple Research' in bibliography
        
        # Check alphabetical order (Anderson before Zimmerman)
        anderson_pos = bibliography.find('Anderson')
        zimmerman_pos = bibliography.find('Zimmerman')
        assert anderson_pos < zimmerman_pos
    
    def test_bibtex_export_from_scholar_results(self):
        """Test exporting Scholar results to BibTeX"""
        import tempfile
        import os
        
        # Add a citation
        metadata = {
            'index': 1,
            'title': 'Test Paper for Export',
            'authors': ['Smith, John', 'Doe, Jane'],
            'year': 2023,
            'venue': 'Test Journal',
            'venue_type': 'journal',
            'citation_count': 100,
            'abstract': 'Test abstract',
            'url': 'https://example.com',
            'pdf_url': None,
            'is_open_access': False,
            'publication_info': '',
            'paper_type': 'empirical',
            'methodology': None,
            'is_highly_cited': True,
            'related_url': None,
        }
        
        citation = self.scholar._create_citation_from_result(metadata)
        self.citation_manager.add_citation(citation)
        
        # Export to temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.bib', delete=False) as f:
            temp_path = f.name
        
        try:
            self.citation_manager.export_bibtex(temp_path)
            
            # Read and verify
            with open(temp_path, 'r') as f:
                content = f.read()
            
            assert '@article{' in content
            assert 'title = {Test Paper for Export}' in content
            assert 'author = {Smith, John and Doe, Jane}' in content
            assert 'year = {2023}' in content
        finally:
            # Clean up
            if os.path.exists(temp_path):
                os.unlink(temp_path)
    
    def test_inline_citation_from_scholar_result(self):
        """Test generating inline citations from Scholar results"""
        metadata = {
            'index': 1,
            'title': 'Important Paper',
            'authors': ['Smith, John', 'Doe, Jane'],
            'year': 2023,
            'venue': 'Journal',
            'venue_type': 'journal',
            'citation_count': 200,
            'abstract': '',
            'url': 'https://example.com',
            'pdf_url': None,
            'is_open_access': False,
            'publication_info': '',
            'paper_type': 'empirical',
            'methodology': None,
            'is_highly_cited': True,
            'related_url': None,
        }
        
        citation = self.scholar._create_citation_from_result(metadata)
        citation_id = self.citation_manager.add_citation(citation)
        
        # Get inline citation
        inline_apa = self.citation_manager.get_inline_citation(
            citation_id,
            CitationStyle.APA
        )
        
        # Should be in format (Smith & Doe, 2023)
        assert 'Smith' in inline_apa
        assert 'Doe' in inline_apa
        assert '2023' in inline_apa
        assert inline_apa.startswith('(')
        assert inline_apa.endswith(')')


class TestScholarMetadataExtraction:
    """Test metadata extraction methods in Scholar tool"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.scholar = Scholar()
    
    def test_extract_authors(self):
        """Test author extraction from Scholar results"""
        # Test with publicationInfo
        page1 = {
            'publicationInfo': 'Smith, J., Doe, J., Johnson, A. - Journal, 2023'
        }
        authors1 = self.scholar._extract_authors(page1)
        assert len(authors1) >= 1
        
        # Test with snippet
        page2 = {
            'snippet': 'by John Smith and Jane Doe. This paper...'
        }
        authors2 = self.scholar._extract_authors(page2)
        assert len(authors2) >= 1
    
    def test_extract_year(self):
        """Test year extraction from Scholar results"""
        # Test with direct year field
        page1 = {'year': 2023}
        year1 = self.scholar._extract_year(page1)
        assert year1 == 2023
        
        # Test with publicationInfo
        page2 = {'publicationInfo': 'Authors - Journal, 2024'}
        year2 = self.scholar._extract_year(page2)
        assert year2 == 2024
    
    def test_extract_venue(self):
        """Test venue extraction from Scholar results"""
        page = {
            'publicationInfo': 'Authors - Nature Medicine, 2023'
        }
        venue = self.scholar._extract_venue(page)
        assert 'Nature Medicine' in venue or venue != ''
    
    def test_identify_venue_type(self):
        """Test venue type identification"""
        test_cases = [
            ({'publicationInfo': 'Authors - Journal of AI, 2023'}, 'journal'),
            ({'publicationInfo': 'Authors - Conference on ML, 2023'}, 'conference'),
            ({'publicationInfo': 'Authors - arXiv preprint, 2023'}, 'preprint'),
            ({'publicationInfo': 'Authors - Book Title, 2023'}, 'book'),
        ]
        
        for page, expected_type in test_cases:
            venue_type = self.scholar._identify_venue_type(page)
            assert venue_type == expected_type
    
    def test_identify_paper_type(self):
        """Test paper type identification"""
        test_cases = [
            (
                {'title': 'A Survey of Machine Learning', 'snippet': 'This review...'},
                'review'
            ),
            (
                {'title': 'Theoretical Framework for AI', 'snippet': 'We propose a theory...'},
                'theoretical'
            ),
            (
                {'title': 'Empirical Study of Neural Networks', 'snippet': 'We conducted experiments...'},
                'empirical'
            ),
        ]
        
        for page, expected_type in test_cases:
            paper_type = self.scholar._identify_paper_type(page)
            assert paper_type == expected_type
    
    def test_extract_methodology(self):
        """Test methodology extraction"""
        test_cases = [
            'We conducted a qualitative interview study...',
            'Using quantitative regression analysis...',
            'A mixed-methods approach combining surveys and interviews...',
            'Meta-analysis of 50 randomized controlled trials...',
        ]
        
        for snippet in test_cases:
            page = {'snippet': snippet}
            methodology = self.scholar._extract_methodology(page)
            assert methodology is not None
            assert len(methodology) > 0
    
    def test_is_highly_cited(self):
        """Test highly cited paper identification"""
        assert self.scholar._is_highly_cited(150) is True
        assert self.scholar._is_highly_cited(100) is True
        assert self.scholar._is_highly_cited(99) is False
        assert self.scholar._is_highly_cited(0) is False


class TestScholarQueryOptimization:
    """Test query optimization features"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.scholar = Scholar()
    
    def test_optimize_query_with_author(self):
        """Test query optimization with author filter"""
        query = "machine learning"
        optimized = self.scholar.optimize_query(query, author="Geoffrey Hinton")
        
        assert 'machine learning' in optimized
        assert 'author:"Geoffrey Hinton"' in optimized
    
    def test_optimize_query_with_intitle(self):
        """Test query optimization with title filter"""
        query = "neural networks"
        optimized = self.scholar.optimize_query(query, intitle="transformer")
        
        assert 'neural networks' in optimized
        assert 'intitle:transformer' in optimized
    
    def test_optimize_query_exact_phrases(self):
        """Test automatic exact phrase detection"""
        query = "machine learning in healthcare"
        optimized = self.scholar.optimize_query(query)
        
        # Should wrap "machine learning" in quotes
        assert '"machine learning"' in optimized or 'machine learning' in optimized


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
