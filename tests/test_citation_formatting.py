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


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
