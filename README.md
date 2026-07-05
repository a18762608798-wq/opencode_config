# OpenCode 配置与教程

OpenCode 全局配置目录，包含中文入门教程、配置示例和参考资料。

## 目录结构

```
~/.config/opencode/
├── opencode.jsonc       # OpenCode 全局配置
├── package.json         # 插件依赖
├── docs/                # 中文入门教程
├── examples/            # Agent / Skill / MCP 配置示例
├── agents/              # 全局 Agent 定义
├── skills/              # 全局 Skill 定义
└── mcp.json             # 全局 MCP 服务器配置
```

## 快速开始

1. 安装 OpenCode：参见 [安装指南](docs/01-getting-started/02-installation.md)
2. 抓取配置：`git clone <repo-url> ~/.config/opencode`
3. 安装依赖：`npm install`
4. 阅读教程：[docs/index.md](docs/index.md)

## 学习路径

| 阶段 | 内容 | 路径 |
|------|------|------|
| 快速上手 | 安装、配置、第一个会话 | `docs/01-getting-started/` |
| 核心功能 | TUI、Agent、Skills、Plan 模式、MCP | `docs/02-core-features/` |
| 进阶玩法 | 无头模式、自定义 Agent、上下文工程 | `docs/03-advanced/` |
| 参考手册 | CLI 命令、配置文件、FAQ | `docs/04-reference/` |

## 示例

- [基础 Agent 配置](examples/01-basic-agents.md) — 代码审查、测试、文档生成等常用 Agent
- [MCP Server 示例](examples/mcp-server/README.md) — Python / Node.js MCP Server 完整实现
- [自定义 Skill](examples/custom-skill/README.md) — Git 工作流、API 设计等 Skill 模板

## 相关链接

- [OpenCode 官网](https://opencode.ai)
- [GitHub 仓库](https://github.com/anomalyco/opencode)
- [MCP 协议文档](https://modelcontextprotocol.io/)
