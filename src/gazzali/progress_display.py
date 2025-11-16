#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Progress Display Module for Gazzali Research

Provides visual progress indicators and notifications for terminal output.
"""

import sys
from typing import Optional
from .progress_tracker import ProgressTracker, ResearchStage


# Color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    DIM = '\033[2m'


class ProgressDisplay:
    """
    Display progress information in terminal with visual indicators.
    """
    
    # Stage display names
    STAGE_NAMES = {
        ResearchStage.INITIALIZATION: "Initialization",
        ResearchStage.QUESTION_REFINEMENT: "Question Refinement",
        ResearchStage.RESEARCH: "Deep Research",
        ResearchStage.CITATION_EXTRACTION: "Citation Extraction",
        ResearchStage.REPORT_GENERATION: "Report Generation",
        ResearchStage.BIBLIOGRAPHY_GENERATION: "Bibliography Generation",
        ResearchStage.COMPLETE: "Complete"
    }
    
    # Stage icons
    STAGE_ICONS = {
        ResearchStage.INITIALIZATION: "⚙️",
        ResearchStage.QUESTION_REFINEMENT: "🔍",
        ResearchStage.RESEARCH: "🔬",
        ResearchStage.CITATION_EXTRACTION: "📚",
        ResearchStage.REPORT_GENERATION: "📝",
        ResearchStage.BIBLIOGRAPHY_GENERATION: "📖",
        ResearchStage.COMPLETE: "✅"
    }
    
    def __init__(self, tracker: ProgressTracker, verbose: bool = True):
        """
        Initialize progress display.
        
        Args:
            tracker: ProgressTracker instance
            verbose: Whether to show detailed progress
        """
        self.tracker = tracker
        self.verbose = verbose
        self.last_progress = 0.0
    
    def show_stage_start(self, stage: ResearchStage, message: str = ""):
        """
        Display stage start notification.
        
        Args:
            stage: Stage that started
            message: Optional message
        """
        stage_name = self.STAGE_NAMES.get(stage, stage.value)
        icon = self.STAGE_ICONS.get(stage, "▶️")
        
        print(f"\n{Colors.OKCYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.ENDC}")
        print(f"{Colors.BOLD}{icon} STAGE: {stage_name.upper()}{Colors.ENDC}")
        print(f"{Colors.OKCYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.ENDC}\n")
        
        if message:
            print(f"{message}\n")
        
        # Show overall progress
        self._show_progress_bar()
    
    def show_stage_progress(self, stage: ResearchStage, message: str = ""):
        """
        Display stage progress update.
        
        Args:
            stage: Stage being updated
            message: Progress message
        """
        if not self.verbose:
            return
        
        if message:
            print(f"{Colors.DIM}  → {message}{Colors.ENDC}")
        
        # Update progress bar if significant change
        current_progress = self.tracker.get_overall_progress()
        if current_progress - self.last_progress >= 5.0:  # Update every 5%
            self._show_progress_bar()
            self.last_progress = current_progress
    
    def show_stage_complete(self, stage: ResearchStage, message: str = ""):
        """
        Display stage completion notification.
        
        Args:
            stage: Stage that completed
            message: Completion message
        """
        stage_name = self.STAGE_NAMES.get(stage, stage.value)
        
        # Get stage duration
        stage_progress = self.tracker.stages.get(stage)
        duration_str = ""
        if stage_progress and stage_progress.duration:
            duration_str = f" ({self._format_duration(stage_progress.duration)})"
        
        print(f"\n{Colors.OKGREEN}✅ {stage_name} Complete{duration_str}{Colors.ENDC}")
        
        if message:
            print(f"   {message}")
        
        # Show updated progress
        self._show_progress_bar()
        print()
    
    def show_stage_failed(self, stage: ResearchStage, error_message: str):
        """
        Display stage failure notification.
        
        Args:
            stage: Stage that failed
            error_message: Error message
        """
        stage_name = self.STAGE_NAMES.get(stage, stage.value)
        
        print(f"\n{Colors.FAIL}❌ {stage_name} Failed{Colors.ENDC}")
        print(f"   {error_message}\n")
    
    def _show_progress_bar(self):
        """Display progress bar with time estimates"""
        status = self.tracker.get_status_summary()
        progress = status["overall_progress"]
        elapsed = status["elapsed_formatted"]
        remaining = status["remaining_formatted"]
        
        # Progress bar
        bar_width = 50
        filled = int(bar_width * progress / 100)
        bar = "█" * filled + "░" * (bar_width - filled)
        
        print(f"\n{Colors.BOLD}Progress:{Colors.ENDC} [{bar}] {progress:.1f}%")
        print(f"{Colors.BOLD}Elapsed:{Colors.ENDC} {elapsed}  |  {Colors.BOLD}Remaining:{Colors.ENDC} {remaining}")
        print(f"{Colors.BOLD}Stages:{Colors.ENDC} {status['completed_stages']}/{status['total_stages']} complete\n")
    
    def show_substep(self, substep: str):
        """
        Display substep progress.
        
        Args:
            substep: Substep description
        """
        if self.verbose:
            print(f"{Colors.DIM}    • {substep}{Colors.ENDC}")
    
    def show_summary(self):
        """Display final summary"""
        status = self.tracker.get_status_summary()
        
        print(f"\n{Colors.OKCYAN}╔════════════════════════════════════════════════════════════════╗{Colors.ENDC}")
        print(f"{Colors.OKCYAN}║{Colors.ENDC} {Colors.OKGREEN}✅ RESEARCH WORKFLOW COMPLETE{Colors.ENDC}                             {Colors.OKCYAN}║{Colors.ENDC}")
        print(f"{Colors.OKCYAN}╚════════════════════════════════════════════════════════════════╝{Colors.ENDC}\n")
        
        print(f"{Colors.BOLD}Summary:{Colors.ENDC}")
        print(f"  • Total Time:        {Colors.OKGREEN}{status['elapsed_formatted']}{Colors.ENDC}")
        print(f"  • Stages Completed:  {Colors.OKGREEN}{status['completed_stages']}/{status['total_stages']}{Colors.ENDC}")
        
        # Show stage breakdown
        print(f"\n{Colors.BOLD}Stage Breakdown:{Colors.ENDC}")
        for stage, progress in self.tracker.stages.items():
            if stage == ResearchStage.COMPLETE:
                continue
            
            stage_name = self.STAGE_NAMES.get(stage, stage.value)
            icon = self.STAGE_ICONS.get(stage, "▶️")
            
            if progress.status == "complete":
                duration = self._format_duration(progress.duration) if progress.duration else "N/A"
                print(f"  {Colors.OKGREEN}✓{Colors.ENDC} {icon} {stage_name:<30} {duration}")
            elif progress.status == "failed":
                print(f"  {Colors.FAIL}✗{Colors.ENDC} {icon} {stage_name:<30} Failed")
            else:
                print(f"  {Colors.DIM}○{Colors.ENDC} {icon} {stage_name:<30} Skipped")
        
        print()
    
    def show_intermediate_output(self, stage: ResearchStage, output_summary: str):
        """
        Display intermediate output notification.
        
        Args:
            stage: Stage that produced output
            output_summary: Summary of the output
        """
        stage_name = self.STAGE_NAMES.get(stage, stage.value)
        
        print(f"\n{Colors.OKCYAN}📄 Intermediate Output: {stage_name}{Colors.ENDC}")
        print(f"   {output_summary}\n")
    
    def _format_duration(self, seconds: Optional[float]) -> str:
        """
        Format duration in human-readable format.
        
        Args:
            seconds: Duration in seconds
        
        Returns:
            Formatted duration string
        """
        if seconds is None:
            return "Unknown"
        
        if seconds < 60:
            return f"{int(seconds)}s"
        elif seconds < 3600:
            minutes = int(seconds / 60)
            secs = int(seconds % 60)
            return f"{minutes}m {secs}s"
        else:
            hours = int(seconds / 3600)
            minutes = int((seconds % 3600) / 60)
            return f"{hours}h {minutes}m"


def create_progress_display(tracker: ProgressTracker, verbose: bool = True) -> ProgressDisplay:
    """
    Factory function to create progress display.
    
    Args:
        tracker: ProgressTracker instance
        verbose: Whether to show detailed progress
    
    Returns:
        ProgressDisplay instance
    """
    return ProgressDisplay(tracker, verbose)
