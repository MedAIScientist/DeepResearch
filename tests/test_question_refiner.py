#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit tests for Research Question Refiner Module

Tests the question refinement logic including:
- Refinement of broad topics into specific questions
- FINER criteria assessment
- Question type classification
- Scope assessment accuracy
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import json
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from gazzali.question_refiner import (
    QuestionRefiner,
    RefinedQuestion,
    QualityAssessment
)


class TestQuestionRefiner(unittest.TestCase):
    """Test cases for QuestionRefiner class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.api_key = "test_api_key"
        self.refiner = QuestionRefiner(api_key=self.api_key)
    
    def test_initialization(self):
        """Test QuestionRefiner initialization"""
        self.assertEqual(self.refiner.api_key, self.api_key)
        self.assertEqual(self.refiner.model, "grok-beta")
        self.assertEqual(self.refiner.base_url, "https://api.x.ai/v1")
    
    def test_initialization_custom_model(self):
        """Test initialization with custom model"""
        refiner = QuestionRefiner(
            api_key="test_key",
            model="custom-model",
            base_url="https://custom.api.com"
        )
        
        self.assertEqual(refiner.model, "custom-model")
        self.assertEqual(refiner.base_url, "https://custom.api.com")


class TestQuestionRefinement(unittest.TestCase):
    """Test question refinement functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.refiner = QuestionRefiner(api_key="test_key")
    
    @patch('gazzali.question_refiner.requests.post')
    def test_refine_broad_topic_ai(self, mock_post):
        """Test refinement of broad AI topic"""
        # Mock API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{
                "message": {
                    "content": json.dumps({
                        "refined_questions": [
                            "How do transformer architectures improve natural language understanding compared to RNN-based models?",
                            "What are the computational efficiency trade-offs between different attention mechanisms in large language models?",
                            "How does pre-training corpus size affect downstream task performance in language models?"
                        ],
                        "question_type": "comparative",
                        "key_variables": ["model architecture", "performance metrics", "computational cost"],
                        "key_populations": ["language models", "NLP systems"],
                        "contexts": ["natural language processing", "deep learning"],
                        "scope_assessment": "appropriate",
                        "feasibility_notes": "Requires access to computational resources and benchmark datasets",
                        "finer_scores": {
                            "feasible": 7,
                            "interesting": 9,
                            "novel": 6,
                            "ethical": 10,
                            "relevant": 9
                        },
                        "suggestions": ["Consider focusing on specific model sizes", "Define clear evaluation metrics"]
                    })
                }
            }]
        }
        mock_post.return_value = mock_response
        
        result = self.refiner.refine_question("artificial intelligence and machine learning")
        
        self.assertIsInstance(result, RefinedQuestion)
        self.assertEqual(result.original_topic, "artificial intelligence and machine learning")
        self.assertEqual(len(result.refined_questions), 3)
        self.assertEqual(result.question_type, "comparative")
        self.assertIn("model architecture", result.key_variables)
        self.assertEqual(result.scope_assessment, "appropriate")
        self.assertIsNotNone(result.quality_assessment)
        self.assertEqual(result.quality_assessment.finer_scores["feasible"], 7)
    
    @patch('gazzali.question_refiner.requests.post')
    def test_refine_broad_topic_climate(self, mock_post):
        """Test refinement of broad climate change topic"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{
                "message": {
                    "content": json.dumps({
                        "refined_questions": [
                            "How does ocean acidification affect coral reef biodiversity in tropical regions?",
                            "What is the relationship between Arctic ice melt rates and global sea level rise projections?"
                        ],
                        "question_type": "causal",
                        "key_variables": ["ocean pH", "coral biodiversity", "ice melt rate", "sea level"],
                        "key_populations": ["coral reefs", "Arctic ecosystems"],
                        "contexts": ["tropical oceans", "Arctic region"],
                        "scope_assessment": "appropriate",
                        "feasibility_notes": "Requires long-term monitoring data and climate models",
                        "finer_scores": {
                            "feasible": 6,
                            "interesting": 10,
                            "novel": 7,
                            "ethical": 9,
                            "relevant": 10
                        },
                        "suggestions": ["Specify time period for analysis"]
                    })
                }
            }]
        }
        mock_post.return_value = mock_response
        
        result = self.refiner.refine_question("climate change impacts")
        
        self.assertEqual(result.question_type, "causal")
        self.assertIn("ocean pH", result.key_variables)
        self.assertEqual(result.quality_assessment.finer_scores["relevant"], 10)

    
    @patch('gazzali.question_refiner.requests.post')
    def test_refine_with_discipline_context(self, mock_post):
        """Test refinement with discipline-specific context"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{
                "message": {
                    "content": json.dumps({
                        "refined_questions": [
                            "How do different psychotherapeutic approaches affect treatment outcomes for anxiety disorders?"
                        ],
                        "question_type": "comparative",
                        "key_variables": ["therapy type", "treatment outcomes", "anxiety severity"],
                        "key_populations": ["patients with anxiety disorders"],
                        "contexts": ["clinical psychology", "mental health treatment"],
                        "scope_assessment": "appropriate",
                        "feasibility_notes": "Requires clinical trial data or meta-analysis",
                        "finer_scores": {
                            "feasible": 8,
                            "interesting": 8,
                            "novel": 5,
                            "ethical": 8,
                            "relevant": 9
                        },
                        "suggestions": []
                    })
                }
            }]
        }
        mock_post.return_value = mock_response
        
        result = self.refiner.refine_question(
            "mental health treatment",
            discipline="social",
            context="Focus on evidence-based interventions"
        )
        
        self.assertIsInstance(result, RefinedQuestion)
        self.assertIn("therapy type", result.key_variables)
        
        # Verify API was called with discipline and context
        mock_post.assert_called_once()
        call_args = mock_post.call_args
        payload = call_args[1]['json']
        prompt = payload['messages'][1]['content']
        self.assertIn("social", prompt)
        self.assertIn("evidence-based interventions", prompt)
    
    @patch('gazzali.question_refiner.requests.post')
    def test_refine_too_broad_topic(self, mock_post):
        """Test refinement of overly broad topic"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{
                "message": {
                    "content": json.dumps({
                        "refined_questions": [
                            "What are the primary factors influencing student engagement in online learning environments?",
                            "How does synchronous vs asynchronous instruction affect learning outcomes in higher education?"
                        ],
                        "question_type": "descriptive",
                        "key_variables": ["student engagement", "learning environment", "instruction mode"],
                        "key_populations": ["students", "educators"],
                        "contexts": ["online education", "higher education"],
                        "scope_assessment": "too_broad",
                        "feasibility_notes": "Topic is very broad; recommend narrowing to specific educational level or subject",
                        "finer_scores": {
                            "feasible": 5,
                            "interesting": 7,
                            "novel": 4,
                            "ethical": 10,
                            "relevant": 8
                        },
                        "suggestions": [
                            "Narrow to specific educational level (K-12, undergraduate, graduate)",
                            "Focus on specific subject area",
                            "Specify time period or context (e.g., post-pandemic)"
                        ]
                    })
                }
            }]
        }
        mock_post.return_value = mock_response
        
        result = self.refiner.refine_question("education")
        
        self.assertEqual(result.scope_assessment, "too_broad")
        self.assertGreater(len(result.quality_assessment.suggestions), 0)
        self.assertLess(result.quality_assessment.finer_scores["feasible"], 7)

    
    @patch('gazzali.question_refiner.requests.post')
    def test_refine_api_error(self, mock_post):
        """Test handling of API errors during refinement"""
        mock_post.side_effect = Exception("API connection failed")
        
        with self.assertRaises(ValueError) as context:
            self.refiner.refine_question("test topic")
        
        self.assertIn("Failed to refine question", str(context.exception))
    
    @patch('gazzali.question_refiner.requests.post')
    def test_refine_invalid_json_response(self, mock_post):
        """Test handling of invalid JSON in API response"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{
                "message": {
                    "content": "This is not valid JSON"
                }
            }]
        }
        mock_post.return_value = mock_response
        
        with self.assertRaises(ValueError) as context:
            self.refiner.refine_question("test topic")
        
        self.assertIn("Failed to parse", str(context.exception))
    
    @patch('gazzali.question_refiner.requests.post')
    def test_refine_markdown_wrapped_json(self, mock_post):
        """Test handling of JSON wrapped in markdown code blocks"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{
                "message": {
                    "content": """```json
{
    "refined_questions": ["How does X affect Y?"],
    "question_type": "causal",
    "key_variables": ["X", "Y"],
    "key_populations": ["population"],
    "contexts": ["context"],
    "scope_assessment": "appropriate",
    "feasibility_notes": "Feasible",
    "finer_scores": {
        "feasible": 8,
        "interesting": 7,
        "novel": 6,
        "ethical": 9,
        "relevant": 8
    },
    "suggestions": []
}
```"""
                }
            }]
        }
        mock_post.return_value = mock_response
        
        result = self.refiner.refine_question("test topic")
        
        self.assertIsInstance(result, RefinedQuestion)
        self.assertEqual(len(result.refined_questions), 1)
        self.assertEqual(result.question_type, "causal")


class TestQuestionTypeClassification(unittest.TestCase):
    """Test question type classification"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.refiner = QuestionRefiner(api_key="test_key")
    
    @patch('gazzali.question_refiner.requests.post')
    def test_descriptive_question_type(self, mock_post):
        """Test classification of descriptive questions"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{
                "message": {
                    "content": json.dumps({
                        "refined_questions": ["What are the characteristics of X?"],
                        "question_type": "descriptive",
                        "key_variables": ["characteristics"],
                        "key_populations": ["X"],
                        "contexts": ["context"],
                        "scope_assessment": "appropriate",
                        "feasibility_notes": "Feasible",
                        "finer_scores": {"feasible": 8, "interesting": 7, "novel": 6, "ethical": 9, "relevant": 8},
                        "suggestions": []
                    })
                }
            }]
        }
        mock_post.return_value = mock_response
        
        result = self.refiner.refine_question("characteristics of X")
        self.assertEqual(result.question_type, "descriptive")

    
    @patch('gazzali.question_refiner.requests.post')
    def test_comparative_question_type(self, mock_post):
        """Test classification of comparative questions"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{
                "message": {
                    "content": json.dumps({
                        "refined_questions": ["How does A compare to B in terms of C?"],
                        "question_type": "comparative",
                        "key_variables": ["A", "B", "C"],
                        "key_populations": ["groups"],
                        "contexts": ["context"],
                        "scope_assessment": "appropriate",
                        "feasibility_notes": "Feasible",
                        "finer_scores": {"feasible": 8, "interesting": 7, "novel": 6, "ethical": 9, "relevant": 8},
                        "suggestions": []
                    })
                }
            }]
        }
        mock_post.return_value = mock_response
        
        result = self.refiner.refine_question("compare A and B")
        self.assertEqual(result.question_type, "comparative")
    
    @patch('gazzali.question_refiner.requests.post')
    def test_causal_question_type(self, mock_post):
        """Test classification of causal questions"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{
                "message": {
                    "content": json.dumps({
                        "refined_questions": ["Does X cause Y?"],
                        "question_type": "causal",
                        "key_variables": ["X", "Y"],
                        "key_populations": ["subjects"],
                        "contexts": ["context"],
                        "scope_assessment": "appropriate",
                        "feasibility_notes": "Requires experimental design",
                        "finer_scores": {"feasible": 6, "interesting": 9, "novel": 8, "ethical": 7, "relevant": 9},
                        "suggestions": []
                    })
                }
            }]
        }
        mock_post.return_value = mock_response
        
        result = self.refiner.refine_question("effect of X on Y")
        self.assertEqual(result.question_type, "causal")
    
    @patch('gazzali.question_refiner.requests.post')
    def test_relationship_question_type(self, mock_post):
        """Test classification of relationship questions"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{
                "message": {
                    "content": json.dumps({
                        "refined_questions": ["What is the relationship between X and Y?"],
                        "question_type": "relationship",
                        "key_variables": ["X", "Y"],
                        "key_populations": ["subjects"],
                        "contexts": ["context"],
                        "scope_assessment": "appropriate",
                        "feasibility_notes": "Feasible with correlational study",
                        "finer_scores": {"feasible": 8, "interesting": 7, "novel": 6, "ethical": 9, "relevant": 8},
                        "suggestions": []
                    })
                }
            }]
        }
        mock_post.return_value = mock_response
        
        result = self.refiner.refine_question("relationship between X and Y")
        self.assertEqual(result.question_type, "relationship")
    
    @patch('gazzali.question_refiner.requests.post')
    def test_mixed_question_type(self, mock_post):
        """Test classification of mixed question types"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{
                "message": {
                    "content": json.dumps({
                        "refined_questions": ["What are the characteristics of X and how do they compare to Y?"],
                        "question_type": "mixed",
                        "key_variables": ["X characteristics", "Y characteristics"],
                        "key_populations": ["X", "Y"],
                        "contexts": ["context"],
                        "scope_assessment": "appropriate",
                        "feasibility_notes": "Requires both descriptive and comparative analysis",
                        "finer_scores": {"feasible": 7, "interesting": 8, "novel": 6, "ethical": 9, "relevant": 8},
                        "suggestions": []
                    })
                }
            }]
        }
        mock_post.return_value = mock_response
        
        result = self.refiner.refine_question("characteristics and comparison")
        self.assertEqual(result.question_type, "mixed")



class TestFINERCriteriaAssessment(unittest.TestCase):
    """Test FINER criteria assessment functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.refiner = QuestionRefiner(api_key="test_key")
    
    @patch('gazzali.question_refiner.requests.post')
    def test_assess_high_quality_question(self, mock_post):
        """Test assessment of high-quality research question"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{
                "message": {
                    "content": json.dumps({
                        "is_specific": True,
                        "is_answerable": True,
                        "is_novel": True,
                        "scope": "appropriate",
                        "finer_scores": {
                            "feasible": 9,
                            "interesting": 8,
                            "novel": 8,
                            "ethical": 10,
                            "relevant": 9
                        },
                        "suggestions": []
                    })
                }
            }]
        }
        mock_post.return_value = mock_response
        
        result = self.refiner.assess_question_quality(
            "How does daily meditation practice affect cortisol levels in adults with chronic stress?"
        )
        
        self.assertIsInstance(result, QualityAssessment)
        self.assertTrue(result.is_specific)
        self.assertTrue(result.is_answerable)
        self.assertTrue(result.is_novel)
        self.assertEqual(result.scope, "appropriate")
        self.assertEqual(result.overall_quality(), "excellent")
        self.assertEqual(len(result.suggestions), 0)
    
    @patch('gazzali.question_refiner.requests.post')
    def test_assess_poor_quality_question(self, mock_post):
        """Test assessment of poor-quality research question"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{
                "message": {
                    "content": json.dumps({
                        "is_specific": False,
                        "is_answerable": False,
                        "is_novel": False,
                        "scope": "too_broad",
                        "finer_scores": {
                            "feasible": 3,
                            "interesting": 4,
                            "novel": 2,
                            "ethical": 8,
                            "relevant": 5
                        },
                        "suggestions": [
                            "Make the question more specific",
                            "Define clear variables and populations",
                            "Narrow the scope to a manageable research project"
                        ]
                    })
                }
            }]
        }
        mock_post.return_value = mock_response
        
        result = self.refiner.assess_question_quality("What is health?")
        
        self.assertFalse(result.is_specific)
        self.assertFalse(result.is_answerable)
        self.assertFalse(result.is_novel)
        self.assertEqual(result.scope, "too_broad")
        # Average score is 4.4, which falls in "needs_improvement" range (4-6)
        self.assertEqual(result.overall_quality(), "needs_improvement")
        self.assertGreater(len(result.suggestions), 0)
    
    @patch('gazzali.question_refiner.requests.post')
    def test_finer_feasible_criterion(self, mock_post):
        """Test FINER feasible criterion assessment"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{
                "message": {
                    "content": json.dumps({
                        "is_specific": True,
                        "is_answerable": False,
                        "is_novel": True,
                        "scope": "appropriate",
                        "finer_scores": {
                            "feasible": 2,  # Low feasibility
                            "interesting": 9,
                            "novel": 8,
                            "ethical": 10,
                            "relevant": 9
                        },
                        "suggestions": [
                            "Question requires resources beyond typical research capacity",
                            "Consider scaling down to a more feasible scope"
                        ]
                    })
                }
            }]
        }
        mock_post.return_value = mock_response
        
        result = self.refiner.assess_question_quality(
            "What is the complete molecular structure of consciousness across all species?"
        )
        
        self.assertEqual(result.finer_scores["feasible"], 2)
        self.assertFalse(result.is_answerable)
        # Check that suggestions mention resources or capacity (related to feasibility)
        self.assertIn("resources", result.suggestions[0].lower())

    
    @patch('gazzali.question_refiner.requests.post')
    def test_finer_interesting_criterion(self, mock_post):
        """Test FINER interesting criterion assessment"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{
                "message": {
                    "content": json.dumps({
                        "is_specific": True,
                        "is_answerable": True,
                        "is_novel": False,
                        "scope": "appropriate",
                        "finer_scores": {
                            "feasible": 8,
                            "interesting": 3,  # Low interest
                            "novel": 2,
                            "ethical": 10,
                            "relevant": 4
                        },
                        "suggestions": [
                            "Question addresses well-established knowledge",
                            "Consider focusing on a more novel aspect"
                        ]
                    })
                }
            }]
        }
        mock_post.return_value = mock_response
        
        result = self.refiner.assess_question_quality(
            "Does water freeze at 0 degrees Celsius?"
        )
        
        self.assertEqual(result.finer_scores["interesting"], 3)
        self.assertEqual(result.finer_scores["novel"], 2)
    
    @patch('gazzali.question_refiner.requests.post')
    def test_finer_ethical_criterion(self, mock_post):
        """Test FINER ethical criterion assessment"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{
                "message": {
                    "content": json.dumps({
                        "is_specific": True,
                        "is_answerable": True,
                        "is_novel": True,
                        "scope": "appropriate",
                        "finer_scores": {
                            "feasible": 7,
                            "interesting": 8,
                            "novel": 7,
                            "ethical": 3,  # Ethical concerns
                            "relevant": 8
                        },
                        "suggestions": [
                            "Question raises significant ethical concerns",
                            "Consider alternative approaches that minimize harm",
                            "Ensure proper ethical review and consent procedures"
                        ]
                    })
                }
            }]
        }
        mock_post.return_value = mock_response
        
        result = self.refiner.assess_question_quality(
            "What happens if we expose vulnerable populations to harmful substances?"
        )
        
        self.assertEqual(result.finer_scores["ethical"], 3)
        self.assertIn("ethical", result.suggestions[0].lower())
    
    @patch('gazzali.question_refiner.requests.post')
    def test_assess_with_discipline_context(self, mock_post):
        """Test assessment with discipline-specific context"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{
                "message": {
                    "content": json.dumps({
                        "is_specific": True,
                        "is_answerable": True,
                        "is_novel": True,
                        "scope": "appropriate",
                        "finer_scores": {
                            "feasible": 8,
                            "interesting": 9,
                            "novel": 7,
                            "ethical": 9,
                            "relevant": 9
                        },
                        "suggestions": []
                    })
                }
            }]
        }
        mock_post.return_value = mock_response
        
        result = self.refiner.assess_question_quality(
            "How do quantum entanglement effects scale in multi-qubit systems?",
            discipline="stem"
        )
        
        self.assertEqual(result.overall_quality(), "excellent")
        
        # Verify discipline was included in API call
        mock_post.assert_called_once()
        call_args = mock_post.call_args
        payload = call_args[1]['json']
        prompt = payload['messages'][1]['content']
        self.assertIn("stem", prompt)


class TestScopeAssessment(unittest.TestCase):
    """Test scope assessment functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.refiner = QuestionRefiner(api_key="test_key")
    
    @patch('gazzali.question_refiner.requests.post')
    def test_scope_too_broad(self, mock_post):
        """Test detection of overly broad scope"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{
                "message": {
                    "content": json.dumps({
                        "is_specific": False,
                        "is_answerable": False,
                        "is_novel": True,
                        "scope": "too_broad",
                        "finer_scores": {
                            "feasible": 2,
                            "interesting": 7,
                            "novel": 6,
                            "ethical": 9,
                            "relevant": 8
                        },
                        "suggestions": [
                            "Narrow to specific population or context",
                            "Focus on particular aspect or variable",
                            "Define clear boundaries for investigation"
                        ]
                    })
                }
            }]
        }
        mock_post.return_value = mock_response
        
        result = self.refiner.assess_question_quality("What is the meaning of life?")
        
        self.assertEqual(result.scope, "too_broad")
        self.assertFalse(result.is_specific)
        self.assertGreater(len(result.suggestions), 0)

    
    @patch('gazzali.question_refiner.requests.post')
    def test_scope_appropriate(self, mock_post):
        """Test detection of appropriate scope"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{
                "message": {
                    "content": json.dumps({
                        "is_specific": True,
                        "is_answerable": True,
                        "is_novel": True,
                        "scope": "appropriate",
                        "finer_scores": {
                            "feasible": 8,
                            "interesting": 8,
                            "novel": 7,
                            "ethical": 9,
                            "relevant": 9
                        },
                        "suggestions": []
                    })
                }
            }]
        }
        mock_post.return_value = mock_response
        
        result = self.refiner.assess_question_quality(
            "How does gamification affect student engagement in undergraduate computer science courses?"
        )
        
        self.assertEqual(result.scope, "appropriate")
        self.assertTrue(result.is_specific)
        self.assertTrue(result.is_answerable)
    
    @patch('gazzali.question_refiner.requests.post')
    def test_scope_too_narrow(self, mock_post):
        """Test detection of overly narrow scope"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{
                "message": {
                    "content": json.dumps({
                        "is_specific": True,
                        "is_answerable": True,
                        "is_novel": False,
                        "scope": "too_narrow",
                        "finer_scores": {
                            "feasible": 9,
                            "interesting": 3,
                            "novel": 2,
                            "ethical": 10,
                            "relevant": 4
                        },
                        "suggestions": [
                            "Question is too specific and may lack broader relevance",
                            "Consider expanding to include related contexts or populations",
                            "Broaden to increase generalizability"
                        ]
                    })
                }
            }]
        }
        mock_post.return_value = mock_response
        
        result = self.refiner.assess_question_quality(
            "What is the exact temperature of the third beaker in lab room 305 at 3:47 PM on Tuesday?"
        )
        
        self.assertEqual(result.scope, "too_narrow")
        self.assertFalse(result.is_novel)
        self.assertIn("broaden", result.suggestions[2].lower())


class TestQualityAssessment(unittest.TestCase):
    """Test QualityAssessment class functionality"""
    
    def test_overall_quality_excellent(self):
        """Test overall quality calculation for excellent questions"""
        assessment = QualityAssessment(
            is_specific=True,
            is_answerable=True,
            is_novel=True,
            scope="appropriate",
            finer_scores={
                "feasible": 9,
                "interesting": 8,
                "novel": 8,
                "ethical": 10,
                "relevant": 9
            }
        )
        
        self.assertEqual(assessment.overall_quality(), "excellent")
    
    def test_overall_quality_good(self):
        """Test overall quality calculation for good questions"""
        assessment = QualityAssessment(
            is_specific=True,
            is_answerable=True,
            is_novel=True,
            scope="appropriate",
            finer_scores={
                "feasible": 7,
                "interesting": 6,
                "novel": 6,
                "ethical": 8,
                "relevant": 7
            }
        )
        
        self.assertEqual(assessment.overall_quality(), "good")
    
    def test_overall_quality_needs_improvement(self):
        """Test overall quality calculation for questions needing improvement"""
        assessment = QualityAssessment(
            is_specific=False,
            is_answerable=True,
            is_novel=False,
            scope="too_broad",
            finer_scores={
                "feasible": 5,
                "interesting": 4,
                "novel": 4,
                "ethical": 7,
                "relevant": 5
            }
        )
        
        self.assertEqual(assessment.overall_quality(), "needs_improvement")
    
    def test_overall_quality_poor(self):
        """Test overall quality calculation for poor questions"""
        assessment = QualityAssessment(
            is_specific=False,
            is_answerable=False,
            is_novel=False,
            scope="too_broad",
            finer_scores={
                "feasible": 2,
                "interesting": 3,
                "novel": 2,
                "ethical": 5,
                "relevant": 3
            }
        )
        
        self.assertEqual(assessment.overall_quality(), "poor")
    
    def test_overall_quality_no_scores(self):
        """Test overall quality with no FINER scores"""
        assessment = QualityAssessment(
            is_specific=True,
            is_answerable=True,
            is_novel=True,
            scope="appropriate"
        )
        
        self.assertEqual(assessment.overall_quality(), "needs_improvement")


class TestRefinedQuestion(unittest.TestCase):
    """Test RefinedQuestion class functionality"""
    
    def test_get_best_question(self):
        """Test getting the best refined question"""
        refined = RefinedQuestion(
            original_topic="broad topic",
            refined_questions=[
                "Specific question 1",
                "Specific question 2",
                "Specific question 3"
            ],
            question_type="descriptive"
        )
        
        self.assertEqual(refined.get_best_question(), "Specific question 1")
    
    def test_get_best_question_empty_list(self):
        """Test getting best question when list is empty"""
        refined = RefinedQuestion(
            original_topic="broad topic",
            refined_questions=[],
            question_type="descriptive"
        )
        
        self.assertEqual(refined.get_best_question(), "broad topic")
    
    def test_refined_question_with_quality_assessment(self):
        """Test RefinedQuestion with quality assessment"""
        quality = QualityAssessment(
            is_specific=True,
            is_answerable=True,
            is_novel=True,
            scope="appropriate",
            finer_scores={"feasible": 8, "interesting": 7, "novel": 6, "ethical": 9, "relevant": 8}
        )
        
        refined = RefinedQuestion(
            original_topic="AI research",
            refined_questions=["How does X affect Y in AI systems?"],
            question_type="causal",
            key_variables=["X", "Y"],
            key_populations=["AI systems"],
            contexts=["machine learning"],
            scope_assessment="appropriate",
            feasibility_notes="Requires computational resources",
            quality_assessment=quality
        )
        
        self.assertEqual(refined.quality_assessment.overall_quality(), "good")
        self.assertIn("X", refined.key_variables)
        self.assertIn("AI systems", refined.key_populations)


class TestPromptBuilding(unittest.TestCase):
    """Test prompt building functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.refiner = QuestionRefiner(api_key="test_key")
    
    def test_build_refinement_prompt_basic(self):
        """Test basic refinement prompt building"""
        prompt = self.refiner._build_refinement_prompt("test topic", None, None)
        
        self.assertIn("test topic", prompt)
        self.assertIn("FINER criteria", prompt)
        self.assertIn("refined_questions", prompt)
        self.assertIn("question_type", prompt)
        self.assertIn("key_variables", prompt)
    
    def test_build_refinement_prompt_with_discipline(self):
        """Test refinement prompt with discipline"""
        prompt = self.refiner._build_refinement_prompt("test topic", "stem", None)
        
        self.assertIn("stem", prompt)
        self.assertIn("Academic Discipline", prompt)
    
    def test_build_refinement_prompt_with_context(self):
        """Test refinement prompt with additional context"""
        prompt = self.refiner._build_refinement_prompt(
            "test topic",
            None,
            "Focus on recent developments"
        )
        
        self.assertIn("Focus on recent developments", prompt)
        self.assertIn("Additional Context", prompt)
    
    def test_build_assessment_prompt_basic(self):
        """Test basic assessment prompt building"""
        prompt = self.refiner._build_assessment_prompt("test question", None)
        
        self.assertIn("test question", prompt)
        self.assertIn("FINER criteria", prompt)
        self.assertIn("is_specific", prompt)
        self.assertIn("is_answerable", prompt)
        self.assertIn("is_novel", prompt)
    
    def test_build_assessment_prompt_with_discipline(self):
        """Test assessment prompt with discipline"""
        prompt = self.refiner._build_assessment_prompt("test question", "humanities")
        
        self.assertIn("humanities", prompt)


if __name__ == "__main__":
    unittest.main()
