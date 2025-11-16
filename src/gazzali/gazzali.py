#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gazzali Research - Academic AI Research Assistant CLI

Main command-line interface for Gazzali Research, supporting both standard
and academic research modes with enhanced citation management, literature
review synthesis, and scholarly output formats.
"""

import sys
import os
import json
import subprocess
import argparse
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any

from .config import get_env
from .academic_config import AcademicConfig
from .chunked_research import run_chunked_research, synthesize_results
from .workflows.templates import (
    WorkflowTemplate,
    WorkflowType,
    get_workflow_template,
    get_workflow_by_name,
    list_available_workflows,
)


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


def print_banner():
    """Print application banner"""
    banner = f"""
{Colors.OKCYAN}╔════════════════════════════════════════════════════════════════╗
║     Gazzali Research - Academic AI Research Assistant         ║
║     Deep research with scholarly rigor and proper citations   ║
╚════════════════════════════════════════════════════════════════╝{Colors.ENDC}
"""
    print(banner)


def check_environment():
    """Check if required environment variables are set"""
    errors = []
    warnings = []
    
    # Check OpenRouter API key
    openrouter_key = get_env("OPENROUTER_API_KEY")
    if not openrouter_key or openrouter_key == "EMPTY":
        errors.append("OPENROUTER_API_KEY is not set")
    elif not openrouter_key.startswith("sk-or-"):
        warnings.append("OPENROUTER_API_KEY doesn't start with 'sk-or-'")
    else:
        print(f"{Colors.OKGREEN}✓{Colors.ENDC} OpenRouter API Key: {openrouter_key[:15]}...")
    
    # Check other API keys (optional but recommended)
    serper_key = get_env("SERPER_API_KEY")
    if not serper_key or serper_key == "serper-your-key":
        warnings.append("SERPER_API_KEY not set (web search may not work)")
    else:
        print(f"{Colors.OKGREEN}✓{Colors.ENDC} Serper API Key: {serper_key[:10]}...")
    
    jina_key = get_env("JINA_API_KEY")
    if not jina_key or jina_key == "jina-your-key":
        warnings.append("JINA_API_KEY not set (web reading may not work)")
    else:
        print(f"{Colors.OKGREEN}✓{Colors.ENDC} Jina API Key: {jina_key[:10]}...")
    
    # Print warnings
    if warnings:
        print(f"\n{Colors.WARNING}⚠️  Warnings:{Colors.ENDC}")
        for warning in warnings:
            print(f"   - {warning}")
    
    # Print errors and exit if any
    if errors:
        print(f"\n{Colors.FAIL}❌ Errors:{Colors.ENDC}")
        for error in errors:
            print(f"   - {error}")
        print(f"\n{Colors.FAIL}Please export required API keys:{Colors.ENDC}")
        print(f"   export OPENROUTER_API_KEY=\"sk-or-v1-your-key\"")
        sys.exit(1)
    
    print()


def list_workflows_and_exit():
    """List available workflow templates and exit"""
    print(f"\n{Colors.BOLD}📋 Available Workflow Templates{Colors.ENDC}\n")
    
    workflows = list_available_workflows()
    for workflow in workflows:
        print(f"{Colors.OKCYAN}▸ {workflow['name']}{Colors.ENDC}")
        print(f"  Type: {workflow['type']}")
        print(f"  Description: {workflow['description']}")
        print(f"  Word Count: {workflow['word_count_range']} words")
        print(f"  Min Sources: {workflow['min_sources']} peer-reviewed\n")
    
    print(f"{Colors.BOLD}Usage:{Colors.ENDC}")
    print(f"  python -m gazzali.gazzali --academic --workflow <type> \"Your question\"\n")
    
    sys.exit(0)


def load_workflow_template(workflow_name: str) -> Optional[WorkflowTemplate]:
    """
    Load a workflow template by name.
    
    Args:
        workflow_name: Name or type of workflow
    
    Returns:
        WorkflowTemplate instance or None if not found
    """
    try:
        # Try as WorkflowType enum value
        workflow_type = WorkflowType(workflow_name)
        return get_workflow_template(workflow_type)
    except (ValueError, KeyError):
        # Try by name
        return get_workflow_by_name(workflow_name)


def save_custom_workflow(name: str, config: AcademicConfig, workflow_dir: Path) -> bool:
    """
    Save current configuration as a custom workflow.
    
    Args:
        name: Custom workflow name
        config: Academic configuration to save
        workflow_dir: Directory to save workflows
    
    Returns:
        True if saved successfully
    """
    try:
        workflow_dir.mkdir(parents=True, exist_ok=True)
        
        # Sanitize filename
        safe_name = "".join(c if c.isalnum() or c in ('-', '_') else '_' for c in name)
        filepath = workflow_dir / f"{safe_name}.json"
        
        # Save configuration
        workflow_data = {
            "name": name,
            "config": config.to_dict(),
            "created_at": datetime.now().isoformat(),
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(workflow_data, f, indent=2, ensure_ascii=False)
        
        print(f"{Colors.OKGREEN}✓{Colors.ENDC} Saved custom workflow: {filepath}\n")
        return True
        
    except Exception as e:
        print(f"{Colors.FAIL}❌ Failed to save workflow: {e}{Colors.ENDC}\n")
        return False


def load_custom_workflow(name: str, workflow_dir: Path) -> Optional[AcademicConfig]:
    """
    Load a custom workflow configuration.
    
    Args:
        name: Custom workflow name
        workflow_dir: Directory containing workflows
    
    Returns:
        AcademicConfig instance or None if not found
    """
    try:
        # Sanitize filename
        safe_name = "".join(c if c.isalnum() or c in ('-', '_') else '_' for c in name)
        filepath = workflow_dir / f"{safe_name}.json"
        
        if not filepath.exists():
            print(f"{Colors.FAIL}❌ Custom workflow not found: {name}{Colors.ENDC}\n")
            return None
        
        with open(filepath, 'r', encoding='utf-8') as f:
            workflow_data = json.load(f)
        
        # Reconstruct config from dict
        config_dict = workflow_data.get('config', {})
        
        # Convert string enums back to enum types
        from .academic_config import CitationStyle, OutputFormat, Discipline
        
        config = AcademicConfig(
            citation_style=CitationStyle(config_dict.get('citation_style', 'apa')),
            output_format=OutputFormat(config_dict.get('output_format', 'paper')),
            discipline=Discipline(config_dict.get('discipline', 'general')),
            word_count_target=config_dict.get('word_count_target', 8000),
            include_abstract=config_dict.get('include_abstract', True),
            include_methodology=config_dict.get('include_methodology', True),
            scholar_priority=config_dict.get('scholar_priority', True),
            export_bibliography=config_dict.get('export_bibliography', False),
            min_peer_reviewed=config_dict.get('min_peer_reviewed', 5),
            source_quality_threshold=config_dict.get('source_quality_threshold', 7),
        )
        
        print(f"{Colors.OKGREEN}✓{Colors.ENDC} Loaded custom workflow: {workflow_data.get('name', name)}\n")
        return config
        
    except Exception as e:
        print(f"{Colors.FAIL}❌ Failed to load workflow: {e}{Colors.ENDC}\n")
        return None


def display_academic_config(config: AcademicConfig, workflow_name: Optional[str] = None):
    """Display academic configuration settings with enhanced visual formatting"""
    print(f"\n{Colors.OKCYAN}╔════════════════════════════════════════════════════════════════╗{Colors.ENDC}")
    print(f"{Colors.OKCYAN}║{Colors.ENDC} {Colors.BOLD}📚 ACADEMIC MODE ENABLED{Colors.ENDC}                                      {Colors.OKCYAN}║{Colors.ENDC}")
    print(f"{Colors.OKCYAN}╚════════════════════════════════════════════════════════════════╝{Colors.ENDC}\n")
    
    if workflow_name:
        print(f"{Colors.BOLD}Workflow:{Colors.ENDC} {Colors.OKGREEN}{workflow_name}{Colors.ENDC}\n")
    
    print(f"{Colors.BOLD}Configuration:{Colors.ENDC}")
    print(f"  • Citation Style:     {Colors.OKGREEN}{config.citation_style.value.upper()}{Colors.ENDC}")
    print(f"  • Output Format:      {Colors.OKGREEN}{config.output_format.value.capitalize()}{Colors.ENDC}")
    print(f"  • Discipline:         {Colors.OKGREEN}{config.discipline.value.capitalize()}{Colors.ENDC}")
    print(f"  • Word Count Target:  {Colors.OKGREEN}{config.word_count_target:,}{Colors.ENDC}")
    print(f"  • Scholar Priority:   {Colors.OKGREEN}{'Enabled' if config.scholar_priority else 'Disabled'}{Colors.ENDC}")
    
    # Validate configuration
    issues = config.validate()
    if issues:
        print(f"\n{Colors.WARNING}⚠️  Configuration Warnings:{Colors.ENDC}")
        for issue in issues:
            print(f"   - {issue}")
    
    print()


def get_question_interactive():
    """Get question from user interactively"""
    print(f"{Colors.BOLD}🤔 Enter your research question (blank line to finish):{Colors.ENDC}\n")
    
    lines = []
    while True:
        try:
            line = input()
            if line == "" and lines:
                break
            lines.append(line)
        except EOFError:
            break
    
    question = "\n".join(lines).strip()
    
    if not question:
        print(f"{Colors.FAIL}❌ Question cannot be empty!{Colors.ENDC}")
        sys.exit(1)
    
    return question


def refine_question(question: str, config: AcademicConfig) -> Optional[str]:
    """
    Refine research question using QuestionRefiner with enhanced progress display.
    
    Args:
        question: Original research question
        config: Academic configuration
    
    Returns:
        Refined question or None if refinement fails
    """
    try:
        from .question_refiner import QuestionRefiner
        
        print(f"\n{Colors.OKCYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.ENDC}")
        print(f"{Colors.BOLD}🔍 STAGE 1: Question Refinement{Colors.ENDC}")
        print(f"{Colors.OKCYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.ENDC}\n")
        
        print(f"Analyzing research question for academic rigor...")
        
        openrouter_key = get_env("OPENROUTER_API_KEY")
        if not openrouter_key:
            print(f"{Colors.WARNING}⚠️  Cannot refine question: API key not set{Colors.ENDC}")
            return None
        
        refiner = QuestionRefiner(api_key=openrouter_key)
        refined = refiner.refine_question(
            broad_topic=question,
            discipline=config.discipline.value if config.discipline else None
        )
        
        if refined and refined.refined_questions:
            print(f"\n{Colors.OKGREEN}✅ Question Refinement Complete!{Colors.ENDC}\n")
            
            # Display original question
            print(f"{Colors.BOLD}Original Question:{Colors.ENDC}")
            print(f"  {refined.original_topic}\n")
            
            # Display refined questions
            print(f"{Colors.BOLD}Refined Questions:{Colors.ENDC}")
            for i, q in enumerate(refined.refined_questions, 1):
                marker = "→" if i == 1 else " "
                print(f"  {marker} {i}. {q}")
            
            # Display quality assessment
            print(f"\n{Colors.BOLD}Quality Assessment:{Colors.ENDC}")
            print(f"  • Question Type:  {Colors.OKGREEN}{refined.question_type}{Colors.ENDC}")
            print(f"  • Scope:          {Colors.OKGREEN}{refined.scope_assessment}{Colors.ENDC}")
            
            if refined.key_variables:
                print(f"  • Key Variables:  {', '.join(refined.key_variables)}")
            
            print(f"\n{Colors.OKCYAN}Using refined question for research...{Colors.ENDC}\n")
            
            # Use the first refined question
            return refined.refined_questions[0]
        
    except ImportError:
        print(f"{Colors.WARNING}⚠️  QuestionRefiner not available{Colors.ENDC}")
    except Exception as e:
        print(f"{Colors.WARNING}⚠️  Question refinement failed: {e}{Colors.ENDC}")
    
    return None


def create_question_file(question: str, project_root: Path) -> tuple[str, str]:
    """
    Create temporary JSONL file with the question in the inference directory.
    
    Args:
        question: Research question
        project_root: Project root directory
    
    Returns:
        Tuple of (filepath, filename)
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"cli_question_{timestamp}.jsonl"
    
    # Save to inference eval_data directory 
    inference_dir = project_root / "DeepResearch" / "inference" / "eval_data"
    inference_dir.mkdir(parents=True, exist_ok=True)
    filepath = inference_dir / filename
    
    question_data = {
        "question": question,
        "answer": ""
    }
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(question_data, f, ensure_ascii=False)
        f.write('\n')
    
    return str(filepath), filename


def run_research(dataset_filename: str, project_root: Path, academic_mode: bool = False, academic_config: Optional[AcademicConfig] = None, workflow_template: Optional[WorkflowTemplate] = None) -> bool:
    """
    Run the DeepResearch agent with progress indicators.
    
    Args:
        dataset_filename: Name of the dataset file
        project_root: Project root directory
        academic_mode: Whether academic mode is enabled
        academic_config: Academic configuration (if academic mode enabled)
        workflow_template: Optional workflow template for specialized prompts
    
    Returns:
        True if research completed successfully
    """
    inference_dir = project_root / "DeepResearch" / "inference"
    
    # Change to inference directory
    os.chdir(inference_dir)
    
    # Get configuration from environment or use defaults
    model_path = get_env("MODEL_PATH", "") or ""
    output_path = get_env("OUTPUT_PATH")
    if not output_path:
        output_path = str(project_root / "outputs")

    temperature = float(get_env("TEMPERATURE", "0.85"))
    presence_penalty = float(get_env("PRESENCE_PENALTY", "1.1"))
    max_workers = int(get_env("MAX_WORKERS", "1"))
    rollout_count = int(get_env("ROLLOUT_COUNT", "1"))
    
    # Use the relative path from inference directory
    dataset_path = f"eval_data/{dataset_filename}"
    
    # Set academic mode environment variables for the agent to read
    if academic_mode and academic_config:
        os.environ["GAZZALI_ACADEMIC_MODE"] = "true"
        os.environ["GAZZALI_DISCIPLINE"] = academic_config.discipline.value
        os.environ["GAZZALI_OUTPUT_FORMAT"] = academic_config.output_format.value
        os.environ["GAZZALI_CITATION_STYLE"] = academic_config.citation_style.value
        
        # Set workflow-specific environment variables if template provided
        if workflow_template:
            os.environ["GAZZALI_WORKFLOW_TYPE"] = workflow_template.workflow_type.value
            os.environ["GAZZALI_SEARCH_STRATEGY"] = workflow_template.search_strategy
    else:
        os.environ["GAZZALI_ACADEMIC_MODE"] = "false"
    
    # Run run_multi_react.py
    cmd = [
        sys.executable,
        "run_multi_react.py",
        "--dataset", dataset_path,
        "--output", output_path,
        "--model", model_path,
        "--temperature", str(temperature),
        "--presence_penalty", str(presence_penalty),
        "--max_workers", str(max_workers),
        "--roll_out_count", str(rollout_count)
    ]
    
    # Display research stage header
    stage_num = "2" if academic_mode else "1"
    print(f"\n{Colors.OKCYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.ENDC}")
    print(f"{Colors.BOLD}🔬 STAGE {stage_num}: Deep Research{Colors.ENDC}")
    print(f"{Colors.OKCYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.ENDC}\n")
    
    if academic_mode:
        print(f"{Colors.OKGREEN}Academic Mode:{Colors.ENDC} Prioritizing peer-reviewed sources")
        print(f"{Colors.OKGREEN}Research Agent:{Colors.ENDC} Tongyi DeepResearch 30B")
        
        if workflow_template:
            print(f"{Colors.OKGREEN}Workflow:{Colors.ENDC} {workflow_template.name}")
            print(f"{Colors.OKGREEN}Search Strategy:{Colors.ENDC} {workflow_template.search_strategy[:80]}...")
        else:
            print(f"{Colors.OKGREEN}Search Strategy:{Colors.ENDC} Scholar-first with quality filtering")
        print()
    else:
        print(f"Launching Tongyi DeepResearch agent...\n")
    
    try:
        subprocess.run(cmd, check=True, capture_output=False, text=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n{Colors.FAIL}❌ Research process failed: {e}{Colors.ENDC}")
        return False


def find_latest_output(output_dir: Path) -> Optional[Path]:
    """
    Find the latest output file.
    
    Args:
        output_dir: Output directory path
    
    Returns:
        Path to latest output file or None
    """
    if not output_dir.exists():
        return None
    
    files = []
    for filepath in output_dir.rglob('*.jsonl'):
        # Only include iter*.jsonl files (actual results)
        if 'iter' in filepath.name:
            files.append((filepath, filepath.stat().st_mtime))
    
    if not files:
        return None
    
    # Sort by modification time, newest first
    files.sort(key=lambda x: x[1], reverse=True)
    return files[0][0]


def save_markdown_report(data: Dict[str, Any], output_dir: Path) -> Optional[Path]:
    """
    Save the result as a Markdown report.
    
    Args:
        data: Research result data
        output_dir: Output directory
    
    Returns:
        Path to saved report or None
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_filename = f"report_{timestamp}.md"
    report_path = output_dir / "reports"
    
    # Create reports directory
    report_path.mkdir(parents=True, exist_ok=True)
    
    report_file = report_path / report_filename
    
    try:
        with open(report_file, 'w', encoding='utf-8') as f:
            # Header
            f.write("# Gazzali Research Report\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("---\n\n")

            if 'question' in data:
                f.write("## 🎯 Research Question\n\n")
                f.write(f"{data['question']}\n\n")
                f.write("---\n\n")

            findings = data.get('prediction')
            if findings and findings != "[Failed]":
                f.write("## 📊 Research Findings\n\n")
                f.write(f"{findings}\n\n")
            elif 'answer' in data:
                f.write("## 📊 Research Findings\n\n")
                f.write(f"{data['answer']}\n\n")

            f.write("---\n\n")
            f.write("## 📋 Metadata\n\n")
            f.write("- **Research Model:** Alibaba Tongyi DeepResearch 30B (via OpenRouter)\n")
            f.write(f"- **Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            if 'rollout_idx' in data:
                f.write(f"- **Rollout:** {data['rollout_idx']}\n")
            f.write("\n")
            
        return report_file
    except Exception as e:
        print(f"{Colors.WARNING}⚠️  Could not save report: {e}{Colors.ENDC}")
        return None


def display_result(output_file: Optional[Path]) -> Optional[Dict[str, Any]]:
    """
    Display the research result.
    
    Args:
        output_file: Path to output file
    
    Returns:
        Result data dictionary or None
    """
    if not output_file or not output_file.exists():
        print(f"{Colors.WARNING}⚠️  Result file not found{Colors.ENDC}")
        return None
    
    print(f"\n{Colors.OKCYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.ENDC}")
    print(f"{Colors.OKGREEN}✅ Research complete!{Colors.ENDC}")
    print(f"{Colors.OKCYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.ENDC}\n")
    
    print(f"{Colors.BOLD}📁 Result file:{Colors.ENDC} {output_file}\n")
    
    result_data = None
    
    # Try to read and display the result
    try:
        with open(output_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    data = json.loads(line)
                    result_data = data
                    
                    # Display question
                    if 'question' in data:
                        print(f"{Colors.BOLD}❓ Question:{Colors.ENDC} {data['question']}\n")
                    
                    # Check for errors
                    if 'error' in data:
                        print(f"{Colors.FAIL}❌ Error:{Colors.ENDC} {data['error']}\n")
                        continue
                    
                    # Display prediction (the agent's answer)
                    if 'prediction' in data and data['prediction'] != "[Failed]":
                        print(f"{Colors.BOLD}📝 Answer:{Colors.ENDC}\n")
                        print(data['prediction'])
                        print()
                    elif 'answer' in data:
                        print(f"{Colors.BOLD}📝 Answer:{Colors.ENDC}\n")
                        print(data['answer'])
                        print()
    except Exception as e:
        print(f"{Colors.WARNING}⚠️  Unable to read results: {e}{Colors.ENDC}")
    
    return result_data


def generate_academic_report(
    question: str,
    research_results: str,
    config: AcademicConfig,
    output_dir: Path,
    citation_manager: Optional[Any] = None
) -> Optional[Path]:
    """
    Generate academic report with proper formatting and citations.
    
    Args:
        question: Research question
        research_results: Research findings
        config: Academic configuration
        output_dir: Output directory
        citation_manager: Optional existing citation manager
    
    Returns:
        Path to generated report or None
    """
    try:
        from .report_generator import AcademicReportGenerator
        from .citation_manager import CitationManager
        
        # Display stage header
        print(f"\n{Colors.OKCYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.ENDC}")
        print(f"{Colors.BOLD}📝 STAGE 3: Academic Report Generation{Colors.ENDC}")
        print(f"{Colors.OKCYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.ENDC}\n")
        
        print(f"Synthesizing research into academic format...")
        print(f"  • Format: {Colors.OKGREEN}{config.output_format.value.capitalize()}{Colors.ENDC}")
        print(f"  • Citation Style: {Colors.OKGREEN}{config.citation_style.value.upper()}{Colors.ENDC}")
        print(f"  • Target Length: {Colors.OKGREEN}{config.word_count_target:,} words{Colors.ENDC}\n")
        
        openrouter_key = get_env("OPENROUTER_API_KEY")
        if not openrouter_key:
            print(f"{Colors.WARNING}⚠️  Cannot generate academic report: API key not set{Colors.ENDC}")
            return None
        
        # Initialize or use existing citation manager
        if citation_manager is None:
            citation_manager = CitationManager()
        
        # Initialize report generator
        generator = AcademicReportGenerator(
            config=config,
            citation_manager=citation_manager
        )
        
        # Generate report
        print(f"Generating structured sections...")
        report = generator.generate_report(
            question=question,
            research_results=research_results,
            api_key=openrouter_key
        )
        
        # Save report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_q = "".join(c if c.isalnum() or c in (' ', '-', '_') else '' for c in question)[:50]
        report_filename = f"academic_{config.output_format.value}_{timestamp}_{safe_q}.md"
        report_path = output_dir / "reports" / report_filename
        report_path.parent.mkdir(parents=True, exist_ok=True)
        
        report.save(str(report_path), format='markdown')
        
        # Display success with detailed metrics
        print(f"\n{Colors.OKGREEN}✅ Academic Report Complete!{Colors.ENDC}\n")
        
        print(f"{Colors.BOLD}📁 Output:{Colors.ENDC}")
        print(f"  {report_path}\n")
        
        print(f"{Colors.BOLD}📊 Report Metrics:{Colors.ENDC}")
        print(f"  • Word Count:        {Colors.OKGREEN}{report.word_count:,}{Colors.ENDC}")
        print(f"  • Sections:          {Colors.OKGREEN}{len(report.sections)}{Colors.ENDC}")
        print(f"  • Citations:         {Colors.OKGREEN}{len(citation_manager.citations)}{Colors.ENDC}")
        
        # Calculate source quality metrics
        peer_reviewed = sum(1 for c in citation_manager.citations.values() 
                          if c.venue_type.value in ['journal', 'conference'])
        if len(citation_manager.citations) > 0:
            quality_pct = (peer_reviewed / len(citation_manager.citations)) * 100
            print(f"  • Peer-Reviewed:     {Colors.OKGREEN}{peer_reviewed} ({quality_pct:.1f}%){Colors.ENDC}")
        
        # Show highly cited sources
        highly_cited = [c for c in citation_manager.citations.values() 
                       if c.citation_count and c.citation_count > 100]
        if highly_cited:
            print(f"  • Highly Cited:      {Colors.OKGREEN}{len(highly_cited)} sources{Colors.ENDC}")
        
        print()
        
        # Export bibliography if requested
        if config.export_bibliography:
            bib_path = report_path.with_suffix('.bib')
            citation_manager.export_bibtex(str(bib_path))
            print(f"{Colors.OKGREEN}✓{Colors.ENDC} Bibliography exported: {bib_path}\n")
        
        return report_path
        
    except ImportError as e:
        print(f"{Colors.WARNING}⚠️  Academic report generation not available: {e}{Colors.ENDC}")
    except Exception as e:
        print(f"{Colors.WARNING}⚠️  Academic report generation failed: {e}{Colors.ENDC}")
    
    return None


def main():
    """Main CLI function"""
    parser = argparse.ArgumentParser(
        description="Gazzali Research - Academic AI Research Assistant",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode
  python -m gazzali.gazzali

  # Standard research
  python -m gazzali.gazzali "What are the major AI safety milestones in 2024?"

  # Academic mode with APA citations
  python -m gazzali.gazzali --academic --citation-style apa "Impact of AI on education"

  # Literature review in social sciences
  python -m gazzali.gazzali --academic --output-format review --discipline social \\
      "Social media effects on mental health"

  # Research proposal with question refinement
  python -m gazzali.gazzali --academic --output-format proposal --refine \\
      "Climate change adaptation strategies"

  # Chunked research for large topics
  python -m gazzali.gazzali --chunked "Map the global AI regulation landscape"
        """
    )

    # Positional arguments
    parser.add_argument(
        'question',
        nargs='?',
        help='Research question (optional in interactive mode)'
    )
    
    # Academic mode arguments
    parser.add_argument(
        '--academic',
        action='store_true',
        help='Enable academic research mode with enhanced features'
    )
    parser.add_argument(
        '--citation-style',
        choices=['apa', 'mla', 'chicago', 'ieee'],
        help='Citation format style (default: apa)'
    )
    parser.add_argument(
        '--output-format',
        choices=['paper', 'review', 'proposal', 'abstract', 'presentation'],
        help='Output document format (default: paper)'
    )
    parser.add_argument(
        '--discipline',
        choices=['general', 'stem', 'social', 'humanities', 'medical'],
        help='Academic discipline for terminology and conventions (default: general)'
    )
    parser.add_argument(
        '--refine',
        action='store_true',
        help='Refine research question before starting'
    )
    parser.add_argument(
        '--word-count',
        type=int,
        help='Target word count for report (default: 8000)'
    )
    parser.add_argument(
        '--export-bib',
        action='store_true',
        help='Export bibliography to .bib file'
    )
    
    # Workflow template arguments
    parser.add_argument(
        '--workflow',
        choices=['literature_review', 'systematic_review', 'methodology_comparison', 'theoretical_analysis'],
        help='Use a preset workflow template for common research tasks'
    )
    parser.add_argument(
        '--list-workflows',
        action='store_true',
        help='List available workflow templates and exit'
    )
    parser.add_argument(
        '--save-workflow',
        metavar='NAME',
        help='Save current configuration as a custom workflow'
    )
    parser.add_argument(
        '--load-workflow',
        metavar='NAME',
        help='Load a custom workflow configuration'
    )
    
    # General arguments
    parser.add_argument(
        '--chunked',
        action='store_true',
        help='Enable chunked research mode for very large topics'
    )
    parser.add_argument(
        '--no-keep',
        action='store_true',
        help='Do not keep temporary dataset files'
    )
    parser.add_argument(
        '--output-dir',
        help='Custom output directory (defaults to <project>/outputs)'
    )
    
    args = parser.parse_args()
    
    # Handle list workflows command
    if args.list_workflows:
        list_workflows_and_exit()
    
    # Print banner
    print_banner()
    
    # Get project root
    project_root = Path(__file__).parent.absolute()
    
    # Check environment
    check_environment()
    
    # Workflow directory for custom workflows
    workflow_dir = project_root / ".gazzali" / "workflows"
    
    # Load academic configuration if in academic mode
    academic_config = None
    workflow_name = None
    workflow_template = None
    
    if args.academic:
        # Priority order:
        # 1. Load custom workflow if specified
        # 2. Load preset workflow template if specified
        # 3. Load from environment
        # 4. Override with command-line args
        
        if args.load_workflow:
            # Load custom workflow
            academic_config = load_custom_workflow(args.load_workflow, workflow_dir)
            if academic_config:
                workflow_name = f"Custom: {args.load_workflow}"
            else:
                print(f"{Colors.WARNING}⚠️  Falling back to default configuration{Colors.ENDC}\n")
                academic_config = AcademicConfig.from_env()
        
        elif args.workflow:
            # Load preset workflow template
            workflow_template = load_workflow_template(args.workflow)
            if workflow_template:
                academic_config = workflow_template.academic_config
                workflow_name = workflow_template.name
                print(f"{Colors.OKGREEN}✓{Colors.ENDC} Loaded workflow template: {workflow_name}\n")
            else:
                print(f"{Colors.WARNING}⚠️  Workflow not found: {args.workflow}{Colors.ENDC}")
                print(f"{Colors.WARNING}⚠️  Falling back to default configuration{Colors.ENDC}\n")
                academic_config = AcademicConfig.from_env()
        
        else:
            # Load from environment
            academic_config = AcademicConfig.from_env()
        
        # Override with command-line arguments (highest priority)
        if args.citation_style or args.output_format or args.discipline or args.word_count or args.export_bib:
            academic_config = AcademicConfig.from_args(args)
        
        display_academic_config(academic_config, workflow_name)
        
        # Save workflow if requested
        if args.save_workflow:
            save_custom_workflow(args.save_workflow, academic_config, workflow_dir)
    
    # Get question
    if args.question:
        question = args.question
        print(f"{Colors.BOLD}❓ Question:{Colors.ENDC} {question}\n")
    else:
        question = get_question_interactive()
    
    # Refine question if requested
    if args.refine and academic_config:
        refined = refine_question(question, academic_config)
        if refined:
            question = refined
            print(f"{Colors.BOLD}❓ Using refined question:{Colors.ENDC} {question}\n")
    
    # Create question file
    question_filepath, question_filename = create_question_file(question, project_root)
    print(f"{Colors.OKGREEN}✓{Colors.ENDC} Created dataset file: {question_filepath}\n")
    
    # Determine output directory
    if args.output_dir:
        output_dir = Path(args.output_dir)
    else:
        output_dir = project_root / "outputs"
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Check if chunked mode is enabled
    if args.chunked:
        print(f"\n{Colors.BOLD}🧩 Chunked research mode enabled{Colors.ENDC}\n")
        
        # Run chunked research
        chunked_results = run_chunked_research(question, project_root)
        
        # Synthesize all results
        openrouter_key = get_env("OPENROUTER_API_KEY")
        if openrouter_key and len(chunked_results) > 1:
            final_report = synthesize_results(question, chunked_results, openrouter_key)
            
            # Save synthesized report
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_q = "".join(c if c.isalnum() or c in (' ', '-', '_') else '' for c in question)[:50]
            report_filename = f"chunked_synthesis_{timestamp}_{safe_q}.md"
            report_path = output_dir / "reports" / report_filename
            report_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(final_report)
            
            print(f"\n{Colors.OKGREEN}✅ Chunked research completed!{Colors.ENDC}")
            print(f"{Colors.BOLD}📁 Synthesized report:{Colors.ENDC} {report_path}\n")
            print(f"{Colors.BOLD}📊 Processed chunks:{Colors.ENDC} {len(chunked_results)}\n")

            print(f"{Colors.BOLD}📝 Report preview:{Colors.ENDC}\n")
            print(final_report[:1000] + "...\n")
        else:
            print(f"{Colors.WARNING}⚠️  Chunked mode failed, falling back to standard pipeline{Colors.ENDC}\n")
            success = run_research(question_filename, project_root, academic_mode=args.academic, academic_config=academic_config, workflow_template=workflow_template)
    else:
        # Normal mode
        success = run_research(question_filename, project_root, academic_mode=args.academic, academic_config=academic_config, workflow_template=workflow_template)
    
    if not args.chunked and success:
        # Find and display result
        latest_output = find_latest_output(output_dir)
        result_data = display_result(latest_output)
        
        # Save basic Markdown report
        if result_data and 'error' not in result_data:
            report_file = save_markdown_report(result_data, output_dir)
            if report_file:
                print(f"{Colors.OKGREEN}✓{Colors.ENDC} Saved primary research report: {report_file}\n")
            
            # Extract research results
            research_results = result_data.get('prediction', result_data.get('answer', ''))
            original_question = result_data.get('question', question)
            
            # Generate academic report if in academic mode
            if args.academic and academic_config:
                academic_report_path = generate_academic_report(
                    question=original_question,
                    research_results=research_results,
                    config=academic_config,
                    output_dir=output_dir
                )
                
                # Display final academic success message
                if academic_report_path:
                    print(f"\n{Colors.OKCYAN}╔════════════════════════════════════════════════════════════════╗{Colors.ENDC}")
                    print(f"{Colors.OKCYAN}║{Colors.ENDC} {Colors.OKGREEN}✅ ACADEMIC RESEARCH COMPLETE{Colors.ENDC}                              {Colors.OKCYAN}║{Colors.ENDC}")
                    print(f"{Colors.OKCYAN}╚════════════════════════════════════════════════════════════════╝{Colors.ENDC}\n")
                    
                    print(f"{Colors.BOLD}Your scholarly report is ready!{Colors.ENDC}")
                    print(f"  • Peer-reviewed sources prioritized")
                    print(f"  • Proper {academic_config.citation_style.value.upper()} citations")
                    print(f"  • Academic writing standards applied")
                    print(f"  • {academic_config.output_format.value.capitalize()} format structure\n")
            else:
                # Standard mode - basic report already saved
                print(f"\n{Colors.OKCYAN}╔════════════════════════════════════════════════════════════════╗{Colors.ENDC}")
                print(f"{Colors.OKCYAN}║{Colors.ENDC} {Colors.OKGREEN}✅ RESEARCH COMPLETE{Colors.ENDC}                                       {Colors.OKCYAN}║{Colors.ENDC}")
                print(f"{Colors.OKCYAN}╚════════════════════════════════════════════════════════════════╝{Colors.ENDC}\n")
    
    # Cleanup temp file unless --no-keep
    if not args.no_keep:
        try:
            os.remove(question_filepath)
            print(f"{Colors.OKGREEN}✓{Colors.ENDC} Cleaned temporary dataset\n")
        except Exception:
            pass
    else:
        print(f"{Colors.WARNING}ℹ️  Temporary dataset retained: {question_filepath}{Colors.ENDC}\n")

    print(f"{Colors.BOLD}📊 Explore all outputs:{Colors.ENDC} ls -lth {output_dir}/\n")


if __name__ == "__main__":
    main()
