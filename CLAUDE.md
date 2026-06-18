# CLAUDE.md - LLM Council Skill

## Project Overview

This is a Claude Code skill that extracts the core deliberation logic from the [LLM Council web app](https://github.com/karpathy/llm-council). It's a CLI tool that runs 3-stage multi-model deliberation and returns structured JSON.

## Architecture

**Stateless design:** No storage, no web framework, no UI. Pure orchestration logic + CLI wrapper.

**3-Stage Process:**
1. Stage 1: Parallel queries to N council models
2. Stage 2: Anonymized peer ranking (prevents model bias)
3. Stage 3: Chairman synthesis of all responses + rankings

**Key Components:**

- `council/deliberate.py` — Core orchestration (adapted from original `backend/council.py`)
  - All functions accept optional `models` and `chairman_model` params
  - Defaults to config values if not provided
  - `run_full_council()` orchestrates all stages and returns structured dict
  
- `council/openrouter.py` — Thin async HTTP client for OpenRouter API
  - `query_model()` — Single model query
  - `query_models_parallel()` — Parallel queries via `asyncio.gather()`
  
- `council/config.py` — Default model lists + API key loading
  - Uses `python-dotenv` for `.env` file
  
- `council_run.py` — CLI entry point
  - Takes query via CLI arg or `--query-file`
  - Accepts `--models`, `--chairman`, `--stages` overrides
  - Outputs JSON to stdout, progress to stderr

## Design Decisions

### Why OpenRouter?

Single API for 100+ models from multiple providers (OpenAI, Anthropic, Google, Meta, X.AI, etc.). Avoids managing multiple API keys. Cost tracking and rate limiting built-in.

### Why Async?

The bottleneck is API latency (1-10s per model). Parallel queries cut total time from sum(latencies) to max(latencies). A 3-model council goes from ~15s sequential to ~5s parallel.

### Why Anonymization in Stage 2?

Without it, models exhibit clear favoritism (e.g., GPT models ranking other GPT responses higher regardless of quality). Anonymous labels ("Response A", "Response B") force objective evaluation.

### Why Parameterized Functions?

Original web app hardcoded models in config. The skill needs runtime flexibility (user can say "use these 5 models" without editing config). Functions accept optional params, fall back to defaults. Clean backward compatibility.

## JSON Output Structure

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
    "label_to_model": {"Response A": "model1", "Response B": "model2", "Response C": "model3"},
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

**Partial runs:** With `--stages 1`, only `stage1` is populated. With `--stages 2`, `stage1` + `stage2`.

## Skill Integration

The `.claude/skills/llm-council/SKILL.md` instructs Claude Code to:
1. Run `council_run.py` with user's query
2. Parse JSON from stdout
3. Present results based on user intent:
   - Default: Show synthesis + aggregate rankings
   - On request: Show stage1 responses, stage2 evaluations, or raw JSON

## Environment Setup

Required: `OPENROUTER_API_KEY` in `.env` file at project root.

```bash
cp .env.example .env
# Edit .env and add your key
```

## Testing

**Quick stage 1 test (fast, verifies connectivity):**
```bash
cd ~/s/llm-council-skill
uv run python council_run.py "What is 2+2?" --stages 1
```

**Full 3-stage test:**
```bash
uv run python council_run.py "Explain the CAP theorem"
```

**Custom models:**
```bash
uv run python council_run.py "Compare Python vs Go" \
  --models "openai/gpt-4o,anthropic/claude-sonnet-4"
```

## Error Handling

- If all models fail in Stage 1, JSON contains `"error": "All models failed to respond..."`
- If individual models fail, they're silently excluded (graceful degradation)
- Script exits with code 1 on fatal errors (empty query, missing API key, etc.)

## Performance

Typical timings (3 models):
- Stage 1: ~5-10s (limited by slowest model)
- Stage 2: ~8-15s (models read all Stage 1 responses + evaluate)
- Stage 3: ~5-10s (chairman reads everything)

**Total:** ~20-35s for full 3-stage deliberation. Use `--stages 1` for quick 5s comparisons.

## Differences from Original Web App

| Original | Skill Version |
|----------|---------------|
| FastAPI + React UI | CLI + JSON output |
| Hardcoded models in config | Parameterized (overridable via CLI) |
| Persistent storage (`data/conversations/`) | Stateless (no storage) |
| Streaming SSE responses | Batch JSON output |
| Title generation for conversations | N/A (single-query tool) |
| Multi-message conversation threads | One-shot Q&A |

## Dependencies

Minimal — only what's needed:
- `httpx` — Async HTTP client
- `python-dotenv` — `.env` file loading

**Not needed:** FastAPI, uvicorn, pydantic, or any web framework. This is pure logic + CLI.

## Future Enhancements

- Streaming output (emit stages as they complete)
- Configurable timeout per model
- Support for reasoning models (o1, etc.) with special handling
- Caching of Stage 1 responses for multiple Stage 2 experiments
- Parallel chairman synthesis (multiple chairmen vote on final answer)
