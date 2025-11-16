#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for progress tracking functionality."""

import time
import json
import tempfile
from pathlib import Path

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from gazzali.progress_tracker import ProgressTracker, ResearchStage, StageProgress
from gazzali.progress_display import ProgressDisplay, create_progress_display


def test_progress_tracker_initialization():
    """Test progress tracker initialization"""
    # Standard mode
    tracker = ProgressTracker(academic_mode=False, chunked_mode=False)
    assert tracker.academic_mode is False
    assert tracker.chunked_mode is False
    assert len(tracker.stages) > 0
    
    # Academic mode
    tracker_academic = ProgressTracker(academic_mode=True, chunked_mode=False)
    assert tracker_academic.academic_mode is True
    assert len(tracker_academic.stages) > len(tracker.stages)  # More stages in academic mode


def test_stage_progress():
    """Test stage progress tracking"""
    tracker = ProgressTracker(academic_mode=True)
    
    # Start a stage
    tracker.start_stage(ResearchStage.RESEARCH, "Starting research...")
    stage = tracker.stages[ResearchStage.RESEARCH]
    
    assert stage.status == "in_progress"
    assert stage.start_time is not None
    assert stage.message == "Starting research..."
    
    # Update progress
    tracker.update_stage(ResearchStage.RESEARCH, 50.0, "Halfway done")
    assert stage.progress_percent == 50.0
    assert stage.message == "Halfway done"
    
    # Complete stage
    tracker.complete_stage(ResearchStage.RESEARCH, "Research complete")
    assert stage.status == "complete"
    assert stage.end_time is not None
    assert stage.progress_percent == 100.0


def test_overall_progress():
    """Test overall progress calculation"""
    tracker = ProgressTracker(academic_mode=True)
    
    # Initially 0%
    assert tracker.get_overall_progress() == 0.0
    
    # Complete first stage
    tracker.start_stage(ResearchStage.INITIALIZATION)
    tracker.complete_stage(ResearchStage.INITIALIZATION)
    
    progress = tracker.get_overall_progress()
    assert progress > 0.0
    assert progress < 100.0
    
    # Complete all stages
    for stage in tracker.stages.keys():
        if stage != ResearchStage.COMPLETE:
            tracker.start_stage(stage)
            tracker.complete_stage(stage)
    
    # Should be 100%
    assert tracker.get_overall_progress() == 100.0


def test_time_estimation():
    """Test time estimation"""
    tracker = ProgressTracker(academic_mode=True)
    
    # Initial estimate based on averages
    initial_estimate = tracker.estimate_remaining_time()
    assert initial_estimate is not None
    assert initial_estimate > 0
    
    # Complete a stage
    tracker.start_stage(ResearchStage.INITIALIZATION)
    time.sleep(0.1)  # Small delay
    tracker.complete_stage(ResearchStage.INITIALIZATION)
    
    # Estimate should be updated
    new_estimate = tracker.estimate_remaining_time()
    assert new_estimate is not None
    assert new_estimate < initial_estimate  # Should be less after completing a stage


def test_status_summary():
    """Test status summary generation"""
    tracker = ProgressTracker(academic_mode=True)
    
    tracker.start_stage(ResearchStage.INITIALIZATION)
    tracker.complete_stage(ResearchStage.INITIALIZATION)
    
    status = tracker.get_status_summary()
    
    assert "overall_progress" in status
    assert "completed_stages" in status
    assert "total_stages" in status
    assert "elapsed_time" in status
    assert "elapsed_formatted" in status
    assert "estimated_remaining" in status
    assert "remaining_formatted" in status
    assert "stages" in status
    
    assert status["completed_stages"] == 1
    assert status["overall_progress"] > 0


def test_intermediate_outputs():
    """Test intermediate output storage"""
    tracker = ProgressTracker(academic_mode=True)
    
    # Complete stage with output
    output_data = {"result": "test data", "count": 42}
    tracker.start_stage(ResearchStage.RESEARCH)
    tracker.complete_stage(ResearchStage.RESEARCH, "Done", output=output_data)
    
    outputs = tracker.get_intermediate_outputs()
    assert len(outputs) == 1
    assert outputs[0]["stage"] == ResearchStage.RESEARCH.value
    assert outputs[0]["output"] == output_data


def test_progress_report_save():
    """Test saving progress report to file"""
    tracker = ProgressTracker(academic_mode=True)
    
    tracker.start_stage(ResearchStage.INITIALIZATION)
    tracker.complete_stage(ResearchStage.INITIALIZATION)
    
    # Save to temp file
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        temp_path = f.name
    
    try:
        tracker.save_progress_report(temp_path)
        
        # Verify file exists and is valid JSON
        assert Path(temp_path).exists()
        
        with open(temp_path, 'r') as f:
            report = json.load(f)
        
        assert "timestamp" in report
        assert "academic_mode" in report
        assert "status" in report
        assert report["academic_mode"] is True
        
    finally:
        # Cleanup
        Path(temp_path).unlink(missing_ok=True)


def test_progress_display_creation():
    """Test progress display creation"""
    tracker = ProgressTracker(academic_mode=True)
    display = create_progress_display(tracker, verbose=True)
    
    assert display is not None
    assert display.tracker == tracker
    assert display.verbose is True


def test_stage_duration():
    """Test stage duration calculation"""
    stage = StageProgress(stage=ResearchStage.RESEARCH)
    
    # No duration initially
    assert stage.duration is None
    
    # Start stage
    stage.start_time = time.time()
    time.sleep(0.1)
    
    # Duration while in progress
    duration = stage.duration
    assert duration is not None
    assert duration >= 0.1
    
    # Complete stage
    stage.end_time = time.time()
    final_duration = stage.duration
    assert final_duration is not None
    assert final_duration >= 0.1


def test_substep_tracking():
    """Test substep tracking"""
    tracker = ProgressTracker(academic_mode=True)
    
    substeps = ["Step 1", "Step 2", "Step 3"]
    tracker.start_stage(ResearchStage.RESEARCH, "Starting", substeps=substeps)
    
    stage = tracker.stages[ResearchStage.RESEARCH]
    assert stage.substeps == substeps
    assert stage.current_substep == "Step 1"
    
    # Update to next substep
    tracker.update_stage(ResearchStage.RESEARCH, 50, current_substep="Step 2")
    assert stage.current_substep == "Step 2"


def test_failed_stage():
    """Test stage failure handling"""
    tracker = ProgressTracker(academic_mode=True)
    
    tracker.start_stage(ResearchStage.RESEARCH)
    tracker.fail_stage(ResearchStage.RESEARCH, "Test error")
    
    stage = tracker.stages[ResearchStage.RESEARCH]
    assert stage.status == "failed"
    assert stage.message == "Test error"
    assert stage.end_time is not None


if __name__ == "__main__":
    # Run tests
    print("Running progress tracking tests...")
    
    test_progress_tracker_initialization()
    print("✓ Tracker initialization")
    
    test_stage_progress()
    print("✓ Stage progress")
    
    test_overall_progress()
    print("✓ Overall progress")
    
    test_time_estimation()
    print("✓ Time estimation")
    
    test_status_summary()
    print("✓ Status summary")
    
    test_intermediate_outputs()
    print("✓ Intermediate outputs")
    
    test_progress_report_save()
    print("✓ Progress report save")
    
    test_progress_display_creation()
    print("✓ Progress display creation")
    
    test_stage_duration()
    print("✓ Stage duration")
    
    test_substep_tracking()
    print("✓ Substep tracking")
    
    test_failed_stage()
    print("✓ Failed stage")
    
    print("\n✅ All tests passed!")
