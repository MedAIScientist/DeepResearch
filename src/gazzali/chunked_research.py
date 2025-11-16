#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Chunked Research Engine - Break large research questions into manageable chunks
Process each chunk separately, then synthesize all results into comprehensive report
"""

import os
import sys
import json
import subprocess
from datetime import datetime
from pathlib import Path
from openai import OpenAI

from .config import get_env

def decompose_question(question: str, api_key: str) -> list:
    """
    Use LLM to decompose a large research question into smaller sub-questions
    
    Args:
        question: Original large research question
        api_key: OpenRouter API key
        
    Returns:
        list: List of sub-questions to research separately
    """
    client = OpenAI(
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1"
    )
    
    decomposition_prompt = f"""You are a research planning assistant. Your task is to break down a large research question into smaller, focused sub-questions that can be researched independently.

**Original Question:**
{question}

**Your Task:**
Decompose this question into 3-7 focused sub-questions. Each sub-question should:
1. Be specific and self-contained
2. Cover different aspects of the main question
3. Be suitable for independent research
4. Together, cover the entire scope of the original question

**Output Format:**
Provide ONLY a JSON array of sub-questions, nothing else. Example:
["What is X?", "How does Y work?", "What are the applications of Z?"]

**Response (JSON array only):**"""

    print("🧩 Decomposing master question into focused sub-questions...")
    
    try:
        response = client.chat.completions.create(
            model="openai/gpt-4o-mini",  # Fast and cheap for decomposition
            messages=[
                {"role": "user", "content": decomposition_prompt}
            ],
            temperature=0.3,
            max_tokens=1000
        )
        
        content = response.choices[0].message.content.strip()
        
        # Clean up response (remove markdown code blocks if present)
        if content.startswith('```'):
            content = content.split('```')[1]
            if content.startswith('json'):
                content = content[4:]
            content = content.strip()
        
        # Parse JSON
        sub_questions = json.loads(content)
        
        print(f"✓ Generated {len(sub_questions)} sub-questions:")
        for i, q in enumerate(sub_questions, 1):
            print(f"  {i}. {q[:100]}...")
        
        return sub_questions
        
    except Exception as e:
        print(f"⚠️  Automatic decomposition failed: {e}")
        print("📝 Proceeding with the original question as a single chunk...")
        return [question]

def run_chunked_research(question: str, project_root: str) -> list:
    """
    Run research on each sub-question separately
    
    Args:
        question: Original question
        project_root: Project root directory
        
    Returns:
        list: List of research results for each chunk
    """
    # Decompose question
    api_key = get_env("OPENROUTER_API_KEY")
    if not api_key:
        print("⚠️  OPENROUTER_API_KEY missing; unable to run chunked mode")
        return [question]
    
    sub_questions = decompose_question(question, api_key)
    
    results = []
    
    for i, sub_q in enumerate(sub_questions, 1):
        print(f"\n{'='*70}")
        print(f"📊 CHUNK {i}/{len(sub_questions)}")
        print(f"{'='*70}")
        print(f"Question: {sub_q}\n")
        
        # Create question file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"chunk_{i}_{timestamp}.jsonl"
        inference_dir = os.path.join(project_root, "DeepResearch", "inference", "eval_data")
        filepath = os.path.join(inference_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump({"question": sub_q, "answer": ""}, f, ensure_ascii=False)
            f.write('\n')
        
        # Run research on this chunk
        os.chdir(os.path.join(project_root, "DeepResearch", "inference"))
        
        output_path = get_env("OUTPUT_PATH", os.path.join(project_root, "outputs"))
        
        cmd = [
            sys.executable,
            "run_multi_react.py",
            "--dataset", f"eval_data/{filename}",
            "--output", output_path,
            "--model", "",
            "--temperature", "0.85",
            "--presence_penalty", "1.1",
            "--max_workers", "1",
            "--roll_out_count", "1"
        ]
        
        try:
            subprocess.run(cmd, check=True, timeout=600)  # 10 min per chunk
            
            # Find result
            result_dir = os.path.join(output_path, "openrouter-api", f"eval_data/{filename}")
            result_file = os.path.join(result_dir, "iter1.jsonl")
            
            if os.path.exists(result_file):
                with open(result_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        if line.strip():
                            data = json.loads(line)
                            if 'prediction' in data:
                                results.append({
                                    'question': sub_q,
                                    'answer': data['prediction']
                                })
                                print(f"✓ Chunk {i} completed")
                                break
            
            # Cleanup
            os.remove(filepath)
            
        except Exception as e:
            print(f"❌ Chunk {i} failed: {e}")
            results.append({
                'question': sub_q,
                'answer': f"[Error: Research failed for this chunk]"
            })
    
    return results

def synthesize_results(original_question: str, chunked_results: list, api_key: str) -> str:
    """
    Synthesize all chunked results into one comprehensive report
    
    Args:
        original_question: Original research question
        chunked_results: List of results from each chunk
        api_key: OpenRouter API key
        
    Returns:
        str: Comprehensive synthesized report
    """
    # Combine all results
    combined_results = "\n\n".join([
        f"## Sub-Question {i}: {r['question']}\n\n{r['answer']}"
        for i, r in enumerate(chunked_results, 1)
    ])
    
    synthesis_prompt = f"""You are merging multiple research briefs into a single authoritative report for the following master question.

## Original Question
{original_question}

## Collected Research Briefs ({len(chunked_results)} chunks)
{combined_results}

## Deliverable Requirements
- Respond in **English** only
- Produce 8,000+ words with a clear executive summary, thematic chapters, cross-comparisons, implications, and recommendations
- Expand beyond the raw notes: add context, reasoning, quantitative framing, and forward-looking insights
- Use Markdown headings, tables, bullet lists, and callouts for clarity
- Reference specific sources inline using Markdown links when appropriate
- Eliminate redundant statements while preserving every critical fact

Craft the complete report now."""

    report_model = get_env("REPORT_MODEL", "x-ai/grok-4-fast")

    print("\n🔄 Consolidating all chunks into a unified report...")
    print(f"📝 Model: {report_model}")
    
    client = OpenAI(
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1",
        timeout=1800.0
    )
    
    # Calculate safe max_tokens based on input size and configuration
    input_tokens = len(combined_results) // 4  # Rough estimate
    available_tokens = 250000 - input_tokens  # Leave buffer for metadata
    report_max_tokens = int(get_env("REPORT_MAX_TOKENS", "32000"))
    max_output_tokens = min(available_tokens, report_max_tokens)
    
    print(f"📊 Input: ~{input_tokens} tokens")
    print(f"📊 Max output: {max_output_tokens} tokens")
    
    try:
        response = client.chat.completions.create(
            model=report_model,
            messages=[
                {
                    "role": "system",
                    "content": "You specialize in synthesizing multiple research dossiers into a single, exhaustive English-language report with executive polish." 
                },
                {
                    "role": "user",
                    "content": synthesis_prompt
                }
            ],
            temperature=0.7,
            max_tokens=max_output_tokens,  # Dynamic based on input size
            timeout=1800.0,
            extra_headers={
                "HTTP-Referer": "https://github.com/Alibaba-NLP/DeepResearch",
                "X-Title": "DeepResearch Chunked Synthesis"
            }
        )
        
        report = response.choices[0].message.content
        print(f"✓ Synthesis complete: {len(report)} characters")
        
        return report
        
    except Exception as e:
        print(f"❌ Synthesis error: {e}")
        return f"# Synthesis Error\n\n{combined_results}"

if __name__ == "__main__":
    print("Chunked Research Engine - Test Mode")

    test_question = "Summarize the major AI breakthroughs announced in 2024"
    project_root = Path(__file__).parent.absolute()

    api_key = get_env("OPENROUTER_API_KEY")
    if not api_key:
        print("❌ OPENROUTER_API_KEY is not set!")
        sys.exit(1)

    # Test decomposition
    sub_questions = decompose_question(test_question, api_key)
    print(f"\nTest: produced {len(sub_questions)} sub-questions")

