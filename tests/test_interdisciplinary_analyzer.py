#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit tests for Interdisciplinary Analyzer Module
"""

import unittest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from gazzali.interdisciplinary_analyzer import (
    InterdisciplinaryAnalyzer,
    AcademicDiscipline,
    DisciplinaryPerspective,
    InterdisciplinaryInsight
)


class TestInterdisciplinaryAnalyzer(unittest.TestCase):
    """Test cases for InterdisciplinaryAnalyzer class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.analyzer = InterdisciplinaryAnalyzer()
    
    def test_identify_disciplines_psychology(self):
        """Test identification of psychology discipline"""
        text = """
        This study examines cognitive processes and behavioral responses.
        Participants showed increased attention and improved memory performance.
        The psychological mechanisms underlying learning were investigated.
        """
        
        disciplines = self.analyzer.identify_disciplines(text)
        
        self.assertIn(AcademicDiscipline.PSYCHOLOGY, disciplines)
    
    def test_identify_disciplines_multiple(self):
        """Test identification of multiple disciplines"""
        text = """
        This interdisciplinary study combines neural imaging with economic
        decision-making models. Participants' brain activity was measured
        using fMRI while they made financial choices. The research integrates
        neuroscience methods with economic theory to understand utility
        maximization in the human brain.
        """
        
        disciplines = self.analyzer.identify_disciplines(text)
        
        # Should identify both neuroscience and economics
        self.assertIn(AcademicDiscipline.NEUROSCIENCE, disciplines)
        self.assertIn(AcademicDiscipline.ECONOMICS, disciplines)
    
    def test_add_perspective(self):
        """Test adding a disciplinary perspective"""
        content = "This study uses experimental methods to test hypotheses."
        source = "Smith et al., 2020"
        
        perspective = self.analyzer.add_perspective(
            discipline=AcademicDiscipline.PSYCHOLOGY,
            content=content,
            source=source
        )
        
        self.assertEqual(perspective.discipline, AcademicDiscipline.PSYCHOLOGY)
        self.assertIn(source, perspective.sources)
        self.assertIn(AcademicDiscipline.PSYCHOLOGY, self.analyzer.perspectives)
    
    def test_convergence_analysis(self):
        """Test convergence analysis across disciplines"""
        # Add perspectives from multiple disciplines with overlapping concepts
        self.analyzer.add_perspective(
            discipline=AcademicDiscipline.PSYCHOLOGY,
            content="Memory consolidation is crucial for Learning processes.",
            source="Psych Source"
        )
        
        self.analyzer.add_perspective(
            discipline=AcademicDiscipline.NEUROSCIENCE,
            content="Neural mechanisms support Memory consolidation during sleep.",
            source="Neuro Source"
        )
        
        insights = self.analyzer.analyze_convergence_divergence()
        
        # Should identify convergence on "Memory" concept
        self.assertIsInstance(insights, InterdisciplinaryInsight)
        self.assertTrue(len(insights.convergence_areas) > 0)
    
    def test_translate_terminology(self):
        """Test terminology translation across disciplines"""
        translations = self.analyzer.translate_terminology("network")
        
        # Should have translations for multiple disciplines
        self.assertIn(AcademicDiscipline.COMPUTER_SCIENCE, translations)
        self.assertIn(AcademicDiscipline.SOCIOLOGY, translations)
        self.assertIn(AcademicDiscipline.NEUROSCIENCE, translations)
        
        # Check that translations are different
        cs_def = translations[AcademicDiscipline.COMPUTER_SCIENCE]
        soc_def = translations[AcademicDiscipline.SOCIOLOGY]
        self.assertNotEqual(cs_def, soc_def)
    
    def test_generate_synthesis(self):
        """Test synthesis generation"""
        # Add multiple perspectives
        self.analyzer.add_perspective(
            discipline=AcademicDiscipline.PSYCHOLOGY,
            content="Cognitive processes affect decision making.",
            source="Source 1"
        )
        
        self.analyzer.add_perspective(
            discipline=AcademicDiscipline.ECONOMICS,
            content="Economic models predict rational choices.",
            source="Source 2"
        )
        
        synthesis = self.analyzer.generate_synthesis()
        
        # Should generate non-empty synthesis
        self.assertIsInstance(synthesis, str)
        self.assertTrue(len(synthesis) > 0)
        self.assertIn("Psychology", synthesis)
        self.assertIn("Economics", synthesis)
    
    def test_get_search_queries_for_disciplines(self):
        """Test generation of discipline-specific search queries"""
        base_query = "artificial intelligence ethics"
        disciplines = [
            AcademicDiscipline.COMPUTER_SCIENCE,
            AcademicDiscipline.PHILOSOPHY
        ]
        
        queries = self.analyzer.get_search_queries_for_disciplines(
            base_query=base_query,
            disciplines=disciplines
        )
        
        # Should include base query
        self.assertIn(base_query, queries)
        
        # Should include discipline-specific queries
        self.assertTrue(any("computer science" in q.lower() for q in queries))
        self.assertTrue(any("philosophy" in q.lower() for q in queries))
    
    def test_format_interdisciplinary_report_section(self):
        """Test formatting of interdisciplinary report section"""
        # Add perspectives
        perspective1 = self.analyzer.add_perspective(
            discipline=AcademicDiscipline.PSYCHOLOGY,
            content="Psychological research on behavior.",
            source="Psych Source"
        )
        perspective1.add_framework("Cognitive Theory")
        perspective1.add_methodology("Experiments")
        perspective1.add_finding("Behavior is influenced by cognition")
        
        perspective2 = self.analyzer.add_perspective(
            discipline=AcademicDiscipline.SOCIOLOGY,
            content="Sociological analysis of social structures.",
            source="Soc Source"
        )
        perspective2.add_framework("Social Structure Theory")
        perspective2.add_methodology("Surveys")
        perspective2.add_finding("Social context shapes behavior")
        
        # Analyze convergence
        self.analyzer.analyze_convergence_divergence()
        
        # Generate report section
        report_section = self.analyzer.format_interdisciplinary_report_section()
        
        # Should contain key elements
        self.assertIn("Interdisciplinary Perspectives", report_section)
        self.assertIn("Psychology", report_section)
        self.assertIn("Sociology", report_section)
        self.assertIn("Cognitive Theory", report_section)
        self.assertIn("Social Structure Theory", report_section)
    
    def test_get_terminology_glossary(self):
        """Test generation of terminology glossary"""
        glossary = self.analyzer.get_terminology_glossary()
        
        # Should include predefined terms
        self.assertIn("network", glossary)
        self.assertIn("system", glossary)
        self.assertIn("model", glossary)
        
        # Each term should have multiple discipline definitions
        self.assertTrue(len(glossary["network"]) > 1)
    
    def test_clear(self):
        """Test clearing analyzer state"""
        # Add some data
        self.analyzer.add_perspective(
            discipline=AcademicDiscipline.PSYCHOLOGY,
            content="Test content",
            source="Test source"
        )
        
        # Clear
        self.analyzer.clear()
        
        # Should be empty
        self.assertEqual(len(self.analyzer.perspectives), 0)
        self.assertEqual(len(self.analyzer.insights.convergence_areas), 0)


if __name__ == '__main__':
    unittest.main()
