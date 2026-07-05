# AGENTS.md

## About this repo

This is the **OpenCode global config directory** (`~/.config/opencode`), not a software project. It hosts Chinese-language OpenCode documentation (`docs/`), example configs (`examples/`), and the global `opencode.jsonc`.

## Key architecture facts

- `opencode.jsonc` — global OpenCode config ($schema: `https://opencode.ai/config.json`)
- `package.json` — only dependency is `@opencode-ai/plugin`; no build/test/lint/typecheck commands exist
- No `.opencode/` directory exists in this repo — project-level configs live in `<project>/.opencode/`
- Config hierarchy: project-level (`.opencode/`) overrides global (`~/.config/opencode/`)
- Standard OpenCode subdirectories: `agents/`, `skills/`, `credentials/`, `sessions/`, `logs/`, `mcp.json`

## Documentation

- All docs are in **Chinese (zh-CN)**
- `docs/index.md` — entry point (入门教程)
- `examples/` — ready-to-copy agent/skill/MCP config examples
- No CI, no tests, no build process — this is a static documentation/config repo

## OpenCode config conventions

- Model identifiers use format: `provider/model-name` (e.g. `anthropic/claude-sonnet-4-20250514`)
- API keys reference env vars via `env:VAR_NAME` syntax in config
- Agent definitions are JSON files with: `name`, `description`, `model`, `tools`, `systemPrompt`, optional `subagents`
- Skill files are Markdown with YAML frontmatter (`name`, `description`, `triggers`)
- MCP servers are declared in `mcp.json` under `mcpServers` key

## Git

- `.gitignore` covers Node, Python, editor, OS, and build artifacts
- `node_modules/` is gitignored — run `npm install` after clone to restore dependencies
