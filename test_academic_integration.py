#!/usr/bin/env python3
"""
Quick test script to verify academic prompt integration
"""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_academic_prompt_import():
    """Test that academic prompts can be imported"""
    try:
        from gazzali.prompts.academic_prompts import get_academic_research_prompt
        from gazzali.academic_config import AcademicConfig
        print("✅ Academic prompts module imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Failed to import academic prompts: {e}")
        return False

def test_academic_config():
    """Test academic configuration"""
    try:
        from gazzali.academic_config import AcademicConfig, Discipline, OutputFormat, CitationStyle
        
        # Create config
        config = AcademicConfig(
            discipline=Discipline.STEM,
            output_format=OutputFormat.PAPER,
            citation_style=CitationStyle.APA
        )
        
        print(f"✅ Academic config created: {config.discipline.value}, {config.output_format.value}")
        
        # Test prompt modifiers
        modifiers = config.get_prompt_modifiers()
        assert 'terminology' in modifiers
        assert 'methodology_focus' in modifiers
        print("✅ Prompt modifiers generated successfully")
        
        return True
    except Exception as e:
        print(f"❌ Academic config test failed: {e}")
        return False

def test_academic_prompt_generation():
    """Test academic prompt generation"""
    try:
        from gazzali.prompts.academic_prompts import get_academic_research_prompt
        
        # Generate prompt for STEM discipline
        prompt = get_academic_research_prompt(
            discipline="stem",
            output_format="paper"
        )
        
        # Check that prompt contains expected content
        assert "academic research assistant" in prompt.lower()
        assert "peer-reviewed" in prompt.lower()
        assert "google_scholar" in prompt.lower()
        assert "stem" in prompt.lower() or "STEM" in prompt
        
        print("✅ Academic prompt generated successfully")
        print(f"   Prompt length: {len(prompt)} characters")
        
        return True
    except Exception as e:
        print(f"❌ Prompt generation test failed: {e}")
        return False

def test_environment_variable_handling():
    """Test environment variable handling"""
    try:
        # Set test environment variables
        os.environ["GAZZALI_ACADEMIC_MODE"] = "true"
        os.environ["GAZZALI_DISCIPLINE"] = "stem"
        os.environ["GAZZALI_OUTPUT_FORMAT"] = "paper"
        os.environ["GAZZALI_CITATION_STYLE"] = "apa"
        
        # Verify they can be read
        assert os.getenv("GAZZALI_ACADEMIC_MODE") == "true"
        assert os.getenv("GAZZALI_DISCIPLINE") == "stem"
        
        print("✅ Environment variables set and read successfully")
        
        # Clean up
        del os.environ["GAZZALI_ACADEMIC_MODE"]
        del os.environ["GAZZALI_DISCIPLINE"]
        del os.environ["GAZZALI_OUTPUT_FORMAT"]
        del os.environ["GAZZALI_CITATION_STYLE"]
        
        return True
    except Exception as e:
        print(f"❌ Environment variable test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("Testing Academic Prompt Integration")
    print("=" * 60)
    print()
    
    tests = [
        ("Import Test", test_academic_prompt_import),
        ("Config Test", test_academic_config),
        ("Prompt Generation Test", test_academic_prompt_generation),
        ("Environment Variables Test", test_environment_variable_handling),
    ]
    
    results = []
    for name, test_func in tests:
        print(f"\n{name}:")
        print("-" * 60)
        result = test_func()
        results.append(result)
        print()
    
    print("=" * 60)
    print(f"Results: {sum(results)}/{len(results)} tests passed")
    print("=" * 60)
    
    return all(results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
