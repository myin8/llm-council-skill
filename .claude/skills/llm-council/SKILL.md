---
skill: llm-council
version: 1.0.0
description: Multi-model deliberation system where LLMs collaboratively answer questions through 3 stages
triggers:
  - "ask the council"
  - "council deliberation"
  - "/llm-council"
---

# LLM Council Skill

Run a 3-stage multi-model deliberation process where different LLMs collaboratively answer a user's question.

## Process Overview

**Stage 1 - Parallel Responses:** Query multiple models independently with the same question

**Stage 2 - Anonymized Peer Review:** Each model evaluates and ranks the anonymized Stage 1 responses (prevents favoritism)

**Stage 3 - Chairman Synthesis:** A designated chairman model synthesizes all responses and rankings into a final comprehensive answer

## Usage

When the user wants a multi-model perspective on a question:

```bash
cd ~/s/llm-council-skill
uv run python council_run.py "<user's question>" [options]
```

### Options

- `--stages N` — Run only stages 1 through N (default: 3)
  - `--stages 1` — Quick comparison of model responses (no ranking)
  - `--stages 2` — Include peer evaluation and ranking
  - `--stages 3` — Full deliberation with final synthesis

- `--models MODEL1,MODEL2,...` — Override default council models (comma-separated OpenRouter IDs)
  - Default: `openai/gpt-5.1,google/gemini-3-pro-preview,anthropic/claude-sonnet-4.5`

- `--chairman MODEL` — Override default chairman model
  - Default: `google/gemini-3-pro-preview`

- `--query-file FILE` — Read query from file (for longer prompts)

### Output Format

The script outputs structured JSON to stdout:

```json
{
  "query": "...",
  "models": ["model1", "model2", ...],
  "chairman_model": "...",
  "stage1": [
    {"model": "openai/gpt-5.1", "response": "..."}
  ],
  "stage2": {
    "evaluations": [
      {"model": "...", "evaluation": "...", "parsed_ranking": ["Response C", "Response A", "Response B"]}
    ],
    "label_to_model": {"Response A": "openai/gpt-5.1", ...},
    "aggregate_rankings": [
      {"model": "...", "average_rank": 1.33, "rankings_count": 3}
    ]
  },
  "stage3": {
    "model": "google/gemini-3-pro-preview",
    "synthesis": "..."
  }
}
```

## Your Role

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

The skill requires `OPENROUTER_API_KEY` in a `.env` file in `~/s/llm-council-skill/.env`. If missing, the script will fail with an authentication error.

## Quick Test

To verify setup:
```bash
cd ~/s/llm-council-skill
uv run python council_run.py "What is 2+2?" --stages 1
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
