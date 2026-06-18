# Pre-Publication Checklist

Complete these tasks before publishing the package.

## 1. Create GitHub Repository

- [ ] Create repository on GitHub
- [ ] Name: `llm-council-skill` (or your preferred name)
- [ ] Description: "Multi-model deliberation system for Claude Code"
- [ ] Visibility: Public
- [ ] Initialize: No (we already have code)

**Repository URL:** `https://github.com/yourusername/llm-council-skill`

## 2. Update Repository URLs

### In `install.sh` (line 8):
```bash
# Before:
REPO_URL="https://github.com/yourusername/llm-council-skill"

# After:
REPO_URL="https://github.com/ACTUAL-USERNAME/llm-council-skill"
```

### In `README.md`:

Find and replace:
```bash
# Before:
https://github.com/yourusername/llm-council-skill

# After:
https://github.com/ACTUAL-USERNAME/llm-council-skill
```

Also update the curl command:
```bash
# Before:
curl -fsSL https://raw.githubusercontent.com/yourusername/llm-council-skill/main/install.sh | bash

# After:
curl -fsSL https://raw.githubusercontent.com/ACTUAL-USERNAME/llm-council-skill/main/install.sh | bash
```

### In `pyproject.toml`:

Update the `[project.urls]` section:
```toml
[project.urls]
Homepage = "https://github.com/ACTUAL-USERNAME/llm-council-skill"
Documentation = "https://github.com/ACTUAL-USERNAME/llm-council-skill/blob/main/README.md"
Repository = "https://github.com/ACTUAL-USERNAME/llm-council-skill"
Issues = "https://github.com/ACTUAL-USERNAME/llm-council-skill/issues"
```

## 3. Update Author Information

### In `LICENSE`:
```
# Before:
Copyright (c) 2026 [Your Name]

# After:
Copyright (c) 2026 Your Actual Name
```

### In `pyproject.toml`:
```toml
# Before:
authors = [
    {name = "Your Name", email = "your.email@example.com"}
]

# After:
authors = [
    {name = "Your Actual Name", email = "your.actual@email.com"}
]
```

## 4. Test Installation Locally

Before publishing, test everything works:

```bash
# Test 1: Package imports
uv run python -c "from council import run_full_council; print('✅ Import OK')"

# Test 2: CLI help
python council_run.py --help

# Test 3: Quick run (requires OPENROUTER_API_KEY in .env)
# uv run python council_run.py "What is 2+2?" --stages 1

# Test 4: Check all docs are readable
ls -lh *.md

# Test 5: Verify .env.example exists
cat .env.example

# Test 6: Check skill definition
cat .claude/skills/llm-council/SKILL.md
```

## 5. Initialize Git (if not already done)

```bash
git init
git branch -M main
```

## 6. First Commit

```bash
git add .
git commit -m "Initial commit - LLM Council Skill v1.0.0

- Multi-model deliberation system
- 3-stage council process (parallel responses, peer ranking, synthesis)
- CLI with JSON output
- Claude Code skill integration
- Complete documentation and installation scripts"
```

## 7. Connect to GitHub

```bash
git remote add origin https://github.com/ACTUAL-USERNAME/llm-council-skill.git
```

## 8. Push to GitHub

```bash
# Push main branch
git push -u origin main

# Create and push tag
git tag -a v1.0.0 -m "Release v1.0.0 - Initial release"
git push origin v1.0.0
```

## 9. Create GitHub Release

1. Go to: `https://github.com/ACTUAL-USERNAME/llm-council-skill/releases`
2. Click "Draft a new release"
3. Choose tag: `v1.0.0`
4. Release title: `v1.0.0 - Initial Release`
5. Description:

```markdown
## LLM Council Skill v1.0.0

First stable release of the LLM Council skill for Claude Code.

### Features

- **3-Stage Deliberation:** Multiple models collaborate to answer questions
  - Stage 1: Parallel responses from council models
  - Stage 2: Anonymized peer evaluation and ranking
  - Stage 3: Chairman synthesis of all perspectives

- **Flexible CLI:** Override models, run partial stages, read from files
- **Claude Code Integration:** Native skill with triggers
- **JSON Output:** Structured results for programmatic use
- **OpenRouter Support:** Access 100+ models via single API

### Installation

**One-line install:**
```bash
curl -fsSL https://raw.githubusercontent.com/ACTUAL-USERNAME/llm-council-skill/main/install.sh | bash
```

**Manual install:**
```bash
git clone https://github.com/ACTUAL-USERNAME/llm-council-skill ~/s/llm-council-skill
cd ~/s/llm-council-skill
cp .env.example .env
# Add OPENROUTER_API_KEY to .env
uv sync
```

### Requirements

- Python 3.10+
- OpenRouter API key (get free key at https://openrouter.ai/keys)
- Claude Code (for skill integration)

### Documentation

- [Installation Guide](INSTALL.md)
- [Quick Start](QUICKSTART.md)
- [Architecture](CLAUDE.md)

### Credits

Original implementation by Andrej Karpathy. Adapted as a Claude Code skill.
```

6. Click "Publish release"

## 10. Post-Publication Tasks

- [ ] Test the one-line installer:
  ```bash
  cd /tmp
  curl -fsSL https://raw.githubusercontent.com/ACTUAL-USERNAME/llm-council-skill/main/install.sh | bash
  ```

- [ ] Test cloning from GitHub:
  ```bash
  cd /tmp
  git clone https://github.com/ACTUAL-USERNAME/llm-council-skill test-clone
  cd test-clone
  cp .env.example .env
  uv sync
  ```

- [ ] Update any external references (if you shared early)

- [ ] Share with community:
  - Claude Code Discord/forums
  - Reddit (r/ClaudeAI)
  - Twitter/X
  - Personal blog

## Optional: Publish to PyPI

If you want to publish to PyPI (enables `pip install llm-council-skill`):

1. **Get PyPI account:**
   - Sign up at https://pypi.org/
   - Generate API token in account settings

2. **Build package:**
   ```bash
   uv build
   ```

3. **Test on TestPyPI first:**
   ```bash
   uv publish --repository testpypi
   ```

4. **Verify test installation:**
   ```bash
   pip install --index-url https://test.pypi.org/simple/ llm-council-skill
   ```

5. **Publish to production PyPI:**
   ```bash
   uv publish
   ```

6. **Update README with pip install:**
   ```markdown
   ### PyPI Installation
   
   ```bash
   pip install llm-council-skill
   ```
   
   Then install skill files:
   ```bash
   mkdir -p ~/.claude/skills
   # Copy .claude/skills/llm-council/ to ~/.claude/skills/
   ```

## Quick Reference Commands

```bash
# URL replacements
sed -i '' 's/yourusername/ACTUAL-USERNAME/g' install.sh
sed -i '' 's/yourusername/ACTUAL-USERNAME/g' README.md
sed -i '' 's/yourusername/ACTUAL-USERNAME/g' pyproject.toml

# Author replacements
sed -i '' 's/\[Your Name\]/Your Actual Name/g' LICENSE
sed -i '' 's/Your Name/Your Actual Name/g' pyproject.toml
sed -i '' 's/your.email@example.com/your.actual@email.com/g' pyproject.toml

# Git commands
git init
git branch -M main
git add .
git commit -m "Initial commit - LLM Council Skill v1.0.0"
git remote add origin https://github.com/ACTUAL-USERNAME/llm-council-skill.git
git push -u origin main
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0
```

## Final Check

Before you run the above commands:

- [x] Package structure is correct
- [x] All documentation is complete
- [x] Tests pass locally
- [ ] Repository URLs are updated
- [ ] Author information is updated
- [ ] GitHub repository is created
- [ ] You have your OpenRouter API key ready for testing

Once these are done, you're ready to publish! 🚀
