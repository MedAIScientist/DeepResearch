#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Progress Tracking Module for Gazzali Research

Provides progress indicators, time estimation, and stage completion notifications
for research workflows.
"""

import time
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
from enum import Enum


class ResearchStage(Enum):
    """Research workflow stages"""
    INITIALIZATION = "initialization"
    QUESTION_REFINEMENT = "question_refinement"
    RESEARCH = "research"
    CITATION_EXTRACTION = "citation_extraction"
    REPORT_GENERATION = "report_generation"
    BIBLIOGRAPHY_GENERATION = "bibliography_generation"
    COMPLETE = "complete"


@dataclass
class StageProgress:
    """Progress information for a single stage"""
    stage: ResearchStage
    status: str = "pending"  # pending, in_progress, complete, failed
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    progress_percent: float = 0.0
    message: str = ""
    substeps: List[str] = field(default_factory=list)
    current_substep: Optional[str] = None
    
    @property
    def duration(self) -> Optional[float]:
        """Calculate stage duration in seconds"""
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        elif self.start_time:
            return time.time() - self.start_time
        return None
    
    @property
    def is_complete(self) -> bool:
        """Check if stage is complete"""
        return self.status == "complete"
    
    @property
    def is_in_progress(self) -> bool:
        """Check if stage is in progress"""
        return self.status == "in_progress"


class ProgressTracker:
    """
    Track progress through research workflow stages with time estimation.
    
    Provides:
    - Stage-by-stage progress tracking
    - Estimated time remaining
    - Intermediate outputs at key stages
    - Stage completion notifications
    """
    
    # Average durations for each stage (in seconds) - used for estimation
    STAGE_DURATIONS = {
        ResearchStage.INITIALIZATION: 2,
        ResearchStage.QUESTION_REFINEMENT: 15,
        ResearchStage.RESEARCH: 180,  # 3 minutes average
        ResearchStage.CITATION_EXTRACTION: 10,
        ResearchStage.REPORT_GENERATION: 60,
        ResearchStage.BIBLIOGRAPHY_GENERATION: 5,
    }
    
    def __init__(self, academic_mode: bool = False, chunked_mode: bool = False):
        """
        Initialize progress tracker.
        
        Args:
            academic_mode: Whether academic mode is enabled
            chunked_mode: Whether chunked research mode is enabled
        """
        self.academic_mode = academic_mode
        self.chunked_mode = chunked_mode
        self.stages: Dict[ResearchStage, StageProgress] = {}
        self.start_time = time.time()
        self.total_stages = 0
        self.completed_stages = 0
        self.intermediate_outputs: List[Dict[str, Any]] = []
        
        # Initialize stages based on mode
        self._initialize_stages()
    
    def _initialize_stages(self):
        """Initialize stages based on workflow mode"""
        stages_to_track = [ResearchStage.INITIALIZATION, ResearchStage.RESEARCH]
        
        if self.academic_mode:
            # Add academic-specific stages
            stages_to_track.insert(1, ResearchStage.QUESTION_REFINEMENT)
            stages_to_track.append(ResearchStage.CITATION_EXTRACTION)
            stages_to_track.append(ResearchStage.REPORT_GENERATION)
            stages_to_track.append(ResearchStage.BIBLIOGRAPHY_GENERATION)
        
        stages_to_track.append(ResearchStage.COMPLETE)
        
        for stage in stages_to_track:
            self.stages[stage] = StageProgress(stage=stage)
        
        self.total_stages = len(stages_to_track) - 1  # Exclude COMPLETE
    
    def start_stage(self, stage: ResearchStage, message: str = "", substeps: Optional[List[str]] = None):
        """
        Mark a stage as started.
        
        Args:
            stage: Stage to start
            message: Optional message describing the stage
            substeps: Optional list of substeps for this stage
        """
        if stage not in self.stages:
            self.stages[stage] = StageProgress(stage=stage)
        
        stage_progress = self.stages[stage]
        stage_progress.status = "in_progress"
        stage_progress.start_time = time.time()
        stage_progress.message = message
        
        if substeps:
            stage_progress.substeps = substeps
            stage_progress.current_substep = substeps[0] if substeps else None
    
    def update_stage(self, stage: ResearchStage, progress_percent: float, message: str = "", current_substep: Optional[str] = None):
        """
        Update progress for a stage.
        
        Args:
            stage: Stage to update
            progress_percent: Progress percentage (0-100)
            message: Optional progress message
            current_substep: Current substep being executed
        """
        if stage in self.stages:
            stage_progress = self.stages[stage]
            stage_progress.progress_percent = min(100.0, max(0.0, progress_percent))
            
            if message:
                stage_progress.message = message
            
            if current_substep:
                stage_progress.current_substep = current_substep
    
    def complete_stage(self, stage: ResearchStage, message: str = "", output: Optional[Dict[str, Any]] = None):
        """
        Mark a stage as complete.
        
        Args:
            stage: Stage to complete
            message: Optional completion message
            output: Optional intermediate output from this stage
        """
        if stage in self.stages:
            stage_progress = self.stages[stage]
            stage_progress.status = "complete"
            stage_progress.end_time = time.time()
            stage_progress.progress_percent = 100.0
            
            if message:
                stage_progress.message = message
            
            self.completed_stages += 1
            
            # Store intermediate output
            if output:
                self.intermediate_outputs.append({
                    "stage": stage.value,
                    "timestamp": datetime.now().isoformat(),
                    "duration": stage_progress.duration,
                    "output": output
                })
    
    def fail_stage(self, stage: ResearchStage, error_message: str):
        """
        Mark a stage as failed.
        
        Args:
            stage: Stage that failed
            error_message: Error message
        """
        if stage in self.stages:
            stage_progress = self.stages[stage]
            stage_progress.status = "failed"
            stage_progress.end_time = time.time()
            stage_progress.message = error_message
    
    def get_overall_progress(self) -> float:
        """
        Calculate overall progress percentage.
        
        Returns:
            Progress percentage (0-100)
        """
        if self.total_stages == 0:
            return 0.0
        
        total_progress = 0.0
        for stage, progress in self.stages.items():
            if stage == ResearchStage.COMPLETE:
                continue
            
            if progress.status == "complete":
                total_progress += 100.0
            elif progress.status == "in_progress":
                total_progress += progress.progress_percent
        
        return total_progress / self.total_stages
    
    def get_elapsed_time(self) -> float:
        """
        Get elapsed time since tracking started.
        
        Returns:
            Elapsed time in seconds
        """
        return time.time() - self.start_time
    
    def estimate_remaining_time(self) -> Optional[float]:
        """
        Estimate remaining time based on completed stages and averages.
        
        Returns:
            Estimated remaining time in seconds, or None if cannot estimate
        """
        if self.completed_stages == 0:
            # Use average durations for all stages
            total_estimated = sum(
                self.STAGE_DURATIONS.get(stage, 60)
                for stage in self.stages.keys()
                if stage != ResearchStage.COMPLETE
            )
            return total_estimated
        
        # Calculate average time per completed stage
        completed_time = 0.0
        for stage, progress in self.stages.items():
            if progress.is_complete and progress.duration:
                completed_time += progress.duration
        
        if completed_time == 0:
            return None
        
        avg_time_per_stage = completed_time / self.completed_stages
        remaining_stages = self.total_stages - self.completed_stages
        
        # Adjust for current stage progress
        current_stage_progress = 0.0
        for progress in self.stages.values():
            if progress.is_in_progress:
                current_stage_progress = progress.progress_percent / 100.0
                break
        
        estimated_remaining = (remaining_stages - current_stage_progress) * avg_time_per_stage
        return max(0.0, estimated_remaining)
    
    def get_status_summary(self) -> Dict[str, Any]:
        """
        Get comprehensive status summary.
        
        Returns:
            Dictionary with status information
        """
        elapsed = self.get_elapsed_time()
        remaining = self.estimate_remaining_time()
        
        return {
            "overall_progress": self.get_overall_progress(),
            "completed_stages": self.completed_stages,
            "total_stages": self.total_stages,
            "elapsed_time": elapsed,
            "elapsed_formatted": self._format_duration(elapsed),
            "estimated_remaining": remaining,
            "remaining_formatted": self._format_duration(remaining) if remaining else "Calculating...",
            "current_stage": self._get_current_stage(),
            "stages": {
                stage.value: {
                    "status": progress.status,
                    "progress": progress.progress_percent,
                    "message": progress.message,
                    "duration": progress.duration,
                    "current_substep": progress.current_substep
                }
                for stage, progress in self.stages.items()
            }
        }
    
    def _get_current_stage(self) -> Optional[str]:
        """Get the name of the current stage in progress"""
        for stage, progress in self.stages.items():
            if progress.is_in_progress:
                return stage.value
        return None
    
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
    
    def get_intermediate_outputs(self) -> List[Dict[str, Any]]:
        """
        Get all intermediate outputs from completed stages.
        
        Returns:
            List of intermediate outputs
        """
        return self.intermediate_outputs
    
    def save_progress_report(self, filepath: str):
        """
        Save progress report to file.
        
        Args:
            filepath: Path to save report
        """
        import json
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "academic_mode": self.academic_mode,
            "chunked_mode": self.chunked_mode,
            "status": self.get_status_summary(),
            "intermediate_outputs": self.intermediate_outputs
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
