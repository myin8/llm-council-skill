---
name: llm-council-skill
description: "Run questions through a council of multiple LLMs that independently respond, peer-review each other anonymously, and synthesize a final verdict. Use when: (1) a decision has real stakes and uncertainty, (2) the user asks for 'council', 'multi-model comparison', 'peer-ranked perspectives', or 'what would different models say', (3) exploring tradeoffs or design decisions. Do NOT use for: simple factual lookups, creative tasks with no right answer, or questions where a single model is sufficient."
license: MIT
compatibility: Requires Python 3.10+, project dependencies, OPENROUTER_API_KEY, and network access to OpenRouter.
metadata:
  version: "1.3.0"
---

# LLM Council

Run a three-stage deliberation where multiple language models answer a question, rank each other's anonymized responses, and produce a final synthesis.

## When to Use the Council

**Good council questions** have genuine uncertainty and stakes:

- "Should I use Postgres or DynamoDB for this use case?"
- "Which of these 3 API design approaches is strongest?"
- "Is this architecture decision sound or am I missing something?"
- "Compare these model outputs — which is more accurate?"
- "I'm torn between approach X and Y. What am I not seeing?"

**Bad council questions** have one right answer or no answer at all:

- "What's the capital of France?" (factual lookup)
- "Write me a landing page" (creative task, not a decision)
- "Summarize this document" (processing task)
- "Should I use camelCase or snake_case?" (style preference)

The council shines when there's **genuine uncertainty** and **multiple reasonable perspectives** can illuminate blind spots.

## Requirements

- Python 3.10 or newer
- Project dependencies: `uv sync` or `pip install -r requirements.txt`
- `OPENROUTER_API_KEY` in environment or `.env` at skill root
- Network access to OpenRouter

## Workflow

1. Start from the skill root (the directory containing this `SKILL.md`)
2. If dependencies are missing, run `uv sync`
3. Run the council:

```bash
uv run python scripts/run_council.py "<user question>"
```

For long prompts:

```bash
uv run python scripts/run_council.py --query-file question.txt
```

The script outputs JSON to stdout and progress to stderr.

## Options

- `--stages 1` — independent model responses only (fast comparison)
- `--stages 2` — add anonymized peer ranking
- `--stages 3` — full flow with chairman synthesis (default)
- `--models MODEL1,MODEL2,...` — override default OpenRouter council models
- `--chairman MODEL` — override synthesis model

If installed as a package:

```bash
llm-council "<user question>" --stages 1
```

## Output Structure

The command returns JSON with:

- `stage1`: array of `{model, response}` objects
- `stage2.evaluations`: peer-review text and parsed rankings
- `stage2.aggregate_rankings`: models sorted by average peer rank
- `stage3.synthesis`: final synthesized answer

## Presenting Results

Format the council verdict in a structured way. Do NOT just dump JSON. Present:

### For full 3-stage council:

```markdown
## Council Verdict: {short topic}

### Where Models Agree
{Points multiple models converged on independently. High-confidence signals.}

### Where Models Disagree
{Genuine conflicts. Present both sides and why reasonable models differ.}

### Model Rankings (by Peer Review)
1. **{model}** — Avg rank: {average_rank} ({rankings_count} votes)
2. **{model}** — Avg rank: {average_rank} ({rankings_count} votes)
...

### Synthesis
{stage3.synthesis content}

### Recommended Next Step
{Extract or synthesize one concrete action from the verdict, if applicable}
```

### For stage 1 only (--stages 1):

Show each model's response with clear labels. No synthesis or rankings.

### For stage 2 (--stages 2):

Include model responses + aggregate rankings. No synthesis.

### General presentation rules:

- **Don't invent content.** If stage 3 wasn't run, don't make up a synthesis.
- **Highlight disagreements.** When models conflict, that's signal. Show both sides.
- **Surface rankings.** The peer-review rankings reveal which responses were strongest.
- **Be concise.** The user wants clarity, not a dump of all the raw text.

## Edge Cases

- **Non-zero exit:** Report stderr error. Only ask for missing prereqs if unfixable from repo.
- **JSON contains `error` key:** Surface it directly to the user.
- **Partial stage requests:** If only stage 1 or 2 was run, do not fabricate missing data.
- **Model failures:** The runner degrades gracefully with fewer responses. Present what succeeded.

## Example Invocation

User says: *"Council this: Should I use REST or GraphQL for my mobile API?"*

**You should:**

1. Check that this is a good council question (yes — genuine tradeoff with stakes)
2. Run: `uv run python scripts/run_council.py "Should I use REST or GraphQL for my mobile API?"`
3. Parse the JSON result
4. Present using the verdict format above:
   - Where models agree (e.g., both are viable)
   - Where models disagree (e.g., REST = simpler, GraphQL = more flexible)
   - Rankings (which model gave the most helpful response)
   - Synthesis (chairman's recommendation with reasoning)
   - One action (e.g., "prototype a simple endpoint in both and measure dev time")

**You should NOT:**

- Run the council on "What is REST?" (factual lookup)
- Run the council on "Write me a REST API" (creation task)
- Just show the raw JSON and say "here's what the council said"
- Make up a synthesis if only stages 1-2 were run

## When NOT to Use

Skip the council if:

- The question has one objectively correct answer
- The user is asking for content creation, not evaluation
- The user wants a quick answer (council is slower)
- The question doesn't have meaningful tradeoffs to explore

If unsure, default to a single model and only invoke the council when explicitly requested or when a genuine decision point warrants multiple perspectives.
