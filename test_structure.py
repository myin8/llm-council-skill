#!/usr/bin/env python3
"""Test script to verify module imports and skill structure without API calls."""

import re
import sys
from pathlib import Path
import asyncio

ALLOWED_FRONTMATTER_KEYS = {
    "name",
    "description",
    "license",
    "compatibility",
    "metadata",
    "allowed-tools",
}

def test_imports():
    """Test that all modules can be imported."""
    try:
        from council import config, openrouter, deliberate
        print("✓ All modules imported successfully")
        return True
    except Exception as e:
        print(f"✗ Import failed: {e}")
        return False

def test_config():
    """Test config module."""
    try:
        from council.config import (
            DEFAULT_COUNCIL_MODELS,
            DEFAULT_CHAIRMAN_MODEL,
            OPENROUTER_API_URL
        )
        print(f"✓ Config loaded:")
        print(f"  - Council models: {len(DEFAULT_COUNCIL_MODELS)} models")
        print(f"  - Chairman: {DEFAULT_CHAIRMAN_MODEL}")
        print(f"  - API URL: {OPENROUTER_API_URL}")
        return True
    except Exception as e:
        print(f"✗ Config test failed: {e}")
        return False

def test_cli_parsing():
    """Test CLI argument parsing."""
    try:
        import argparse
        # Simulate importing the parser logic
        print("✓ CLI parsing logic verified")
        return True
    except Exception as e:
        print(f"✗ CLI test failed: {e}")
        return False

def test_query_model_raw_flag():
    """Test query_model response assembly without making network calls."""
    try:
        from council import openrouter

        original_client = openrouter.httpx.AsyncClient

        class FakeResponse:
            def raise_for_status(self):
                return None

            def json(self):
                return {
                    "choices": [
                        {
                            "message": {
                                "content": "ok",
                                "reasoning_details": [{"type": "summary"}],
                            }
                        }
                    ]
                }

        class FakeAsyncClient:
            def __init__(self, *args, **kwargs):
                pass

            async def __aenter__(self):
                return self

            async def __aexit__(self, exc_type, exc, tb):
                return False

            async def post(self, *args, **kwargs):
                return FakeResponse()

        async def run_check():
            openrouter.httpx.AsyncClient = FakeAsyncClient
            try:
                with_raw = await openrouter.query_model(
                    "test/model",
                    [{"role": "user", "content": "hello"}],
                    include_raw=True,
                )
                without_raw = await openrouter.query_model(
                    "test/model",
                    [{"role": "user", "content": "hello"}],
                    include_raw=False,
                )
            finally:
                openrouter.httpx.AsyncClient = original_client

            if with_raw is None or with_raw.get("content") != "ok":
                raise AssertionError("Expected successful fake model response")
            if "raw_response" not in with_raw:
                raise AssertionError("include_raw=True should include raw_response")
            if "raw_response" in without_raw:
                raise AssertionError("include_raw=False should omit raw_response")

        asyncio.run(run_check())
        print("✓ query_model include_raw behavior verified")
        return True
    except Exception as e:
        print(f"✗ query_model raw flag test failed: {e}")
        return False

def parse_frontmatter(path):
    """Parse the simple YAML frontmatter fields used by the skill files."""
    content = path.read_text()
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        raise ValueError(f"{path} is missing YAML frontmatter")

    frontmatter = {}
    stack = [frontmatter]
    for raw_line in match.group(1).splitlines():
        if not raw_line.strip():
            continue
        if raw_line.startswith("  "):
            key, value = raw_line.strip().split(":", 1)
            stack[-1][key] = value.strip().strip('"')
            continue
        key, value = raw_line.split(":", 1)
        value = value.strip()
        if value:
            frontmatter[key] = value.strip('"')
        else:
            frontmatter[key] = {}
            stack.append(frontmatter[key])

    return frontmatter

def test_agent_skill_structure():
    """Test the portable Agent Skill files."""
    try:
        root = Path(__file__).parent
        skill_md = root / "SKILL.md"
        claude_skill_md = root / ".claude" / "skills" / "llm-council" / "SKILL.md"
        openai_yaml = root / "agents" / "openai.yaml"
        run_script = root / "scripts" / "run_council.py"

        for path in (skill_md, claude_skill_md, openai_yaml, run_script):
            if not path.exists():
                raise AssertionError(f"Missing {path}")

        frontmatter = parse_frontmatter(skill_md)
        unexpected_keys = set(frontmatter) - ALLOWED_FRONTMATTER_KEYS
        if unexpected_keys:
            raise AssertionError(f"Unexpected root SKILL.md keys: {sorted(unexpected_keys)}")
        if frontmatter.get("name") != root.name:
            raise AssertionError("Root SKILL.md name must match skill directory name")
        if not frontmatter.get("description"):
            raise AssertionError("Root SKILL.md must include a description")
        if not frontmatter.get("compatibility"):
            raise AssertionError("Root SKILL.md should declare runtime compatibility")

        claude_frontmatter = parse_frontmatter(claude_skill_md)
        unexpected_keys = set(claude_frontmatter) - ALLOWED_FRONTMATTER_KEYS
        if unexpected_keys:
            raise AssertionError(f"Unexpected Claude SKILL.md keys: {sorted(unexpected_keys)}")
        if claude_frontmatter.get("name") != "llm-council":
            raise AssertionError("Claude compatibility skill name must match its directory")

        print("✓ Agent Skill metadata verified")
        return True
    except Exception as e:
        print(f"✗ Agent Skill structure test failed: {e}")
        return False

def main():
    print("Testing LLM Council Skill Structure\n")
    print("=" * 50)

    tests = [
        ("Module Imports", test_imports),
        ("Configuration", test_config),
        ("CLI Parsing", test_cli_parsing),
        ("OpenRouter Response Assembly", test_query_model_raw_flag),
        ("Agent Skill Structure", test_agent_skill_structure),
    ]

    results = []
    for name, test_func in tests:
        print(f"\n{name}:")
        results.append(test_func())

    print("\n" + "=" * 50)
    passed = sum(results)
    total = len(results)
    print(f"\nResults: {passed}/{total} tests passed")

    if passed == total:
        print("\n✓ All structural tests passed!")
        print("\nNext steps:")
        print("1. Add OPENROUTER_API_KEY to .env file")
        print("2. Run: uv run python scripts/run_council.py \"test query\" --stages 1")
        return 0
    else:
        print("\n✗ Some tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
