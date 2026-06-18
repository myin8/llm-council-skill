# Distribution Checklist

This document tracks the packaging status for distributing the LLM Council Skill.

## Package Status: ✅ Ready

The repository is fully packaged as a Claude Code skill with multiple distribution options.

## File Structure

```
llm-council-skill/
├── .claude/
│   └── skills/
│       └── llm-council/
│           └── SKILL.md              ✅ Skill definition with triggers
├── council/
│   ├── __init__.py                   ✅ Package marker
│   ├── config.py                     ✅ Default models and config
│   ├── openrouter.py                 ✅ API client
│   └── deliberate.py                 ✅ Core orchestration logic
├── council_run.py                    ✅ CLI entry point
├── pyproject.toml                    ✅ Package metadata (PyPI-ready)
├── requirements.txt                  ✅ pip compatibility
├── MANIFEST.in                       ✅ Build includes
├── .env.example                      ✅ Environment template
├── .gitignore                        ✅ Ignore patterns
├── LICENSE                           ✅ MIT License
├── README.md                         ✅ Project overview
├── INSTALL.md                        ✅ Installation guide
├── QUICKSTART.md                     ✅ Usage examples
├── CLAUDE.md                         ✅ Architecture docs
├── PACKAGING.md                      ✅ Distribution guide
├── CHANGELOG.md                      ✅ Version history
├── COMPARISON.md                     ✅ Comparison to original
├── SUMMARY.md                        ✅ Project summary
└── install.sh                        ✅ One-command installer
```

## Distribution Methods

### ✅ Method 1: Git Repository (Primary)

**Status:** Ready to publish

**Installation:**
```bash
git clone <repo-url> ~/.local/share/llm-council-skill
cd ~/.local/share/llm-council-skill
cp .env.example .env
# Add OPENROUTER_API_KEY to .env
uv sync
```

**One-line installer:**
```bash
curl -fsSL https://raw.githubusercontent.com/yourusername/llm-council-skill/main/install.sh | bash
```

**Checklist:**
- [x] Repository structure complete
- [x] Documentation complete
- [x] Install script tested
- [ ] GitHub repository created
- [ ] Update repo URLs in:
  - [ ] README.md
  - [ ] install.sh
  - [ ] pyproject.toml

### 🔄 Method 2: PyPI Package (Optional)

**Status:** Package structure ready, not yet published

**Installation (after publishing):**
```bash
pip install llm-council-skill
```

**Build and publish:**
```bash
# Build
uv build

# Test upload (TestPyPI)
uv publish --repository testpypi

# Production upload
uv publish
```

**Checklist:**
- [x] pyproject.toml configured
- [x] MANIFEST.in created
- [x] Console script entry point
- [ ] Author information updated
- [ ] PyPI account setup
- [ ] Build tested locally
- [ ] Published to TestPyPI
- [ ] Published to PyPI

### ⏳ Method 3: Claude Code Plugin Registry (Future)

**Status:** Waiting for official plugin system

Will enable:
```bash
claude skill install llm-council
```

## Pre-Distribution Tasks

### Required Before Git Publishing

1. **Update Repository URLs**
   - [ ] Create GitHub repository
   - [ ] Update URL in `install.sh` (line 8)
   - [ ] Update URL in `README.md` (Installation section)
   - [ ] Update URLs in `pyproject.toml` ([project.urls])

2. **Update Author Information**
   - [ ] Replace "[Your Name]" in `LICENSE`
   - [ ] Update author in `pyproject.toml`

3. **Test Installation**
   - [x] Test CLI: `uv run python council_run.py "What is 2+2?" --stages 1`
   - [x] Test package structure
   - [ ] Test install.sh script
   - [ ] Test on fresh environment

4. **Review Documentation**
   - [x] README.md has clear instructions
   - [x] INSTALL.md covers all methods
   - [x] QUICKSTART.md has examples
   - [x] CLAUDE.md explains architecture
   - [x] PACKAGING.md documents distribution

### Optional Enhancements

- [ ] Add screenshots/demos to README
- [ ] Create example queries in examples/
- [ ] Add CI/CD pipeline (.github/workflows/)
- [ ] Add contribution guidelines (CONTRIBUTING.md)
- [ ] Add code of conduct (CODE_OF_CONDUCT.md)
- [ ] Add unit tests (tests/)
- [ ] Add integration tests
- [ ] Set up documentation site (e.g., Read the Docs)

## Testing Checklist

### Local Testing

```bash
# 1. Test CLI directly
cd ~/.local/share/llm-council-skill
uv run python council_run.py "What is 2+2?" --stages 1

# 2. Test full 3-stage run
uv run python council_run.py "Explain the CAP theorem"

# 3. Test custom models
uv run python council_run.py "Compare Python vs Go" \
  --models "openai/gpt-4o,anthropic/claude-sonnet-4"

# 4. Test from file
echo "What is machine learning?" > test_query.txt
uv run python council_run.py --query-file test_query.txt --stages 1

# 5. Test package import
uv pip install -e .
python -c "from council import run_full_council; print('OK')"

# 6. Test console script (after pip install -e .)
llm-council "Test query" --stages 1
```

### Claude Code Integration Testing

1. **Install skill:**
   ```bash
   cd ~/.local/share/llm-council-skill
   ```

2. **Test triggers in Claude Code:**
   - "Ask the council: What is 2+2?"
   - "Run a council deliberation on machine learning"
   - `/llm-council`

3. **Verify output formatting:**
   - Check that JSON is parsed correctly
   - Check that synthesis is displayed
   - Check that rankings are shown

### Fresh Environment Testing

```bash
# Clean test in new directory
cd /tmp
rm -rf llm-council-skill-test
git clone <repo-url> llm-council-skill-test
cd llm-council-skill-test
cp .env.example .env
# Add test API key
uv sync
uv run python council_run.py "What is 2+2?" --stages 1
```

## Release Process

### 1. Prepare Release

1. Update version number:
   - `pyproject.toml` → `version = "1.0.0"`
   - `.claude/skills/llm-council/SKILL.md` → `version: 1.0.0`

2. Update `CHANGELOG.md`:
   ```markdown
   ## [1.0.0] - 2026-06-17
   
   ### Added
   - Initial release
   - 3-stage council deliberation
   - CLI with JSON output
   - Claude Code skill integration
   ```

3. Commit changes:
   ```bash
   git add .
   git commit -m "Release v1.0.0"
   git tag v1.0.0
   ```

### 2. Publish to GitHub

```bash
git push origin main
git push origin v1.0.0
```

### 3. Create GitHub Release

1. Go to repository → Releases → Draft a new release
2. Tag: `v1.0.0`
3. Title: "v1.0.0 - Initial Release"
4. Description: Copy from CHANGELOG.md
5. Attach any release assets (optional)
6. Publish release

### 4. Publish to PyPI (Optional)

```bash
# Build
uv build

# Test upload
uv publish --repository testpypi

# Verify test installation
pip install --index-url https://test.pypi.org/simple/ llm-council-skill

# Production upload
uv publish
```

## Post-Release Tasks

- [ ] Announce on relevant channels
- [ ] Update documentation site (if any)
- [ ] Monitor for issues/feedback
- [ ] Respond to bug reports
- [ ] Plan next version features

## Version Management

Follow semantic versioning (MAJOR.MINOR.PATCH):

- **MAJOR:** Breaking changes to API or skill interface
- **MINOR:** New features, backward compatible
- **PATCH:** Bug fixes, backward compatible

### Version Update Locations

When bumping version:
1. `pyproject.toml` → `version = "X.Y.Z"`
2. `.claude/skills/llm-council/SKILL.md` → `version: X.Y.Z`
3. `CHANGELOG.md` → Add new section
4. Git tag → `git tag vX.Y.Z`

## Support and Maintenance

### Issue Tracking

- Use GitHub Issues for bugs and feature requests
- Label issues: `bug`, `enhancement`, `documentation`, `question`
- Set up issue templates (optional)

### Update Frequency

- **Patch releases:** As needed for bug fixes
- **Minor releases:** Every 2-3 months for features
- **Major releases:** Only when breaking changes required

### Maintenance Tasks

- Monitor OpenRouter API changes
- Update default model list quarterly
- Keep dependencies updated
- Respond to security advisories

## Current Status Summary

✅ **Ready for Git distribution**
- All documentation complete
- Package structure validated
- CLI tested and working
- Skill definition complete

🔄 **Needs before publishing:**
- Create GitHub repository
- Update placeholder URLs
- Update author information
- Test install.sh on clean system

⏳ **Optional enhancements:**
- PyPI publication
- CI/CD setup
- Expanded test coverage
- Community guidelines

## Next Steps

1. **Create GitHub repository**
2. **Update all placeholder URLs and author info**
3. **Test install.sh script**
4. **Push to GitHub**
5. **Create first release (v1.0.0)**
6. **Share with Claude Code community**
