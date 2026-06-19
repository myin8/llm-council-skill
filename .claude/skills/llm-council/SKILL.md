---
name: llm-council
description: Run multi-model LLM council deliberations through OpenRouter. Use when the user asks for a council, multi-model comparison, peer-ranked model perspectives, or a synthesized answer that should combine several model responses.
license: MIT
compatibility: Requires Python 3.10+, project dependencies, OPENROUTER_API_KEY, and network access to OpenRouter.
metadata:
  version: "1.2.0"
---

# LLM Council

This is the Claude compatibility entry point. The canonical Agent Skill is the repository-root `SKILL.md`, which follows the Agent Skills specification for Codex and other coding agents.

Run a three-stage multi-model deliberation process where different LLMs collaboratively answer a user's question.

## Process

- Stage 1: query multiple models independently with the same question.
- Stage 2: ask models to evaluate and rank anonymized Stage 1 responses.
- Stage 3: ask a chairman model to synthesize the responses and rankings.

## Usage

Start from the repository root, then run:

```bash
uv run python scripts/run_council.py "<user's question>" [options]
```

If this compatibility skill was loaded from `.claude/skills/llm-council`, the repository root is three directories up from this file.

## Options

- `--stages N` — Run only stages 1 through N (default: 3)
  - `--stages 1` — Quick comparison of model responses (no ranking)
  - `--stages 2` — Include peer evaluation and ranking
  - `--stages 3` — Full deliberation with final synthesis

- `--models MODEL1,MODEL2,...` — Override default council models (comma-separated OpenRouter IDs)

- `--chairman MODEL` — Override default chairman model

- `--query-file FILE` — Read query from file (for longer prompts)

## Output Format

The script outputs structured JSON to stdout:

```json
{
  "query": "...",
  "models": ["model1", "model2", ...],
  "chairman_model": "...",
  "stage1": [
    {"model": "model1", "response": "..."}
  ],
  "stage2": {
    "evaluations": [
      {"model": "...", "evaluation": "...", "parsed_ranking": ["Response C", "Response A", "Response B"]}
    ],
    "label_to_model": {"Response A": "model1"},
    "aggregate_rankings": [
      {"model": "...", "average_rank": 1.33, "rankings_count": 3}
    ]
  },
  "stage3": {
    "model": "...",
    "synthesis": "..."
  }
}
```

## Agent Role

1. **Run the script** with the user's question
2. **Parse the JSON** result
3. **Present findings** based on what the user asked for:
   - If they want the final answer: show `stage3.synthesis`
   - If they want to see all perspectives: show stage1 responses
   - If they want rankings: show `stage2.aggregate_rankings`
   - Default: show synthesis + aggregate rankings in a readable format

### Example Presentation Format

```markdown
## Council Synthesis

[stage3.synthesis content]

## Model Rankings (by peer evaluation)

1. **[model]** — Average rank: [avg_rank] ([rankings_count] votes)
2. **[model]** — Average rank: [avg_rank] ([rankings_count] votes)
3. **[model]** — Average rank: [avg_rank] ([rankings_count] votes)
```

## Edge Cases

- If the script fails (non-zero exit), check stderr for errors
- If `"error"` key exists in JSON, report it to the user
- If only stage1 is requested, rankings/synthesis won't be present
- Empty responses mean model API calls failed (graceful degradation)

## Environment Setup

The skill requires `OPENROUTER_API_KEY` in the environment or in a `.env` file at the repository root. If missing, the script will fail with an authentication error.

## Quick Test

To verify setup:
```bash
uv run python scripts/run_council.py "What is 2+2?" --stages 1
```

Should return JSON with stage1 containing 3 model responses.

## When to Use

- User wants multiple AI perspectives on a complex question
- User wants to see which models perform best on a specific query
- User wants a synthesized answer that considers multiple viewpoints
- User explicitly asks for "council", "multi-model", or "deliberation"

## When NOT to Use

- Simple factual lookups (single model is faster)
- Tasks requiring tool use or code execution
- Real-time or latency-sensitive queries (council is slower)
- Questions that don't benefit from multiple perspectives
