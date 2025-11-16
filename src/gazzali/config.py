"""Configuration utilities for Gazzali Research."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv


_PROJECT_ROOT = Path(__file__).resolve().parents[2]
_ENV_PATH = _PROJECT_ROOT / ".env"

if _ENV_PATH.exists():
    load_dotenv(dotenv_path=_ENV_PATH, override=False)


def get_env(name: str, default: Optional[str] = None) -> Optional[str]:
    """Return environment variable value with optional default."""
    return os.getenv(name, default)


def get_env_bool(name: str, default: bool = False) -> bool:
    """
    Parse boolean from environment variable.
    
    Args:
        name: Environment variable name
        default: Default value if not set or invalid
    
    Returns:
        Boolean value from environment or default
    
    Examples:
        >>> os.environ['TEST_FLAG'] = 'true'
        >>> get_env_bool('TEST_FLAG')
        True
        >>> get_env_bool('MISSING_FLAG', default=False)
        False
    """
    value = os.getenv(name, "").lower()
    if value in ("true", "1", "yes", "on"):
        return True
    elif value in ("false", "0", "no", "off"):
        return False
    return default


def get_env_int(name: str, default: int = 0) -> int:
    """
    Parse integer from environment variable.
    
    Args:
        name: Environment variable name
        default: Default value if not set or invalid
    
    Returns:
        Integer value from environment or default
    
    Examples:
        >>> os.environ['MAX_COUNT'] = '100'
        >>> get_env_int('MAX_COUNT')
        100
        >>> get_env_int('MISSING_COUNT', default=50)
        50
    """
    try:
        return int(os.getenv(name, str(default)))
    except (ValueError, TypeError):
        return default


def get_env_float(name: str, default: float = 0.0) -> float:
    """
    Parse float from environment variable.
    
    Args:
        name: Environment variable name
        default: Default value if not set or invalid
    
    Returns:
        Float value from environment or default
    
    Examples:
        >>> os.environ['TEMPERATURE'] = '0.85'
        >>> get_env_float('TEMPERATURE')
        0.85
        >>> get_env_float('MISSING_TEMP', default=1.0)
        1.0
    """
    try:
        return float(os.getenv(name, str(default)))
    except (ValueError, TypeError):
        return default


# ============================================================================
# Academic Configuration Helpers
# ============================================================================

def get_citation_style() -> str:
    """
    Get citation style from environment.
    
    Returns:
        Citation style (apa, mla, chicago, ieee) or default 'apa'
    """
    style = get_env("CITATION_STYLE", "apa").lower()
    valid_styles = {"apa", "mla", "chicago", "ieee"}
    return style if style in valid_styles else "apa"


def get_output_format() -> str:
    """
    Get output format from environment.
    
    Returns:
        Output format (paper, review, proposal, abstract, presentation) or default 'paper'
    """
    fmt = get_env("OUTPUT_FORMAT", "paper").lower()
    valid_formats = {"paper", "review", "proposal", "abstract", "presentation"}
    return fmt if fmt in valid_formats else "paper"


def get_discipline() -> str:
    """
    Get academic discipline from environment.
    
    Returns:
        Discipline (general, stem, social, humanities, medical) or default 'general'
    """
    discipline = get_env("DISCIPLINE", "general").lower()
    valid_disciplines = {"general", "stem", "social", "humanities", "medical"}
    return discipline if discipline in valid_disciplines else "general"


def get_word_count_target() -> int:
    """
    Get target word count from environment.
    
    Returns:
        Word count target (default: 8000)
    """
    return get_env_int("WORD_COUNT_TARGET", 8000)


def get_include_abstract() -> bool:
    """
    Get whether to include abstract section.
    
    Returns:
        True if abstract should be included (default: True)
    """
    return get_env_bool("INCLUDE_ABSTRACT", True)


def get_include_methodology() -> bool:
    """
    Get whether to include methodology section.
    
    Returns:
        True if methodology should be included (default: True)
    """
    return get_env_bool("INCLUDE_METHODOLOGY", True)


def get_scholar_priority() -> bool:
    """
    Get whether to prioritize Scholar tool over general search.
    
    Returns:
        True if Scholar should be prioritized (default: True)
    """
    return get_env_bool("SCHOLAR_PRIORITY", True)


def get_export_bibliography() -> bool:
    """
    Get whether to export bibliography to separate file.
    
    Returns:
        True if bibliography should be exported (default: False)
    """
    return get_env_bool("EXPORT_BIBLIOGRAPHY", False)


def get_min_peer_reviewed_sources() -> int:
    """
    Get minimum number of peer-reviewed sources.
    
    Returns:
        Minimum peer-reviewed sources (default: 5)
    """
    return get_env_int("MIN_PEER_REVIEWED_SOURCES", 5)


def get_source_quality_threshold() -> int:
    """
    Get minimum source quality threshold (0-10).
    
    Returns:
        Quality threshold (default: 7)
    """
    threshold = get_env_int("SOURCE_QUALITY_THRESHOLD", 7)
    # Clamp to valid range
    return max(0, min(10, threshold))

