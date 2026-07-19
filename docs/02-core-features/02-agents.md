# Agent 系统

## 什么是 Agent？

Agent 是 OpenCode 中最核心的概念。一个 Agent 定义了：

- 🎭 **角色身份**：AI 扮演什么角色（架构师、代码审查员、测试工程师...）
- 📋 **行为规则**：AI 应该遵循的规范和约束
- 🛠️ **可用工具**：AI 可以使用的技能（Skills）和 MCP 工具
- 📝 **系统提示词**：定制化的初始指令

## 内置 Agent

OpenCode 自带几个预设 Agent：

### Build Agent（默认）

通用开发 Agent，能处理大多数编程任务。

```
Agent: Build
描述: 通用开发助手，可以创建、修改、删除文件
```

### Plan Agent

只读规划 Agent，用于分析和设计。

```
Agent: Plan
描述: 只读分析模式，不会修改任何文件
```

## 创建自定义 Agent

创建 `.opencode/agents/code-reviewer.md`：(推荐)

```markdown
---
description: Read-only project analyst for understanding project architecture and implementation
mode: subagent
model: deepseek/deepseek-v4-flash
temperature: 0.1
permission: 
    edit: deny
---

You are a read-only project analyst.

Your purpose is to help the primary agent understand the current project before making changes.

Investigate:

- Project structure and purpose
- Important entry points
- Module responsibilities
- Control flow and data flow
- Configuration and dependencies
- Relevant tests and conventions
- Files related to the requested task
- Potential risks and uncertainties

Use repository evidence rather than assumptions.

Do not modify, create, delete, rename, or overwrite files.

Return:

1. Summary
2. Relevant files
3. Architecture and execution flow
4. Constraints and conventions
5. Risks and uncertainties
6. Recommended next steps
```

其中:

* mode: primary, subagent, all(default)

## 调用

### 手动调用：

```text
@code-reviewer 审查当前未提交的代码改动
```

### 主 agent 自动调用

`ai.codecompanion`: `acp_session_options` and choose mode.
`opencode`: `Tab`

## Agent 配置选项

| 配置项 | 类型 | 说明 |
|--------|------|------|
| `name` | string | Agent 名称 |
| `description` | string | Agent 描述 |
| `systemPrompt` | string | 系统提示词 |
| `model` | string | 指定模型（格式：provider/model） |
| `tools` | string[] | 可用工具列表 |
| `skills` | string[] | 关联的 Skills |
| `mcpServers` | string[] | 关联的 MCP 服务器 |

### 可用工具列表

| 工具名 | 功能 |
|--------|------|
| `read_file` | 读取文件 |
| `write_file` | 写入/修改文件 |
| `delete_file` | 删除文件 |
| `search_code` | 搜索代码 |
| `run_command` | 执行命令 |
| `list_files` | 列出文件 |
| `web_search` | 网络搜索 |
| `web_fetch` | 获取网页内容 |

## Agent vs Subagent

| 特性 | Agent | Subagent |
|------|-------|----------|
| 定义位置 | `.opencode/agents/` | Agent 内部定义 |
| 触发方式 | 用户手动切换 | Agent 自动调用 |
| 使用场景 | 切换工作模式 | 分解复杂任务 |
| 独立性 | 独立会话上下文 | 继承父 Agent 上下文 |

```

## 最佳实践

1. 🎯 **一个 Agent 一个职责**：不要让一个 Agent 做太多事情
2. 📝 **写清楚 systemPrompt**：越具体，AI 表现越好
3. 🔧 **合理限制工具**：只给 Agent 需要的工具，减少误操作风险
4. 🧪 **多 Agent 协作**：用 Subagent 拆分复杂任务
5. 📊 **迭代优化**：根据实际使用效果不断调整 prompt

## 下一步

学习完 Agent 系统，接下来了解 👉 [Skills 技能](03-skills.md)
