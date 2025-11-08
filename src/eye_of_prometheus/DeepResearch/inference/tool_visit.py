import json
import os
import signal
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Union
import requests
from qwen_agent.tools.base import BaseTool, register_tool
from prompt import EXTRACTOR_PROMPT 
from openai import OpenAI
import random
from urllib.parse import urlparse, unquote
import time 
from transformers import AutoTokenizer
import tiktoken

try:
    from eye_of_prometheus.config import get_env
except Exception:  # pragma: no cover
    def get_env(name: str, default=None):
        return os.getenv(name, default)

VISIT_SERVER_TIMEOUT = int(os.getenv("VISIT_SERVER_TIMEOUT", 200))
WEBCONTENT_MAXLENGTH = int(os.getenv("WEBCONTENT_MAXLENGTH", 150000))

JINA_API_KEY = get_env("JINA_API_KEY", "") or os.getenv("JINA_API_KEYS", "")


@staticmethod
def truncate_to_tokens(text: str, max_tokens: int = 95000) -> str:
    encoding = tiktoken.get_encoding("cl100k_base")
    
    tokens = encoding.encode(text)
    if len(tokens) <= max_tokens:
        return text
    
    truncated_tokens = tokens[:max_tokens]
    return encoding.decode(truncated_tokens)

OSS_JSON_FORMAT = """# Response Formats
## visit_content
{"properties":{"rational":{"type":"string","description":"Locate the **specific sections/data** directly related to the user's goal within the webpage content"},"evidence":{"type":"string","description":"Identify and extract the **most relevant information** from the content, never miss any important information, output the **full original context** of the content as far as possible, it can be more than three paragraphs.","summary":{"type":"string","description":"Organize into a concise paragraph with logical flow, prioritizing clarity and judge the contribution of the information to the goal."}}}}"""


@register_tool('visit', allow_overwrite=True)
class Visit(BaseTool):
    # The `description` tells the agent the functionality of this tool.
    name = 'visit'
    description = 'Visit webpage(s) and return the summary of the content.'
    # The `parameters` tell the agent what input parameters the tool has.
    parameters = {
        "type": "object",
        "properties": {
            "url": {
                "type": ["string", "array"],
                "items": {
                    "type": "string"
                    },
                "minItems": 1,
                "description": "The URL(s) of the webpage(s) to visit. Can be a single URL or an array of URLs."
        },
        "goal": {
                "type": "string",
                "description": "The goal of the visit for webpage(s)."
        }
        },
        "required": ["url", "goal"]
    }
    # The `call` method is the main function of the tool.
    def call(self, params: Union[str, dict], **kwargs) -> str:
        try:
            url = params["url"]
            goal = params["goal"]
        except:
            return "[Visit] Invalid request format: Input must be a JSON object containing 'url' and 'goal' fields"

        start_time = time.time()
        
        # Create log folder if it doesn't exist
        log_folder = "log"
        os.makedirs(log_folder, exist_ok=True)

        if isinstance(url, str):
            response = self.readpage_jina(url, goal)
        else:
            response = []
            assert isinstance(url, List)
            start_time = time.time()
            for u in url: 
                if time.time() - start_time > 900:
                    cur_response = "The useful information in {url} for user goal {goal} as follows: \n\n".format(url=url, goal=goal)
                    cur_response += "Evidence in page: \n" + "The provided webpage content could not be accessed. Please check the URL or file format." + "\n\n"
                    cur_response += "Summary: \n" + "The webpage content could not be processed, and therefore, no information is available." + "\n\n"
                else:
                    try:
                        cur_response = self.readpage_jina(u, goal)
                    except Exception as e:
                        cur_response = f"Error fetching {u}: {str(e)}"
                response.append(cur_response)
            response = "\n=======\n".join(response)
        
        print(f'Summary Length {len(response)}; Summary Content {response}')
        return response.strip()
        
    def call_server(self, msgs, max_retries=2):
        api_key = os.environ.get("API_KEY")
        url_llm = os.environ.get("API_BASE")
        model_name = os.environ.get("SUMMARY_MODEL_NAME", "")
        client = OpenAI(
            api_key=api_key,
            base_url=url_llm,
        )
        for attempt in range(max_retries):
            try:
                chat_response = client.chat.completions.create(
                    model=model_name,
                    messages=msgs,
                    temperature=0.7
                )
                content = chat_response.choices[0].message.content
                if content:
                    try:
                        json.loads(content)
                    except:
                        # extract json from string 
                        left = content.find('{')
                        right = content.rfind('}') 
                        if left != -1 and right != -1 and left <= right: 
                            content = content[left:right+1]
                    return content
            except Exception as e:
                # print(e)
                if attempt == (max_retries - 1):
                    return ""
                continue


    def jina_readpage(self, url: str) -> str:
        """
        Read webpage content using Jina Reader API.
        Correct usage: POST request with URL in body
        
        Args:
            url: The URL to read
            
        Returns:
            str: The webpage content or error message
        """
        # Validate and clean URL
        if not url or not isinstance(url, str):
            return "[visit] Invalid URL provided."
        
        url = url.strip()
        
        # Remove Jina prefix if agent mistakenly added it
        if url.startswith('https://r.jina.ai/'):
            url = url.replace('https://r.jina.ai/', '', 1)
        elif url.startswith('http://r.jina.ai/'):
            url = url.replace('http://r.jina.ai/', '', 1)
        
        # Check if URL is valid (must start with http:// or https://)
        if not url.startswith(('http://', 'https://')):
            # Try to fix common issues
            if url.startswith('www.'):
                url = f'https://{url}'
            elif url == 'https:' or url == 'http:':
                return "[visit] Invalid URL: incomplete protocol."
            else:
                url = f'https://{url}'
        
        # Additional validation
        if len(url) < 10 or '.' not in url:
            return f"[visit] Invalid URL format: {url}"
        
        max_retries = 3
        timeout = 50
        
        for attempt in range(max_retries):
            # Correct Jina Reader API headers
            headers = {
                "Authorization": f"Bearer {JINA_API_KEY}",
                "Content-Type": "application/json",
                "Accept": "application/json",
                "X-Return-Format": "markdown",  # Get markdown format
                "X-With-Links-Summary": "true",  # Include links
                "X-Timeout": "30"  # Set timeout
            }
            
            # Request body with URL
            payload = {
                "url": url
            }
            
            try:
                # POST request to Jina Reader API
                response = requests.post(
                    "https://r.jina.ai/",
                    headers=headers,
                    json=payload,
                    timeout=timeout
                )
                
                if response.status_code == 200:
                    try:
                        # Parse JSON response
                        data = response.json()
                        
                        # Extract content from response
                        if "data" in data and "content" in data["data"]:
                            webpage_content = data["data"]["content"]
                            
                            # Optionally add links if available
                            if "links" in data["data"] and data["data"]["links"]:
                                webpage_content += "\n\n## Referenced Links\n"
                                for link_text, link_url in list(data["data"]["links"].items())[:10]:
                                    webpage_content += f"- [{link_text}]({link_url})\n"
                            
                            return webpage_content
                        else:
                            return f"[visit] Unexpected response format: {data}"
                    except json.JSONDecodeError as e:
                        # Fallback to text response if JSON parsing fails
                        return response.text
                else:
                    error_msg = response.text
                    print(f"[visit] Jina API error (attempt {attempt + 1}/{max_retries}): Status {response.status_code}")
                    if attempt == max_retries - 1:
                        return f"[visit] Failed to read page after {max_retries} attempts. Status: {response.status_code}"
                    
            except requests.exceptions.Timeout:
                print(f"[visit] Timeout (attempt {attempt + 1}/{max_retries})")
                if attempt == max_retries - 1:
                    return "[visit] Failed to read page: Timeout"
            except Exception as e:
                print(f"[visit] Exception (attempt {attempt + 1}/{max_retries}): {str(e)}")
                if attempt == max_retries - 1:
                    return f"[visit] Failed to read page: {str(e)}"
            
            time.sleep(1)  # Wait before retry
                
        return "[visit] Failed to read page after all retries."

    def html_readpage_jina(self, url: str) -> str:
        max_attempts = 8
        for attempt in range(max_attempts):
            content = self.jina_readpage(url)
            service = "jina"     
            print(service)
            if content and not content.startswith("[visit] Failed to read page.") and content != "[visit] Empty content." and not content.startswith("[document_parser]"):
                return content
        return "[visit] Failed to read page."

    def readpage_jina(self, url: str, goal: str) -> str:
        """
        Read webpage content using Jina Reader API.
        Jina already returns LLM-friendly Markdown, so no additional summarization needed.
        
        Args:
            url: The URL to read
            goal: The goal/purpose of reading the page
            
        Returns:
            str: The webpage content in Markdown format or error message
        """
        # Get content from Jina Reader API (already in LLM-friendly Markdown format)
        content = self.html_readpage_jina(url)
        
        if content and not content.startswith("[visit] Failed to read page.") and content != "[visit] Empty content." and not content.startswith("[document_parser]"):
            # Jina Reader API already provides clean Markdown content
            # Truncate to reasonable size to avoid context window issues
            # Aim for ~15k tokens max per page (~60k characters)
            max_tokens = 15000  # Reduced from 95000 to prevent context overflow
            content = truncate_to_tokens(content, max_tokens=max_tokens)
            
            # Format the content with context
            formatted_content = f"""# Webpage Content from: {url}

**Research Goal:** {goal}

---

{content}
"""
            
            print(f"[visit] ✓ Successfully retrieved content from {url} ({len(content)} characters, ~{max_tokens} tokens max)")
            return formatted_content
        else:
            # If content retrieval failed, return error message
            error_message = f"""# Failed to retrieve content from: {url}

**Research Goal:** {goal}

---

**Error:** The webpage content could not be accessed. The URL may be invalid, the page may be protected, or there may be network issues.

Please try a different URL or source.
"""
            print(f"[visit] ✗ Failed to retrieve content from {url}")
            return error_message

    