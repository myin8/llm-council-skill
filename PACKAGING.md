# Packaging as a Claude Code Skill

## Current Structure

This repository is already packaged as a Claude Code skill with:

1. **Skill Definition:** `.claude/skills/llm-council/SKILL.md`
   - Defines triggers, usage, and presentation format
   - Instructs Claude Code how to invoke and parse results

2. **Python Package:** `pyproject.toml` + `council/` module
   - Standard Python package structure
   - Dependencies: httpx, python-dotenv
   - CLI entry point: `council_run.py`

3. **Documentation:**
   - `README.md` — Overview and quick start
   - `CLAUDE.md` — Architecture and design decisions
   - `INSTALL.md` — Installation instructions
   - `QUICKSTART.md` — Usage examples

## Skill Directory Structure

```
.claude/
└── skills/
    └── llm-council/
        └── SKILL.md              # Skill definition with frontmatter
```

The `SKILL.md` frontmatter follows Claude Code conventions:

```yaml
---
skill: llm-council
version: 1.0.0
description: Multi-model deliberation system where LLMs collaboratively answer questions through 3 stages
triggers:
  - "ask the council"
  - "council deliberation"
  - "/llm-council"
---
```

## Distribution Options

### Option 1: Git Repository (Current)

Users clone the entire repository to `~/s/llm-council-skill/`:

```bash
git clone <repo-url> ~/s/llm-council-skill
cd ~/s/llm-council-skill
cp .env.example .env
# Add OPENROUTER_API_KEY to .env
uv sync
```

**Pros:**
- Simple installation
- Easy updates with `git pull`
- Full source code available

**Cons:**
- Requires Git
- User must place in specific directory

### Option 2: PyPI Package (Future)

Publish to PyPI as `llm-council-skill`:

```bash
pip install llm-council-skill
```

**Pros:**
- Standard Python package installation
- Version management via pip/uv
- No Git required

**Cons:**
- Still need `.claude/skills/` directory in project
- API key configuration required post-install

### Option 3: Claude Code Plugin Registry (Future)

If Claude Code adds a plugin/skill registry:

```bash
claude skill install llm-council
```

**Pros:**
- One-command install
- Automatic placement in correct directory
- Version management built-in

**Cons:**
- Requires official Claude Code plugin system
- Not available yet

## Current Recommended Distribution

**Ship as a Git repository** with:

1. Clone instructions in README
2. Installation script (optional):

```bash
#!/bin/bash
# install.sh
set -e

INSTALL_DIR="${HOME}/s/llm-council-skill"

echo "Installing LLM Council Skill to ${INSTALL_DIR}"

# Clone or update
if [ -d "${INSTALL_DIR}" ]; then
    echo "Directory exists, pulling latest changes..."
    cd "${INSTALL_DIR}"
    git pull
else
    echo "Cloning repository..."
    git clone <repo-url> "${INSTALL_DIR}"
    cd "${INSTALL_DIR}"
fi

# Setup environment
if [ ! -f .env ]; then
    cp .env.example .env
    echo "Created .env file. Please add your OPENROUTER_API_KEY."
fi

# Install dependencies
echo "Installing dependencies..."
uv sync

echo "Installation complete!"
echo "Add your OPENROUTER_API_KEY to ${INSTALL_DIR}/.env"
echo "Test with: cd ${INSTALL_DIR} && uv run python council_run.py 'What is 2+2?' --stages 1"
```

## File Checklist for Distribution

- [x] `.claude/skills/llm-council/SKILL.md` — Skill definition
- [x] `council/` — Python package with core logic
- [x] `council_run.py` — CLI entry point
- [x] `pyproject.toml` — Python project metadata
- [x] `requirements.txt` — pip-compatible dependencies
- [x] `.env.example` — Environment template
- [x] `.gitignore` — Excludes .env, __pycache__, etc.
- [x] `README.md` — Project overview
- [x] `INSTALL.md` — Installation guide
- [x] `QUICKSTART.md` — Usage examples
- [x] `CLAUDE.md` — Architecture documentation
- [x] `LICENSE` — (Optional) License file
- [ ] `CHANGELOG.md` — Version history
- [ ] `CONTRIBUTING.md` — (Optional) Contribution guidelines

## Publishing to PyPI (Optional)

If you want to publish to PyPI:

1. **Build the package:**
   ```bash
   uv build
   ```

2. **Upload to PyPI:**
   ```bash
   uv publish
   ```

3. **Users install with:**
   ```bash
   pip install llm-council-skill
   ```

**Note:** The `.claude/skills/` directory still needs to be in a Claude Code project for the skill to be discoverable.

## Skill Versioning

Version in three places:
1. `pyproject.toml` — `version = "1.0.0"`
2. `.claude/skills/llm-council/SKILL.md` — `version: 1.0.0`
3. `CHANGELOG.md` — Version history

Keep them synchronized.

## Testing the Package

Before distribution:

```bash
# Test CLI directly
uv run python council_run.py "Test question" --stages 1

# Test as installed package
uv pip install -e .
python -c "from council import run_full_council; print('Import OK')"

# Test skill invocation (from Claude Code)
# Type: "ask the council: What is 2+2?"
```

## Distribution Checklist

Before releasing:

- [ ] All tests pass
- [ ] Documentation is complete and accurate
- [ ] `.env.example` has clear instructions
- [ ] Version numbers are synchronized
- [ ] CHANGELOG.md is updated
- [ ] README.md has installation instructions
- [ ] License file is included (if open source)
- [ ] Repository is tagged with version (e.g., `v1.0.0`)

## Updates and Maintenance

For users to update:

```bash
cd ~/s/llm-council-skill
git pull
uv sync  # Update dependencies if changed
```

For maintainers:

1. Make changes
2. Update version in `pyproject.toml` and `SKILL.md`
3. Update `CHANGELOG.md`
4. Commit and tag: `git tag v1.1.0`
5. Push: `git push && git push --tags`
