#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit tests for Academic Configuration Module
"""

import unittest
import os
from unittest.mock import patch
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from gazzali.academic_config import (
    AcademicConfig,
    CitationStyle,
    OutputFormat,
    Discipline,
    get_default_config
)


class TestAcademicConfig(unittest.TestCase):
    """Test cases for AcademicConfig class"""
    
    def test_default_configuration(self):
        """Test default configuration values"""
        config = get_default_config()
        
        self.assertEqual(config.citation_style, CitationStyle.APA)
        self.assertEqual(config.output_format, OutputFormat.PAPER)
        self.assertEqual(config.discipline, Discipline.GENERAL)
        self.assertEqual(config.word_count_target, 8000)
        self.assertTrue(config.include_abstract)
        self.assertTrue(config.include_methodology)
        self.assertTrue(config.scholar_priority)
        self.assertFalse(config.export_bibliography)
        self.assertEqual(config.min_peer_reviewed, 5)
        self.assertEqual(config.source_quality_threshold, 7)
    
    def test_from_env_default_values(self):
        """Test loading configuration from environment with defaults"""
        # Clear any existing environment variables
        env_vars = [
            "CITATION_STYLE", "OUTPUT_FORMAT", "DISCIPLINE",
            "WORD_COUNT_TARGET", "INCLUDE_ABSTRACT", "INCLUDE_METHODOLOGY",
            "SCHOLAR_PRIORITY", "EXPORT_BIBLIOGRAPHY",
            "MIN_PEER_REVIEWED_SOURCES", "SOURCE_QUALITY_THRESHOLD"
        ]
        
        for var in env_vars:
            if var in os.environ:
                del os.environ[var]
        
        config = AcademicConfig.from_env()
        
        # Should use defaults
        self.assertEqual(config.citation_style, CitationStyle.APA)
        self.assertEqual(config.output_format, OutputFormat.PAPER)
        self.assertEqual(config.discipline, Discipline.GENERAL)
    
    @patch.dict(os.environ, {
        "CITATION_STYLE": "mla",
        "OUTPUT_FORMAT": "review",
        "DISCIPLINE": "stem",
        "WORD_COUNT_TARGET": "10000",
        "INCLUDE_ABSTRACT": "false",
        "INCLUDE_METHODOLOGY": "false",
        "SCHOLAR_PRIORITY": "false",
        "EXPORT_BIBLIOGRAPHY": "true",
        "MIN_PEER_REVIEWED_SOURCES": "10",
        "SOURCE_QUALITY_THRESHOLD": "8"
    })
    def test_from_env_custom_values(self):
        """Test loading configuration from environment with custom values"""
        config = AcademicConfig.from_env()
        
        self.assertEqual(config.citation_style, CitationStyle.MLA)
        self.assertEqual(config.output_format, OutputFormat.REVIEW)
        self.assertEqual(config.discipline, Discipline.STEM)
        self.assertEqual(config.word_count_target, 10000)
        self.assertFalse(config.include_abstract)
        self.assertFalse(config.include_methodology)
        self.assertFalse(config.scholar_priority)
        self.assertTrue(config.export_bibliography)
        self.assertEqual(config.min_peer_reviewed, 10)
        self.assertEqual(config.source_quality_threshold, 8)
    
    def test_from_args(self):
        """Test loading configuration from command-line arguments"""
        # Mock argparse.Namespace
        class MockArgs:
            citation_style = "chicago"
            output_format = "proposal"
            discipline = "social"
            word_count = 5000
            export_bib = True
        
        args = MockArgs()
        config = AcademicConfig.from_args(args)
        
        self.assertEqual(config.citation_style, CitationStyle.CHICAGO)
        self.assertEqual(config.output_format, OutputFormat.PROPOSAL)
        self.assertEqual(config.discipline, Discipline.SOCIAL)
        self.assertEqual(config.word_count_target, 5000)
        self.assertTrue(config.export_bibliography)
    
    def test_from_args_partial(self):
        """Test loading configuration with only some arguments provided"""
        class MockArgs:
            citation_style = "ieee"
            # Other attributes not present
        
        args = MockArgs()
        config = AcademicConfig.from_args(args)
        
        # Should have the provided value
        self.assertEqual(config.citation_style, CitationStyle.IEEE)
        # Should have defaults for others
        self.assertEqual(config.output_format, OutputFormat.PAPER)
    
    def test_get_prompt_modifiers_stem(self):
        """Test prompt modifiers for STEM discipline"""
        config = AcademicConfig(discipline=Discipline.STEM)
        modifiers = config.get_prompt_modifiers()
        
        self.assertIn("terminology", modifiers)
        self.assertIn("methodology_focus", modifiers)
        self.assertIn("structure", modifiers)
        self.assertIn("depth", modifiers)
        self.assertIn("source_priorities", modifiers)
        self.assertIn("analysis_approach", modifiers)
        self.assertIn("writing_conventions", modifiers)
        
        # Check STEM-specific content
        self.assertIn("technical", modifiers["terminology"].lower())
        self.assertIn("experimental", modifiers["methodology_focus"].lower())
        self.assertIn("reproducibility", modifiers["methodology_focus"].lower())
        self.assertIn("quantitative", modifiers["analysis_approach"].lower())
        self.assertIn("passive voice", modifiers["writing_conventions"].lower())
    
    def test_get_prompt_modifiers_social(self):
        """Test prompt modifiers for social sciences discipline"""
        config = AcademicConfig(discipline=Discipline.SOCIAL)
        modifiers = config.get_prompt_modifiers()
        
        self.assertIn("social science", modifiers["terminology"].lower())
        self.assertIn("qualitative", modifiers["methodology_focus"].lower())
        self.assertIn("validity", modifiers["methodology_focus"].lower())
        self.assertIn("reliability", modifiers["methodology_focus"].lower())
        self.assertIn("cultural context", modifiers["analysis_approach"].lower())
    
    def test_get_prompt_modifiers_humanities(self):
        """Test prompt modifiers for humanities discipline"""
        config = AcademicConfig(discipline=Discipline.HUMANITIES)
        modifiers = config.get_prompt_modifiers()
        
        self.assertIn("humanities", modifiers["terminology"].lower())
        self.assertIn("textual", modifiers["methodology_focus"].lower())
        self.assertIn("hermeneutics", modifiers["terminology"].lower())
        self.assertIn("interpretive", modifiers["analysis_approach"].lower())
        self.assertIn("primary sources", modifiers["source_priorities"].lower())
    
    def test_get_prompt_modifiers_medical(self):
        """Test prompt modifiers for medical discipline"""
        config = AcademicConfig(discipline=Discipline.MEDICAL)
        modifiers = config.get_prompt_modifiers()
        
        self.assertIn("medical", modifiers["terminology"].lower())
        self.assertIn("clinical", modifiers["methodology_focus"].lower())
        self.assertIn("evidence-based", modifiers["methodology_focus"].lower())
        self.assertIn("patient outcomes", modifiers["methodology_focus"].lower())
        self.assertIn("clinical significance", modifiers["analysis_approach"].lower())
    
    def test_get_prompt_modifiers_paper_format(self):
        """Test prompt modifiers for paper output format"""
        config = AcademicConfig(output_format=OutputFormat.PAPER)
        modifiers = config.get_prompt_modifiers()
        
        self.assertIn("Abstract", modifiers["structure"])
        self.assertIn("comprehensive", modifiers["depth"].lower())
    
    def test_get_prompt_modifiers_review_format(self):
        """Test prompt modifiers for review output format"""
        config = AcademicConfig(output_format=OutputFormat.REVIEW)
        modifiers = config.get_prompt_modifiers()
        
        self.assertIn("Literature review", modifiers["structure"])
        self.assertIn("systematic", modifiers["depth"].lower())
    
    def test_get_prompt_modifiers_proposal_format(self):
        """Test prompt modifiers for proposal output format"""
        config = AcademicConfig(output_format=OutputFormat.PROPOSAL)
        modifiers = config.get_prompt_modifiers()
        
        self.assertIn("proposal", modifiers["structure"].lower())
        self.assertIn("forward-looking", modifiers["depth"].lower())
    
    def test_get_prompt_modifiers_abstract_format(self):
        """Test prompt modifiers for abstract output format"""
        config = AcademicConfig(output_format=OutputFormat.ABSTRACT)
        modifiers = config.get_prompt_modifiers()
        
        self.assertIn("abstract", modifiers["structure"].lower())
        self.assertIn("250-300 words", modifiers["structure"])
    
    def test_get_report_structure_paper(self):
        """Test report structure for paper format"""
        config = AcademicConfig(output_format=OutputFormat.PAPER)
        sections = config.get_report_structure()
        
        self.assertIn("Abstract", sections)
        self.assertIn("Introduction", sections)
        self.assertIn("Literature Review", sections)
        self.assertIn("Methodology", sections)
        self.assertIn("Findings", sections)
        self.assertIn("Discussion", sections)
        self.assertIn("Conclusion", sections)
        self.assertIn("References", sections)
    
    def test_get_report_structure_paper_no_abstract(self):
        """Test report structure for paper without abstract"""
        config = AcademicConfig(
            output_format=OutputFormat.PAPER,
            include_abstract=False
        )
        sections = config.get_report_structure()
        
        self.assertNotIn("Abstract", sections)
        self.assertIn("Introduction", sections)
    
    def test_get_report_structure_paper_no_methodology(self):
        """Test report structure for paper without methodology"""
        config = AcademicConfig(
            output_format=OutputFormat.PAPER,
            include_methodology=False
        )
        sections = config.get_report_structure()
        
        self.assertNotIn("Methodology", sections)
        self.assertIn("Findings", sections)
    
    def test_get_report_structure_review(self):
        """Test report structure for literature review format"""
        config = AcademicConfig(output_format=OutputFormat.REVIEW)
        sections = config.get_report_structure()
        
        self.assertIn("Abstract", sections)
        self.assertIn("Introduction", sections)
        self.assertIn("Thematic Analysis", sections)
        self.assertIn("Research Gaps", sections)
        self.assertIn("References", sections)
    
    def test_get_report_structure_proposal(self):
        """Test report structure for proposal format"""
        config = AcademicConfig(output_format=OutputFormat.PROPOSAL)
        sections = config.get_report_structure()
        
        self.assertIn("Research Questions", sections)
        self.assertIn("Proposed Methodology", sections)
        self.assertIn("Expected Outcomes", sections)
        self.assertIn("Timeline", sections)
    
    def test_get_report_structure_abstract(self):
        """Test report structure for abstract format"""
        config = AcademicConfig(output_format=OutputFormat.ABSTRACT)
        sections = config.get_report_structure()
        
        self.assertEqual(len(sections), 1)
        self.assertEqual(sections[0], "Abstract")
    
    def test_validate_valid_config(self):
        """Test validation of valid configuration"""
        config = get_default_config()
        issues = config.validate()
        
        self.assertEqual(len(issues), 0)
    
    def test_validate_low_word_count(self):
        """Test validation with very low word count"""
        config = AcademicConfig(word_count_target=300)
        issues = config.validate()
        
        self.assertTrue(any("low" in issue.lower() for issue in issues))
    
    def test_validate_high_word_count(self):
        """Test validation with very high word count"""
        config = AcademicConfig(word_count_target=60000)
        issues = config.validate()
        
        self.assertTrue(any("high" in issue.lower() for issue in issues))
    
    def test_validate_negative_min_peer_reviewed(self):
        """Test validation with negative minimum peer-reviewed sources"""
        config = AcademicConfig(min_peer_reviewed=-1)
        issues = config.validate()
        
        self.assertTrue(any("negative" in issue.lower() for issue in issues))
    
    def test_validate_invalid_quality_threshold(self):
        """Test validation with invalid quality threshold"""
        config = AcademicConfig(source_quality_threshold=15)
        issues = config.validate()
        
        self.assertTrue(any("threshold" in issue.lower() for issue in issues))
    
    def test_validate_abstract_word_count_mismatch(self):
        """Test validation for abstract format with high word count"""
        config = AcademicConfig(
            output_format=OutputFormat.ABSTRACT,
            word_count_target=5000
        )
        issues = config.validate()
        
        self.assertTrue(any("abstract" in issue.lower() for issue in issues))
    
    def test_to_dict(self):
        """Test conversion to dictionary"""
        config = AcademicConfig(
            citation_style=CitationStyle.MLA,
            output_format=OutputFormat.REVIEW,
            discipline=Discipline.HUMANITIES,
            word_count_target=6000
        )
        
        config_dict = config.to_dict()
        
        self.assertEqual(config_dict["citation_style"], "mla")
        self.assertEqual(config_dict["output_format"], "review")
        self.assertEqual(config_dict["discipline"], "humanities")
        self.assertEqual(config_dict["word_count_target"], 6000)
        self.assertIsInstance(config_dict, dict)
    
    def test_str_representation(self):
        """Test string representation"""
        config = get_default_config()
        config_str = str(config)
        
        self.assertIn("AcademicConfig", config_str)
        self.assertIn("Citation Style", config_str)
        self.assertIn("apa", config_str.lower())
    
    def test_all_citation_styles(self):
        """Test all citation style options"""
        styles = [CitationStyle.APA, CitationStyle.MLA, 
                 CitationStyle.CHICAGO, CitationStyle.IEEE]
        
        for style in styles:
            config = AcademicConfig(citation_style=style)
            self.assertEqual(config.citation_style, style)
    
    def test_all_output_formats(self):
        """Test all output format options"""
        formats = [OutputFormat.PAPER, OutputFormat.REVIEW,
                  OutputFormat.PROPOSAL, OutputFormat.ABSTRACT,
                  OutputFormat.PRESENTATION]
        
        for fmt in formats:
            config = AcademicConfig(output_format=fmt)
            self.assertEqual(config.output_format, fmt)
    
    def test_all_disciplines(self):
        """Test all discipline options"""
        disciplines = [Discipline.GENERAL, Discipline.STEM,
                      Discipline.SOCIAL, Discipline.HUMANITIES,
                      Discipline.MEDICAL]
        
        for discipline in disciplines:
            config = AcademicConfig(discipline=discipline)
            self.assertEqual(config.discipline, discipline)
    
    def test_get_discipline_prompt_text_stem(self):
        """Test discipline prompt text generation for STEM"""
        config = AcademicConfig(discipline=Discipline.STEM)
        prompt_text = config.get_discipline_prompt_text()
        
        self.assertIn("STEM", prompt_text)
        self.assertIn("Terminology", prompt_text)
        self.assertIn("Methodology Focus", prompt_text)
        self.assertIn("Source Priorities", prompt_text)
        self.assertIn("Analysis Approach", prompt_text)
        self.assertIn("Writing Conventions", prompt_text)
    
    def test_get_discipline_prompt_text_general(self):
        """Test discipline prompt text generation for general (should be empty)"""
        config = AcademicConfig(discipline=Discipline.GENERAL)
        prompt_text = config.get_discipline_prompt_text()
        
        self.assertEqual(prompt_text, "")
    
    def test_get_discipline_prompt_text_medical(self):
        """Test discipline prompt text generation for medical"""
        config = AcademicConfig(discipline=Discipline.MEDICAL)
        prompt_text = config.get_discipline_prompt_text()
        
        self.assertIn("MEDICAL", prompt_text)
        self.assertIn("clinical", prompt_text.lower())
        self.assertIn("evidence-based", prompt_text.lower())


if __name__ == "__main__":
    unittest.main()
