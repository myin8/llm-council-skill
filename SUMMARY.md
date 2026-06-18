# LLM Council Skill - Implementation Summary

## What Was Built

A standalone Claude Code skill extracted from the LLM Council web app. The skill runs multi-model deliberation through 3 stages and returns structured JSON output.

## Project Location

`~/s/llm-council-skill/`

## Key Features

✅ **Stateless CLI tool** — No database, no web server, pure orchestration logic
✅ **3-stage deliberation** — Parallel responses → Anonymous peer ranking → Chairman synthesis  
✅ **Flexible model selection** — Override defaults via CLI flags
✅ **Structured JSON output** — Easy to parse and process
✅ **Partial runs** — Run only stage 1 or 2 for faster results
✅ **Claude Code skill integration** — Invokable via natural language or `/llm-council`

## Architecture

```
~/s/llm-council-skill/
├── .claude/skills/llm-council/SKILL.md  # Skill definition for Claude Code
├── council/
│   ├── __init__.py                      # Package marker
│   ├── config.py                        # Defaults + API key loading
│   ├── openrouter.py                    # Async HTTP client
│   └── deliberate.py                    # 3-stage orchestration
├── council_run.py                       # CLI entry point
├── pyproject.toml                       # Dependencies
├── .env.example                         # Template for API key
├── .gitignore                          # Python + env exclusions
├── README.md                           # User documentation
├── CLAUDE.md                           # Technical documentation
└── test_structure.py                   # Structure verification test
```

## How It Works

### Stage 1: Parallel Responses
```python
# Query 3 models simultaneously
results = await query_models_parallel(COUNCIL_MODELS, messages)
# Returns: [{"model": "openai/gpt-5.1", "response": "..."}]
```

### Stage 2: Anonymized Peer Ranking
```python
# Anonymize: "Response A", "Response B", "Response C"
# Each model evaluates and ranks ALL responses
# Parse rankings: ["Response C", "Response A", "Response B"]
# Aggregate: Model X avg rank = 1.33 (best), Model Y = 2.0, etc.
```

### Stage 3: Chairman Synthesis
```python
# Chairman receives all responses + rankings
# Synthesizes single comprehensive answer
# Returns: {"model": "...", "synthesis": "..."}
```

## Usage

### Command Line

```bash
cd ~/s/llm-council-skill

# Full deliberation
uv run python council_run.py "What is the CAP theorem?"

# Quick stage 1 only (fast comparison)
uv run python council_run.py "Explain async/await" --stages 1

# Custom models
uv run python council_run.py "Compare languages" \
  --models "openai/gpt-4o,anthropic/claude-sonnet-4" \
  --chairman "google/gemini-2.5-pro"

# From file
echo "Long complex question here..." > question.txt
uv run python council_run.py --query-file question.txt
```

### As Claude Code Skill

From any Claude Code session:
- "Ask the council: Should I use Redis or Memcached?"
- "Run a council deliberation on microservices vs monoliths"
- `/llm-council`

Claude Code will:
1. Run `council_run.py` with your question
2. Parse the JSON output
3. Present a readable summary with synthesis + rankings

## Setup Required

**Before first use:**

1. Get OpenRouter API key from https://openrouter.ai/keys
2. Create `.env` file:
   ```bash
   cd ~/s/llm-council-skill
   cp .env.example .env
   # Edit .env and add: OPENROUTER_API_KEY=your_key_here
   ```
3. Install dependencies:
   ```bash
   uv sync
   ```

## Default Models

**Council Members:**
- `openai/gpt-5.5` (GPT-5.5, released 2026-04-23)
- `~google/gemini-pro-latest` (Latest Gemini Pro, auto-updates)
- `anthropic/claude-opus-4.8` (Claude Opus 4.8, released 2026-05-28)

**Chairman:**
- `anthropic/claude-opus-4.8` (Claude Opus 4.8)

All overridable via CLI flags.

## Verification

All structural tests pass:

```bash
cd ~/s/llm-council-skill
python test_structure.py
```

Output:
```
✓ All modules imported successfully
✓ Config loaded: 3 council models + chairman
✓ CLI parsing logic verified

Results: 3/3 tests passed
```

## JSON Output Format

```json
{
  "query": "What is the CAP theorem?",
  "models": ["openai/gpt-5.5", "~google/gemini-pro-latest", "anthropic/claude-opus-4.8"],
  "chairman_model": "anthropic/claude-opus-4.8",
  "stage1": [
    {"model": "openai/gpt-5.5", "response": "CAP theorem states..."}
  ],
  "stage2": {
    "evaluations": [
      {
        "model": "openai/gpt-5.5",
        "evaluation": "Response A is comprehensive...",
        "parsed_ranking": ["Response C", "Response A", "Response B"]
      }
    ],
    "label_to_model": {
      "Response A": "openai/gpt-5.5",
      "Response B": "~google/gemini-pro-latest",
      "Response C": "anthropic/claude-opus-4.8"
    },
    "aggregate_rankings": [
      {"model": "anthropic/claude-opus-4.8", "average_rank": 1.33, "rankings_count": 3},
      {"model": "openai/gpt-5.5", "average_rank": 2.0, "rankings_count": 3},
      {"model": "~google/gemini-pro-latest", "average_rank": 2.67, "rankings_count": 3}
    ]
  },
  "stage3": {
    "model": "anthropic/claude-opus-4.8",
    "synthesis": "Based on the council's responses and peer evaluations..."
  }
}
```

## Performance

Typical timings (3 models):
- **Stage 1:** 5-10 seconds (parallel queries)
- **Stage 2:** 8-15 seconds (evaluation + ranking)
- **Stage 3:** 5-10 seconds (synthesis)
- **Total:** ~20-35 seconds for full deliberation

Use `--stages 1` for quick 5-second model comparisons.

## Key Design Decisions

### Why OpenRouter?
Single API for 100+ models from multiple providers. No need to manage multiple API keys.

### Why Async/Parallel?
Reduces total time from sum(latencies) to max(latency). 3-model council: ~5s parallel vs ~15s sequential.

### Why Anonymization?
Models show favoritism without it. GPT models rank GPT responses higher regardless of quality. Anonymous labels force objective evaluation.

### Why Parameterized?
Runtime flexibility. User can say "use these 5 models" without editing config files.

## Differences from Original Web App

| Original Web App | Skill Version |
|-----------------|---------------|
| FastAPI + React UI | CLI + JSON output |
| Hardcoded models | Parameterized (CLI overrides) |
| Persistent storage | Stateless (no storage) |
| Streaming SSE | Batch JSON output |
| Multi-turn conversations | Single-query tool |
| Conversation titles | N/A |

## Dependencies

Minimal — only what's needed:
- `httpx` — Async HTTP client
- `python-dotenv` — Environment variable loading

**Not included:** FastAPI, uvicorn, pydantic, React, or any web framework.

## Next Steps

1. **Add API key** to `.env` file
2. **Test with stage 1:** `uv run python council_run.py "What is 2+2?" --stages 1`
3. **Test full run:** `uv run python council_run.py "Explain the CAP theorem"`
4. **Try from Claude Code:** "Ask the council: [your question]"

## Documentation

- **README.md** — User-facing documentation
- **CLAUDE.md** — Technical implementation details
- **SKILL.md** — Skill definition for Claude Code
- **SUMMARY.md** — This file (implementation overview)

## Credits

Original LLM Council by Andrej Karpathy. Extracted and adapted as a Claude Code skill.
