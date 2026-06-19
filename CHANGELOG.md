# Changelog

All notable changes to the LLM Council Skill.

## [1.2.0] - 2026-06-18

### Changed
- Converted the repository from a Claude-only skill layout to a portable Agent Skills layout.
- Added root `SKILL.md` as the canonical skill entry point.
- Added `agents/openai.yaml` metadata for Codex/OpenAI surfaces.
- Added `scripts/run_council.py` as the conventional bundled script entry point.
- Added `compatibility` metadata for runtime requirements.
- Kept `.claude/skills/llm-council/SKILL.md` as a compatibility mirror.
- Updated packaging metadata and docs to describe Codex and other Agent Skills-compatible clients.

## [1.1.0] - 2026-06-17

### Changed
- **Updated default models to latest releases:**
  - Council: `openai/gpt-5.5` (was gpt-5.1), `~google/gemini-pro-latest` (was gemini-3-pro-preview), `anthropic/claude-opus-4.8` (was claude-sonnet-4.5)
  - Chairman: `anthropic/claude-opus-4.8` (was google/gemini-3-pro-preview)
  - Added commented alternatives: `x-ai/grok-4.3`, `anthropic/claude-fable-5`

### Updated Documentation
- README.md: Default models section
- SUMMARY.md: Default models and JSON examples
- QUICKSTART.md: Default models reference
- COMPARISON.md: Added default models note

### Notes
- Synced with upstream llm-council web app model updates
- All structural tests pass with new models
- No breaking changes to CLI or JSON output format

## [1.0.0] - 2026-06-17

### Added
- Initial release
- 3-stage deliberation system (parallel responses → anonymous peer ranking → synthesis)
- CLI interface with JSON output
- Claude-specific skill integration
- Parameterized model selection via CLI flags
- Partial runs with `--stages` flag
- Query from file support with `--query-file`
- Comprehensive documentation (README, CLAUDE.md, QUICKSTART.md, SUMMARY.md, COMPARISON.md)
- Structure verification tests

### Features
- Zero infrastructure (no web server or database)
- Stateless execution
- Graceful degradation on model failures
- OpenRouter integration for 100+ models
- Async/parallel execution for performance
