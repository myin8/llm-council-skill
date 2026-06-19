---
name: llm-council
description: "Run questions through a council of multiple LLMs that independently respond, peer-review each other anonymously, and synthesize a final verdict. Use when: (1) a decision has real stakes and uncertainty, (2) the user asks for 'council', 'multi-model comparison', 'peer-ranked perspectives', or 'what would different models say', (3) exploring tradeoffs or design decisions. Do NOT use for: simple factual lookups, creative tasks, or questions where a single model is sufficient."
license: MIT
compatibility: Requires Python 3.10+, project dependencies, OPENROUTER_API_KEY, and network access to OpenRouter.
metadata:
  version: "1.3.0"
---

# LLM Council

**Note:** This is the Claude compatibility entry point. The canonical Agent Skill is the repository-root `SKILL.md`, which follows the Agent Skills specification for Codex and other coding agents.

Run a three-stage multi-model deliberation process where different LLMs collaboratively answer a user's question through independent responses, anonymous peer review, and synthesis.

## When to Use

**Good council questions:**
- "Should I use Postgres or DynamoDB for this use case?"
- "Which of these 3 API designs is strongest?"
- "Compare these model outputs — which is more accurate?"
- "I'm torn between X and Y. What am I not seeing?"

**Skip the council for:**
- Factual lookups ("What is X?")
- Creative tasks ("Write me a landing page")
- Simple style preferences
- Questions with one right answer

## Process

- **Stage 1:** Query multiple models independently with the same question
- **Stage 2:** Models evaluate and rank anonymized Stage 1 responses
- **Stage 3:** Chairman model synthesizes responses and rankings into final verdict

## Usage

Start from the repository root (three directories up from this file if loaded from `.claude/skills/llm-council`):

```bash
uv run python scripts/run_council.py "<user's question>" [options]
```

### Options

- `--stages N` — Run only stages 1 through N (default: 3)
  - `--stages 1` — Quick comparison (no ranking or synthesis)
  - `--stages 2` — Include peer ranking
  - `--stages 3` — Full deliberation with synthesis
- `--models MODEL1,MODEL2,...` — Override default council models (comma-separated OpenRouter IDs)
- `--chairman MODEL` — Override default chairman model
- `--query-file FILE` — Read query from file (for longer prompts)

## Output Format

The script returns JSON:

```json
{
  "query": "...",
  "models": ["model1", "model2", ...],
  "chairman_model": "...",
  "stage1": [{"model": "...", "response": "..."}],
  "stage2": {
    "evaluations": [...],
    "label_to_model": {...},
    "aggregate_rankings": [{"model": "...", "average_rank": 1.5, "rankings_count": 3}]
  },
  "stage3": {"model": "...", "synthesis": "..."}
}
```

## Presenting Results

**Do not dump raw JSON.** Structure the verdict:

```markdown
## Council Verdict: {topic}

### Where Models Agree
{Independent convergence points — high-confidence signals}

### Where Models Disagree
{Genuine conflicts with reasoning from both sides}

### Model Rankings (by Peer Review)
1. **{model}** — Avg rank: {average_rank} ({rankings_count} votes)
2. ...

### Synthesis
{stage3.synthesis content}

### Recommended Next Step
{One concrete action, if applicable}
```

**Rules:**
- Don't invent missing stages (if only stage 1 was run, don't make up synthesis)
- Highlight disagreements (conflicts are signal, not noise)
- Be concise (clarity over completeness)

## Environment Setup

Requires `OPENROUTER_API_KEY` in environment or `.env` at repository root.

## Quick Test

```bash
uv run python scripts/run_council.py "What is 2+2?" --stages 1
```

Returns JSON with stage1 containing model responses.

## When to Use vs Single Model

**Use the council when:**
- Decision has real stakes and uncertainty
- User explicitly requests "council", "multi-model", or "compare models"
- Exploring tradeoffs where different perspectives add value

**Use single model when:**
- Factual lookup with one right answer
- Creative/generative task (not a decision)
- Speed matters (council is slower)
- No meaningful tradeoffs to explore

If unsure, default to single model. Only invoke council when explicitly requested or when a genuine decision warrants multiple perspectives.

## Edge Cases

- **Script fails:** Report stderr error
- **JSON has `error` key:** Surface directly
- **Partial stages:** Don't fabricate missing synthesis/rankings
- **Model failures:** Present successful responses only
