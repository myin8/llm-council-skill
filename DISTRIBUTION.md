# Distribution Checklist

## Package Status

The repository is packaged as a portable Agent Skill with a Python CLI.

## Required Files

- [x] `SKILL.md` - canonical Agent Skills entry point.
- [x] `agents/openai.yaml` - Codex/OpenAI UI metadata.
- [x] `.claude/skills/llm-council/SKILL.md` - legacy Claude compatibility mirror.
- [x] `scripts/run_council.py` - bundled Agent Skills script entry point.
- [x] `council/` - Python package.
- [x] `council_run.py` - CLI entry point.
- [x] `pyproject.toml` - Python package metadata.
- [x] `MANIFEST.in` - package include rules.
- [x] `.env.example` - environment template.
- [x] `README.md`, `INSTALL.md`, `QUICKSTART.md`, `PACKAGING.md`.

## Distribution Methods

### Git Repository

```bash
git clone https://github.com/myin8/llm-council-skill ~/.local/share/llm-council-skill
cd ~/.local/share/llm-council-skill
cp .env.example .env
uv sync
```

### Installer

```bash
curl -fsSL https://raw.githubusercontent.com/myin8/llm-council-skill/main/install.sh | bash
```

### PyPI

```bash
pip install llm-council-skill
llm-council "What is the CAP theorem?"
```

Python packaging covers the CLI. Agent clients should still receive the full skill folder so they can read `SKILL.md` and bundled metadata.

## Pre-Publish Tasks

- [ ] Confirm GitHub repository URL.
- [ ] Update author information in `pyproject.toml` and `LICENSE`.
- [ ] Run structural validation.
- [ ] Run a stage 1 smoke test with a real OpenRouter key.
- [ ] Build the package with `uv build`.
- [ ] Confirm packaged files include `SKILL.md`, `agents/openai.yaml`, `scripts/run_council.py`, and `.claude/skills/llm-council/SKILL.md`.

## Validation Commands

```bash
uv run python test_structure.py
uv run python scripts/run_council.py "What is 2+2?" --stages 1
```

The final command requires `OPENROUTER_API_KEY`.
