# 什么是 OpenCode？

## 概述

OpenCode 是一个**开源终端 AI 编程代理**（AI Coding Agent）。简单来说，它就像一个住在你终端里的资深开发者，随时准备帮你：

- ✍️ 编写和调试代码
- 📖 理解现有代码库
- 🔄 重构和优化代码
- 💬 回答技术问题
- 🤖 自动化重复任务

## 核心设计理念

### 1. 终端原生（Terminal-Native）

OpenCode 不依赖任何 IDE。它运行在终端中，通过 **TUI（Text User Interface）** 提供丰富的交互体验。这意味着：

- 可以访问本地文件系统和操作系统工具
- 轻量级，启动迅速
- 适合远程服务器和 CI/CD 环境

### 2. 模型无关（Model-Agnostic）

与 Claude Code（仅支持 Anthropic）或 GitHub Copilot 不同，OpenCode 支持几乎所有主流 LLM 提供商：

| 提供商 | 模型示例 |
|--------|---------|
| Anthropic | Claude Sonnet, Claude Haiku |
| OpenAI | GPT-4o, GPT-5 |
| Google | Gemini 2.5, Gemini 3.1 |
| DeepSeek | DeepSeek-V3, DeepSeek-R1 |
| 本地模型 | Ollama 运行的任意模型 |
| OpenRouter | 统一接入 200+ 模型 |

### 3. 可组合架构

OpenCode 的核心架构由三个关键概念组成：

```
┌─────────────────────────────────────────┐
│              OpenCode TUI               │
├─────────────────────────────────────────┤
│  Agent  │  Skill  │  MCP Server  │ ...  │
├─────────────────────────────────────────┤
│           LLM Provider Layer            │
│   (Anthropic / OpenAI / Gemini / ...)   │
└─────────────────────────────────────────┘
```

- **Agent**：定义 AI 的角色、能力和行为规则
- **Skill**：可复用的能力模块，Agent 可以按需加载
- **MCP（Model Context Protocol）**：标准化的工具扩展协议，让 Agent 访问外部服务

## 与其他工具对比

| 特性 | OpenCode | Claude Code | GitHub Copilot | Cursor |
|------|----------|-------------|----------------|--------|
| 开源 | ✅ | ❌ | ❌ | ❌ |
| 终端原生 | ✅ | ✅ | ✅ | ❌ |
| 多模型 | ✅ 75+ | ❌ 仅 Claude | ✅ | ✅ |
| Agent 系统 | ✅ 强大 | ✅ 基本 | ❌ | ❌ |
| MCP 支持 | ✅ | ✅ | ❌ | ✅ |
| 自定义 Skill | ✅ | ❌ | ❌ | ❌ |
| 无头模式 | ✅ | ✅ | ❌ | ❌ |
| 本地模型 | ✅ | ❌ | ❌ | ❌ |

## OpenCode 能做什么？

### 场景一：快速理解陌生代码库

```bash
cd /path/to/new-project
opencode
```

在 TUI 中提问：
> 解释一下这个项目的认证流程是怎么实现的？

### 场景二：跨越多个文件重构

> 把所有的 `var` 声明改成 `const/let`，并修复由此产生的所有问题。

### 场景三：自动化 CI/CD 集成

```bash
# 在 CI 流水线中自动审查代码
opencode run --prompt "Review this PR for security issues" --format json
```

## 下一步

了解 OpenCode 是什么之后，接下来 👉 [安装 OpenCode](02-installation.md)
