# Project Notes - LLM Council Agent Skill

## Project Overview

This repository is a portable Agent Skill that extracts the core deliberation logic from the [LLM Council web app](https://github.com/karpathy/llm-council). It provides a CLI that runs three-stage multi-model deliberation and returns structured JSON.

The canonical skill entry point is the repository-root `SKILL.md`. The `.claude/skills/llm-council/SKILL.md` file is a compatibility mirror for older Claude-specific skill loaders.

## Architecture

**Stateless design:** no storage, web framework, or UI. The repository contains orchestration logic plus a CLI wrapper.

**Three-stage process:**

1. Stage 1: parallel queries to council models.
2. Stage 2: anonymized peer ranking to reduce model-name bias.
3. Stage 3: chairman synthesis of responses and rankings.

## Key Components

- `SKILL.md` - Agent Skills spec entry point for Codex and other compatible agents.
- `agents/openai.yaml` - Codex/OpenAI UI metadata.
- `.claude/skills/llm-council/SKILL.md` - legacy Claude compatibility mirror.
- `council/deliberate.py` - core orchestration.
- `council/openrouter.py` - async HTTP client for OpenRouter.
- `council/config.py` - default model list and API key loading.
- `council_run.py` - CLI entry point.

## Design Decisions

### Why OpenRouter?

OpenRouter provides one API for models from multiple providers, which keeps the skill portable and avoids provider-specific key handling inside the runner.

### Why async?

API latency is the bottleneck. Parallel stage 1 and stage 2 calls reduce wall-clock time from the sum of model latencies to roughly the slowest model call in each stage.

### Why anonymized ranking?

Without anonymization, models can rank familiar provider or model names more favorably. Anonymous labels such as `Response A` and `Response B` push the review toward the response content.

### Why parameterized functions?

The CLI and skill need runtime flexibility. Users can override the council and chairman models without editing source files, while the Python functions keep defaults for simple calls.

## JSON Output

```json
{
  "query": "...",
  "models": ["model1", "model2", "model3"],
  "chairman_model": "chairman_model",
  "stage1": [
    {"model": "...", "response": "..."}
  ],
  "stage2": {
    "evaluations": [
      {"model": "...", "evaluation": "...", "parsed_ranking": ["Response C", "Response A", "Response B"]}
    ],
    "label_to_model": {"Response A": "model1"},
    "aggregate_rankings": [
      {"model": "model1", "average_rank": 1.33, "rankings_count": 3}
    ]
  },
  "stage3": {
    "model": "chairman_model",
    "synthesis": "..."
  }
}
```

With `--stages 1`, only `stage1` is populated. With `--stages 2`, `stage1` and `stage2` are populated.

## Environment Setup

Required: `OPENROUTER_API_KEY` in the environment or in `.env` at the project root.

```bash
cp .env.example .env
# Edit .env and add your key
```

## Testing

```bash
uv run python test_structure.py
uv run python scripts/run_council.py "What is 2+2?" --stages 1
```

The final command requires a valid OpenRouter key.

## Dependencies

- `httpx` - async HTTP client.
- `python-dotenv` - `.env` loading.
