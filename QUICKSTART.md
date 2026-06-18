# Quick Start Guide

Get the LLM Council skill running in 3 steps.

## 1. Add API Key

```bash
cd ~/s/llm-council-skill
cp .env.example .env
```

Edit `.env` and add your OpenRouter API key:
```
OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxxx
```

Get a key at: https://openrouter.ai/keys

## 2. Install Dependencies

```bash
uv sync
```

## 3. Run Your First Council

```bash
# Quick test (stage 1 only, ~5 seconds)
uv run python council_run.py "What is 2+2?" --stages 1

# Full deliberation (~30 seconds)
uv run python council_run.py "What is the CAP theorem?"
```

## Using from Claude Code

From any Claude Code session:

```
Ask the council: Should I use Redis or Memcached for session storage?
```

Or invoke directly:
```
/llm-council
```

## Common Commands

```bash
# Stage 1 only (fast comparison)
uv run python council_run.py "Your question" --stages 1

# Custom models
uv run python council_run.py "Your question" \
  --models "openai/gpt-4o,anthropic/claude-sonnet-4"

# From file
uv run python council_run.py --query-file question.txt

# See all options
uv run python council_run.py --help
```

## Troubleshooting

**"Error: Must provide query argument"**
→ Add a question in quotes: `council_run.py "your question"`

**"Authentication failed"**
→ Check your `.env` file has `OPENROUTER_API_KEY=...`

**"All models failed to respond"**
→ Check your internet connection and API key validity

**Import errors**
→ Run `uv sync` to install dependencies

## What Happens

1. **Stage 1:** Queries 3 models in parallel → individual responses
2. **Stage 2:** Each model ranks anonymized responses → aggregate rankings
3. **Stage 3:** Chairman synthesizes everything → final answer

Output is JSON to stdout. Progress messages go to stderr.

## Default Models

**Council:** GPT-5.5, Gemini Pro (latest), Claude Opus 4.8  
**Chairman:** Claude Opus 4.8

Override with `--models` and `--chairman` flags.

## Performance

- **Stage 1 only:** ~5 seconds
- **Full (stages 1-3):** ~30 seconds
- Runs in parallel where possible

## Learn More

- `README.md` — Full documentation
- `CLAUDE.md` — Technical details
- `.claude/skills/llm-council/SKILL.md` — Skill definition
- `SUMMARY.md` — Implementation overview
