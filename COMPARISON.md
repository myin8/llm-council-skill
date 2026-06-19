# Original Web App vs Agent Skill

## Structure

Original web app:

```text
llm-council/
├── backend/      # FastAPI backend
├── frontend/     # React frontend
└── data/         # Stored conversations
```

Agent Skill:

```text
llm-council-skill/
├── SKILL.md
├── agents/openai.yaml
├── .claude/skills/llm-council/SKILL.md
├── council/
└── council_run.py
```

## Feature Comparison

| Feature | Original web app | Agent Skill |
| --- | --- | --- |
| Core three-stage deliberation | Yes | Yes |
| Parallel queries | Yes | Yes |
| Anonymized ranking | Yes | Yes |
| Web UI | Yes | No |
| Persistent conversation history | Yes | No |
| CLI usage | No | Yes |
| JSON stdout | No | Yes |
| Model override flags | No | Yes |
| Agent Skills support | No | Yes |

## Dependencies

Original web app:

- FastAPI
- Uvicorn
- Pydantic
- React/Vite frontend packages
- `httpx`
- `python-dotenv`

Agent Skill:

- `httpx`
- `python-dotenv`

## When to Use Each

Use the original web app when you want a browser interface, conversation history, or visual tabbed comparison.

Use this Agent Skill when you want a scriptable, stateless council that a coding agent can invoke, parse, and summarize.

## Tradeoff

The Agent Skill removes the visual UI and storage layer. In exchange, it is easier to install into coding-agent workflows, easier to pipe into other tools, and has a much smaller runtime surface.
