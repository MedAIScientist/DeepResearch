#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gazzali Research interactive CLI."""

import sys
import os
import json
import subprocess
import argparse
from datetime import datetime
from pathlib import Path

from .config import get_env
from .report_generator import generate_comprehensive_report, save_comprehensive_report
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
║     Gazzali Research - Research CLI                           ║
║     Run fully automated deep research from the terminal       ║
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

def create_question_file(question, project_root):
    """Create temporary JSONL file with the question in the inference directory"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"cli_question_{timestamp}.jsonl"
    
    # Save to inference eval_data directory 
    inference_dir = os.path.join(project_root, "DeepResearch", "inference", "eval_data")
    os.makedirs(inference_dir, exist_ok=True)
    filepath = os.path.join(inference_dir, filename)
    
    question_data = {
        "question": question,
        "answer": ""
    }
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(question_data, f, ensure_ascii=False)
        f.write('\n')
    
    return filepath, filename

def run_research(dataset_filename, project_root):
    """Run the DeepResearch agent"""
    inference_dir = os.path.join(project_root, "DeepResearch", "inference")
    
    # Change to inference directory
    os.chdir(inference_dir)
    
    # Get configuration from environment or use defaults
    # For OpenRouter, model_path can be empty - run_multi_react.py will handle it
    model_path = get_env("MODEL_PATH", "") or ""
    output_path = get_env("OUTPUT_PATH")
    if not output_path:
        output_path = os.path.join(project_root, "outputs")

    temperature = float(get_env("TEMPERATURE", "0.85"))
    presence_penalty = float(get_env("PRESENCE_PENALTY", "1.1"))
    max_workers = int(get_env("MAX_WORKERS", "1"))  # Use 1 for CLI to avoid complexity
    rollout_count = int(get_env("ROLLOUT_COUNT", "1"))  # Use 1 for CLI
    
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
        result = subprocess.run(cmd, check=True, capture_output=False, text=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n{Colors.FAIL}❌ Research process failed: {e}{Colors.ENDC}")
        return False

def find_latest_output(output_dir):
    """Find the latest output file"""
    if not os.path.exists(output_dir):
        return None
    
    files = []
    for root, dirs, filenames in os.walk(output_dir):
        for filename in filenames:
            if filename.endswith('.jsonl'):
                filepath = os.path.join(root, filename)
                # Only include iter*.jsonl files (actual results)
                if 'iter' in filename:
                    files.append((filepath, os.path.getmtime(filepath)))
    
    if not files:
        return None
    
    # Sort by modification time, newest first
    files.sort(key=lambda x: x[1], reverse=True)
    return files[0][0]

def save_markdown_report(data, output_dir):
    """Save the result as a Markdown report"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_filename = f"report_{timestamp}.md"
    report_path = os.path.join(output_dir, "reports")
    
    # Create reports directory
    os.makedirs(report_path, exist_ok=True)
    
    report_file = os.path.join(report_path, report_filename)
    
    try:
        with open(report_file, 'w', encoding='utf-8') as f:
            # Header
            f.write("# Gazzali Research Research Report\n\n")
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
            f.write("- **Research model:** Alibaba Tongyi DeepResearch 30B (via OpenRouter)\n")
            f.write(f"- **Generated at:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            if 'rollout_idx' in data:
                f.write(f"- **Rollout:** {data['rollout_idx']}\n")
            f.write("\n")
            
        return report_file
    except Exception as e:
        print(f"{Colors.WARNING}⚠️  Rapor kaydedilemedi: {e}{Colors.ENDC}")
        return None

def display_result(output_file):
    """Display the research result"""
    if not output_file or not os.path.exists(output_file):
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
                    result_data = data  # Save for MD report
                    
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
        print(f"{Colors.WARNING}⚠️  Unable to read results, please inspect the file manually: {e}{Colors.ENDC}")
    
    return result_data

def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="Gazzali Research - Deep Research CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode
  python -m gazzali.ask

  # Ask a single question directly
  python -m gazzali.ask "What are the major AI safety milestones in 2024?"

  # Run chunked research for large questions
  python -m gazzali.ask --chunked "Map the global AI regulation landscape"
        """
    )

    parser.add_argument('question', nargs='?', help='Research question (optional in interactive mode)')
    parser.add_argument('--no-keep', action='store_true', help='Keep temporary dataset files for debugging')
    parser.add_argument('--output-dir', help='Custom output directory (defaults to <project>/outputs)')
    parser.add_argument('--chunked', action='store_true', help='Enable chunked research mode for very large topics')
    
    args = parser.parse_args()
    
    # Print banner
    print_banner()
    
    # Get project root
    project_root = Path(__file__).parent.absolute()
    
    # Check environment
    check_environment()
    
    # Get question
    if args.question:
        question = args.question
        print(f"{Colors.BOLD}❓ Question:{Colors.ENDC} {question}\n")
    else:
        question = get_question_interactive()
    
    # Create question file
    question_filepath, question_filename = create_question_file(question, project_root)
    print(f"{Colors.OKGREEN}✓{Colors.ENDC} Created dataset file: {question_filepath}\n")
    
    # Determine output directory
    if args.output_dir:
        output_dir = args.output_dir
    else:
        output_dir = os.path.join(project_root, "outputs")
    
    os.makedirs(output_dir, exist_ok=True)
    
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
            report_path = os.path.join(output_dir, "reports", report_filename)
            os.makedirs(os.path.join(output_dir, "reports"), exist_ok=True)
            
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
        
        # Save basic Markdown report (English research results)
        if result_data and 'error' not in result_data:
            report_file = save_markdown_report(result_data, output_dir)
            if report_file:
                print(f"{Colors.OKGREEN}✓{Colors.ENDC} Saved primary research report: {report_file}\n")
            
            # Generate comprehensive report using the configured synthesis model
            openrouter_key = get_env("OPENROUTER_API_KEY")
            if openrouter_key and openrouter_key.startswith("sk-or-"):
                print(f"\n{Colors.OKCYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.ENDC}")
                print(f"{Colors.BOLD}📊 Generating comprehensive synthesis report...{Colors.ENDC}")
                print(f"{Colors.OKCYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.ENDC}\n")
                
                try:
                    # Extract research results
                    research_results = result_data.get('prediction', result_data.get('answer', ''))
                    original_question = result_data.get('question', question)
                    
                    # Default: x-ai/grok-4-fast (override with REPORT_MODEL env var)
                    # Alternative models: "anthropic/claude-3.5-sonnet", "openai/gpt-4o", "moonshotai/kimi-k2-0905"
                    report_model = get_env("REPORT_MODEL", "x-ai/grok-4-fast")
                    comprehensive_report = generate_comprehensive_report(
                        question=original_question,
                        research_results=research_results,
                        api_key=openrouter_key,
                        model=report_model
                    )
                    
                    # Save comprehensive report
                    comprehensive_file = save_comprehensive_report(
                        report=comprehensive_report,
                        output_dir=output_dir,
                        question=original_question
                    )
                    
                    print(f"\n{Colors.OKGREEN}✅ Comprehensive report generated!{Colors.ENDC}")
                    print(f"{Colors.BOLD}📁 Comprehensive report:{Colors.ENDC} {comprehensive_file}\n")
                    
                except Exception as e:
                    print(f"{Colors.WARNING}⚠️  Comprehensive report generation failed: {e}{Colors.ENDC}\n")
    
    # Cleanup temp file unless --no-keep
    if not args.no_keep:
        try:
            os.remove(question_filepath)
            print(f"{Colors.OKGREEN}✓{Colors.ENDC} Cleaned temporary dataset\n")
        except:
            pass
    else:
        print(f"{Colors.WARNING}ℹ️  Temporary dataset retained: {question_filepath}{Colors.ENDC}\n")

    print(f"{Colors.BOLD}📊 Explore all outputs with:{Colors.ENDC} ls -lth {output_dir}/\n")

if __name__ == "__main__":
    main()

