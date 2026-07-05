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

### 方式一：TUI 交互创建

在 TUI 中输入：

```
/agent create
```

跟随交互向导完成 Agent 创建。

### 方式二：JSON 配置

在项目根目录创建 `.opencode/agents/` 目录，添加 JSON 配置文件：

```json
// .opencode/agents/code-reviewer.json
{
  "name": "Code Reviewer",
  "description": "专注于代码审查的 Agent",
  "systemPrompt": "你是一个资深的代码审查专家。你的任务是：\n1. 检查代码的安全漏洞\n2. 评估代码可读性和可维护性\n3. 提出优化建议\n4. 不直接修改代码，而是给出建议",
  "tools": ["read_file", "search_code", "run_command"],
  "model": "anthropic/claude-sonnet-4-20250514"
}
```

### 方式三：Markdown 定义

创建 `.opencode/agents/code-reviewer.md`：

````markdown
---
name: Code Reviewer
description: 代码审查专家
model: anthropic/claude-sonnet-4-20250514
tools:
  - read_file
  - search_code
  - run_command
---

# 角色

你是一位资深代码审查专家，拥有 15 年软件开发经验。

# 审查清单

每次审查请关注以下方面：

1. **安全性**
   - SQL 注入、XSS、CSRF 风险
   - 敏感信息泄露
   - 权限校验完整性

2. **性能**
   - N+1 查询问题
   - 不必要的循环和计算
   - 缓存策略

3. **可维护性**
   - 函数复杂度（建议 < 15 行）
   - 命名是否清晰
   - 是否有充分的注释

4. **最佳实践**
   - 错误处理是否完善
   - 类型定义是否完整
   - 测试覆盖率

# 输出格式

使用以下格式给出审查意见：

## 🔴 Critical
（必须修复的问题）

## 🟡 Warning
（建议修复的问题）

## 🔵 Suggestion
（可选的优化建议）
````

## 在会话中切换 Agent

```
# 在 TUI 中
/agent

# 在弹出的列表中选择要使用的 Agent
```

或启动时指定：

```bash
opencode --agent "Code Reviewer"
```

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

### Subagent 示例

在 Agent 配置中定义 Subagent：

```json
{
  "name": "Full-Stack Developer",
  "subagents": [
    {
      "name": "Frontend Specialist",
      "description": "专注于前端开发",
      "trigger": "用户提到 UI、组件、样式等前端任务时自动调用",
      "systemPrompt": "你是 React + TypeScript 前端专家..."
    },
    {
      "name": "Backend Specialist",
      "description": "专注于后端开发",
      "trigger": "用户提到 API、数据库、服务端任务时自动调用",
      "systemPrompt": "你是 Node.js 后端专家..."
    }
  ]
}
```

## 实践：创建你的第一个 Agent

### 场景

你希望有一个专门帮你写单元测试的 Agent。

### 步骤

1. 创建配置文件 `~/.config/opencode/agents/test-writer.json`：

```json
{
  "name": "Test Writer",
  "description": "专注于编写单元测试",
  "systemPrompt": "你是一个测试工程师。你的任务是：\n1. 为给定的代码编写全面的单元测试\n2. 覆盖正常情况、边界情况和错误情况\n3. 使用项目已有的测试框架\n4. 保持测试简洁、可读",
  "tools": ["read_file", "write_file", "search_code", "run_command"]
}
```

2. 在 TUI 中切换：

```
/agent
# 选择 "Test Writer"
```

3. 开始使用：

```
@src/utils/math.ts 为这个文件写完整的单元测试
```

## 最佳实践

1. 🎯 **一个 Agent 一个职责**：不要让一个 Agent 做太多事情
2. 📝 **写清楚 systemPrompt**：越具体，AI 表现越好
3. 🔧 **合理限制工具**：只给 Agent 需要的工具，减少误操作风险
4. 🧪 **多 Agent 协作**：用 Subagent 拆分复杂任务
5. 📊 **迭代优化**：根据实际使用效果不断调整 prompt

## 下一步

学习完 Agent 系统，接下来了解 👉 [Skills 技能](03-skills.md)
