#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Progress Tracking Demo

Demonstrates the progress tracking features of Gazzali Research.
"""

import sys
import time
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from gazzali.progress_tracker import ProgressTracker, ResearchStage
from gazzali.progress_display import create_progress_display


def simulate_research_workflow():
    """Simulate a complete research workflow with progress tracking"""
    
    print("=" * 70)
    print("Gazzali Research - Progress Tracking Demo")
    print("=" * 70)
    print()
    
    # Initialize progress tracker for academic mode
    tracker = ProgressTracker(academic_mode=True, chunked_mode=False)
    display = create_progress_display(tracker, verbose=True)
    
    # Stage 1: Initialization
    display.show_stage_start(
        ResearchStage.INITIALIZATION,
        "Setting up academic research workflow..."
    )
    time.sleep(1)
    display.show_stage_complete(
        ResearchStage.INITIALIZATION,
        "Configuration loaded successfully"
    )
    
    # Stage 2: Question Refinement
    substeps = [
        "Analyzing question structure",
        "Assessing FINER criteria",
        "Generating refined alternatives",
        "Evaluating quality"
    ]
    
    tracker.start_stage(
        ResearchStage.QUESTION_REFINEMENT,
        "Refining research question...",
        substeps=substeps
    )
    display.show_stage_start(
        ResearchStage.QUESTION_REFINEMENT,
        "Analyzing research question for academic rigor..."
    )
    
    for i, substep in enumerate(substeps):
        display.show_substep(substep)
        time.sleep(0.5)
        progress = ((i + 1) / len(substeps)) * 100
        tracker.update_stage(
            ResearchStage.QUESTION_REFINEMENT,
            progress,
            current_substep=substep
        )
    
    display.show_stage_complete(
        ResearchStage.QUESTION_REFINEMENT,
        "Generated 3 refined questions"
    )
    
    # Stage 3: Deep Research
    display.show_stage_start(
        ResearchStage.RESEARCH,
        "Launching Tongyi DeepResearch agent with Scholar-first strategy..."
    )
    
    research_steps = [
        "Searching Google Scholar for peer-reviewed sources",
        "Analyzing top 10 papers",
        "Extracting key findings",
        "Synthesizing information"
    ]
    
    for i, step in enumerate(research_steps):
        display.show_stage_progress(ResearchStage.RESEARCH, step)
        time.sleep(1)
        progress = ((i + 1) / len(research_steps)) * 100
        tracker.update_stage(ResearchStage.RESEARCH, progress, step)
    
    display.show_stage_complete(
        ResearchStage.RESEARCH,
        "Analyzed 15 peer-reviewed sources"
    )
    
    # Stage 4: Citation Extraction
    display.show_stage_start(
        ResearchStage.CITATION_EXTRACTION,
        "Extracting and organizing citations..."
    )
    time.sleep(1)
    tracker.update_stage(ResearchStage.CITATION_EXTRACTION, 50, "Processing metadata...")
    time.sleep(0.5)
    display.show_stage_complete(
        ResearchStage.CITATION_EXTRACTION,
        "Extracted 23 citations (87% peer-reviewed)"
    )
    
    # Stage 5: Report Generation
    display.show_stage_start(
        ResearchStage.REPORT_GENERATION,
        "Synthesizing research into academic paper format..."
    )
    
    report_steps = [
        "Generating abstract",
        "Structuring literature review",
        "Formatting citations",
        "Creating discussion section"
    ]
    
    for i, step in enumerate(report_steps):
        display.show_stage_progress(ResearchStage.REPORT_GENERATION, step)
        time.sleep(0.8)
        progress = ((i + 1) / len(report_steps)) * 100
        tracker.update_stage(ResearchStage.REPORT_GENERATION, progress, step)
    
    display.show_stage_complete(
        ResearchStage.REPORT_GENERATION,
        "Generated 8,234 word academic paper"
    )
    
    # Stage 6: Bibliography Generation
    display.show_stage_start(
        ResearchStage.BIBLIOGRAPHY_GENERATION,
        "Exporting bibliography in APA format..."
    )
    time.sleep(0.5)
    display.show_stage_complete(
        ResearchStage.BIBLIOGRAPHY_GENERATION,
        "Exported 23 citations to BibTeX"
    )
    
    # Mark complete
    tracker.complete_stage(ResearchStage.COMPLETE, "All stages completed")
    
    # Show final summary
    display.show_summary()
    
    # Show status details
    print("\n" + "=" * 70)
    print("Detailed Status Report")
    print("=" * 70)
    
    status = tracker.get_status_summary()
    print(f"\nOverall Progress: {status['overall_progress']:.1f}%")
    print(f"Total Time: {status['elapsed_formatted']}")
    print(f"Stages Completed: {status['completed_stages']}/{status['total_stages']}")
    
    print("\nStage Breakdown:")
    for stage_name, stage_info in status['stages'].items():
        if stage_name != 'complete':
            duration = stage_info['duration']
            duration_str = f"{duration:.1f}s" if duration else "N/A"
            print(f"  • {stage_name:30} {stage_info['status']:10} {duration_str}")
    
    # Show intermediate outputs
    outputs = tracker.get_intermediate_outputs()
    if outputs:
        print(f"\nIntermediate Outputs: {len(outputs)} saved")
    
    print("\n" + "=" * 70)
    print("Demo Complete!")
    print("=" * 70)


if __name__ == "__main__":
    simulate_research_workflow()
