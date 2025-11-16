import json
import json5
import os
from typing import Dict, Iterator, List, Literal, Optional, Tuple, Union
from qwen_agent.llm.schema import Message
from qwen_agent.utils.utils import build_text_completion_prompt
from openai import OpenAI, APIError, APIConnectionError, APITimeoutError
from transformers import AutoTokenizer 
from datetime import datetime
from qwen_agent.agents.fncall_agent import FnCallAgent
from qwen_agent.llm import BaseChatModel
from qwen_agent.llm.schema import ASSISTANT, DEFAULT_SYSTEM_MESSAGE, Message
from qwen_agent.settings import MAX_LLM_CALL_PER_RUN
from qwen_agent.tools import BaseTool
from qwen_agent.utils.utils import format_as_text_message, merge_generate_cfgs
from prompt import *
import time
import asyncio

from tool_file import *
from tool_scholar import *
from tool_python import *
from tool_search import *
from tool_visit import *

# Import academic prompts for academic mode
try:
    import sys
    from pathlib import Path
    # Add parent directories to path to import from gazzali package
    gazzali_root = Path(__file__).parent.parent.parent.parent
    if str(gazzali_root) not in sys.path:
        sys.path.insert(0, str(gazzali_root))
    
    from src.gazzali.prompts.academic_prompts import get_academic_research_prompt
    from src.gazzali.academic_config import AcademicConfig
    ACADEMIC_PROMPTS_AVAILABLE = True
except ImportError:
    ACADEMIC_PROMPTS_AVAILABLE = False
    print("Warning: Academic prompts not available. Running in standard mode.")

OBS_START = '<tool_response>'
OBS_END = '\n</tool_response>'

MAX_LLM_CALL_PER_RUN = int(os.getenv('MAX_LLM_CALL_PER_RUN', 100))
OPENROUTER_MAX_RETRIES = int(os.getenv("OPENROUTER_MAX_RETRIES", "3"))
OPENROUTER_TIMEOUT = float(os.getenv("OPENROUTER_TIMEOUT", "180"))
OPENROUTER_RETRY_BASE = float(os.getenv("OPENROUTER_RETRY_BASE", "0.5"))
OPENROUTER_RETRY_MAX_SLEEP = float(os.getenv("OPENROUTER_RETRY_MAX_SLEEP", "6"))

TOOL_CLASS = [
    FileParser(),
    Scholar(),
    Visit(),
    Search(),
    PythonInterpreter(),
]
TOOL_MAP = {tool.name: tool for tool in TOOL_CLASS}

import random
import datetime
from collections import Counter


def today_date():
    return datetime.date.today().strftime("%Y-%m-%d")

class MultiTurnReactAgent(FnCallAgent):
    def __init__(self,
                 function_list: Optional[List[Union[str, Dict, BaseTool]]] = None,
                 llm: Optional[Union[Dict, BaseChatModel]] = None,
                 **kwargs):

        self.llm_generate_cfg = llm["generate_cfg"]
        self.llm_local_path = llm.get("model", "openrouter-api")  # Default to openrouter-api if not specified

    def sanity_check_output(self, content):
        return "<think>" in content and "</think>" in content
    
    def call_server(self, msgs, planning_port, max_tries=None):
        if max_tries is None:
            max_tries = OPENROUTER_MAX_RETRIES
        
        # OpenRouter Configuration - Read API key from environment
        openai_api_key = os.getenv("OPENROUTER_API_KEY", "EMPTY")
        
        # Check if using OpenRouter or local vLLM
        if openai_api_key != "EMPTY" and openai_api_key.startswith("sk-or-"):
            # OpenRouter configuration
            openai_api_base = "https://openrouter.ai/api/v1"
            print("--- Using OpenRouter API ---")
        else:
            # Local vLLM configuration
            openai_api_base = f"http://127.0.0.1:{planning_port}/v1"
            print(f"--- Using local vLLM server on port {planning_port} ---")

        client = OpenAI(
            api_key=openai_api_key,
            base_url=openai_api_base,
            timeout=OPENROUTER_TIMEOUT,
        )

        base_sleep_time = OPENROUTER_RETRY_BASE
        for attempt in range(max_tries):
            try:
                print(f"--- Attempting to call the service, try {attempt + 1}/{max_tries} ---")
                
                # Determine model name based on API type
                if openai_api_key != "EMPTY" and openai_api_key.startswith("sk-or-"):
                    # OpenRouter model name - using Tongyi DeepResearch 30B
                    model_name = "alibaba/tongyi-deepresearch-30b-a3b"
                    
                    # OpenRouter-specific headers for better ranking and tracking
                    extra_headers = {
                        "HTTP-Referer": "https://github.com/Alibaba-NLP/DeepResearch",
                        "X-Title": "Tongyi DeepResearch CLI"
                    }
                    
                    chat_response = client.chat.completions.create(
                        model=model_name,
                        messages=msgs,
                        stop=["\n<tool_response>", "<tool_response>"],
                        temperature=self.llm_generate_cfg.get('temperature', 0.6),
                        top_p=self.llm_generate_cfg.get('top_p', 0.95),
                        logprobs=True,
                        max_tokens=10000,
                        presence_penalty=self.llm_generate_cfg.get('presence_penalty', 1.1),
                        extra_headers=extra_headers,
                        extra_body={}
                    )
                else:
                    # Local vLLM uses self.model
                    model_name = self.model
                    
                    chat_response = client.chat.completions.create(
                        model=model_name,
                        messages=msgs,
                        stop=["\n<tool_response>", "<tool_response>"],
                        temperature=self.llm_generate_cfg.get('temperature', 0.6),
                        top_p=self.llm_generate_cfg.get('top_p', 0.95),
                        logprobs=True,
                        max_tokens=10000,
                        presence_penalty=self.llm_generate_cfg.get('presence_penalty', 1.1)
                    )
                
                # Validate response
                if not chat_response or not chat_response.choices:
                    print(f"Warning: Attempt {attempt + 1} received empty or invalid response")
                    raise ValueError("Empty response from API")
                
                content = chat_response.choices[0].message.content

                # OpenRouter reasoning support
                if openai_api_key != "EMPTY" and openai_api_key.startswith("sk-or-"):
                    try:
                        if hasattr(chat_response.choices[0].message, 'reasoning') and chat_response.choices[0].message.reasoning:
                            reasoning_content = "<think>\n" + chat_response.choices[0].message.reasoning.strip() + "\n</think>"
                            content = reasoning_content + content
                    except AttributeError:
                        pass  # No reasoning available, use content as is                
                
                if content and content.strip():
                    print("--- Service call successful, received a valid response ---")
                    return content.strip()
                else:
                    print(f"Warning: Attempt {attempt + 1} received an empty response.")

            except (APIError, APIConnectionError, APITimeoutError) as e:
                print(f"Error: Attempt {attempt + 1} failed with an API or network error: {e}")
            except Exception as e:
                print(f"Error: Attempt {attempt + 1} failed with an unexpected error: {e}")

            if attempt < max_tries - 1:
                sleep_time = base_sleep_time * (2 ** attempt) + random.uniform(0, 1)
                sleep_time = min(sleep_time, OPENROUTER_RETRY_MAX_SLEEP)
                
                print(f"Retrying in {sleep_time:.2f} seconds...")
                time.sleep(sleep_time)
            else:
                print("Error: All retry attempts have been exhausted. The call has failed.")
        
        return f"vllm server error!!!"

    def count_tokens(self, messages):
        # For OpenRouter, use approximate token counting (no local tokenizer needed)
        # Rough estimation: ~4 characters per token for English, ~2-3 for code
        openai_api_key = os.getenv("OPENROUTER_API_KEY", "EMPTY")
        
        if openai_api_key != "EMPTY" and openai_api_key.startswith("sk-or-"):
            # OpenRouter mode: estimate tokens without loading tokenizer
            total_chars = sum(len(str(msg)) for msg in messages)
            # Rough approximation: 1 token ≈ 4 characters
            token_count = total_chars // 4
            return token_count
        else:
            # Local model mode: use actual tokenizer
            tokenizer = AutoTokenizer.from_pretrained(self.llm_local_path) 
            full_prompt = tokenizer.apply_chat_template(messages, tokenize=False)
            tokens = tokenizer(full_prompt, return_tensors="pt")
            token_count = len(tokens["input_ids"][0])
            return token_count

    def _run(self, data: str, model: str, **kwargs) -> List[List[Message]]:
        self.model=model
        try:
            question = data['item']['question']
        except: 
            raw_msg = data['item']['messages'][1]["content"] 
            question = raw_msg.split("User:")[1].strip() if "User:" in raw_msg else raw_msg 

        start_time = time.time()
        planning_port = data['planning_port']
        answer = data['item']['answer']
        self.user_prompt = question
        
        # Academic mode detection and prompt selection
        # Check environment variables set by gazzali.py
        academic_mode = os.getenv("GAZZALI_ACADEMIC_MODE", "false").lower() == "true"
        
        if academic_mode and ACADEMIC_PROMPTS_AVAILABLE:
            print("🎓 Academic Mode: Loading enhanced academic research prompts")
            
            # Get discipline and output format from environment
            discipline = os.getenv("GAZZALI_DISCIPLINE", "general")
            output_format = os.getenv("GAZZALI_OUTPUT_FORMAT", "paper")
            
            # Generate academic prompt with discipline-specific modifiers
            system_prompt = get_academic_research_prompt(
                discipline=discipline,
                output_format=output_format
            )
            
            print(f"   • Discipline: {discipline.upper()}")
            print(f"   • Output Format: {output_format.capitalize()}")
            print(f"   • Scholar-First Strategy: Enabled")
        else:
            # Use standard prompt
            system_prompt = SYSTEM_PROMPT
            cur_date = today_date()
            system_prompt = system_prompt + str(cur_date)
        
        messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": question}]
        num_llm_calls_available = min(MAX_LLM_CALL_PER_RUN, 30)  # Limit to 30 rounds max to prevent infinite loops
        round = 0
        max_context_tokens = 70000  # tightened limit to avoid repeated truncations
        warning_ratio = 0.6

        while num_llm_calls_available > 0:
            # Check whether time is reached
            if time.time() - start_time > 150 * 60:  # 150 minutes in seconds
                prediction = 'No answer found after 2h30mins'
                termination = 'No answer found after 2h30mins'
                result = {
                    "question": question,
                    "answer": answer,
                    "messages": messages,
                    "prediction": prediction,
                    "termination": termination
                }
                return result
            round += 1
            num_llm_calls_available -= 1
            
            # Check token count before making API call
            current_tokens = self.count_tokens(messages)
            print(f"round: {round}, token count: {current_tokens}")
            
            # Aggressive context management to prevent overflow
            if current_tokens > max_context_tokens:
                print(f"⚠️  TOKEN LIMIT EXCEEDED ({current_tokens} > {max_context_tokens})")
                print(f"🔄 Aggressively truncating context...")
                
                # Keep only system prompt and last 2 exchanges (4 messages)
                if len(messages) > 5:
                    messages = [messages[0]] + messages[-4:]
                    new_token_count = self.count_tokens(messages)
                    print(f"✓ First truncation: {current_tokens} → {new_token_count} tokens")
                    
                    # If still too large, keep only system and last exchange
                    if new_token_count > max_context_tokens:
                        messages = [messages[0]] + messages[-2:]
                        final_token_count = self.count_tokens(messages)
                        print(f"✓ Second truncation: {new_token_count} → {final_token_count} tokens")
            
            # Early warning at 70% capacity
            elif current_tokens > int(max_context_tokens * warning_ratio):
                print(f"⚠️  Context approaching {int(warning_ratio*100)}% capacity ({current_tokens}/{max_context_tokens} tokens)")
            
            content = self.call_server(messages, planning_port)

            if isinstance(content, str) and content.strip() == "vllm server error!!!":
                failure_reason = "OpenRouter returned empty responses after all retries."
                print(f"❌ {failure_reason}")
                result = {
                    "question": question,
                    "answer": answer,
                    "messages": messages,
                    "prediction": "[Failed]",
                    "termination": "openrouter failure",
                    "error": failure_reason
                }
                return result
            
            # Detect repetitive content (hallucination loop)
            if len(content) > 100:
                # Check if same phrase repeats many times
                words = content.split()
                if len(words) > 50:
                    # Simple repetition detection: check if any 5-word phrase repeats >10 times
                    phrases = [' '.join(words[i:i+5]) for i in range(len(words)-4)]
                    phrase_counts = Counter(phrases)
                    
                    if phrase_counts:
                        most_common_phrase, count = phrase_counts.most_common(1)[0]
                        
                        if count > 10:
                            print(f"🛑 HALLUCINATION LOOP DETECTED!")
                            print(f"   Phrase '{most_common_phrase[:50]}...' repeated {count} times")
                            print(f"   Forcing answer generation...")
                            # Force the agent to provide final answer
                            messages.append({"role": "user", "content": "You are repeating yourself. Please provide your final answer now in the required format: <answer>your complete answer here</answer>"})
                            content = self.call_server(messages, planning_port)
            
            print(f'Round {round}: {content[:200]}...' if len(content) > 200 else f'Round {round}: {content}')
            
            if '<tool_response>' in content:
                pos = content.find('<tool_response>')
                content = content[:pos]
            messages.append({"role": "assistant", "content": content.strip()})
            if '<tool_call>' in content and '</tool_call>' in content:
                tool_call = content.split('<tool_call>')[1].split('</tool_call>')[0]
                try:
                    if "python" in tool_call.lower():
                        try:
                            code_raw=content.split('<tool_call>')[1].split('</tool_call>')[0].split('<code>')[1].split('</code>')[0].strip()
                            result = TOOL_MAP['PythonInterpreter'].call(code_raw)
                        except:
                            result = "[Python Interpreter Error]: Formatting error."

                    else:
                        tool_call = json5.loads(tool_call)
                        tool_name = tool_call.get('name', '')
                        tool_args = tool_call.get('arguments', {})
                        result = self.custom_call_tool(tool_name, tool_args)

                except:
                    result = 'Error: Tool call is not a valid JSON. Tool call must contain a valid "name" and "arguments" field.'
                result = "<tool_response>\n" + result + "\n</tool_response>"
                # print(result)
                messages.append({"role": "user", "content": result})
            if '<answer>' in content and '</answer>' in content:
                termination = 'answer'
                break
            if num_llm_calls_available <= 0 and '<answer>' not in content:
                messages[-1]['content'] = 'Sorry, the number of llm calls exceeds the limit.'

            # Token count already printed earlier, reuse it
            max_tokens = 110 * 1024
            token_count = self.count_tokens(messages)

            if token_count > max_tokens:
                print(f"Token quantity exceeds the limit: {token_count} > {max_tokens}")
                
                messages[-1]['content'] = "You have now reached the maximum context length you can handle. You should stop making tool calls and, based on all the information above, think again and provide what you consider the most likely answer in the following format:<think>your final thinking</think>\n<answer>your answer</answer>"
                content = self.call_server(messages, planning_port)
                messages.append({"role": "assistant", "content": content.strip()})
                if '<answer>' in content and '</answer>' in content:
                    prediction = messages[-1]['content'].split('<answer>')[1].split('</answer>')[0]
                    termination = 'generate an answer as token limit reached'
                else:
                    prediction = messages[-1]['content']
                    termination = 'format error: generate an answer as token limit reached'
                result = {
                    "question": question,
                    "answer": answer,
                    "messages": messages,
                    "prediction": prediction,
                    "termination": termination
                }
                return result

        if '<answer>' in messages[-1]['content']:
            prediction = messages[-1]['content'].split('<answer>')[1].split('</answer>')[0]
            termination = 'answer'
        else:
            prediction = 'No answer found.'
            termination = 'answer not found'
            if num_llm_calls_available == 0:
                termination = 'exceed available llm calls'
        result = {
            "question": question,
            "answer": answer,
            "messages": messages,
            "prediction": prediction,
            "termination": termination
        }
        return result

    def assess_source_quality(self, tool_name: str, result: str) -> Dict[str, Any]:
        """
        Assess the quality of sources returned by a tool.
        
        Scoring system (0-10):
        - Peer-reviewed journal/conference: 10
        - Academic institution/university: 8
        - Government/research organization: 7
        - Professional organization: 6
        - News from reputable source: 5
        - General web content: 3
        - Unknown/unverified: 2
        
        Args:
            tool_name: Name of the tool that generated the result
            result: The result string from the tool
        
        Returns:
            Dictionary with quality metrics:
                - average_score: Average quality score
                - peer_reviewed_count: Number of peer-reviewed sources
                - total_sources: Total number of sources
                - quality_level: 'high', 'medium', or 'low'
        """
        # Scholar tool results are always high quality (peer-reviewed)
        if tool_name == "google_scholar":
            # Count results (look for numbered items)
            import re
            result_count = len(re.findall(r'^\d+\.\s+\[', result, re.MULTILINE))
            
            return {
                'average_score': 10,
                'peer_reviewed_count': result_count,
                'total_sources': result_count,
                'quality_level': 'high',
                'tool': 'google_scholar'
            }
        
        # Visit tool - assess based on URL and content
        elif tool_name == "visit_page":
            score = 3  # Default for general web
            is_peer_reviewed = False
            
            # Check for academic indicators in result
            result_lower = result.lower()
            
            # Peer-reviewed indicators
            if any(indicator in result_lower for indicator in [
                'doi:', 'journal', 'conference', 'proceedings', 'ieee', 'acm',
                'springer', 'elsevier', 'nature', 'science', 'arxiv'
            ]):
                score = 10
                is_peer_reviewed = True
            
            # Academic institution indicators
            elif any(indicator in result_lower for indicator in [
                '.edu', 'university', 'college', 'research center', 'institute'
            ]):
                score = 8
            
            # Government/research organization
            elif any(indicator in result_lower for indicator in [
                '.gov', 'national', 'federal', 'nih', 'nsf', 'nasa'
            ]):
                score = 7
            
            # Professional organization
            elif any(indicator in result_lower for indicator in [
                'association', 'society', 'organization', '.org'
            ]):
                score = 6
            
            # News sources
            elif any(indicator in result_lower for indicator in [
                'news', 'times', 'post', 'journal', 'magazine'
            ]):
                score = 5
            
            return {
                'average_score': score,
                'peer_reviewed_count': 1 if is_peer_reviewed else 0,
                'total_sources': 1,
                'quality_level': 'high' if score >= 8 else 'medium' if score >= 5 else 'low',
                'tool': 'visit_page'
            }
        
        # Search tool - generally lower quality than Scholar
        elif tool_name == "search":
            # Estimate based on content
            result_lower = result.lower()
            
            # Count academic indicators
            academic_count = sum(1 for indicator in [
                'doi:', 'journal', 'university', '.edu', 'research', 'study'
            ] if indicator in result_lower)
            
            # Count results
            import re
            result_count = len(re.findall(r'^\d+\.\s+', result, re.MULTILINE))
            if result_count == 0:
                result_count = 1
            
            # Estimate peer-reviewed sources (conservative)
            peer_reviewed_estimate = min(academic_count, result_count // 2)
            
            # Average score based on academic indicators
            if academic_count >= 3:
                avg_score = 7
                quality = 'medium'
            elif academic_count >= 1:
                avg_score = 5
                quality = 'medium'
            else:
                avg_score = 3
                quality = 'low'
            
            return {
                'average_score': avg_score,
                'peer_reviewed_count': peer_reviewed_estimate,
                'total_sources': result_count,
                'quality_level': quality,
                'tool': 'search'
            }
        
        # Other tools - neutral quality
        else:
            return {
                'average_score': 5,
                'peer_reviewed_count': 0,
                'total_sources': 1,
                'quality_level': 'medium',
                'tool': tool_name
            }
    
    def filter_low_quality_sources(self, result: str, quality_assessment: Dict[str, Any]) -> str:
        """
        Filter or flag low-quality sources in academic mode.
        
        Args:
            result: The tool result string
            quality_assessment: Quality assessment from assess_source_quality
        
        Returns:
            Filtered or annotated result string
        """
        # Get quality threshold from environment
        quality_threshold = int(os.getenv("SOURCE_QUALITY_THRESHOLD", "7"))
        
        # If quality is below threshold, add warning
        if quality_assessment['average_score'] < quality_threshold:
            warning = (
                f"\n\n⚠️  SOURCE QUALITY WARNING: "
                f"Average quality score ({quality_assessment['average_score']}/10) "
                f"is below threshold ({quality_threshold}/10). "
                f"These sources may not meet academic standards. "
                f"Consider using google_scholar tool for peer-reviewed sources."
            )
            return result + warning
        
        return result
    
    def suggest_scholar_search(self, tool_name: str, tool_args: dict) -> Optional[str]:
        """
        Suggest using Scholar tool instead of general search in academic mode.
        
        Args:
            tool_name: Name of the tool being called
            tool_args: Arguments for the tool
        
        Returns:
            Suggestion message or None
        """
        # Check if in academic mode
        academic_mode = os.getenv("GAZZALI_ACADEMIC_MODE", "false").lower() == "true"
        scholar_priority = os.getenv("SCHOLAR_PRIORITY", "true").lower() == "true"
        
        if not (academic_mode and scholar_priority):
            return None
        
        # If calling search tool, suggest Scholar instead
        if tool_name == "search":
            query = tool_args.get("query", "")
            if query:
                suggestion = (
                    f"\n\n💡 ACADEMIC MODE SUGGESTION: "
                    f"Consider using google_scholar tool instead of search for academic sources. "
                    f"Scholar provides peer-reviewed papers with citation metadata. "
                    f"Example: google_scholar(query=\"{query}\")"
                )
                return suggestion
        
        return None
    
    def custom_call_tool(self, tool_name: str, tool_args: dict, **kwargs):
        """
        Execute tool call with academic mode enhancements.
        
        In academic mode:
        - Prioritizes Scholar tool over general search
        - Assesses source quality
        - Filters low-quality sources
        - Tracks quality metrics
        
        Args:
            tool_name: Name of the tool to call
            tool_args: Arguments for the tool
            **kwargs: Additional arguments
        
        Returns:
            Tool result string (potentially filtered/annotated)
        """
        if tool_name in TOOL_MAP:
            tool_args["params"] = tool_args
            
            # Execute tool call
            if "python" in tool_name.lower():
                result = TOOL_MAP['PythonInterpreter'].call(tool_args)
            elif tool_name == "parse_file":
                params = {"files": tool_args["files"]}
                
                raw_result = asyncio.run(TOOL_MAP[tool_name].call(params, file_root_path="./eval_data/file_corpus"))
                result = raw_result

                if not isinstance(raw_result, str):
                    result = str(raw_result)
            else:
                raw_result = TOOL_MAP[tool_name].call(tool_args, **kwargs)
                result = raw_result
            
            # Academic mode enhancements
            academic_mode = os.getenv("GAZZALI_ACADEMIC_MODE", "false").lower() == "true"
            
            if academic_mode:
                # Assess source quality
                quality_assessment = self.assess_source_quality(tool_name, result)
                
                # Log quality metrics
                print(f"📊 Source Quality Assessment:")
                print(f"   Tool: {tool_name}")
                print(f"   Quality Score: {quality_assessment['average_score']}/10 ({quality_assessment['quality_level']})")
                print(f"   Peer-Reviewed Sources: {quality_assessment['peer_reviewed_count']}/{quality_assessment['total_sources']}")
                
                # Filter low-quality sources
                result = self.filter_low_quality_sources(result, quality_assessment)
                
                # Add Scholar suggestion if appropriate
                suggestion = self.suggest_scholar_search(tool_name, tool_args)
                if suggestion:
                    result = result + suggestion
            
            return result

        else:
            return f"Error: Tool {tool_name} not found"
