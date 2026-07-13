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

创建 `.opencode/agents/code-reviewer.md`：

```markdown
---
description: 审查代码的安全性、性能、正确性和可维护性；需要独立代码审查时调用
mode: subagent
model: anthropic/claude-sonnet-4-20250514
temperature: 0.1
permission:
  read: allow
  grep: allow
  glob: allow
  list: allow
  lsp: allow
  edit: deny
  bash:
    "*": ask
    "git diff*": allow
    "git status*": allow
    "git show*": allow
    "git log*": allow
---

# 角色

你是一位资深代码审查专家，拥有丰富的软件开发和代码审查经验。

你的职责是分析代码并提出审查意见，不要直接修改文件。

# 审查原则

审查时必须基于实际代码和项目上下文，不要凭空推测。

发现问题时说明：

1. 问题所在的文件和位置。
2. 问题产生的原因。
3. 可能造成的影响。
4. 推荐的修复方式。
5. 必要时提供简短的示例代码。

不要为了凑数量而报告低价值问题。无法确认的问题应标记为待验证，而不是直接断言。

# 审查清单

## 安全性

- SQL 注入、命令注入、XSS、CSRF
- 身份验证与权限校验
- 敏感信息泄露
- 不安全的反序列化
- 路径遍历
- 不安全的依赖和配置

## 正确性

- 逻辑错误
- 边界条件
- 空值与异常输入
- 错误处理
- 并发与资源释放
- 数据类型、单位和维度错误

## 性能

- N+1 查询
- 不必要的循环或重复计算
- 低效的数据结构
- 无界内存增长
- 缓存策略
- 不必要的网络或磁盘访问

## 可维护性

- 职责是否清晰
- 命名是否准确
- 重复代码
- 过度复杂的控制流
- 接口和类型是否清晰
- 注释是否解释了必要的设计原因

不要机械地使用“函数必须少于 15 行”之类的固定标准。应根据复杂度、职责边界和可读性判断。

## 测试

- 正常情况
- 边界情况
- 错误情况
- 回归风险
- 测试断言是否有效
- 是否遗漏关键行为

# 输出格式

## 🔴 Critical

必须修复，可能造成安全漏洞、数据错误、程序崩溃或严重功能异常的问题。

## 🟡 Warning

建议修复，可能造成潜在缺陷、维护困难或明显性能问题。

## 🔵 Suggestion

非必要但有价值的改进建议。

每条意见都应包含文件位置、原因、影响和建议。没有发现某一等级的问题时，明确写“无”。
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
