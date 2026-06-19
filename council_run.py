#!/usr/bin/env python3
"""CLI entry point for LLM Council deliberation."""

import asyncio
import argparse
import json
import sys
from pathlib import Path
from council.deliberate import run_full_council


def parse_args():
    parser = argparse.ArgumentParser(
        description="Run LLM Council deliberation on a query",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "What is the CAP theorem?"
  %(prog)s "Explain caching strategies" --stages 2
  %(prog)s "Compare Python vs Go" --models "openai/gpt-4o,anthropic/claude-sonnet-4"
  %(prog)s --query-file question.txt
  %(prog)s "Technical question" --verbose  # Include full API responses
        """
    )

    parser.add_argument(
        "query",
        nargs="?",
        help="The question to ask the council (or use --query-file)"
    )

    parser.add_argument(
        "--query-file",
        type=Path,
        help="Read query from file instead of command line"
    )

    parser.add_argument(
        "--models",
        help="Comma-separated list of OpenRouter model IDs (overrides defaults)"
    )

    parser.add_argument(
        "--chairman",
        help="Chairman model ID (overrides default)"
    )

    parser.add_argument(
        "--stages",
        type=int,
        choices=[1, 2, 3],
        default=3,
        help="Maximum stage to run (default: 3)"
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Include full raw API responses with metadata (tokens, latency, etc.)"
    )

    return parser.parse_args()


async def main():
    args = parse_args()

    # Get query from argument or file
    if args.query_file:
        if not args.query_file.exists():
            print(f"Error: File not found: {args.query_file}", file=sys.stderr)
            sys.exit(1)
        query = args.query_file.read_text().strip()
    elif args.query:
        query = args.query
    else:
        print("Error: Must provide query argument or --query-file", file=sys.stderr)
        sys.exit(1)

    if not query:
        print("Error: Query cannot be empty", file=sys.stderr)
        sys.exit(1)

    # Parse models if provided
    models = None
    if args.models:
        models = [m.strip() for m in args.models.split(",")]

    # Progress messages to stderr
    print(f"Running council deliberation (stages: {args.stages})...", file=sys.stderr)

    try:
        result = await run_full_council(
            user_query=query,
            models=models,
            chairman_model=args.chairman,
            max_stages=args.stages,
            verbose=args.verbose
        )

        # JSON output to stdout
        print(json.dumps(result, indent=2))

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def cli_main():
    """Entry point for console script."""
    asyncio.run(main())


if __name__ == "__main__":
    cli_main()
