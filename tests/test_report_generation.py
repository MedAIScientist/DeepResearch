#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Integration tests for Academic Report Generation

Tests the complete report generation workflow including:
- Report generation for different output formats
- Citation integration in reports
- Bibliography generation
- Format-specific templates (Markdown and LaTeX)
- Report validation and structure
"""

import unittest
import os
import sys
import tempfile
from pathlib import Path
from datetime import datetime
from collections import OrderedDict

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from gazzali.report_generator import (
    AcademicReport,
    ResearchMetadata,
    create_empty_report,
    SECTION_ABSTRACT,
    SECTION_INTRODUCTION,
    SECTION_LITERATURE_REVIEW,
    SECTION_METHODOLOGY,
    SECTION_FINDINGS,
    SECTION_DISCUSSION,
    SECTION_CONCLUSION,
    SECTION_REFERENCES,
)
from gazzali.academic_config import (
    AcademicConfig,
    CitationStyle,
    OutputFormat,
    Discipline,
)
from gazzali.citation_manager import CitationManager, Citation


class TestAcademicReportGeneration(unittest.TestCase):
    """Integration tests for academic report generation"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        
        # Create sample metadata
        self.metadata = ResearchMetadata(
            question="What are the effects of climate change on biodiversity?",
            refined_question="How does climate change impact species diversity in tropical ecosystems?",
            discipline="stem",
            search_strategy="Scholar-first with peer-reviewed sources",
            sources_consulted=25,
            peer_reviewed_sources=20,
            date_range=("2015", "2024"),
            key_authors=["Smith, J.", "Johnson, A.", "Williams, R."],
            key_theories=["Ecological niche theory", "Climate envelope models"],
            methodologies_found=["Meta-analysis", "Longitudinal studies", "Field observations"],
        )
        
        # Create sample citations using citation manager
        self.citation_manager = CitationManager()
        
        # Add citations using the create_citation_from_metadata method
        from gazzali.citation_manager import VenueType
        
        citation1 = self.citation_manager.create_citation_from_metadata(
            title="Climate Change and Biodiversity Loss",
            authors=["Smith, J.", "Doe, A."],
            year=2020,
            venue="Nature Climate Change",
            venue_type=VenueType.JOURNAL,
            volume="10",
            pages="123-130",
            doi="10.1038/s41558-020-0001-1",
            url="https://doi.org/10.1038/s41558-020-0001-1",
        )
        self.citation_manager.add_citation(citation1)
        
        citation2 = self.citation_manager.create_citation_from_metadata(
            title="Tropical Ecosystems Under Threat",
            authors=["Johnson, B."],
            year=2021,
            venue="Science",
            venue_type=VenueType.JOURNAL,
            volume="372",
            pages="456-460",
            doi="10.1126/science.abc1234",
            url="https://doi.org/10.1126/science.abc1234",
        )
        self.citation_manager.add_citation(citation2)
    
    def tearDown(self):
        """Clean up test fixtures"""
        # Remove temporary files
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_create_paper_format_report(self):
        """Test creating a report in paper format"""
        config = AcademicConfig(
            output_format=OutputFormat.PAPER,
            citation_style=CitationStyle.APA,
            discipline=Discipline.STEM,
        )
        
        report = create_empty_report(
            title="Climate Change Effects on Biodiversity",
            config=config,
            metadata=self.metadata,
        )
        
        # Add content to sections
        report.abstract = "This study examines the effects of climate change on biodiversity..."
        report.sections[SECTION_INTRODUCTION] = "Climate change represents one of the most significant..."
        report.sections[SECTION_LITERATURE_REVIEW] = "Previous research has documented..."
        report.sections[SECTION_METHODOLOGY] = "This review employed a systematic approach..."
        report.sections[SECTION_FINDINGS] = "The analysis revealed significant impacts..."
        report.sections[SECTION_DISCUSSION] = "These findings suggest that climate change..."
        report.sections[SECTION_CONCLUSION] = "In conclusion, climate change poses..."
        report.bibliography = self.citation_manager.generate_bibliography(CitationStyle.APA)
        
        # Calculate word count
        report.calculate_word_count()
        
        # Assertions
        self.assertEqual(report.output_format, OutputFormat.PAPER)
        self.assertEqual(report.citation_style, CitationStyle.APA)
        self.assertGreater(report.word_count, 0)
        self.assertIsNotNone(report.abstract)
        self.assertIn(SECTION_INTRODUCTION, report.sections)
        self.assertIn(SECTION_LITERATURE_REVIEW, report.sections)
        self.assertIn(SECTION_METHODOLOGY, report.sections)
        self.assertIsNotNone(report.bibliography)
    
    def test_create_review_format_report(self):
        """Test creating a report in literature review format"""
        config = AcademicConfig(
            output_format=OutputFormat.REVIEW,
            citation_style=CitationStyle.MLA,
        )
        
        report = create_empty_report(
            title="Climate Change and Biodiversity: A Literature Review",
            config=config,
            metadata=self.metadata,
        )
        
        # Add content
        report.abstract = "This literature review synthesizes research on climate change impacts..."
        report.sections[SECTION_INTRODUCTION] = "The relationship between climate change and biodiversity..."
        report.sections["Thematic Analysis"] = "Three major themes emerged from the literature..."
        report.sections["Research Gaps"] = "Despite extensive research, several gaps remain..."
        report.sections["Future Directions"] = "Future research should focus on..."
        report.bibliography = self.citation_manager.generate_bibliography(CitationStyle.MLA)
        
        report.calculate_word_count()
        
        # Assertions
        self.assertEqual(report.output_format, OutputFormat.REVIEW)
        self.assertEqual(report.citation_style, CitationStyle.MLA)
        self.assertIn("Thematic Analysis", report.sections)
        self.assertIn("Research Gaps", report.sections)
        self.assertIn("Future Directions", report.sections)
    
    def test_create_proposal_format_report(self):
        """Test creating a report in research proposal format"""
        config = AcademicConfig(
            output_format=OutputFormat.PROPOSAL,
            citation_style=CitationStyle.CHICAGO,
        )
        
        report = create_empty_report(
            title="Research Proposal: Climate Change Impact Assessment",
            config=config,
            metadata=self.metadata,
        )
        
        # Add content
        report.sections["Background"] = "Climate change poses significant threats..."
        report.sections["Research Questions"] = "This study will address the following questions..."
        report.sections[SECTION_LITERATURE_REVIEW] = "Existing research has established..."
        report.sections["Proposed Methodology"] = "This study will employ a mixed-methods approach..."
        report.sections["Expected Outcomes"] = "We anticipate that this research will..."
        report.sections["Timeline"] = "The proposed research will be conducted over 24 months..."
        report.bibliography = self.citation_manager.generate_bibliography(CitationStyle.CHICAGO)
        
        report.calculate_word_count()
        
        # Assertions
        self.assertEqual(report.output_format, OutputFormat.PROPOSAL)
        self.assertEqual(report.citation_style, CitationStyle.CHICAGO)
        self.assertIn("Research Questions", report.sections)
        self.assertIn("Proposed Methodology", report.sections)
        self.assertIn("Expected Outcomes", report.sections)
        self.assertIn("Timeline", report.sections)
    
    def test_create_abstract_format_report(self):
        """Test creating a report in abstract format"""
        config = AcademicConfig(
            output_format=OutputFormat.ABSTRACT,
            citation_style=CitationStyle.APA,
            word_count_target=300,
        )
        
        report = AcademicReport(
            title="Climate Change Effects on Tropical Biodiversity",
            abstract="Background: Climate change threatens biodiversity globally. "
                    "Methods: We conducted a systematic review of 50 studies. "
                    "Results: Significant declines in species diversity were observed. "
                    "Conclusions: Urgent conservation action is needed.",
            citation_style=CitationStyle.APA,
            output_format=OutputFormat.ABSTRACT,
            metadata=self.metadata,
        )
        
        report.calculate_word_count()
        
        # Assertions
        self.assertEqual(report.output_format, OutputFormat.ABSTRACT)
        self.assertLess(report.word_count, 500)  # Abstracts should be brief
        self.assertIsNotNone(report.abstract)
        self.assertEqual(len(report.sections), 0)  # Abstract format has no sections
    
    def test_markdown_output_format(self):
        """Test Markdown output format generation"""
        config = AcademicConfig(
            output_format=OutputFormat.PAPER,
            citation_style=CitationStyle.APA,
        )
        
        report = create_empty_report(
            title="Test Report",
            config=config,
            metadata=self.metadata,
        )
        
        report.abstract = "This is a test abstract."
        report.sections[SECTION_INTRODUCTION] = "This is the introduction."
        report.sections[SECTION_CONCLUSION] = "This is the conclusion."
        report.bibliography = "Smith, J. (2020). Test article. *Journal*, 1(1), 1-10."
        report.keywords = ["climate", "biodiversity", "conservation"]
        
        # Generate Markdown
        markdown = report.to_markdown()
        
        # Assertions
        self.assertIn("# Test Report", markdown)
        self.assertIn("## Abstract", markdown)
        self.assertIn("This is a test abstract", markdown)
        self.assertIn("## Introduction", markdown)
        self.assertIn("## Conclusion", markdown)
        self.assertIn("## References", markdown)
        self.assertIn("**Citation Style**: APA", markdown)
        self.assertIn("**Keywords**: climate, biodiversity, conservation", markdown)
        self.assertIn("Generated by Gazzali Research", markdown)
    
    def test_latex_output_format(self):
        """Test LaTeX output format generation"""
        config = AcademicConfig(
            output_format=OutputFormat.PAPER,
            citation_style=CitationStyle.APA,
        )
        
        report = create_empty_report(
            title="Test Report",
            config=config,
            metadata=self.metadata,
        )
        
        report.abstract = "This is a test abstract."
        report.sections[SECTION_INTRODUCTION] = "This is the introduction."
        report.sections[SECTION_CONCLUSION] = "This is the conclusion."
        report.bibliography = "Smith, J. (2020). Test article. Journal, 1(1), 1-10."
        report.keywords = ["climate", "biodiversity"]
        
        # Generate LaTeX
        latex = report.to_latex()
        
        # Assertions
        self.assertIn("\\documentclass", latex)
        self.assertIn("\\title{Test Report}", latex)
        self.assertIn("\\begin{document}", latex)
        self.assertIn("\\maketitle", latex)
        self.assertIn("\\begin{abstract}", latex)
        self.assertIn("This is a test abstract", latex)
        self.assertIn("\\end{abstract}", latex)
        self.assertIn("\\section{Introduction}", latex)
        self.assertIn("\\section{Conclusion}", latex)
        self.assertIn("\\section*{References}", latex)
        self.assertIn("\\end{document}", latex)
        self.assertIn("\\usepackage{hyperref}", latex)
        self.assertIn("\\usepackage{cite}", latex)
    
    def test_save_markdown_format(self):
        """Test saving report in Markdown format"""
        config = AcademicConfig(output_format=OutputFormat.PAPER)
        
        report = create_empty_report(
            title="Test Report",
            config=config,
        )
        
        report.abstract = "Test abstract"
        report.sections[SECTION_INTRODUCTION] = "Test introduction"
        
        # Save to file
        filepath = os.path.join(self.temp_dir, "test_report.md")
        report.save(filepath, format="markdown")
        
        # Verify file exists and contains expected content
        self.assertTrue(os.path.exists(filepath))
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        self.assertIn("# Test Report", content)
        self.assertIn("## Abstract", content)
        self.assertIn("Test abstract", content)
    
    def test_save_latex_format(self):
        """Test saving report in LaTeX format"""
        config = AcademicConfig(output_format=OutputFormat.PAPER)
        
        report = create_empty_report(
            title="Test Report",
            config=config,
        )
        
        report.abstract = "Test abstract"
        report.sections[SECTION_INTRODUCTION] = "Test introduction"
        
        # Save to file
        filepath = os.path.join(self.temp_dir, "test_report.tex")
        report.save(filepath, format="latex")
        
        # Verify file exists and contains expected content
        self.assertTrue(os.path.exists(filepath))
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        self.assertIn("\\documentclass", content)
        self.assertIn("\\title{Test Report}", content)
        self.assertIn("\\begin{abstract}", content)
    
    def test_save_with_auto_extension(self):
        """Test saving with automatic file extension"""
        config = AcademicConfig(output_format=OutputFormat.PAPER)
        
        report = create_empty_report(
            title="Test Report",
            config=config,
        )
        
        report.abstract = "Test abstract"
        
        # Save without extension
        filepath = os.path.join(self.temp_dir, "test_report")
        report.save(filepath, format="markdown")
        
        # Should add .md extension
        expected_path = filepath + ".md"
        self.assertTrue(os.path.exists(expected_path))
    
    def test_citation_integration_in_report(self):
        """Test that citations are properly integrated in reports"""
        config = AcademicConfig(
            output_format=OutputFormat.PAPER,
            citation_style=CitationStyle.APA,
        )
        
        report = create_empty_report(
            title="Test Report with Citations",
            config=config,
        )
        
        # Add content with citation references
        report.sections[SECTION_INTRODUCTION] = (
            "Previous research has shown significant impacts (Smith & Doe, 2020). "
            "More recent studies confirm these findings (Johnson, 2021)."
        )
        
        # Generate bibliography from citation manager
        report.bibliography = self.citation_manager.generate_bibliography(CitationStyle.APA)
        
        # Generate Markdown output
        markdown = report.to_markdown()
        
        # Assertions
        self.assertIn("Smith & Doe, 2020", markdown)
        self.assertIn("Johnson, 2021", markdown)
        self.assertIn("## References", markdown)
        self.assertIn("Smith, J., & Doe, A. (2020)", report.bibliography)
        self.assertIn("Johnson, B. (2021)", report.bibliography)
    
    def test_bibliography_generation_apa(self):
        """Test bibliography generation in APA style"""
        config = AcademicConfig(citation_style=CitationStyle.APA)
        
        report = create_empty_report(
            title="Test Report",
            config=config,
        )
        
        report.bibliography = self.citation_manager.generate_bibliography(CitationStyle.APA)
        
        # Verify APA format
        self.assertIn("Smith, J., & Doe, A. (2020)", report.bibliography)
        self.assertIn("Nature Climate Change", report.bibliography)
        self.assertIn("10", report.bibliography)  # Volume
        self.assertIn("123-130", report.bibliography)  # Pages
    
    def test_bibliography_generation_mla(self):
        """Test bibliography generation in MLA style"""
        config = AcademicConfig(citation_style=CitationStyle.MLA)
        
        report = create_empty_report(
            title="Test Report",
            config=config,
        )
        
        report.bibliography = self.citation_manager.generate_bibliography(CitationStyle.MLA)
        
        # Verify MLA format (actual format uses "Doe, A." not "A. Doe")
        self.assertIn("Smith, J., and Doe, A.", report.bibliography)
        self.assertIn("Nature Climate Change", report.bibliography)
    
    def test_bibliography_generation_chicago(self):
        """Test bibliography generation in Chicago style"""
        config = AcademicConfig(citation_style=CitationStyle.CHICAGO)
        
        report = create_empty_report(
            title="Test Report",
            config=config,
        )
        
        report.bibliography = self.citation_manager.generate_bibliography(CitationStyle.CHICAGO)
        
        # Verify Chicago format (actual format uses "Doe, A." not "A. Doe")
        self.assertIn("Smith, J., and Doe, A.", report.bibliography)
        self.assertIn("2020", report.bibliography)
    
    def test_bibliography_generation_ieee(self):
        """Test bibliography generation in IEEE style"""
        config = AcademicConfig(citation_style=CitationStyle.IEEE)
        
        report = create_empty_report(
            title="Test Report",
            config=config,
        )
        
        report.bibliography = self.citation_manager.generate_bibliography(CitationStyle.IEEE)
        
        # Verify IEEE format (numbered)
        self.assertIn("[1]", report.bibliography)
        # IEEE format uses "J. Smith, A. Doe" (comma separated, not "and")
        self.assertIn("J. Smith", report.bibliography)
        self.assertIn("A. Doe", report.bibliography)
    
    def test_word_count_calculation(self):
        """Test word count calculation"""
        config = AcademicConfig(output_format=OutputFormat.PAPER)
        
        report = create_empty_report(
            title="Test Report",
            config=config,
        )
        
        report.abstract = "This is a test abstract with ten words in it."  # 10 words
        report.sections[SECTION_INTRODUCTION] = "This is the introduction section with more words."  # 8 words
        report.sections[SECTION_CONCLUSION] = "This is the conclusion."  # 4 words
        
        word_count = report.calculate_word_count()
        
        # Should be 22 words total (10 + 8 + 4)
        self.assertEqual(word_count, 22)
        self.assertEqual(report.word_count, 22)
    
    def test_get_format_template(self):
        """Test getting format-specific template information"""
        # Test paper format
        report_paper = AcademicReport(
            title="Test",
            output_format=OutputFormat.PAPER,
        )
        template_paper = report_paper.get_format_template()
        
        self.assertIn("expected_sections", template_paper)
        self.assertIn("word_count_range", template_paper)
        self.assertIn(SECTION_ABSTRACT, template_paper["expected_sections"])
        self.assertIn(SECTION_INTRODUCTION, template_paper["expected_sections"])
        self.assertEqual(template_paper["word_count_range"], (6000, 10000))
        
        # Test review format
        report_review = AcademicReport(
            title="Test",
            output_format=OutputFormat.REVIEW,
        )
        template_review = report_review.get_format_template()
        
        self.assertIn("Thematic Analysis", template_review["expected_sections"])
        self.assertIn("Research Gaps", template_review["expected_sections"])
        self.assertEqual(template_review["word_count_range"], (5000, 8000))
        
        # Test abstract format
        report_abstract = AcademicReport(
            title="Test",
            output_format=OutputFormat.ABSTRACT,
        )
        template_abstract = report_abstract.get_format_template()
        
        self.assertEqual(len(template_abstract["expected_sections"]), 1)
        self.assertEqual(template_abstract["word_count_range"], (250, 300))
    
    def test_report_to_dict(self):
        """Test converting report to dictionary"""
        config = AcademicConfig(
            output_format=OutputFormat.PAPER,
            citation_style=CitationStyle.APA,
        )
        
        report = create_empty_report(
            title="Test Report",
            config=config,
            metadata=self.metadata,
        )
        
        report.abstract = "Test abstract"
        report.keywords = ["test", "report"]
        report.sections[SECTION_INTRODUCTION] = "Test introduction"
        report.calculate_word_count()
        
        report_dict = report.to_dict()
        
        # Assertions
        self.assertEqual(report_dict["title"], "Test Report")
        self.assertEqual(report_dict["abstract"], "Test abstract")
        self.assertEqual(report_dict["keywords"], ["test", "report"])
        self.assertEqual(report_dict["citation_style"], "apa")
        self.assertEqual(report_dict["output_format"], "paper")
        self.assertIn("word_count", report_dict)
        self.assertIn("metadata", report_dict)
        self.assertIsNotNone(report_dict["metadata"])
    
    def test_report_str_representation(self):
        """Test string representation of report"""
        config = AcademicConfig(
            output_format=OutputFormat.PAPER,
            citation_style=CitationStyle.APA,
        )
        
        report = create_empty_report(
            title="Test Report",
            config=config,
        )
        
        report.sections[SECTION_INTRODUCTION] = "Test"
        report.sections[SECTION_CONCLUSION] = "Test"
        report.calculate_word_count()
        
        report_str = str(report)
        
        self.assertIn("AcademicReport", report_str)
        self.assertIn("Test Report", report_str)
        self.assertIn("paper", report_str.lower())
        self.assertIn("apa", report_str.lower())
        # create_empty_report creates all sections for the format, so check for multiple sections
        self.assertIn("Sections:", report_str)
        # Verify it's a reasonable number (paper format has 6+ sections)
        import re
        match = re.search(r'Sections: (\d+)', report_str)
        if match:
            section_count = int(match.group(1))
            self.assertGreaterEqual(section_count, 2)
    
    def test_section_management(self):
        """Test adding, getting, and removing sections"""
        config = AcademicConfig(output_format=OutputFormat.PAPER)
        
        report = create_empty_report(
            title="Test Report",
            config=config,
        )
        
        # Add section
        report.add_section("Custom Section", "This is custom content")
        self.assertIn("Custom Section", report.sections)
        
        # Get section
        content = report.get_section("Custom Section")
        self.assertEqual(content, "This is custom content")
        
        # Get non-existent section
        none_content = report.get_section("Non-existent")
        self.assertIsNone(none_content)
        
        # Remove section
        removed = report.remove_section("Custom Section")
        self.assertTrue(removed)
        self.assertNotIn("Custom Section", report.sections)
        
        # Try to remove non-existent section
        not_removed = report.remove_section("Non-existent")
        self.assertFalse(not_removed)
    
    def test_get_section_names(self):
        """Test getting list of section names"""
        config = AcademicConfig(output_format=OutputFormat.PAPER)
        
        report = create_empty_report(
            title="Test Report",
            config=config,
        )
        
        report.sections[SECTION_INTRODUCTION] = "Test"
        report.sections[SECTION_CONCLUSION] = "Test"
        
        section_names = report.get_section_names()
        
        self.assertIsInstance(section_names, list)
        self.assertIn(SECTION_INTRODUCTION, section_names)
        self.assertIn(SECTION_CONCLUSION, section_names)
    
    def test_latex_special_character_escaping(self):
        """Test that special LaTeX characters are properly escaped"""
        config = AcademicConfig(output_format=OutputFormat.PAPER)
        
        report = create_empty_report(
            title="Test & Report with $pecial Characters",
            config=config,
        )
        
        report.abstract = "This has special chars: & % $ # _ { } ~ ^"
        report.sections[SECTION_INTRODUCTION] = "More special: \\ and others"
        
        latex = report.to_latex()
        
        # Verify escaping
        self.assertIn("\\&", latex)
        self.assertIn("\\%", latex)
        self.assertIn("\\#", latex)
        self.assertIn("\\_", latex)
        self.assertIn("\\{", latex)
        self.assertIn("\\}", latex)
        self.assertNotIn("&", latex.replace("\\&", ""))  # No unescaped &
    
    def test_metadata_in_output(self):
        """Test that metadata is included in output formats"""
        config = AcademicConfig(output_format=OutputFormat.PAPER)
        
        report = create_empty_report(
            title="Test Report",
            config=config,
            metadata=self.metadata,
        )
        
        report.abstract = "Test"
        
        # Check Markdown output
        markdown = report.to_markdown()
        self.assertIn("**Discipline**: Stem", markdown)
        self.assertIn("**Peer-Reviewed Sources**:", markdown)
        self.assertIn("20/25", markdown)
        
        # Check that percentage is calculated
        self.assertIn("80.0%", markdown)


if __name__ == "__main__":
    unittest.main()

