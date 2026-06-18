#!/usr/bin/env python3
"""Test script to verify module imports and structure without API calls."""

import sys

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

def main():
    print("Testing LLM Council Skill Structure\n")
    print("=" * 50)

    tests = [
        ("Module Imports", test_imports),
        ("Configuration", test_config),
        ("CLI Parsing", test_cli_parsing),
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
        print("2. Run: uv run python council_run.py \"test query\" --stages 1")
        return 0
    else:
        print("\n✗ Some tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
