# LLM Council Skill

A Claude Code skill that runs multi-model deliberation to answer questions through a 3-stage process.

## Overview

LLM Council orchestrates multiple language models to collaboratively answer questions:

1. **Stage 1 - Parallel Responses:** Multiple models respond to the question independently
2. **Stage 2 - Anonymized Peer Review:** Models evaluate and rank each other's anonymized responses
3. **Stage 3 - Chairman Synthesis:** A chairman model synthesizes all responses and rankings into a final answer

The anonymization in Stage 2 prevents models from playing favorites when ranking peers.

## Installation

### Quick Install (Recommended)

```bash
curl -fsSL https://raw.githubusercontent.com/yourusername/llm-council-skill/main/install.sh | bash
```

Or manually:

```bash
git clone https://github.com/yourusername/llm-council-skill ~/s/llm-council-skill
cd ~/s/llm-council-skill
cp .env.example .env
# Edit .env and add your OPENROUTER_API_KEY
uv sync
```

See [INSTALL.md](INSTALL.md) for detailed installation options.

## Usage

### From Command Line

```bash
# Full 3-stage deliberation
uv run python council_run.py "What is the CAP theorem?"

# Quick stage 1 comparison only
uv run python council_run.py "Explain async/await" --stages 1

# Custom models
uv run python council_run.py "Compare Python vs Go" \
  --models "openai/gpt-4o,anthropic/claude-sonnet-4,google/gemini-2.5-pro"

# From file
uv run python council_run.py --query-file question.txt
```

### As a Claude Code Skill

Invoke from Claude Code with:
- "Ask the council: [your question]"
- "Run a council deliberation on [topic]"
- `/llm-council`

Claude Code will run the script, parse the JSON output, and present the findings in a readable format.

## Default Models

**Council Members:**
- `openai/gpt-5.5` (GPT-5.5, released 2026-04-23)
- `~google/gemini-pro-latest` (Latest Gemini Pro, auto-updates)
- `anthropic/claude-opus-4.8` (Claude Opus 4.8, released 2026-05-28)

**Chairman:**
- `anthropic/claude-opus-4.8` (Claude Opus 4.8)

Override with `--models` and `--chairman` flags.

## Output Format

JSON structure:

```json
{
  "query": "...",
  "models": ["model1", "model2", "model3"],
  "chairman_model": "chairman",
  "stage1": [
    {"model": "...", "response": "..."}
  ],
  "stage2": {
    "evaluations": [...],
    "label_to_model": {...},
    "aggregate_rankings": [...]
  },
  "stage3": {
    "model": "...",
    "synthesis": "..."
  }
}
```

## Configuration

Edit `council/config.py` to change default models. Or use CLI flags for per-query overrides.

## Requirements

- Python 3.10+
- OpenRouter API key (supports 100+ models from various providers)
- Dependencies: `httpx`, `python-dotenv`

## Architecture

```
council/
├── __init__.py
├── config.py           # Defaults and API configuration
├── openrouter.py       # HTTP client for OpenRouter API
└── deliberate.py       # 3-stage orchestration logic

council_run.py          # CLI entry point
```

The skill is stateless — each run is independent. No database or file storage.

## Distribution

This repository is packaged as a ready-to-use Claude Code skill. See [PACKAGING.md](PACKAGING.md) for details on:
- Skill structure and conventions
- Distribution options (Git, PyPI, plugin registry)
- Version management
- Publishing workflow

## Credits

Original implementation by Andrej Karpathy. Extracted and adapted as a Claude Code skill.
