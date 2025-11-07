#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Report Generator - Converts DeepResearch results into comprehensive reports
Uses a powerful LLM to synthesize information into detailed, well-structured reports
"""

import os
import json
from datetime import datetime
from typing import Optional

from openai import OpenAI

from .config import get_env

# Report generation prompt template
REPORT_GENERATION_PROMPT = """You are a senior research analyst. You will receive curated research findings in ENGLISH and must deliver an expanded, fully-structured report in **English**.

# Output Expectations

## 1. Format & Structure
- Produce polished **Markdown** with semantic headings (##, ###, ####)
- Include executive summary, background, thematic deep-dives, implications, recommendations, conclusion, and references
- Use tables, bullet lists, and callouts where they add clarity

## 2. Depth & Coverage
- Target **8,000+ words**; every major section should contain rich, multi-paragraph analysis
- Expand on each finding with context, mechanisms, stakeholders, risks, and opportunities
- Integrate quantitative evidence (statistics, figures, ranges) whenever available
- Provide comparisons across geographies, timelines, vendors, and research groups when relevant

## 3. Section Requirements
- **Executive Summary:** 400+ words summarizing key insights and takeaways
- **Context & Background:** Historical build-up, recent catalysts, terminology definitions
- **Key Findings:** One subsection per major theme with data, quotes, and references
- **Deep Analysis:** Systems-level reasoning, causal chains, scenario exploration, limitations
- **Implications:** Business, policy, technical, and societal impact projections
- **Forward Look:** Emerging trends, unanswered questions, research or product roadmap suggestions
- **Conclusion:** Synthesize lessons learned and action priorities
- **References:** Markdown list of all cited sources with descriptive labels and URLs

## 4. Style Guide
- Write in **professional, objective English**; avoid marketing tone
- Assume the reader is an executive with technical literacy but limited time
- Provide definitions for specialized jargon on first use
- Prefer complete sentences and paragraphs of 5–7 sentences

# Research Findings (Input)

{research_results}

# Original Question

{original_question}

---

# Task Checklist

1. Ingest and understand all findings
2. Reframe them into a coherent, story-driven narrative
3. Provide additional analysis, cross-references, and interpretive commentary
4. Deliver the final report in English only
5. Preserve factual accuracy; cite sources inline with Markdown links when possible
6. Hit the target length and structural requirements above

Now draft the full report."""

from typing import Optional


def generate_comprehensive_report(question: str, research_results: str, api_key: str, model: Optional[str] = None) -> str:
    """
    Generate a comprehensive report from research results using a powerful LLM
    
    Args:
        question: Original research question
        research_results: Results from DeepResearch
        api_key: OpenRouter API key
        model: Model to use for report generation
        
    Returns:
        str: Comprehensive report in Markdown format
    """
    
    model_name = model or get_env("REPORT_MODEL", "x-ai/grok-4-fast")

    context_limit = int(get_env("REPORT_CONTEXT_LIMIT", "2000000"))
    max_tokens_setting = int(get_env("REPORT_MAX_TOKENS", "800000"))

    client = OpenAI(
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1",
        timeout=1800.0  # 30 minutes for very long report generation
    )
    
    # Prepare the prompt
    prompt = REPORT_GENERATION_PROMPT.format(
        research_results=research_results,
        original_question=question
    )
    
    input_tokens = max(len(prompt) // 4, 1)
    available_tokens = max(context_limit - input_tokens, 1000)
    max_output_tokens = min(max_tokens_setting, available_tokens)

    print("🔄 Generating comprehensive synthesis report...")
    print(f"📝 Model: {model_name}")
    print("⏱️  Timeout: 30 minutes for large outputs")
    print(f"📊 Input tokens (approx): {input_tokens:,}")
    print(f"📊 Requested output tokens (max): {max_output_tokens:,}")

    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {
                    "role": "system",
                    "content": """You are a world-class research report author.

Critical directives:
- Always respond in **English** with polished, executive-ready prose
- Deliver long-form analysis that goes beyond summarizing bullet points
- Use Markdown headings, tables, and lists to maximize readability
- Embed citations inline using Markdown links when specific sources are referenced
- Maintain analytical neutrality; no hype, no speculation without clear caveats

Quality checklist:
1. Integrate every relevant finding from the notes
2. Enrich with additional reasoning, context, and future outlook
3. Ensure sections transition logically and avoid redundancy
4. Provide quantitative framing wherever possible
5. Highlight open questions, risks, and opportunities explicitly

Do not slip into other languages. The final deliverable must be entirely in English."""
                },
                {
                    "role": "user",
                    "content": prompt + "\n\n**Reminder: respond in English only.**"
                }
            ],
            temperature=0.7,
            max_tokens=max_output_tokens,
            timeout=1800.0,  # 30 minute timeout for extremely long comprehensive reports
            extra_headers={
                "HTTP-Referer": "https://github.com/Alibaba-NLP/DeepResearch",
                "X-Title": "DeepResearch Report Generator"
            },
            extra_body={}  # OpenRouter compatibility
        )
        
        # Extract content from response
        message = response.choices[0].message
        
        # Some models expose reasoning traces separately
        reasoning_text = ""
        if hasattr(message, 'reasoning') and message.reasoning:
            reasoning_text = message.reasoning
            print(f"💭 Reasoning steps detected: {len(reasoning_text)} characters")
        
        # Get the actual content
        report = message.content if message.content else ""
        
        # Validate report length
        if len(report) < 500:
            print(f"⚠️  Report content is unusually short ({len(report)} characters); merging with reasoning trace if available.")
            # If main content is too short, it might be in reasoning
            # or there was an error - return what we have with explanation
            if reasoning_text and len(reasoning_text) > len(report):
                report = f"""# Generated Content (model reasoning)

{reasoning_text}

---

# Model Output

{report if report else "(Empty)"}
"""
            print("⚠️  Warning: the model may not have produced the full response.")
        
        print(f"✓ Received report content: {len(report)} characters")
        
        # Add metadata header
        metadata_header = f"""---
title: Eye of Prometheus Comprehensive Report
date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
model: {model_name}
question: {question}
---

"""
        
        full_report = metadata_header + report
        
        print("✅ Comprehensive report assembled!")
        return full_report
        
    except Exception as e:
        print(f"❌ Report generation error: {e}")
        return f"# Error\n\nReport generation failed: {e}\n\n## Research Notes\n\n{research_results}"

def save_comprehensive_report(report: str, output_dir: str, question: str) -> str:
    """
    Save comprehensive report to file
    
    Args:
        report: Report content
        output_dir: Output directory
        question: Original question (for filename)
        
    Returns:
        str: Path to saved report
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create a safe filename from question
    safe_question = "".join(c if c.isalnum() or c in (' ', '-', '_') else '' for c in question)
    safe_question = safe_question[:50].strip()  # Limit length
    
    filename = f"comprehensive_report_{timestamp}_{safe_question}.md"
    
    report_path = os.path.join(output_dir, "reports")
    os.makedirs(report_path, exist_ok=True)
    
    filepath = os.path.join(report_path, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(report)
    
    return filepath

if __name__ == "__main__":
    # Test example
    print("Report Generator Module - Test")
    
    test_question = "Yapay zeka alanındaki son gelişmeler"
    test_results = "GPT-4 çıktı, Claude 3 geliştirildi, Gemini tanıtıldı..."
    
    api_key = get_env("OPENROUTER_API_KEY")
    if not api_key:
        print("❌ OPENROUTER_API_KEY tanımlı değil!")
    else:
        report = generate_comprehensive_report(test_question, test_results, api_key)
        print(report[:500] + "...")

