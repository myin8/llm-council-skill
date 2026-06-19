# Quick Start

Get the LLM Council Agent Skill running in three steps.

## 1. Add API Key

```bash
cd ~/.local/share/llm-council-skill
cp .env.example .env
```

Edit `.env` and add your OpenRouter API key:

```text
OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxxx
```

## 2. Install Dependencies

```bash
uv sync
```

## 3. Run the Council

```bash
uv run python scripts/run_council.py "What is 2+2?" --stages 1
uv run python scripts/run_council.py "What is the CAP theorem?"
```

## Agent Usage

Agents that support the Agent Skills format should discover the root `SKILL.md`.

Example prompts:

```text
Ask the council: Should I use Redis or Memcached for session storage?
```

```text
Use $llm-council-skill to compare model perspectives on this architecture decision.
```

Older Claude-specific loaders can use `.claude/skills/llm-council/SKILL.md`, which mirrors the root skill instructions.

## Common Commands

```bash
uv run python scripts/run_council.py "Your question" --stages 1
uv run python scripts/run_council.py "Your question" \
  --models "openai/gpt-4o,anthropic/claude-sonnet-4"
uv run python scripts/run_council.py --query-file question.txt
uv run python scripts/run_council.py --help
```

## Troubleshooting

**"Error: Must provide query argument"**

Add a question in quotes: `uv run python scripts/run_council.py "your question"`.

**"Authentication failed" or missing API key**

Check that `.env` has `OPENROUTER_API_KEY=...`.

**"All models failed to respond"**

Check your internet connection, OpenRouter account, API key, and selected model IDs.

**Import errors**

Run `uv sync` to install dependencies.
