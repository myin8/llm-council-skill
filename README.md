# LLM Council Agent Skill

A portable [Agent Skill](https://agentskills.io/specification) that runs multi-model deliberation through OpenRouter and returns structured JSON.

## Overview

LLM Council orchestrates multiple language models through a three-stage process:

1. **Parallel responses:** multiple models answer the question independently.
2. **Anonymized peer review:** models rank each other's anonymized responses.
3. **Chairman synthesis:** a synthesis model combines the responses and rankings into a final answer.

The anonymized review step reduces model-name bias when models rank peer responses.

## Skill Layout

This repository root is the canonical Agent Skill:

```text
llm-council-skill/
├── SKILL.md                     # Agent Skills spec entry point
├── agents/openai.yaml           # Codex/OpenAI UI metadata
├── .claude/skills/llm-council/  # Legacy Claude compatibility mirror
├── scripts/run_council.py       # Agent Skills script entry point
├── council/                     # Python package
└── council_run.py               # CLI runner
```

The root `SKILL.md` follows the Agent Skills specification and can be used by Codex and other agents that support the format. The `.claude/skills/llm-council/SKILL.md` file is kept only for older Claude-specific loaders.

## Installation

```bash
git clone https://github.com/myin8/llm-council-skill ~/.local/share/llm-council-skill
cd ~/.local/share/llm-council-skill
cp .env.example .env
# Edit .env and add OPENROUTER_API_KEY
uv sync
```

Or use the installer:

```bash
curl -fsSL https://raw.githubusercontent.com/myin8/llm-council-skill/main/install.sh | bash
```

See [INSTALL.md](INSTALL.md) for details.

## Usage

From the command line:

```bash
uv run python scripts/run_council.py "What is the CAP theorem?"
uv run python scripts/run_council.py "Explain async/await" --stages 1
uv run python scripts/run_council.py "Compare Python vs Go" \
  --models "openai/gpt-4o,anthropic/claude-sonnet-4,google/gemini-2.5-pro"
uv run python scripts/run_council.py --query-file question.txt
```

After editable/package installation, the console script is available:

```bash
llm-council "What is the CAP theorem?"
```

From a coding agent that supports Agent Skills, invoke the skill naturally:

- "Ask the council: [your question]"
- "Run a council deliberation on [topic]"
- "Use `$llm-council-skill` to compare model perspectives on [topic]"

## Output Format

The runner writes progress to stderr and JSON to stdout:

```json
{
  "query": "...",
  "models": ["model1", "model2", "model3"],
  "chairman_model": "chairman",
  "stage1": [
    {"model": "model1", "response": "..."}
  ],
  "stage2": {
    "evaluations": [],
    "label_to_model": {},
    "aggregate_rankings": []
  },
  "stage3": {
    "model": "chairman",
    "synthesis": "..."
  }
}
```

## Configuration

Set `OPENROUTER_API_KEY` in `.env` or in the environment. Change default models in [council/config.py](council/config.py), or override them per run with `--models` and `--chairman`.

## Requirements

- Python 3.10+
- OpenRouter API key
- `httpx`
- `python-dotenv`

## Credits

Original implementation by Andrej Karpathy. Extracted and adapted as a portable Agent Skill.
