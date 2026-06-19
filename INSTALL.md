# Installation Guide

## Quick Install

```bash
git clone https://github.com/myin8/llm-council-skill ~/.local/share/llm-council-skill
cd ~/.local/share/llm-council-skill
cp .env.example .env
# Edit .env and add OPENROUTER_API_KEY
uv sync
```

## Installation Methods

### Method 1: uv

```bash
cd ~/.local/share/llm-council-skill
uv sync
```

### Method 2: pip

```bash
cd ~/.local/share/llm-council-skill
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Method 3: editable package

```bash
cd ~/.local/share/llm-council-skill
pip install -e .
```

This also installs the `llm-council` console script.

## Agent Skill Installation

The repository root is the skill directory because it contains the spec-compliant `SKILL.md`.

Use the whole repository as the skill folder for agents that support Agent Skills:

```text
~/.local/share/llm-council-skill/SKILL.md
```

Codex/OpenAI metadata lives in:

```text
~/.local/share/llm-council-skill/agents/openai.yaml
```

Legacy Claude-specific metadata remains in:

```text
~/.local/share/llm-council-skill/.claude/skills/llm-council/SKILL.md
```

## Verify Installation

```bash
uv run python test_structure.py
uv run python scripts/run_council.py "What is 2+2?" --stages 1
```

Expected output from the council runner is JSON with `query`, `models`, `chairman_model`, and populated stage fields for the requested stage count.

## OpenRouter API Key

The skill checks for the API key in this order:
1. **Global environment variable** (checked first)
2. **Project `.env` file** (fallback)

### Option 1: Global Environment (Recommended)

Set the key in your shell profile (`~/.bashrc`, `~/.zshrc`, etc.):

```bash
export OPENROUTER_API_KEY=your_key_here
```

This makes the key available to all projects and tools.

### Option 2: Project-Specific .env

Create `.env` in the project directory:

```bash
cd ~/.local/share/llm-council-skill
cp .env.example .env
# Edit .env and add: OPENROUTER_API_KEY=your_key_here
```

Get your key from: https://openrouter.ai/keys

## Requirements

- Python 3.10 or higher
- OpenRouter API key
- Internet connection for API calls
