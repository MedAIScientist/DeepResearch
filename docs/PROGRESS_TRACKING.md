# Progress Tracking Documentation

## Overview

Gazzali Research includes comprehensive progress tracking for research workflows, providing real-time feedback on research stages, estimated time remaining, and intermediate outputs.

## Features

### 1. Stage-by-Stage Progress Tracking

The system tracks progress through distinct research stages:

- **Initialization**: Setting up the research environment and configuration
- **Question Refinement**: Analyzing and refining research questions (academic mode only)
- **Deep Research**: Conducting the main research using Tongyi DeepResearch agent
- **Citation Extraction**: Extracting and organizing citations (academic mode only)
- **Report Generation**: Synthesizing research into structured reports (academic mode only)
- **Bibliography Generation**: Creating formatted bibliographies (academic mode only)

### 2. Visual Progress Indicators

Progress is displayed with:
- **Progress bars**: Visual representation of overall completion
- **Stage headers**: Clear indication of current stage
- **Substep tracking**: Detailed progress within each stage
- **Color-coded output**: Easy-to-read status indicators

Example output:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔬 STAGE: DEEP RESEARCH
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Prioritizing peer-reviewed sources with Scholar-first strategy

Progress: [████████████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░] 48.5%
Elapsed: 2m 15s  |  Remaining: 2m 30s
Stages: 2/5 complete
```

### 3. Time Estimation

The progress tracker provides:
- **Elapsed time**: Time since research started
- **Estimated remaining time**: Based on completed stages and historical averages
- **Stage durations**: Individual timing for each completed stage

Time estimates adapt based on:
- Average durations for each stage type
- Actual completion times from current session
- Academic vs. standard mode differences

### 4. Intermediate Outputs

At key stages, the system generates intermediate outputs:
- **Question refinement results**: Refined questions and quality assessments
- **Research findings**: Raw research data from the agent
- **Citation database**: Extracted citations and metadata
- **Section drafts**: Individual report sections as they're generated

Intermediate outputs are:
- Saved automatically to the output directory
- Timestamped for tracking
- Available for review during long-running research

### 5. Stage Completion Notifications

Each stage completion includes:
- **Success indicator**: Visual confirmation of completion
- **Duration**: Time taken for the stage
- **Summary**: Key metrics or outputs from the stage
- **Next steps**: What's coming next in the workflow

Example:
```
✅ Question Refinement Complete (15s)
   Generated 3 refined questions

Progress: [██████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░] 20.0%
Elapsed: 17s  |  Remaining: 1m 8s
Stages: 1/5 complete
```

## Usage

### Automatic Progress Tracking

Progress tracking is automatically enabled in academic mode:

```bash
python -m gazzali.gazzali --academic "Your research question"
```

### Verbose Mode

For detailed progress information (default):

```bash
python -m gazzali.gazzali --academic --verbose "Your research question"
```

### Quiet Mode

For minimal output (future feature):

```bash
python -m gazzali.gazzali --academic --quiet "Your research question"
```

## Progress Report Files

### JSON Progress Reports

Progress reports are automatically saved to:
```
outputs/reports/progress_YYYYMMDD_HHMMSS.json
```

Report structure:
```json
{
  "timestamp": "2024-01-15T14:30:00",
  "academic_mode": true,
  "chunked_mode": false,
  "status": {
    "overall_progress": 100.0,
    "completed_stages": 5,
    "total_stages": 5,
    "elapsed_time": 245.3,
    "elapsed_formatted": "4m 5s",
    "estimated_remaining": 0,
    "remaining_formatted": "0s",
    "current_stage": null,
    "stages": {
      "initialization": {
        "status": "complete",
        "progress": 100.0,
        "message": "Configuration loaded",
        "duration": 2.1,
        "current_substep": null
      },
      "question_refinement": {
        "status": "complete",
        "progress": 100.0,
        "message": "Generated 3 refined questions",
        "duration": 15.4,
        "current_substep": null
      },
      "research": {
        "status": "complete",
        "progress": 100.0,
        "message": "Research agent completed successfully",
        "duration": 180.2,
        "current_substep": null
      },
      "report_generation": {
        "status": "complete",
        "progress": 100.0,
        "message": "Generated 8,234 word paper",
        "duration": 45.8,
        "current_substep": null
      },
      "bibliography_generation": {
        "status": "complete",
        "progress": 100.0,
        "message": "Exported 23 citations",
        "duration": 1.8,
        "current_substep": null
      }
    }
  },
  "intermediate_outputs": [
    {
      "stage": "question_refinement",
      "timestamp": "2024-01-15T14:30:15",
      "duration": 15.4,
      "output": {
        "refined_questions": ["...", "...", "..."],
        "quality_assessment": "..."
      }
    }
  ]
}
```

### Using Progress Reports

Progress reports can be used for:
- **Performance analysis**: Identify bottlenecks in the workflow
- **Time estimation**: Improve future time estimates
- **Debugging**: Understand where failures occurred
- **Auditing**: Track research workflow execution

## Stage Details

### Initialization Stage
- **Duration**: ~2 seconds
- **Activities**:
  - Load configuration
  - Validate API keys
  - Set up output directories
  - Initialize citation manager (academic mode)

### Question Refinement Stage
- **Duration**: ~15 seconds
- **Activities**:
  - Analyze question quality
  - Generate refined questions
  - Assess FINER criteria
  - Identify key variables
- **Intermediate Output**: Refined questions and quality assessment

### Deep Research Stage
- **Duration**: ~3 minutes (varies significantly)
- **Activities**:
  - Launch Tongyi DeepResearch agent
  - Execute Scholar searches (academic mode)
  - Visit and analyze sources
  - Extract information
  - Generate research findings
- **Intermediate Output**: Raw research data

### Citation Extraction Stage
- **Duration**: ~10 seconds
- **Activities**:
  - Parse research results
  - Extract citation metadata
  - Deduplicate citations
  - Assess source quality
- **Intermediate Output**: Citation database

### Report Generation Stage
- **Duration**: ~60 seconds
- **Activities**:
  - Structure report sections
  - Generate abstract
  - Format citations
  - Apply academic writing style
  - Create bibliography
- **Intermediate Output**: Formatted report

### Bibliography Generation Stage
- **Duration**: ~5 seconds
- **Activities**:
  - Sort citations
  - Format bibliography
  - Export to BibTeX/RIS
- **Intermediate Output**: Bibliography files

## Customization

### Adjusting Stage Durations

Default stage durations can be customized in `progress_tracker.py`:

```python
STAGE_DURATIONS = {
    ResearchStage.INITIALIZATION: 2,
    ResearchStage.QUESTION_REFINEMENT: 15,
    ResearchStage.RESEARCH: 180,
    ResearchStage.CITATION_EXTRACTION: 10,
    ResearchStage.REPORT_GENERATION: 60,
    ResearchStage.BIBLIOGRAPHY_GENERATION: 5,
}
```

### Adding Custom Stages

To add custom stages:

1. Add to `ResearchStage` enum in `progress_tracker.py`
2. Add display name to `STAGE_NAMES` in `progress_display.py`
3. Add icon to `STAGE_ICONS` in `progress_display.py`
4. Initialize in workflow

### Progress Callbacks

For programmatic access to progress:

```python
from gazzali.progress_tracker import ProgressTracker, ResearchStage

tracker = ProgressTracker(academic_mode=True)

# Start stage
tracker.start_stage(ResearchStage.RESEARCH, "Starting research...")

# Update progress
tracker.update_stage(ResearchStage.RESEARCH, 50, "Halfway through...")

# Complete stage
tracker.complete_stage(ResearchStage.RESEARCH, "Research complete")

# Get status
status = tracker.get_status_summary()
print(f"Overall progress: {status['overall_progress']}%")
```

## Troubleshooting

### Progress Not Updating

If progress appears stuck:
1. Check that the research agent is running (not hung)
2. Verify API keys are valid
3. Check network connectivity
4. Review logs for errors

### Inaccurate Time Estimates

Time estimates may be inaccurate:
- During first run (no historical data)
- For very large or complex questions
- When network is slow
- When API rate limits are hit

Estimates improve over time as the system learns typical durations.

### Missing Intermediate Outputs

If intermediate outputs aren't saved:
1. Check output directory permissions
2. Verify disk space
3. Check for file system errors
4. Review progress report for stage failures

## Best Practices

1. **Monitor progress**: Keep an eye on time estimates for long-running research
2. **Review intermediate outputs**: Check quality at each stage
3. **Save progress reports**: Keep for performance analysis
4. **Adjust expectations**: First runs may take longer than estimates
5. **Use verbose mode**: For detailed insight into workflow execution

## Future Enhancements

Planned improvements:
- Real-time progress streaming to web interface
- Configurable progress update intervals
- Progress persistence across restarts
- Historical performance analytics
- Adaptive time estimation based on question complexity
- Progress notifications (email, webhook)
- Parallel stage execution tracking

## API Reference

### ProgressTracker

Main class for tracking research progress.

**Methods:**
- `start_stage(stage, message, substeps)`: Mark stage as started
- `update_stage(stage, progress_percent, message)`: Update stage progress
- `complete_stage(stage, message, output)`: Mark stage as complete
- `fail_stage(stage, error_message)`: Mark stage as failed
- `get_overall_progress()`: Get overall progress percentage
- `get_elapsed_time()`: Get elapsed time in seconds
- `estimate_remaining_time()`: Estimate remaining time
- `get_status_summary()`: Get comprehensive status
- `save_progress_report(filepath)`: Save progress to file

### ProgressDisplay

Class for displaying progress in terminal.

**Methods:**
- `show_stage_start(stage, message)`: Display stage start
- `show_stage_progress(stage, message)`: Display progress update
- `show_stage_complete(stage, message)`: Display completion
- `show_stage_failed(stage, error_message)`: Display failure
- `show_substep(substep)`: Display substep
- `show_summary()`: Display final summary
- `show_intermediate_output(stage, summary)`: Display intermediate output

### ResearchStage

Enum of research workflow stages.

**Values:**
- `INITIALIZATION`
- `QUESTION_REFINEMENT`
- `RESEARCH`
- `CITATION_EXTRACTION`
- `REPORT_GENERATION`
- `BIBLIOGRAPHY_GENERATION`
- `COMPLETE`

## Examples

### Basic Usage

```python
from gazzali.progress_tracker import ProgressTracker, ResearchStage
from gazzali.progress_display import create_progress_display

# Initialize
tracker = ProgressTracker(academic_mode=True)
display = create_progress_display(tracker)

# Run workflow
display.show_stage_start(ResearchStage.INITIALIZATION)
# ... do initialization ...
display.show_stage_complete(ResearchStage.INITIALIZATION)

display.show_stage_start(ResearchStage.RESEARCH)
# ... do research ...
display.show_stage_complete(ResearchStage.RESEARCH)

# Show summary
display.show_summary()
```

### With Substeps

```python
substeps = [
    "Analyzing question",
    "Generating alternatives",
    "Assessing quality"
]

tracker.start_stage(
    ResearchStage.QUESTION_REFINEMENT,
    "Refining question...",
    substeps=substeps
)

for i, substep in enumerate(substeps):
    display.show_substep(substep)
    # ... do substep work ...
    progress = ((i + 1) / len(substeps)) * 100
    tracker.update_stage(
        ResearchStage.QUESTION_REFINEMENT,
        progress,
        current_substep=substep
    )

tracker.complete_stage(ResearchStage.QUESTION_REFINEMENT)
```

### Saving Intermediate Outputs

```python
# Complete stage with output
output = {
    "refined_questions": ["Q1", "Q2", "Q3"],
    "quality_score": 0.85
}

tracker.complete_stage(
    ResearchStage.QUESTION_REFINEMENT,
    "Generated 3 questions",
    output=output
)

# Later, retrieve outputs
outputs = tracker.get_intermediate_outputs()
for output in outputs:
    print(f"Stage: {output['stage']}")
    print(f"Duration: {output['duration']}s")
    print(f"Output: {output['output']}")
```

## Support

For issues or questions about progress tracking:
1. Check this documentation
2. Review progress report JSON files
3. Check GitHub issues
4. Open a new issue with progress report attached
