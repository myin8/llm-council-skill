"""Configuration for the LLM Council."""

import os
from dotenv import load_dotenv

# Load .env file if present, but don't override existing environment variables
# This allows the API key to be set globally or in .env
load_dotenv(override=False)

# OpenRouter API key - checked in this order:
# 1. Global environment variable OPENROUTER_API_KEY
# 2. .env file in project root
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Default council members - list of OpenRouter model identifiers
DEFAULT_COUNCIL_MODELS = [
    "openai/gpt-5.5",  # GPT-5.5 (released 2026-04-23)
    "~google/gemini-pro-latest",  # Latest Gemini Pro (auto-updates)
    "anthropic/claude-opus-4.8",  # Claude Opus 4.8 (released 2026-05-28)
    # "x-ai/grok-4.3",  # Grok 4.3 (released 2026-04-30)
    # "anthropic/claude-fable-5",  # Claude Fable 5 Mythos-class (released 2026-06-09)
]

# Default chairman model - synthesizes final response
DEFAULT_CHAIRMAN_MODEL = "anthropic/claude-opus-4.8"

# OpenRouter API endpoint
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
