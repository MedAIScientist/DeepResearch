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


def display_academic_config(config: AcademicConfig):
    """Display academic configuration settings"""
    print(f"{Colors.BOLD}📚 Academic Mode Configuration:{Colors.ENDC}")
    print(f"   Citation Style: {config.citation_style.value.upper()}")
    print(f"   Output Format: {config.output_format.value.capitalize()}")
    print(f"   Discipline: {config.discipline.value.capitalize()}")
    print(f"   Word Count Target: {config.word_count_target}")
    print(f"   Scholar Priority: {'Yes' if config.scholar_priority else 'No'}")
    
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
    Refine research question using QuestionRefiner.
    
    Args:
        question: Original research question
        config: Academic configuration
    
    Returns:
        Refined question or None if refinement fails
    """
    try:
        from .question_refiner import QuestionRefiner
        
        print(f"\n{Colors.OKCYAN}🔍 Refining research question...{Colors.ENDC}\n")
        
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
            print(f"{Colors.OKGREEN}✓{Colors.ENDC} Question refined successfully!\n")
            print(f"{Colors.BOLD}Original:{Colors.ENDC} {refined.original_topic}\n")
            print(f"{Colors.BOLD}Refined Questions:{Colors.ENDC}")
            for i, q in enumerate(refined.refined_questions, 1):
                print(f"   {i}. {q}")
            print(f"\n{Colors.BOLD}Question Type:{Colors.ENDC} {refined.question_type}")
            print(f"{Colors.BOLD}Scope:{Colors.ENDC} {refined.scope_assessment}\n")
            
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


def run_research(dataset_filename: str, project_root: Path) -> bool:
    """
    Run the DeepResearch agent.
    
    Args:
        dataset_filename: Name of the dataset file
        project_root: Project root directory
    
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
    
    print(f"{Colors.OKCYAN}🚀 Launching Tongyi DeepResearch agent...{Colors.ENDC}")
    print(f"{Colors.OKCYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.ENDC}\n")
    
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
    output_dir: Path
) -> Optional[Path]:
    """
    Generate academic report with proper formatting and citations.
    
    Args:
        question: Research question
        research_results: Research findings
        config: Academic configuration
        output_dir: Output directory
    
    Returns:
        Path to generated report or None
    """
    try:
        from .report_generator import AcademicReportGenerator
        from .citation_manager import CitationManager
        
        print(f"\n{Colors.OKCYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.ENDC}")
        print(f"{Colors.BOLD}📚 Generating academic report...{Colors.ENDC}")
        print(f"{Colors.OKCYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.ENDC}\n")
        
        openrouter_key = get_env("OPENROUTER_API_KEY")
        if not openrouter_key:
            print(f"{Colors.WARNING}⚠️  Cannot generate academic report: API key not set{Colors.ENDC}")
            return None
        
        # Initialize citation manager
        citation_manager = CitationManager()
        
        # Initialize report generator
        generator = AcademicReportGenerator(
            config=config,
            citation_manager=citation_manager
        )
        
        # Generate report
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
        
        print(f"\n{Colors.OKGREEN}✅ Academic report generated!{Colors.ENDC}")
        print(f"{Colors.BOLD}📁 Report:{Colors.ENDC} {report_path}\n")
        print(f"{Colors.BOLD}📊 Statistics:{Colors.ENDC}")
        print(f"   Word Count: {report.word_count}")
        print(f"   Sections: {len(report.sections)}")
        print(f"   Citations: {len(citation_manager.citations)}\n")
        
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
    
    # Print banner
    print_banner()
    
    # Get project root
    project_root = Path(__file__).parent.absolute()
    
    # Check environment
    check_environment()
    
    # Load academic configuration if in academic mode
    academic_config = None
    if args.academic:
        # Load from environment first, then override with args
        academic_config = AcademicConfig.from_env()
        if args.citation_style or args.output_format or args.discipline or args.word_count or args.export_bib:
            academic_config = AcademicConfig.from_args(args)
        
        display_academic_config(academic_config)
    
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
            success = run_research(question_filename, project_root)
    else:
        # Normal mode
        success = run_research(question_filename, project_root)
    
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
            else:
                # Standard mode - basic report already saved
                print(f"{Colors.OKGREEN}✅ Research completed successfully!{Colors.ENDC}\n")
    
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
