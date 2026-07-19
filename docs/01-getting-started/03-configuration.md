# 配置指南

## 概述

OpenCode 安装完成后，需要配置 LLM 提供商才能使用。OpenCode 支持两种认证方式：

1. **OpenCode Zen**（推荐新手）— 官方精选模型，开箱即用
2. **第三方提供商** — 使用你自己的 API Key

## 方式一：OpenCode Zen（推荐）

OpenCode Zen 是官方维护的精选模型列表，已经过测试和验证，无需自行管理多个 API Key。

### 步骤

在 TUI 中输入 `/connect` 命令，选择提供商。

Use `opencode models` to see the sepcific models name of acp.

## 方式二：配置第三方提供商

### 本地模型 (Ollama)

```bash
# 确保 Ollama 已安装并运行
ollama serve

# 拉取模型
ollama pull qwen2.5-coder:7b

# 在 OpenCode TUI 中 /connect 选择 ollama
```

## 配置文件

Ref to [opencode_rule](https://opencode.ai/docs/rules/)

`~/.config/opencode/` — 只放配置（opencode.jsonc）和插件依赖（package.json + node_modules/）

`opencode.jsonc` 和 `package.json` 是主要需要徐改的文件。

```text
~/.config/opencode/
├── opencode.jsonc       # 全局运行配置
├── tui.jsonc            # 全局 TUI 配置
├── AGENTS.md            # 全局自然语言规则(**软约束**)
└── agents/
    └── test-writer.md   # 自定义 Agent
```

在项目中使用：

```text
project/
├── opencode.jsonc       # 项目运行配置
├── AGENTS.md            # 项目自然语言规则(优于全局, 但也能读取全局权限配置).
└── .opencode/
    └── agents/          # 项目专用 Agent
```

## 切换模型

在 TUI 中：

- 按 `Ctrl+T` 切换模型变体(但是要有才行，deepseek这种需要手动配置).
- 使用 `/model` 命令查看和切换可用模型
- 启动时指定模型：`opencode --model openai/gpt-4o`

## 下一步

配置完成后，开始你的 👉 [第一次使用](04-first-session.md)
