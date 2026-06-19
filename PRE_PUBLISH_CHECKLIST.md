# Pre-Publish Checklist

## Metadata

- [ ] `pyproject.toml` has final package version.
- [ ] `pyproject.toml` has final author metadata.
- [ ] `LICENSE` has final copyright holder.
- [ ] Repository URLs point to the final GitHub repository.

## Agent Skill Files

- [ ] Root `SKILL.md` exists and uses `name: llm-council-skill`.
- [ ] Root `SKILL.md` description explains what the skill does and when to use it.
- [ ] Root `SKILL.md` declares runtime requirements in `compatibility`.
- [ ] `scripts/run_council.py` runs `--help` without requiring an API key.
- [ ] `agents/openai.yaml` has display name, short description, and default prompt.
- [ ] `.claude/skills/llm-council/SKILL.md` remains a compatibility mirror.

## Validation

```bash
uv run python test_structure.py
uv build
```

With a real OpenRouter key:

```bash
uv run python scripts/run_council.py "What is 2+2?" --stages 1
```

## Package Inspection

- [ ] Built package includes `SKILL.md`.
- [ ] Built package includes `agents/openai.yaml`.
- [ ] Built package includes `scripts/run_council.py`.
- [ ] Built package includes `.claude/skills/llm-council/SKILL.md`.
- [ ] Built package includes the `council` module and `council_run.py`.

## Release Notes

- [ ] Changelog mentions Agent Skills compatibility.
- [ ] README explains both CLI use and Agent Skill use.
- [ ] INSTALL explains the root skill directory.
