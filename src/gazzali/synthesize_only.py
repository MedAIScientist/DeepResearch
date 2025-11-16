#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Synthesize Only - Use existing chunk results to create comprehensive report
For when you already have chunk results and just need synthesis
"""

import os
import sys
import json
import glob
from datetime import datetime
from pathlib import Path
from openai import OpenAI

from .config import get_env

def find_latest_chunks(output_dir: str) -> list:
    """Find the most recent set of chunk results"""
    chunk_dirs = glob.glob(os.path.join(output_dir, "openrouter-api", "eval_data", "chunk_*"))
    
    if not chunk_dirs:
        print("❌ No chunk results found!")
        return []
    
    # Sort by modification time to find most recent
    chunk_dirs.sort(key=os.path.getmtime, reverse=True)
    
    # Extract date from most recent chunk
    if chunk_dirs:
        latest_dirname = os.path.basename(chunk_dirs[0])
        # chunk_7_20251107_030918.jsonl → get date part (20251107)
        parts = latest_dirname.split('_')
        if len(parts) >= 3:
            latest_date = parts[2]  # 20251107
            
            # Find all chunks from the same date
            latest_chunks = []
            for chunk_dir in chunk_dirs:
                dirname = os.path.basename(chunk_dir)
                if latest_date in dirname:
                    iter_file = os.path.join(chunk_dir, "iter1.jsonl")
                    if os.path.exists(iter_file):
                        latest_chunks.append(iter_file)
            
            # Sort by chunk number
            latest_chunks.sort(key=lambda x: int(os.path.basename(os.path.dirname(x)).split('_')[1]))
            
            return latest_chunks
    
    return []

def load_chunk_results(chunk_files: list) -> list:
    """Load all chunk results"""
    results = []
    
    for i, chunk_file in enumerate(chunk_files, 1):
        try:
            with open(chunk_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        data = json.loads(line)
                        if 'question' in data and 'prediction' in data:
                            results.append({
                                'question': data['question'],
                                'answer': data['prediction']
                            })
                            print(f"✓ Loaded chunk {i}: {data['question'][:70]}...")
                            break
        except Exception as e:
            print(f"⚠️  Chunk {i} could not be read: {e}")
    
    return results

def synthesize_chunks(original_question: str, chunked_results: list, api_key: str) -> str:
    """Generate a comprehensive report from chunked research results."""

    combined_results = "\n\n".join([
        f"### Chunk {i}\n\n**Question:** {result['question']}\n\n{result['answer']}"
        for i, result in enumerate(chunked_results, 1)
    ])

    synthesis_prompt = f"""You are a senior research analyst tasked with combining {len(chunked_results)} research packets into a single, end-to-end report.

# Original Question
{original_question}

# Research Packets
{combined_results}

## Deliverable Requirements
- Respond in **English** only with 8,000+ words of substantive analysis
- Provide an executive summary, background, themed findings, deep analysis, implications, forward outlook, recommendations, conclusion, and references
- Expand beyond the notes: add causal reasoning, quantitative context, stakeholder perspectives, and comparative viewpoints
- Use Markdown headings, tables, bullet lists, callouts, and inline citations (Markdown links) for evidence
- Avoid redundancy while ensuring every major insight is covered

Deliver the complete report now."""

    client = OpenAI(
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1",
        timeout=1800.0
    )

    input_tokens = len(combined_results) // 4
    available_tokens = 250000 - input_tokens
    report_max_tokens = int(get_env("REPORT_MAX_TOKENS", "32000"))
    max_output_tokens = min(available_tokens, report_max_tokens)

    report_model = get_env("REPORT_MODEL", "x-ai/grok-4-fast")

    print("\n🔄 Launching synthesis run...")
    print(f"📊 Input: ~{input_tokens:,} tokens")
    print(f"📊 Max output: {max_output_tokens:,} tokens (~{max_output_tokens * 4:,} characters)")
    print(f"📝 Model: {report_model}\n")

    try:
        response = client.chat.completions.create(
            model=report_model,
            messages=[
                {
                    "role": "system",
                    "content": "You create exhaustive English-language research reports that integrate multiple evidence packets into a coherent narrative suitable for executives."
                },
                {
                    "role": "user",
                    "content": synthesis_prompt
                }
            ],
            temperature=0.7,
            max_tokens=max_output_tokens,
            timeout=1800.0,
            extra_headers={
                "HTTP-Referer": "https://github.com/Alibaba-NLP/DeepResearch",
                "X-Title": "DeepResearch Chunked Synthesis"
            },
            extra_body={}
        )

        report = response.choices[0].message.content
        print(f"\n✅ Synthesis completed: {len(report):,} characters (~{len(report.split()):,} words)")

        metadata = f"""---
title: Chunked Research Synthesis
date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
model: {report_model}
chunks: {len(chunked_results)}
original_question: {original_question}
---

"""

        return metadata + report

    except Exception as e:
        print(f"❌ Synthesis failed: {e}")
        return f"# Synthesis Error\n\n{str(e)}\n\n{combined_results}"

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Gazzali Research - Synthesis Utility')
    parser.add_argument('question', nargs='?', help='Original research question (optional; inferred from chunks if omitted)')
    parser.add_argument('--output-dir', help='Custom output directory (defaults to <project>/outputs)')
    
    args = parser.parse_args()
    
    print("╔════════════════════════════════════════════════════════════════╗")
    print("║     Chunked Research Synthesis - Offline Combiner             ║")
    print("╚════════════════════════════════════════════════════════════════╝\n")
    
    # Get project root
    project_root = Path(__file__).parent.absolute()
    
    # Determine output directory
    if args.output_dir:
        output_dir = args.output_dir
    else:
        output_dir = os.path.join(project_root, "outputs")
    
    # Find latest chunks
    print("🔍 Searching for the most recent chunk results...\n")
    chunk_files = find_latest_chunks(output_dir)
    
    if not chunk_files:
        print("❌ No chunk outputs detected!")
        print("Run chunked research first: ./scripts/ask.sh --chunked \"Your question\"")
        sys.exit(1)
    
    print(f"✓ Found {len(chunk_files)} chunk outputs\n")
    
    # Load results
    print("📂 Loading chunk outputs...\n")
    results = load_chunk_results(chunk_files)
    
    if not results:
        print("❌ Unable to parse chunk results!")
        sys.exit(1)
    
    print(f"\n✓ Successfully loaded {len(results)} chunks\n")
    
    # Get original question
    if args.question:
        original_question = args.question
    elif results and results[0]['question']:
        # Try to infer from first chunk
        original_question = "Comprehensive research synthesis"
    else:
        original_question = input("Enter the original research question: ")
    
    # Get API key
    api_key = get_env("OPENROUTER_API_KEY")
    if not api_key:
        print("❌ OPENROUTER_API_KEY is not set!")
        sys.exit(1)
    
    # Synthesize
    report = synthesize_chunks(original_question, results, api_key)
    
    # Save report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_q = "".join(c if c.isalnum() or c in (' ', '-', '_') else '' for c in original_question)[:50]
    report_filename = f"synthesis_only_{timestamp}_{safe_q}.md"
    report_path = os.path.join(output_dir, "reports", report_filename)
    os.makedirs(os.path.join(output_dir, "reports"), exist_ok=True)
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n{'='*70}")
    print("✅ Synthesized report saved!")
    print(f"📁 File: {report_path}")
    print(f"📊 Size: {len(report):,} characters")
    print(f"{'='*70}\n")
    
    # Display preview
    print("📝 Report preview:\n")
    print(report[:1500] + "...\n")

if __name__ == "__main__":
    main()

