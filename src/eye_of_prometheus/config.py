"""Configuration utilities for Eye of Prometheus."""

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

