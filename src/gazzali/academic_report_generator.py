#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Academic Report Generator for Gazzali Research

This module provides the core report generation functionality for creating
structured academic reports with proper formatting, citations, and section
organization. It integrates with the synthesis model to generate comprehensive
academic documents.

Requirements addressed:
- 5.1: Academic writing style and formal tone
- 5.2: Structured academic report sections
- 5.3: Hedging language and certainty indicators
- 5.4: Formal language without colloquialisms
- 5.5: Academic formatting standards
"""

from __future__ import annotations

import re
from typing import Optional, Dict, Any, List
from collections import OrderedDict

from .academic_config import AcademicConfig
from .citation_manager import CitationManager, CitationStyle
from .report_generator import (
    AcademicReport,
    ResearchMetadata,
    SECTION_ABSTRACT,
    SECTION_INTRODUCTION,
    SECTION_LITERATURE_REVIEW,
    SECTION_METHODOLOGY,
    SECTION_FINDINGS,
    SECTION_DISCUSSION,
    SECTION_IMPLICATIONS,
    SECTION_LIMITATIONS,
    SECTION_CONCLUSION,
    SECTION_REFERENCES,
)
from .prompts.academic_prompts import get_academic_synthesis_prompt


class AcademicReportGenerator:
    """
    Generates structured academic reports with proper formatting and citations.
    
    This class handles:
    - Integration with synthesis model for content generation
    - Section structure enforcement based on output format
    - Citation formatting and bibliography generation
    - Academic writing style validation
    - Report assembly and formatting
    
    Requirements addressed:
    - 5.1: Generate reports using formal academic language
    - 5.2: Structure reports with required academic sections
    - 5.3: Use hedging language appropriately
    - 5.4: Avoid colloquialisms and informal expressions
    - 5.5: Format data using academic standards
    """
    
    def __init__(
        self,
        config: AcademicConfig,
        citation_manager: CitationManager,
    ):
        """
        Initialize the academic report generator.
        
        Args:
            config: Academic configuration settings
            citation_manager: Citation manager instance for tracking sources
        """
        self.config = config
        self.citation_manager = citation_manager
    
    def generate_report(
        self,
        question: str,
        research_results: str,
        api_key: str,
        metadata: Optional[ResearchMetadata] = None,
        model: str = "openai/grok-2-1212",
    ) -> AcademicReport:
        """
        Generate a complete academic report from research results.
        
        This method:
        1. Prepares the synthesis prompt with academic guidelines
        2. Calls the synthesis model to generate report content
        3. Parses and structures the generated content into sections
        4. Formats citations and generates bibliography
        5. Assembles the final AcademicReport object
        
        Args:
            question: Original research question
            research_results: Raw research findings from the research agent
            api_key: API key for the synthesis model
            metadata: Optional research metadata
            model: Model identifier for synthesis (default: grok-2-1212)
        
        Returns:
            AcademicReport object with all sections and bibliography
        
        Requirements:
            - 5.1: Uses academic synthesis prompt for formal style
            - 5.2: Enforces structured sections
            - 5.3: Integrates citation formatting
        """
        # Generate synthesis prompt with academic guidelines
        synthesis_prompt = get_academic_synthesis_prompt(
            citation_style=self.config.citation_style.value,
            output_format=self.config.output_format.value,
            discipline=self.config.discipline.value,
            word_count_target=self.config.word_count_target,
        )
        
        # Prepare the full prompt with research results
        full_prompt = self._prepare_synthesis_prompt(
            synthesis_prompt,
            question,
            research_results,
        )
        
        # Call synthesis model to generate report content
        report_content = self._call_synthesis_model(
            full_prompt,
            api_key,
            model,
        )
        
        # Parse the generated content into structured sections
        sections = self._parse_sections(report_content)
        
        # Extract abstract if present
        abstract = sections.pop(SECTION_ABSTRACT, "")
        
        # Extract and format bibliography
        bibliography_raw = sections.pop(SECTION_REFERENCES, "")
        bibliography = self._format_citations(bibliography_raw)
        
        # Generate title from question
        title = self._generate_title(question)
        
        # Create AcademicReport object
        report = AcademicReport(
            title=title,
            abstract=abstract,
            sections=OrderedDict(sections),
            bibliography=bibliography,
            metadata=metadata,
            citation_style=self.config.citation_style,
            output_format=self.config.output_format,
        )
        
        # Calculate word count
        report.calculate_word_count()
        
        return report
    
    def _prepare_synthesis_prompt(
        self,
        synthesis_prompt: str,
        question: str,
        research_results: str,
    ) -> str:
        """
        Prepare the full synthesis prompt with research results.
        
        Args:
            synthesis_prompt: Base academic synthesis prompt
            question: Research question
            research_results: Research findings
        
        Returns:
            Complete prompt for synthesis model
        """
        prompt_parts = [
            synthesis_prompt,
            "\n\n# Research Question\n\n",
            question,
            "\n\n# Research Findings\n\n",
            research_results,
            "\n\n# Task\n\n",
            "Synthesize the above research findings into a comprehensive academic report ",
            "following all guidelines and requirements specified above. ",
            "Ensure proper structure, formal academic writing style, thorough citations, ",
            "and critical analysis throughout.",
        ]
        
        return "".join(prompt_parts)
    
    def _call_synthesis_model(
        self,
        prompt: str,
        api_key: str,
        model: str,
    ) -> str:
        """
        Call the synthesis model to generate report content.
        
        Args:
            prompt: Complete synthesis prompt
            api_key: API key for the model
            model: Model identifier
        
        Returns:
            Generated report content
        """
        # Import here to avoid circular dependencies
        from openai import OpenAI
        
        client = OpenAI(
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1",
        )
        
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                temperature=0.7,
                max_tokens=16000,  # Allow for comprehensive reports
            )
            
            content = response.choices[0].message.content
            return content if content else ""
        
        except Exception as e:
            raise RuntimeError(f"Error calling synthesis model: {e}")
    
    def _parse_sections(self, content: str) -> Dict[str, str]:
        """
        Parse generated content into structured sections.
        
        Identifies section headers (## Section Name) and extracts content
        for each section.
        
        Args:
            content: Generated report content
        
        Returns:
            Dictionary mapping section names to content
        """
        sections = OrderedDict()
        
        # Split content by section headers (## Section Name)
        # Pattern matches: ## Section Name or ## **Section Name**
        section_pattern = r'^##\s+\*?\*?([^\n*]+)\*?\*?\s*$'
        
        lines = content.split('\n')
        current_section = None
        current_content = []
        
        for line in lines:
            # Check if this is a section header
            match = re.match(section_pattern, line.strip())
            if match:
                # Save previous section if exists
                if current_section:
                    sections[current_section] = '\n'.join(current_content).strip()
                
                # Start new section
                current_section = match.group(1).strip()
                current_content = []
            else:
                # Add line to current section content
                if current_section:
                    current_content.append(line)
        
        # Save last section
        if current_section:
            sections[current_section] = '\n'.join(current_content).strip()
        
        # If no sections found, treat entire content as one section
        if not sections:
            sections["Content"] = content.strip()
        
        return sections
    
    def _generate_abstract(self, content: str) -> str:
        """
        Generate or extract abstract from content.
        
        If abstract section exists, returns it. Otherwise, generates
        a brief abstract from the introduction and conclusion.
        
        Args:
            content: Full report content
        
        Returns:
            Abstract text (150-250 words)
        
        Note: This is a helper method for future enhancement.
        Currently, the synthesis model generates the abstract.
        """
        # This method is for future use if we need to generate
        # abstracts separately or extract them from content
        return ""
    
    def _structure_literature_review(self, content: str) -> str:
        """
        Structure literature review section with proper organization.
        
        Ensures literature review is organized thematically or chronologically
        with clear subsections and proper flow.
        
        Args:
            content: Raw literature review content
        
        Returns:
            Structured literature review text
        
        Note: This is a helper method for future enhancement.
        Currently, the synthesis model structures the literature review.
        """
        # This method is for future use if we need to restructure
        # literature reviews or add additional organization
        return content
    
    def _extract_methodology_section(self, content: str) -> str:
        """
        Extract and format methodology section.
        
        Ensures methodology section includes:
        - Research design description
        - Data collection methods
        - Analysis techniques
        - Limitations
        
        Args:
            content: Raw methodology content
        
        Returns:
            Formatted methodology text
        
        Note: This is a helper method for future enhancement.
        Currently, the synthesis model generates the methodology section.
        """
        # This method is for future use if we need to extract
        # or enhance methodology sections
        return content
    
    def _format_citations(self, content: str) -> str:
        """
        Format citations in the content according to the configured style.
        
        This method:
        1. Identifies citation references in the text
        2. Looks up citations in the citation manager
        3. Formats them according to the configured citation style
        4. Generates the bibliography
        
        Args:
            content: Content with citation references
        
        Returns:
            Formatted bibliography text
        
        Requirements:
            - 2.2: Format citations in specified style
            - 2.3: Generate bibliography
        """
        # If content is already a formatted bibliography, return it
        if content and (
            content.strip().startswith('[') or 
            any(author_pattern in content for author_pattern in ['et al.', '&', 'and'])
        ):
            return content
        
        # Generate bibliography from citation manager
        bibliography = self._generate_bibliography()
        
        return bibliography
    
    def _generate_bibliography(self) -> str:
        """
        Generate formatted bibliography from citation manager.
        
        Returns:
            Complete bibliography in the configured citation style
        
        Requirements:
            - 2.3: Generate bibliography sorted by author
            - 2.4: Format in specified citation style
        """
        if len(self.citation_manager) == 0:
            return "No citations available."
        
        # Generate bibliography using citation manager
        bibliography = self.citation_manager.generate_bibliography(
            style=self.config.citation_style,
            sort_by_author=True,
        )
        
        return bibliography
    
    def _generate_title(self, question: str) -> str:
        """
        Generate an appropriate title from the research question.
        
        Args:
            question: Research question
        
        Returns:
            Formatted title
        """
        # Clean up question
        title = question.strip()
        
        # Remove question marks
        title = title.rstrip('?')
        
        # Capitalize first letter
        if title:
            title = title[0].upper() + title[1:]
        
        # Add appropriate suffix based on output format
        if self.config.output_format.value == "review":
            if "review" not in title.lower():
                title = f"{title}: A Literature Review"
        elif self.config.output_format.value == "proposal":
            if "proposal" not in title.lower():
                title = f"Research Proposal: {title}"
        
        return title
    
    def validate_report_structure(self, report: AcademicReport) -> List[str]:
        """
        Validate that the report has the required structure.
        
        Checks that all required sections for the output format are present
        and properly formatted.
        
        Args:
            report: AcademicReport to validate
        
        Returns:
            List of validation issues (empty if valid)
        """
        issues = []
        
        # Get required sections for this output format
        required_sections = self.config.get_report_structure()
        
        # Check for required sections
        for section_name in required_sections:
            if section_name == SECTION_REFERENCES:
                # Check bibliography instead
                if not report.bibliography:
                    issues.append(f"Missing required bibliography/references section")
            elif section_name == SECTION_ABSTRACT:
                # Check abstract
                if self.config.include_abstract and not report.abstract:
                    issues.append(f"Missing required abstract")
            else:
                # Check regular section
                if section_name not in report.sections:
                    issues.append(f"Missing required section: {section_name}")
                elif not report.sections[section_name].strip():
                    issues.append(f"Empty required section: {section_name}")
        
        # Check word count
        if report.word_count < 500:
            issues.append(
                f"Word count ({report.word_count}) is very low for academic report"
            )
        
        # Check citation style matches config
        if report.citation_style != self.config.citation_style:
            issues.append(
                f"Citation style mismatch: report uses {report.citation_style.value}, "
                f"config specifies {self.config.citation_style.value}"
            )
        
        return issues
    
    def enhance_report_quality(self, report: AcademicReport) -> AcademicReport:
        """
        Enhance report quality by applying additional formatting and checks.
        
        This method can be extended to:
        - Add section transitions
        - Improve citation integration
        - Enhance academic language
        - Add formatting improvements
        
        Args:
            report: AcademicReport to enhance
        
        Returns:
            Enhanced AcademicReport
        
        Note: This is a placeholder for future enhancements.
        """
        # Future enhancements can be added here
        # For now, return report as-is
        return report


def generate_academic_report(
    question: str,
    research_results: str,
    api_key: str,
    config: Optional[AcademicConfig] = None,
    citation_manager: Optional[CitationManager] = None,
    metadata: Optional[ResearchMetadata] = None,
    model: str = "openai/grok-2-1212",
) -> AcademicReport:
    """
    Convenience function to generate an academic report.
    
    Args:
        question: Research question
        research_results: Research findings from research agent
        api_key: API key for synthesis model
        config: Academic configuration (uses defaults if None)
        citation_manager: Citation manager (creates new if None)
        metadata: Research metadata (optional)
        model: Synthesis model identifier
    
    Returns:
        Complete AcademicReport
    
    Example:
        >>> from gazzali.academic_config import AcademicConfig
        >>> from gazzali.citation_manager import CitationManager
        >>> 
        >>> config = AcademicConfig(citation_style="apa", output_format="paper")
        >>> citation_mgr = CitationManager()
        >>> 
        >>> report = generate_academic_report(
        ...     question="What are the effects of climate change?",
        ...     research_results="[research findings here]",
        ...     api_key="your-api-key",
        ...     config=config,
        ...     citation_manager=citation_mgr,
        ... )
        >>> 
        >>> report.save("climate_report.md", format="markdown")
    """
    # Use defaults if not provided
    if config is None:
        config = AcademicConfig()
    
    if citation_manager is None:
        citation_manager = CitationManager()
    
    # Create generator and generate report
    generator = AcademicReportGenerator(config, citation_manager)
    report = generator.generate_report(
        question=question,
        research_results=research_results,
        api_key=api_key,
        metadata=metadata,
        model=model,
    )
    
    return report
