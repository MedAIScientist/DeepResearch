#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Academic Report Generator Module for Gazzali Research

This module provides data models and generation logic for creating structured
academic reports with proper formatting, citations, and section organization.

Requirements addressed:
- 5.2: Structured academic report sections
- 12.1: Research implications and impact analysis
- 12.2: Theoretical and practical contributions
- 12.3: Future research directions
"""

from __future__ import annotations

from collections import OrderedDict
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List, Dict, Any

from .academic_config import AcademicConfig, CitationStyle, OutputFormat
from .citation_manager import CitationManager


# Standard section name constants
SECTION_ABSTRACT = "Abstract"
SECTION_INTRODUCTION = "Introduction"
SECTION_LITERATURE_REVIEW = "Literature Review"
SECTION_METHODOLOGY = "Methodology"
SECTION_FINDINGS = "Findings"
SECTION_DISCUSSION = "Discussion"
SECTION_IMPLICATIONS = "Implications"
SECTION_LIMITATIONS = "Limitations"
SECTION_CONCLUSION = "Conclusion"
SECTION_REFERENCES = "References"
SECTION_BACKGROUND = "Background"
SECTION_RESEARCH_QUESTIONS = "Research Questions"
SECTION_THEMATIC_ANALYSIS = "Thematic Analysis"
SECTION_RESEARCH_GAPS = "Research Gaps"
SECTION_FUTURE_DIRECTIONS = "Future Directions"
SECTION_PROPOSED_METHODOLOGY = "Proposed Methodology"
SECTION_EXPECTED_OUTCOMES = "Expected Outcomes"
SECTION_TIMELINE = "Timeline"


@dataclass
class ResearchMetadata:
    """
    Metadata about the research process and sources.
    
    Attributes:
        question: Original research question
        refined_question: Refined version of the question (if applicable)
        discipline: Academic discipline
        search_strategy: Description of search approach used
        sources_consulted: Total number of sources examined
        peer_reviewed_sources: Number of peer-reviewed sources
        date_range: Tuple of (start_date, end_date) for literature coverage
        key_authors: List of prominent authors in the field
        key_theories: List of theoretical frameworks identified
        methodologies_found: List of research methodologies encountered
        generated_at: Timestamp of report generation
    """
    question: str
    refined_question: Optional[str] = None
    discipline: str = "general"
    search_strategy: str = ""
    sources_consulted: int = 0
    peer_reviewed_sources: int = 0
    date_range: tuple[str, str] = ("", "")
    key_authors: List[str] = field(default_factory=list)
    key_theories: List[str] = field(default_factory=list)
    methodologies_found: List[str] = field(default_factory=list)
    generated_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert metadata to dictionary.
        
        Returns:
            Dictionary representation of metadata
        """
        return {
            "question": self.question,
            "refined_question": self.refined_question,
            "discipline": self.discipline,
            "search_strategy": self.search_strategy,
            "sources_consulted": self.sources_consulted,
            "peer_reviewed_sources": self.peer_reviewed_sources,
            "date_range": self.date_range,
            "key_authors": self.key_authors,
            "key_theories": self.key_theories,
            "methodologies_found": self.methodologies_found,
            "generated_at": self.generated_at.isoformat(),
        }
    
    def get_peer_reviewed_percentage(self) -> float:
        """
        Calculate percentage of peer-reviewed sources.
        
        Returns:
            Percentage (0-100) of sources that are peer-reviewed
        """
        if self.sources_consulted == 0:
            return 0.0
        return (self.peer_reviewed_sources / self.sources_consulted) * 100


@dataclass
class AcademicReport:
    """
    Represents a complete academic report with all sections and metadata.
    
    Attributes:
        title: Report title
        abstract: Abstract text (if included)
        keywords: List of keywords for the report
        sections: Ordered dictionary of section_name -> content
        bibliography: Formatted bibliography/references section
        metadata: Research metadata
        citation_style: Citation style used
        output_format: Output format type
        word_count: Total word count of the report
        generated_at: Timestamp of generation
    """
    title: str
    abstract: str = ""
    keywords: List[str] = field(default_factory=list)
    sections: OrderedDict[str, str] = field(default_factory=OrderedDict)
    bibliography: str = ""
    metadata: Optional[ResearchMetadata] = None
    citation_style: CitationStyle = CitationStyle.APA
    output_format: OutputFormat = OutputFormat.PAPER
    word_count: int = 0
    generated_at: datetime = field(default_factory=datetime.now)
    
    def to_markdown(self) -> str:
        """
        Convert report to Markdown format.
        
        Returns:
            Formatted Markdown string
        """
        lines = []
        
        # Title
        lines.append(f"# {self.title}\n")
        
        # Metadata section (optional)
        if self.metadata:
            lines.append("---")
            lines.append(f"**Generated**: {self.generated_at.strftime('%Y-%m-%d %H:%M:%S')}")
            lines.append(f"**Citation Style**: {self.citation_style.value.upper()}")
            lines.append(f"**Word Count**: {self.word_count}")
            if self.keywords:
                lines.append(f"**Keywords**: {', '.join(self.keywords)}")
            lines.append("---\n")
        
        # Abstract (if present)
        if self.abstract:
            lines.append(f"## {SECTION_ABSTRACT}\n")
            lines.append(f"{self.abstract}\n")
        
        # Main sections
        for section_name, content in self.sections.items():
            lines.append(f"## {section_name}\n")
            lines.append(f"{content}\n")
        
        # Bibliography/References
        if self.bibliography:
            lines.append(f"## {SECTION_REFERENCES}\n")
            lines.append(f"{self.bibliography}\n")
        
        return "\n".join(lines)
    
    def to_latex(self) -> str:
        """
        Convert report to basic LaTeX format.
        
        Returns:
            Formatted LaTeX string
        """
        lines = []
        
        # Document class and packages
        lines.append("\\documentclass[12pt,a4paper]{article}")
        lines.append("\\usepackage[utf8]{inputenc}")
        lines.append("\\usepackage{graphicx}")
        lines.append("\\usepackage{hyperref}")
        lines.append("\\usepackage{cite}")
        lines.append("")
        
        # Title and metadata
        lines.append(f"\\title{{{self._escape_latex(self.title)}}}")
        lines.append(f"\\date{{{self.generated_at.strftime('%B %d, %Y')}}}")
        lines.append("")
        
        # Begin document
        lines.append("\\begin{document}")
        lines.append("\\maketitle")
        lines.append("")
        
        # Abstract
        if self.abstract:
            lines.append("\\begin{abstract}")
            lines.append(self._escape_latex(self.abstract))
            lines.append("\\end{abstract}")
            lines.append("")
        
        # Keywords
        if self.keywords:
            lines.append("\\noindent\\textbf{Keywords:} " + ", ".join(self.keywords))
            lines.append("")
        
        # Main sections
        for section_name, content in self.sections.items():
            lines.append(f"\\section{{{self._escape_latex(section_name)}}}")
            lines.append(self._escape_latex(content))
            lines.append("")
        
        # Bibliography
        if self.bibliography:
            lines.append(f"\\section{{{SECTION_REFERENCES}}}")
            lines.append(self._escape_latex(self.bibliography))
            lines.append("")
        
        # End document
        lines.append("\\end{document}")
        
        return "\n".join(lines)
    
    def _escape_latex(self, text: str) -> str:
        """
        Escape special LaTeX characters.
        
        Args:
            text: Text to escape
        
        Returns:
            Escaped text safe for LaTeX
        """
        # Basic LaTeX escaping
        replacements = {
            '\\': '\\textbackslash{}',
            '{': '\\{',
            '}': '\\}',
            '$': '\\$',
            '&': '\\&',
            '%': '\\%',
            '#': '\\#',
            '_': '\\_',
            '~': '\\textasciitilde{}',
            '^': '\\textasciicircum{}',
        }
        
        for char, replacement in replacements.items():
            text = text.replace(char, replacement)
        
        return text
    
    def save(self, filepath: str, format: str = 'markdown') -> None:
        """
        Save report to file in specified format.
        
        Args:
            filepath: Path to output file
            format: Output format ('markdown' or 'latex')
        
        Raises:
            ValueError: If format is not supported
        """
        if format.lower() == 'markdown' or format.lower() == 'md':
            content = self.to_markdown()
        elif format.lower() == 'latex' or format.lower() == 'tex':
            content = self.to_latex()
        else:
            raise ValueError(f"Unsupported format: {format}. Use 'markdown' or 'latex'.")
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def calculate_word_count(self) -> int:
        """
        Calculate total word count of the report.
        
        Returns:
            Total number of words in abstract, sections, and bibliography
        """
        total_words = 0
        
        # Count abstract
        if self.abstract:
            total_words += len(self.abstract.split())
        
        # Count sections
        for content in self.sections.values():
            total_words += len(content.split())
        
        # Count bibliography (optional, as it's often not included in word count)
        # Uncomment if bibliography should be included:
        # if self.bibliography:
        #     total_words += len(self.bibliography.split())
        
        self.word_count = total_words
        return total_words
    
    def get_section(self, section_name: str) -> Optional[str]:
        """
        Retrieve content of a specific section.
        
        Args:
            section_name: Name of the section to retrieve
        
        Returns:
            Section content or None if not found
        """
        return self.sections.get(section_name)
    
    def add_section(self, section_name: str, content: str, position: Optional[int] = None) -> None:
        """
        Add or update a section in the report.
        
        Args:
            section_name: Name of the section
            content: Section content
            position: Optional position to insert (None = append at end)
        """
        if position is None:
            # Append at end
            self.sections[section_name] = content
        else:
            # Insert at specific position
            items = list(self.sections.items())
            items.insert(position, (section_name, content))
            self.sections = OrderedDict(items)
    
    def remove_section(self, section_name: str) -> bool:
        """
        Remove a section from the report.
        
        Args:
            section_name: Name of the section to remove
        
        Returns:
            True if section was removed, False if not found
        """
        if section_name in self.sections:
            del self.sections[section_name]
            return True
        return False
    
    def get_section_names(self) -> List[str]:
        """
        Get list of all section names in order.
        
        Returns:
            List of section names
        """
        return list(self.sections.keys())
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert report to dictionary.
        
        Returns:
            Dictionary representation of report
        """
        return {
            "title": self.title,
            "abstract": self.abstract,
            "keywords": self.keywords,
            "sections": dict(self.sections),
            "bibliography": self.bibliography,
            "metadata": self.metadata.to_dict() if self.metadata else None,
            "citation_style": self.citation_style.value,
            "output_format": self.output_format.value,
            "word_count": self.word_count,
            "generated_at": self.generated_at.isoformat(),
        }
    
    def __str__(self) -> str:
        """String representation of report"""
        section_count = len(self.sections)
        return (
            f"AcademicReport(\n"
            f"  Title: {self.title}\n"
            f"  Format: {self.output_format.value}\n"
            f"  Citation Style: {self.citation_style.value}\n"
            f"  Sections: {section_count}\n"
            f"  Word Count: {self.word_count}\n"
            f"  Generated: {self.generated_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
            f")"
        )


def create_empty_report(
    title: str,
    config: AcademicConfig,
    metadata: Optional[ResearchMetadata] = None
) -> AcademicReport:
    """
    Create an empty academic report with proper structure based on configuration.
    
    Args:
        title: Report title
        config: Academic configuration
        metadata: Optional research metadata
    
    Returns:
        AcademicReport with empty sections based on output format
    """
    report = AcademicReport(
        title=title,
        citation_style=config.citation_style,
        output_format=config.output_format,
        metadata=metadata,
    )
    
    # Initialize sections based on output format
    section_names = config.get_report_structure()
    
    for section_name in section_names:
        if section_name == SECTION_REFERENCES:
            # Skip references section as it's handled separately
            continue
        elif section_name == SECTION_ABSTRACT and config.include_abstract:
            # Abstract is stored separately
            continue
        else:
            report.sections[section_name] = ""
    
    return report
