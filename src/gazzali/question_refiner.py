"""
Research Question Refiner Module

This module helps users refine broad research topics into specific, answerable
research questions following the FINER criteria (Feasible, Interesting, Novel,
Ethical, Relevant).

Requirements addressed:
- 6.1: Analyze topics and propose 3-5 specific research questions following FINER criteria
- 6.2: Identify research question type (descriptive, comparative, relationship-based, causal)
- 6.3: Assess research question scope and suggest narrowing or broadening
- 6.4: Identify key variables, populations, and contexts in research questions
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Optional

import requests


@dataclass
class QualityAssessment:
    """
    Assessment of research question quality using FINER criteria.
    
    Attributes:
        is_specific: Whether the question is specific and focused
        is_answerable: Whether the question can be answered with available methods
        is_novel: Whether the question addresses a gap in knowledge
        scope: Assessment of question scope ('too_broad', 'appropriate', 'too_narrow')
        suggestions: List of suggestions for improvement
        finer_scores: Dictionary of FINER criteria scores (0-10 scale)
    """
    is_specific: bool
    is_answerable: bool
    is_novel: bool
    scope: str  # 'too_broad', 'appropriate', 'too_narrow'
    suggestions: list[str] = field(default_factory=list)
    finer_scores: dict[str, int] = field(default_factory=dict)
    
    def overall_quality(self) -> str:
        """
        Calculate overall quality rating.
        
        Returns:
            Quality rating: 'excellent', 'good', 'needs_improvement', or 'poor'
        """
        if not self.finer_scores:
            return 'needs_improvement'
        
        avg_score = sum(self.finer_scores.values()) / len(self.finer_scores)
        
        if avg_score >= 8:
            return 'excellent'
        elif avg_score >= 6:
            return 'good'
        elif avg_score >= 4:
            return 'needs_improvement'
        else:
            return 'poor'


@dataclass
class RefinedQuestion:
    """
    Refined research question with metadata and analysis.
    
    Attributes:
        original_topic: The original broad topic provided by user
        refined_questions: List of 3-5 specific research questions
        question_type: Type of research question (descriptive, comparative, etc.)
        key_variables: List of key variables identified in the question
        key_populations: List of target populations or subjects
        contexts: List of relevant contexts or settings
        scope_assessment: Assessment of question scope
        feasibility_notes: Notes on feasibility and practical considerations
        quality_assessment: Quality assessment using FINER criteria
    """
    original_topic: str
    refined_questions: list[str]
    question_type: str  # 'descriptive', 'comparative', 'relationship', 'causal', 'mixed'
    key_variables: list[str] = field(default_factory=list)
    key_populations: list[str] = field(default_factory=list)
    contexts: list[str] = field(default_factory=list)
    scope_assessment: str = ""
    feasibility_notes: str = ""
    quality_assessment: Optional[QualityAssessment] = None
    
    def get_best_question(self) -> str:
        """
        Get the highest quality refined question.
        
        Returns:
            The first refined question (typically the best one)
        """
        return self.refined_questions[0] if self.refined_questions else self.original_topic


class QuestionRefiner:
    """
    Refines broad research topics into specific, answerable research questions.
    
    This class uses an LLM to analyze broad topics and generate focused research
    questions that follow academic standards and the FINER criteria.
    """
    
    # Question type definitions
    QUESTION_TYPES = {
        'descriptive': 'Describes characteristics, prevalence, or patterns',
        'comparative': 'Compares two or more groups, interventions, or conditions',
        'relationship': 'Examines associations or correlations between variables',
        'causal': 'Investigates cause-and-effect relationships',
        'mixed': 'Combines multiple question types'
    }
    
    # FINER criteria definitions
    FINER_CRITERIA = {
        'feasible': 'Can be investigated with available resources, time, and methods',
        'interesting': 'Engages researchers and has potential impact',
        'novel': 'Addresses a gap in knowledge or provides new insights',
        'ethical': 'Can be conducted ethically without harm',
        'relevant': 'Has significance for theory, practice, or policy'
    }
    
    def __init__(self, api_key: str, model: str = "grok-beta", base_url: str = "https://api.x.ai/v1"):
        """
        Initialize the QuestionRefiner.
        
        Args:
            api_key: API key for the LLM service
            model: Model name to use for refinement
            base_url: Base URL for the API
        """
        self.api_key = api_key
        self.model = model
        self.base_url = base_url
    
    def refine_question(
        self,
        broad_topic: str,
        discipline: Optional[str] = None,
        context: Optional[str] = None
    ) -> RefinedQuestion:
        """
        Refine a broad topic into specific research questions.
        
        Args:
            broad_topic: The broad research topic or interest area
            discipline: Academic discipline (e.g., 'stem', 'social', 'humanities')
            context: Additional context about research goals or constraints
        
        Returns:
            RefinedQuestion object with refined questions and analysis
        
        Raises:
            ValueError: If the API request fails or returns invalid data
        """
        prompt = self._build_refinement_prompt(broad_topic, discipline, context)
        
        try:
            response = self._call_llm(prompt)
            return self._parse_refinement_response(response, broad_topic)
        except Exception as e:
            raise ValueError(f"Failed to refine question: {str(e)}")
    
    def assess_question_quality(
        self,
        question: str,
        discipline: Optional[str] = None
    ) -> QualityAssessment:
        """
        Assess the quality of a research question using FINER criteria.
        
        Args:
            question: The research question to assess
            discipline: Academic discipline for context
        
        Returns:
            QualityAssessment object with detailed evaluation
        
        Raises:
            ValueError: If the API request fails or returns invalid data
        """
        prompt = self._build_assessment_prompt(question, discipline)
        
        try:
            response = self._call_llm(prompt)
            return self._parse_assessment_response(response)
        except Exception as e:
            raise ValueError(f"Failed to assess question quality: {str(e)}")
    
    def _build_refinement_prompt(
        self,
        broad_topic: str,
        discipline: Optional[str],
        context: Optional[str]
    ) -> str:
        """Build the prompt for question refinement."""
        discipline_context = f"\n\nAcademic Discipline: {discipline}" if discipline else ""
        user_context = f"\n\nAdditional Context: {context}" if context else ""
        
        return f"""You are an expert academic research advisor. Your task is to refine a broad research topic into specific, answerable research questions following the FINER criteria (Feasible, Interesting, Novel, Ethical, Relevant).

Broad Research Topic: {broad_topic}{discipline_context}{user_context}

Please provide:
1. 3-5 specific, focused research questions derived from this topic
2. Classification of the primary question type (descriptive, comparative, relationship, causal, or mixed)
3. Key variables that should be investigated
4. Target populations or subjects
5. Relevant contexts or settings
6. Scope assessment (too_broad, appropriate, or too_narrow)
7. Feasibility notes and practical considerations
8. FINER criteria scores (0-10) for each criterion

Format your response as JSON with the following structure:
{{
    "refined_questions": ["question 1", "question 2", "question 3"],
    "question_type": "descriptive|comparative|relationship|causal|mixed",
    "key_variables": ["variable 1", "variable 2"],
    "key_populations": ["population 1", "population 2"],
    "contexts": ["context 1", "context 2"],
    "scope_assessment": "too_broad|appropriate|too_narrow",
    "feasibility_notes": "notes about feasibility",
    "finer_scores": {{
        "feasible": 8,
        "interesting": 7,
        "novel": 6,
        "ethical": 9,
        "relevant": 8
    }},
    "suggestions": ["suggestion 1", "suggestion 2"]
}}

Ensure questions are:
- Specific and focused (not too broad)
- Answerable with research methods
- Clear about what is being investigated
- Appropriate for the discipline
- Ethically sound"""
    
    def _build_assessment_prompt(
        self,
        question: str,
        discipline: Optional[str]
    ) -> str:
        """Build the prompt for question quality assessment."""
        discipline_context = f"\n\nAcademic Discipline: {discipline}" if discipline else ""
        
        return f"""You are an expert academic research advisor. Assess the quality of this research question using the FINER criteria (Feasible, Interesting, Novel, Ethical, Relevant).

Research Question: {question}{discipline_context}

Evaluate:
1. Is the question specific and focused?
2. Is it answerable with available research methods?
3. Does it address a novel aspect or gap in knowledge?
4. What is the scope (too_broad, appropriate, too_narrow)?
5. Score each FINER criterion (0-10 scale)
6. Provide specific suggestions for improvement

Format your response as JSON:
{{
    "is_specific": true|false,
    "is_answerable": true|false,
    "is_novel": true|false,
    "scope": "too_broad|appropriate|too_narrow",
    "finer_scores": {{
        "feasible": 8,
        "interesting": 7,
        "novel": 6,
        "ethical": 9,
        "relevant": 8
    }},
    "suggestions": ["suggestion 1", "suggestion 2"]
}}"""
    
    def _call_llm(self, prompt: str) -> str:
        """
        Call the LLM API with the given prompt.
        
        Args:
            prompt: The prompt to send to the LLM
        
        Returns:
            The LLM's response text
        
        Raises:
            ValueError: If the API request fails
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": "You are an expert academic research advisor specializing in research question formulation and quality assessment."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7,
            "max_tokens": 2000
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=60
            )
            response.raise_for_status()
            
            data = response.json()
            return data["choices"][0]["message"]["content"]
        
        except requests.exceptions.RequestException as e:
            raise ValueError(f"API request failed: {str(e)}")
        except (KeyError, IndexError) as e:
            raise ValueError(f"Invalid API response format: {str(e)}")
    
    def _parse_refinement_response(self, response: str, original_topic: str) -> RefinedQuestion:
        """
        Parse the LLM response into a RefinedQuestion object.
        
        Args:
            response: The LLM's JSON response
            original_topic: The original broad topic
        
        Returns:
            RefinedQuestion object
        
        Raises:
            ValueError: If the response cannot be parsed
        """
        try:
            # Extract JSON from response (handle markdown code blocks)
            json_str = response.strip()
            if json_str.startswith("```"):
                # Remove markdown code block markers
                lines = json_str.split("\n")
                json_str = "\n".join(lines[1:-1]) if len(lines) > 2 else json_str
            
            data = json.loads(json_str)
            
            # Create quality assessment
            quality = QualityAssessment(
                is_specific=data.get("scope", "appropriate") != "too_broad",
                is_answerable=True,  # Assumed if refined by expert system
                is_novel=data.get("finer_scores", {}).get("novel", 5) >= 5,
                scope=data.get("scope_assessment", "appropriate"),
                suggestions=data.get("suggestions", []),
                finer_scores=data.get("finer_scores", {})
            )
            
            return RefinedQuestion(
                original_topic=original_topic,
                refined_questions=data.get("refined_questions", []),
                question_type=data.get("question_type", "descriptive"),
                key_variables=data.get("key_variables", []),
                key_populations=data.get("key_populations", []),
                contexts=data.get("contexts", []),
                scope_assessment=data.get("scope_assessment", ""),
                feasibility_notes=data.get("feasibility_notes", ""),
                quality_assessment=quality
            )
        
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse JSON response: {str(e)}\nResponse: {response}")
        except Exception as e:
            raise ValueError(f"Failed to parse refinement response: {str(e)}")
    
    def _parse_assessment_response(self, response: str) -> QualityAssessment:
        """
        Parse the LLM response into a QualityAssessment object.
        
        Args:
            response: The LLM's JSON response
        
        Returns:
            QualityAssessment object
        
        Raises:
            ValueError: If the response cannot be parsed
        """
        try:
            # Extract JSON from response (handle markdown code blocks)
            json_str = response.strip()
            if json_str.startswith("```"):
                lines = json_str.split("\n")
                json_str = "\n".join(lines[1:-1]) if len(lines) > 2 else json_str
            
            data = json.loads(json_str)
            
            return QualityAssessment(
                is_specific=data.get("is_specific", False),
                is_answerable=data.get("is_answerable", False),
                is_novel=data.get("is_novel", False),
                scope=data.get("scope", "appropriate"),
                suggestions=data.get("suggestions", []),
                finer_scores=data.get("finer_scores", {})
            )
        
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse JSON response: {str(e)}\nResponse: {response}")
        except Exception as e:
            raise ValueError(f"Failed to parse assessment response: {str(e)}")
