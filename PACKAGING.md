# Packaging as an Agent Skill

This repository is packaged as a portable Agent Skill.

## Canonical Structure

```text
llm-council-skill/
├── SKILL.md                     # Required Agent Skills entry point
├── agents/openai.yaml           # Codex/OpenAI UI metadata
├── .claude/skills/llm-council/  # Legacy Claude compatibility mirror
├── scripts/run_council.py       # Bundled script entry point
├── council/
├── council_run.py
└── pyproject.toml
```

The root `SKILL.md` uses the Agent Skills frontmatter fields:

```yaml
name: llm-council-skill
description: Run multi-model LLM council deliberations through OpenRouter...
license: MIT
compatibility: Requires Python 3.10+, project dependencies, OPENROUTER_API_KEY, and network access to OpenRouter.
metadata:
  version: "1.2.0"
```

The skill name matches the repository directory name, as required by the public specification.

## Distribution Options

### Git Repository

```bash
git clone https://github.com/myin8/llm-council-skill ~/.local/share/llm-council-skill
cd ~/.local/share/llm-council-skill
cp .env.example .env
uv sync
```

### Python Package

```bash
pip install llm-council-skill
llm-council "What is the CAP theorem?"
```

Python packaging is useful for the CLI, but agents should still receive the full skill folder so they can read `SKILL.md` and bundled resources.

## Validation

```bash
uv run python test_structure.py
```

## Release Checklist

- [ ] Root `SKILL.md` validates.
- [ ] Compatibility `.claude/skills/llm-council/SKILL.md` validates.
- [ ] `scripts/run_council.py` delegates to the CLI and preserves JSON stdout.
- [ ] `agents/openai.yaml` matches the root skill.
- [ ] `pyproject.toml` and `MANIFEST.in` include skill metadata.
- [ ] README and install instructions refer to Agent Skills, not a single agent product.
- [ ] CLI smoke test passes with a real `OPENROUTER_API_KEY`.
