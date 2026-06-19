#!/usr/bin/env python3
"""Agent Skill wrapper for the LLM Council CLI.

This file exists so agents can follow the conventional Agent Skills
`scripts/` path while the package keeps `council_run.py` as the console
entry point.
"""

import sys
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL_ROOT))

from council_run import cli_main  # noqa: E402


if __name__ == "__main__":
    cli_main()
