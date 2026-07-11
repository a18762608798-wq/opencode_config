# AGENTS.md

## About this repo

This is the user's **~/.config/opencode** — the live global config directory for OpenCode. Treat it as active configuration, not a doc/example project.

## Key architecture facts

- `opencode.jsonc` — global OpenCode config ($schema: `https://opencode.ai/config.json`); this IS the user's config
- `package.json` — only dependency is `@opencode-ai/plugin`; no build/test/lint/typecheck commands exist
- Standard subdirectories may include: `agents/`, `skills/`, `credentials/`, `sessions/`, `logs/`, `mcp.json` — create only as needed
- Config hierarchy: project-level (`.opencode/`) overrides global (`~/.config/opencode/`)
- `docs/` and `examples/` are reference material, not the repo's purpose

## Editing config

- Agent definitions go in `agents/*.json`: `name`, `description`, `model`, `tools`, `systemPrompt`, optional `subagents`
- Skill files go in `skills/*.md`: Markdown with YAML frontmatter (`name`, `description`, `triggers`)
- MCP servers go in `mcp.json` under `mcpServers` key
- Model identifiers use format: `provider/model-name` (e.g. `anthropic/claude-sonnet-4-20250514`)
- API keys reference env vars via `env:VAR_NAME` syntax

## Docs and examples

- All docs are in **Chinese (zh-CN)**
- `docs/index.md` — 入门教程 entry point
- `examples/` — ready-to-copy agent/skill/MCP examples (NOT the user's actual config, just templates)

## Git

- `node_modules/` is gitignored — run `npm install` after clone to restore dependencies
- `.gitignore` covers Node, Python, editor, OS, and build artifacts
