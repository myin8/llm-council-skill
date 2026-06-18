# Installation Guide

## Quick Install

```bash
# 1. Clone the repository
git clone <repository-url> ~/s/llm-council-skill
cd ~/s/llm-council-skill

# 2. Create environment file
cp .env.example .env
# Edit .env and add your OPENROUTER_API_KEY

# 3. Install dependencies
uv sync
```

## Installation Methods

### Method 1: UV (Recommended)

```bash
cd ~/s/llm-council-skill
uv sync
```

This creates a virtual environment and installs all dependencies.

### Method 2: pip

```bash
cd ~/s/llm-council-skill
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Method 3: System-wide Install

```bash
cd ~/s/llm-council-skill
pip install -e .
```

This installs the package in editable mode system-wide.

## Verify Installation

```bash
# Quick test (Stage 1 only, fast)
uv run python council_run.py "What is 2+2?" --stages 1

# Full 3-stage test
uv run python council_run.py "Explain the CAP theorem"
```

Expected output: JSON structure with stage1, stage2, and stage3 keys.

## Claude Code Integration

The skill is automatically available if installed at `~/s/llm-council-skill/`.

Invoke with:
- "Ask the council: [your question]"
- "Run a council deliberation on [topic]"  
- `/llm-council`

## Troubleshooting

### Missing API Key

Error: `OPENROUTER_API_KEY not found in environment`

**Solution:** Create `.env` file with your key:
```bash
echo "OPENROUTER_API_KEY=your_key_here" > .env
```

### Import Errors

Error: `ModuleNotFoundError: No module named 'httpx'`

**Solution:** Install dependencies:
```bash
uv sync
```

### Permission Errors

Error: `Permission denied: council_run.py`

**Solution:** Make the script executable:
```bash
chmod +x council_run.py
```

## OpenRouter API Key

Get your API key from: https://openrouter.ai/keys

Free tier includes:
- $5 credit for new users
- Access to 100+ models
- No credit card required initially

## Requirements

- Python 3.10 or higher
- OpenRouter API key
- Internet connection for API calls

## Directory Structure

```
~/s/llm-council-skill/
├── .claude/
│   └── skills/
│       └── llm-council/
│           └── SKILL.md          # Skill definition for Claude Code
├── council/
│   ├── __init__.py
│   ├── config.py                 # Default models and configuration
│   ├── openrouter.py             # OpenRouter API client
│   └── deliberate.py             # 3-stage orchestration logic
├── council_run.py                # CLI entry point
├── pyproject.toml                # Python project metadata
├── .env.example                  # Environment template
├── .env                          # Your API key (gitignored)
└── README.md                     # Project overview
```

## Next Steps

After installation:

1. **Test the CLI directly:**
   ```bash
   uv run python council_run.py "Your question here"
   ```

2. **Use from Claude Code:**
   - Open Claude Code
   - Type: "Ask the council: What is machine learning?"
   - Claude will run the skill and present formatted results

3. **Customize models:**
   - Edit `council/config.py` for different default models
   - Or use `--models` flag for per-query overrides

4. **Read the docs:**
   - `QUICKSTART.md` — Usage examples
   - `CLAUDE.md` — Architecture and design decisions
   - `COMPARISON.md` — Differences from original web app
