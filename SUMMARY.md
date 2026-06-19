# LLM Council Agent Skill - Summary

## What Was Built

A portable Agent Skill extracted from the LLM Council web app. It runs three-stage multi-model deliberation and returns structured JSON output.

## Key Features

- Stateless CLI tool with no server, database, or UI.
- Three-stage deliberation: parallel responses, anonymized peer ranking, chairman synthesis.
- Runtime model overrides with `--models` and `--chairman`.
- Partial runs with `--stages 1` or `--stages 2`.
- Query loading from files with `--query-file`.
- Spec-compliant root `SKILL.md` for Codex and other Agent Skills clients.
- `agents/openai.yaml` metadata for Codex/OpenAI surfaces.
- `scripts/run_council.py` as the conventional bundled script entry point.
- `.claude/skills/llm-council/SKILL.md` compatibility mirror for older Claude-specific loaders.

## Architecture

```text
llm-council-skill/
├── SKILL.md
├── agents/openai.yaml
├── .claude/skills/llm-council/SKILL.md
├── scripts/run_council.py
├── council/
│   ├── __init__.py
│   ├── config.py
│   ├── openrouter.py
│   └── deliberate.py
├── council_run.py
├── pyproject.toml
├── .env.example
└── test_structure.py
```

## Usage

```bash
uv run python scripts/run_council.py "What is the CAP theorem?"
uv run python scripts/run_council.py "Explain async/await" --stages 1
uv run python scripts/run_council.py "Compare languages" \
  --models "openai/gpt-4o,anthropic/claude-sonnet-4" \
  --chairman "google/gemini-2.5-pro"
uv run python scripts/run_council.py --query-file question.txt
```

Agent prompt examples:

```text
Ask the council: Should I use Redis or Memcached?
```

```text
Use $llm-council-skill to compare model perspectives on this design.
```

## Setup

```bash
cp .env.example .env
# Add OPENROUTER_API_KEY
uv sync
```

## Validation

```bash
uv run python test_structure.py
```

The CLI smoke test requires a real OpenRouter key:

```bash
uv run python scripts/run_council.py "What is 2+2?" --stages 1
```

## Output Shape

```json
{
  "query": "...",
  "models": ["model1", "model2", "model3"],
  "chairman_model": "chairman",
  "stage1": [{"model": "model1", "response": "..."}],
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

## Credits

Original LLM Council by Andrej Karpathy. Extracted and adapted as a portable Agent Skill.
