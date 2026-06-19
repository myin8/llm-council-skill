---
name: llm-council-skill
description: Run multi-model LLM council deliberations through OpenRouter. Use when the user asks for a council, multi-model comparison, peer-ranked model perspectives, or a synthesized answer that should combine several model responses.
license: MIT
compatibility: Requires Python 3.10+, project dependencies, OPENROUTER_API_KEY, and network access to OpenRouter.
metadata:
  version: "1.2.0"
---

# LLM Council

Run a three-stage deliberation process where several language models answer a question, rank anonymized peer responses, and produce a final synthesis.

## Requirements

- Python 3.10 or newer.
- Project dependencies installed with `uv sync` or `pip install -r requirements.txt`.
- `OPENROUTER_API_KEY` set in the environment or in `.env` at the skill root.
- Network access to OpenRouter.

## Workflow

1. Start from the skill root, the directory containing this `SKILL.md`.
2. If dependencies are missing, run `uv sync`.
3. Run the bundled script:

```bash
uv run python scripts/run_council.py "<user question>"
```

For long prompts, write the prompt to a file and run:

```bash
uv run python scripts/run_council.py --query-file question.txt
```

The script delegates to `council_run.py`, preserves JSON on stdout, and sends progress or errors to stderr.

## Options

- `--stages 1` for independent model responses only.
- `--stages 2` to include anonymized peer ranking.
- `--stages 3` for the full flow with chairman synthesis. This is the default.
- `--models MODEL1,MODEL2,...` to override the default OpenRouter council models.
- `--chairman MODEL` to override the synthesis model.

If installed as a Python package, the console script is also available:

```bash
llm-council "<user question>" --stages 1
```

## Output Handling

The command writes progress to stderr and structured JSON to stdout:

- `stage1`: model responses.
- `stage2.evaluations`: peer-review text and parsed rankings.
- `stage2.aggregate_rankings`: average model rankings.
- `stage3.synthesis`: final synthesized answer.

Present the result based on user intent:

- For a final answer, show `stage3.synthesis` and a brief ranking summary.
- For "compare models" requests, show the stage 1 responses and aggregate rankings.
- For debugging or audit requests, show the relevant JSON fields or the raw JSON.

## Edge Cases

- If the command exits non-zero, report the stderr error and ask for the missing prerequisite only if it cannot be fixed from the repo.
- If the JSON contains an `error` key, surface it directly.
- If only stage 1 or 2 was requested, do not invent missing synthesis or rankings.
- If individual model calls fail, the runner may degrade gracefully with fewer responses.
