# Packaging Status

The LLM Council repository is now packaged as a portable Agent Skill rather than a Claude-only skill.

## Current Layout

```text
llm-council-skill/
├── SKILL.md
├── agents/openai.yaml
├── .claude/skills/llm-council/SKILL.md
├── scripts/run_council.py
├── council/
├── council_run.py
├── pyproject.toml
└── MANIFEST.in
```

## Compatibility

- Codex and other Agent Skills clients should use the repository-root `SKILL.md`.
- Codex/OpenAI UI metadata is in `agents/openai.yaml`.
- The bundled script entry point is `scripts/run_council.py`.
- Older Claude-specific clients can use `.claude/skills/llm-council/SKILL.md`.

## Verification

Run:

```bash
uv run python test_structure.py
```

Run the CLI smoke test only when `OPENROUTER_API_KEY` is configured:

```bash
uv run python scripts/run_council.py "What is 2+2?" --stages 1
```
