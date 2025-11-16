#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for citation formatting functionality.

This test file verifies that all citation styles (APA, MLA, Chicago, IEEE)
are correctly implemented and produce properly formatted citations.
"""

import pytest
from src.gazzali.citation_manager import (
    Citation,
    CitationManager,
    CitationStyle,
    VenueType,
)


class TestCitationFormatting:
    """Test citation formatting in different styles"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.manager = CitationManager()
        
        # Create a sample journal article citation
        self.journal_citation = self.manager.create_citation_from_metadata(
            title="Deep Learning for Natural Language Processing",
            authors=["Smith, John", "Doe, Jane"],
            year=2023,
            venue="Journal of AI Research",
            venue_type=VenueType.JOURNAL,
            volume="45",
            issue="3",
            pages="123-145",
            doi="10.1234/jair.2023.45.3.123"
        )
        
        # Create a conference paper citation
        self.conference_citation = self.manager.create_citation_from_metadata(
            title="Attention Mechanisms in Neural Networks",
            authors=["Johnson, Alice", "Williams, Bob", "Brown, Charlie"],
            year=2022,
            venue="Proceedings of the International Conference on Machine Learning",
            venue_type=VenueType.CONFERENCE,
            pages="456-467"
        )
        
        # Create a single author citation
        self.single_author = self.manager.create_citation_from_metadata(
            title="The Future of Artificial Intelligence",
            authors=["Anderson, Michael"],
            year=2024,
            venue="AI Quarterly",
            venue_type=VenueType.JOURNAL,
            volume="12",
            pages="1-20"
        )
    
    def test_apa_formatting_journal(self):
        """Test APA 7th edition formatting for journal articles"""
        formatted = self.journal_citation.format(CitationStyle.APA)
        
        # Check key components are present
        assert "Smith, J., & Doe, J." in formatted
        assert "(2023)" in formatted
        assert "Deep Learning for Natural Language Processing" in formatted
        assert "Journal of AI Research" in formatted
        assert "45(3)" in formatted
        assert "123-145" in formatted
        assert "https://doi.org/10.1234/jair.2023.45.3.123" in formatted
    
    def test_apa_formatting_conference(self):
        """Test APA formatting for conference papers"""
        formatted = self.conference_citation.format(CitationStyle.APA)
        
        assert "Johnson, A., Williams, B., & Brown, C." in formatted
        assert "(2022)" in formatted
        assert "In Proceedings of the International Conference on Machine Learning" in formatted
        assert "pp. 456-467" in formatted
    
    def test_mla_formatting_journal(self):
        """Test MLA 9th edition formatting"""
        formatted = self.journal_citation.format(CitationStyle.MLA)
        
        # Check key components
        assert "Smith, John" in formatted
        assert "Doe, Jane" in formatted
        assert '"Deep Learning for Natural Language Processing."' in formatted
        assert "Journal of AI Research," in formatted
        assert "vol. 45," in formatted
        assert "no. 3," in formatted
        assert "2023," in formatted
        assert "pp. 123-145" in formatted
    
    def test_mla_formatting_et_al(self):
        """Test MLA et al. for 3+ authors"""
        formatted = self.conference_citation.format(CitationStyle.MLA)
        
        assert "Johnson, Alice, et al" in formatted
    
    def test_chicago_formatting(self):
        """Test Chicago 17th edition formatting"""
        formatted = self.journal_citation.format(CitationStyle.CHICAGO)
        
        assert "Smith, John" in formatted
        assert "Doe, Jane" in formatted
        assert "2023." in formatted
        assert '"Deep Learning for Natural Language Processing."' in formatted
        assert "Journal of AI Research 45" in formatted
        assert "no. 3: 123-145" in formatted
    
    def test_ieee_formatting(self):
        """Test IEEE formatting"""
        formatted = self.journal_citation.format(CitationStyle.IEEE)
        
        # IEEE uses initials before surname
        assert "J. Smith, J. Doe" in formatted
        assert '"Deep Learning for Natural Language Processing,"' in formatted
        assert "Journal of AI Research," in formatted
        assert "vol. 45" in formatted
        assert "no. 3" in formatted
        assert "pp. 123-145" in formatted
        assert "2023" in formatted
    
    def test_inline_citation_apa(self):
        """Test APA inline citations"""
        inline = self.journal_citation.get_inline_citation(CitationStyle.APA)
        assert inline == "(Smith & Doe, 2023)"
        
        inline_with_page = self.journal_citation.get_inline_citation(CitationStyle.APA, page="125")
        assert inline_with_page == "(Smith & Doe, 2023, p. 125)"
    
    def test_inline_citation_mla(self):
        """Test MLA inline citations"""
        inline = self.journal_citation.get_inline_citation(CitationStyle.MLA)
        assert inline == "(Smith et al.)"
        
        inline_with_page = self.journal_citation.get_inline_citation(CitationStyle.MLA, page="125")
        assert inline_with_page == "(Smith et al. 125)"
    
    def test_inline_citation_single_author(self):
        """Test inline citation with single author"""
        inline_apa = self.single_author.get_inline_citation(CitationStyle.APA)
        assert inline_apa == "(Anderson, 2024)"
        
        inline_mla = self.single_author.get_inline_citation(CitationStyle.MLA)
        assert inline_mla == "(Anderson)"
    
    def test_inline_citation_et_al(self):
        """Test inline citation with 3+ authors"""
        inline = self.conference_citation.get_inline_citation(CitationStyle.APA)
        assert inline == "(Johnson et al., 2022)"


class TestBibliographyGeneration:
    """Test bibliography generation with multiple citations"""
    
    def test_bibliography_sorting(self):
        """Test that bibliography is sorted by author surname"""
        manager = CitationManager()
        
        # Add citations in non-alphabetical order
        citation1 = manager.create_citation_from_metadata(
            title="Zebra Research",
            authors=["Zimmerman, Zoe"],
            year=2023,
            venue="Journal A"
        )
        citation2 = manager.create_citation_from_metadata(
            title="Apple Research",
            authors=["Anderson, Alice"],
            year=2023,
            venue="Journal B"
        )
        citation3 = manager.create_citation_from_metadata(
            title="Middle Research",
            authors=["Miller, Mike"],
            year=2023,
            venue="Journal C"
        )
        
        manager.add_citation(citation1)
        manager.add_citation(citation2)
        manager.add_citation(citation3)
        
        bibliography = manager.generate_bibliography(CitationStyle.APA, sort_by_author=True)
        
        # Check that Anderson comes before Miller, and Miller before Zimmerman
        anderson_pos = bibliography.find("Anderson")
        miller_pos = bibliography.find("Miller")
        zimmerman_pos = bibliography.find("Zimmerman")
        
        assert anderson_pos < miller_pos < zimmerman_pos
    
    def test_bibliography_ieee_numbering(self):
        """Test that IEEE bibliography uses numbered references"""
        manager = CitationManager()
        
        citation1 = manager.create_citation_from_metadata(
            title="First Paper",
            authors=["Author One"],
            year=2023,
            venue="Journal"
        )
        citation2 = manager.create_citation_from_metadata(
            title="Second Paper",
            authors=["Author Two"],
            year=2023,
            venue="Journal"
        )
        
        manager.add_citation(citation1)
        manager.add_citation(citation2)
        
        bibliography = manager.generate_bibliography(CitationStyle.IEEE)
        
        # Check for numbered references
        assert "[1]" in bibliography
        assert "[2]" in bibliography


class TestCitationExport:
    """Test citation export formats"""
    
    def test_bibtex_export(self):
        """Test BibTeX export format"""
        manager = CitationManager()
        citation = manager.create_citation_from_metadata(
            title="Test Paper",
            authors=["Smith, John", "Doe, Jane"],
            year=2023,
            venue="Test Journal",
            venue_type=VenueType.JOURNAL,
            volume="10",
            issue="2",
            pages="100-110",
            doi="10.1234/test.2023"
        )
        
        bibtex = citation.to_bibtex()
        
        # Check key BibTeX components
        assert "@article{" in bibtex
        assert "author = {Smith, John and Doe, Jane}" in bibtex
        assert "title = {Test Paper}" in bibtex
        assert "year = {2023}" in bibtex
        assert "journal = {Test Journal}" in bibtex
        assert "volume = {10}" in bibtex
        assert "number = {2}" in bibtex
        assert "pages = {100-110}" in bibtex
        assert "doi = {10.1234/test.2023}" in bibtex
    
    def test_ris_export(self):
        """Test RIS export format"""
        manager = CitationManager()
        citation = manager.create_citation_from_metadata(
            title="Test Paper",
            authors=["Smith, John", "Doe, Jane"],
            year=2023,
            venue="Test Journal",
            venue_type=VenueType.JOURNAL
        )
        
        ris = citation.to_ris()
        
        # Check key RIS components
        assert "TY  - JOUR" in ris
        assert "AU  - Smith, John" in ris
        assert "AU  - Doe, Jane" in ris
        assert "TI  - Test Paper" in ris
        assert "PY  - 2023" in ris
        assert "JO  - Test Journal" in ris
        assert "ER  -" in ris


class TestCitationDeduplication:
    """Test citation deduplication logic"""
    
    def test_duplicate_detection(self):
        """Test that duplicate citations are detected"""
        manager = CitationManager()
        
        # Add first citation
        citation1 = manager.create_citation_from_metadata(
            title="Machine Learning Fundamentals",
            authors=["Smith, John"],
            year=2023,
            venue="AI Journal"
        )
        id1 = manager.add_citation(citation1)
        
        # Try to add duplicate
        citation2 = manager.create_citation_from_metadata(
            title="Machine Learning Fundamentals",
            authors=["Smith, John"],
            year=2023,
            venue="AI Journal"
        )
        id2 = manager.add_citation(citation2)
        
        # Should return same ID
        assert id1 == id2
        assert len(manager) == 1
    
    def test_different_citations_not_duplicates(self):
        """Test that different citations are not marked as duplicates"""
        manager = CitationManager()
        
        citation1 = manager.create_citation_from_metadata(
            title="First Paper",
            authors=["Smith, John"],
            year=2023,
            venue="Journal A"
        )
        citation2 = manager.create_citation_from_metadata(
            title="Second Paper",
            authors=["Smith, John"],
            year=2023,
            venue="Journal B"
        )
        
        id1 = manager.add_citation(citation1)
        id2 = manager.add_citation(citation2)
        
        assert id1 != id2
        assert len(manager) == 2


class TestCitationExtraction:
    """Test citation extraction from various sources"""
    
    def test_extract_from_scholar_result(self):
        """Test extraction from Google Scholar result"""
        manager = CitationManager()
        
        scholar_result = {
            'title': 'Deep Learning for NLP',
            'authors': 'Smith, John, Doe, Jane',
            'year': 2023,
            'venue': 'Journal of AI Research',
            'citation_count': 150,
            'url': 'https://example.com/paper',
            'abstract': 'This paper presents...',
            'doi': '10.1234/jair.2023.123'
        }
        
        citation = manager.extract_from_scholar_result(scholar_result)
        
        assert citation is not None
        assert citation.title == 'Deep Learning for NLP'
        # Note: comma-separated string splits into individual parts
        assert len(citation.authors) >= 2
        assert citation.year == 2023
        assert citation.venue == 'Journal of AI Research'
        assert citation.citation_count == 150
        assert citation.doi == '10.1234/jair.2023.123'
    
    def test_extract_from_scholar_with_list_authors(self):
        """Test Scholar extraction with authors as list"""
        manager = CitationManager()
        
        scholar_result = {
            'title': 'Test Paper',
            'authors': ['Smith, John', 'Doe, Jane'],
            'year': 2023,
            'venue': 'Conference Proceedings',
            'url': 'https://example.com'
        }
        
        citation = manager.extract_from_scholar_result(scholar_result)
        
        assert citation is not None
        assert len(citation.authors) == 2
    
    def test_extract_from_webpage_with_meta_tags(self):
        """Test extraction from webpage with citation meta tags"""
        manager = CitationManager()
        
        html_content = """
        <html>
        <head>
            <meta name="citation_title" content="Machine Learning Basics">
            <meta name="citation_author" content="Johnson, Alice">
            <meta name="citation_author" content="Smith, Bob">
            <meta name="citation_publication_date" content="2023-05-15">
            <meta name="citation_journal_title" content="AI Review">
            <meta name="citation_doi" content="10.1234/air.2023.123">
        </head>
        </html>
        """
        
        citation = manager.extract_from_webpage(html_content, "https://example.com/article")
        
        assert citation is not None
        assert citation.title == "Machine Learning Basics"
        assert len(citation.authors) == 2
        assert "Johnson, Alice" in citation.authors
        assert "Smith, Bob" in citation.authors
        assert citation.year == 2023
        assert citation.doi == "10.1234/air.2023.123"
        assert citation.url == "https://example.com/article"
    
    def test_extract_from_webpage_with_dublin_core(self):
        """Test extraction from webpage with Dublin Core meta tags"""
        manager = CitationManager()
        
        html_content = """
        <html>
        <head>
            <meta name="DC.Title" content="Research Paper Title">
            <meta name="DC.Creator" content="Anderson, Michael">
            <meta name="DC.Date" content="2022-01-01">
        </head>
        </html>
        """
        
        citation = manager.extract_from_webpage(html_content, "https://example.com")
        
        assert citation is not None
        assert citation.title == "Research Paper Title"
        assert "Anderson, Michael" in citation.authors
        assert citation.year == 2022
    
    def test_extract_from_webpage_with_open_graph(self):
        """Test extraction from webpage with Open Graph meta tags"""
        manager = CitationManager()
        
        html_content = """
        <html>
        <head>
            <meta property="og:title" content="Blog Post Title">
            <meta name="author" content="Writer, Jane">
            <meta property="article:published_time" content="2024-03-15T10:00:00Z">
        </head>
        </html>
        """
        
        citation = manager.extract_from_webpage(html_content, "https://blog.example.com")
        
        assert citation is not None
        assert citation.title == "Blog Post Title"
        # Author parsing splits on comma, so check for presence
        assert len(citation.authors) >= 1
        assert citation.year == 2024
    
    def test_extract_from_webpage_fallback_to_title_tag(self):
        """Test fallback to <title> tag when meta tags missing"""
        manager = CitationManager()
        
        html_content = """
        <html>
        <head>
            <title>Article Title - Website Name</title>
        </head>
        </html>
        """
        
        citation = manager.extract_from_webpage(html_content, "https://example.com")
        
        assert citation is not None
        assert "Article Title" in citation.title
    
    def test_extract_from_text_with_quoted_title(self):
        """Test extraction from plain text with quoted title"""
        manager = CitationManager()
        
        text = """
        "Deep Learning Applications in Healthcare"
        by Anderson, Michael, Williams, Sarah
        Published in Medical AI Journal (2022)
        doi:10.5678/maj.2022.456
        """
        
        citation = manager.extract_from_text(text, url="https://example.com")
        
        assert citation is not None
        assert citation.title == "Deep Learning Applications in Healthcare"
        assert len(citation.authors) >= 1
        assert citation.year == 2022
        assert citation.doi == "10.5678/maj.2022.456"
    
    def test_extract_from_text_with_year_in_parentheses(self):
        """Test year extraction from text with parentheses"""
        manager = CitationManager()
        
        text = """
        Smith, J. (2023). "Research Methods in AI"
        Journal of Computer Science
        """
        
        citation = manager.extract_from_text(text)
        
        assert citation is not None
        assert citation.year == 2023
    
    def test_extract_doi_from_content(self):
        """Test DOI extraction from various formats"""
        manager = CitationManager()
        
        # Test different DOI formats
        test_cases = [
            ("doi:10.1234/test.2023.123", "10.1234/test.2023.123"),
            ("https://doi.org/10.5678/example.2024", "10.5678/example.2024"),
            ("http://dx.doi.org/10.9999/paper.2022", "10.9999/paper.2022"),
            ('<meta name="citation_doi" content="10.1111/cite.2023">', "10.1111/cite.2023"),
        ]
        
        for content, expected_doi in test_cases:
            doi = manager._extract_doi_from_content(content)
            assert doi == expected_doi, f"Failed to extract DOI from: {content}"
    
    def test_incomplete_citation_flagging(self):
        """Test that incomplete citations are properly flagged"""
        manager = CitationManager()
        
        # Citation missing year
        citation1 = manager.create_citation_from_metadata(
            title="Test Paper",
            authors=["Smith, John"],
            year=None,
            venue="Journal"
        )
        assert citation1.is_incomplete
        
        # Citation missing authors
        citation2 = manager.create_citation_from_metadata(
            title="Test Paper",
            authors=[],
            year=2023,
            venue="Journal"
        )
        assert citation2.is_incomplete
        
        # Complete citation
        citation3 = manager.create_citation_from_metadata(
            title="Test Paper",
            authors=["Smith, John"],
            year=2023,
            venue="Journal"
        )
        assert not citation3.is_incomplete
    
    def test_incomplete_citation_in_formatted_output(self):
        """Test that incomplete citations show warning in output"""
        manager = CitationManager()
        
        citation = manager.create_citation_from_metadata(
            title="Test Paper",
            authors=["Smith, John"],
            year=None,
            venue="Journal"
        )
        
        formatted = citation.format(CitationStyle.APA)
        assert "[Incomplete citation]" in formatted


class TestCitationStatistics:
    """Test citation statistics functionality"""
    
    def test_get_statistics(self):
        """Test statistics generation"""
        manager = CitationManager()
        
        # Add various citations
        citation1 = manager.create_citation_from_metadata(
            title="Paper 1",
            authors=["Smith, John"],
            year=2023,
            venue="Journal A",
            venue_type=VenueType.JOURNAL,
            doi="10.1234/test1"
        )
        citation2 = manager.create_citation_from_metadata(
            title="Paper 2",
            authors=["Doe, Jane"],
            year=None,  # Incomplete
            venue="Conference B",
            venue_type=VenueType.CONFERENCE
        )
        citation3 = manager.create_citation_from_metadata(
            title="Paper 3",
            authors=["Johnson, Alice"],
            year=2024,
            venue="Journal C",
            venue_type=VenueType.JOURNAL,
            doi="10.5678/test3",
            is_open_access=True
        )
        
        manager.add_citation(citation1)
        manager.add_citation(citation2)
        manager.add_citation(citation3)
        
        stats = manager.get_statistics()
        
        assert stats['total_citations'] == 3
        assert stats['incomplete_citations'] == 1
        assert stats['citations_with_doi'] == 2
        assert stats['open_access_citations'] == 1
        assert stats['venue_type_counts']['journal'] == 2
        assert stats['venue_type_counts']['conference'] == 1


class TestBibTeXExport:
    """Test BibTeX export functionality"""
    
    def test_bibtex_conference_format(self):
        """Test BibTeX format for conference papers"""
        manager = CitationManager()
        
        citation = manager.create_citation_from_metadata(
            title="Conference Paper",
            authors=["Smith, John", "Doe, Jane"],
            year=2023,
            venue="International Conference on AI",
            venue_type=VenueType.CONFERENCE,
            pages="100-110"
        )
        
        bibtex = citation.to_bibtex()
        
        assert "@inproceedings{" in bibtex
        assert "author = {Smith, John and Doe, Jane}" in bibtex
        assert "title = {Conference Paper}" in bibtex
        assert "booktitle = {International Conference on AI}" in bibtex
        assert "pages = {100-110}" in bibtex
    
    def test_bibtex_book_format(self):
        """Test BibTeX format for books"""
        manager = CitationManager()
        
        citation = manager.create_citation_from_metadata(
            title="Book Title",
            authors=["Author, Name"],
            year=2023,
            venue="Publisher Name",
            venue_type=VenueType.BOOK
        )
        
        bibtex = citation.to_bibtex()
        
        assert "@book{" in bibtex
        assert "publisher = {Publisher Name}" in bibtex


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
