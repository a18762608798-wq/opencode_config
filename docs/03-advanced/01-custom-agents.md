# 自定义 Agent

## 概述

Agent 是 OpenCode 的灵魂。虽然内置的 Build Agent 能处理大多数任务，但针对特定场景定制 Agent 能大幅提升效率和输出质量。

本章将深入讲解 Agent 的定制化配置。

## Agent 配置完整参考

### JSON 配置结构

```jsonc
{
  // === 基本信息 ===
  "name": "Agent 名称",
  "description": "Agent 的简短描述，用于在列表中识别",

  // === 模型配置 ===
  "model": "provider/model-name",
  // 可选：为不同任务指定不同模型
  "models": {
    "plan": "anthropic/claude-haiku-4-5-20251001",   // 规划阶段用便宜模型
    "build": "anthropic/claude-sonnet-4-20250514"     // 构建阶段用强模型
  },

  // === 提示词 ===
  "systemPrompt": "系统级别的提示词，定义 Agent 的角色和行为",
  // 或引用外部文件
  "systemPromptFile": "./prompts/code-reviewer.md",

  // === 工具权限 ===
  "tools": [
    "read_file",
    "write_file",
    "delete_file",
    "search_code",
    "run_command",
    "list_files",
    "web_search",
    "web_fetch"
  ],

  // === 关联 Skills ===
  "skills": ["git-workflow", "api-design"],

  // === MCP 服务器 ===
  "mcpServers": ["github", "postgres", "filesystem"],

  // === 子 Agent ===
  "subagents": [],

  // === 行为配置 ===
  "config": {
    "maxTokens": 8192,
    "temperature": 0.3,
    "autoApprove": false,         // 是否需要用户确认才执行操作
    "allowCommands": true,         // 是否允许执行 shell 命令
    "commandBlacklist": ["rm -rf", "sudo"],  // 禁止的命令
    "maxConcurrent": 3            // 最大并发操作数
  }
}
```

## 实战：构建专业 Agent

### 示例一：安全审计 Agent

```json
{
  "name": "Security Auditor",
  "description": "专注于应用安全审查的 Agent",
  "model": "anthropic/claude-sonnet-4-20250514",
  "tools": ["read_file", "search_code", "list_files", "web_search"],
  "skills": [],
  "config": {
    "autoApprove": false,
    "allowCommands": false
  },
  "systemPrompt": "你是一位资深应用安全专家，拥有 OWASP 和 CWE 认证。\n\n## 审查标准\n\n按照 OWASP Top 10 对代码进行审查：\n\n1. **注入攻击**（SQL、命令、LDAP 等）\n2. **认证失效**\n3. **敏感数据泄露**\n4. **XML 外部实体（XXE）**\n5. **访问控制失效**\n6. **安全配置错误**\n7. **跨站脚本（XSS）**\n8. **不安全的反序列化**\n9. **使用已知漏洞组件**\n10. **日志和监控不足**\n\n## 输出格式\n\n对每个发现的问题，使用以下格式：\n\n### [严重程度] 问题标题\n- **位置**: 文件:行号\n- **CWE**: CWE-xxx\n- **描述**: 问题的详细描述\n- **影响**: 可能造成的危害\n- **修复建议**: 具体的修复代码示例\n\n严重程度：🔴 Critical / 🟠 High / 🟡 Medium / 🔵 Low"
}
```

### 示例二：数据库管理员 Agent

```json
{
  "name": "DBA Assistant",
  "description": "数据库管理和优化专家",
  "model": "anthropic/claude-sonnet-4-20250514",
  "tools": ["read_file", "write_file", "search_code", "run_command"],
  "mcpServers": ["postgres"],
  "skills": ["database-migration"],
  "config": {
    "autoApprove": false,
    "allowCommands": true,
    "commandBlacklist": ["DROP DATABASE", "DROP TABLE", "TRUNCATE"]
  },
  "systemPrompt": "你是数据库管理专家，精通 PostgreSQL 和 MySQL。\n\n## 职责\n\n1. 审查和优化 SQL 查询\n2. 设计数据库 Schema 和索引\n3. 编写安全的数据库迁移脚本\n4. 分析查询性能瓶颈\n\n## 规则\n\n- 所有 DDL 操作必须包含回滚方案\n- 生产环境操作前必须确认\n- 查询优化建议需附带 EXPLAIN 分析\n- 迁移脚本必须可重复执行（幂等）\n\n## 安全\n\n- 严禁执行 DROP DATABASE、DROP TABLE、TRUNCATE（除非用户明确要求）\n- 所有 SQL 使用参数化查询\n- 敏感数据操作需脱敏处理"
}
```

### 示例三：前端架构师 Agent

```json
{
  "name": "Frontend Architect",
  "description": "React/TypeScript 前端架构设计专家",
  "model": "openai/gpt-5.4",
  "tools": ["read_file", "write_file", "search_code", "web_search"],
  "skills": ["api-design"],
  "config": {
    "temperature": 0.5
  },
  "systemPrompt": "你是资深前端架构师，专精 React 18+ 和 TypeScript。\n\n## 设计原则\n\n1. **组件设计**\n   - 单一职责\n   - 可组合性\n   - Props 类型完整\n\n2. **状态管理**\n   - 服务端状态：TanStack Query\n   - 客户端状态：Zustand\n   - 表单状态：React Hook Form\n\n3. **性能优化**\n   - 代码分割（React.lazy）\n   - 虚拟列表（大数据渲染）\n   - Memoization（useMemo/useCallback）\n   - 图片懒加载\n\n4. **可访问性（a11y）**\n   - 语义化 HTML\n   - ARIA 标签\n   - 键盘导航\n\n## 代码风格\n\n- 函数组件 + Hooks，不使用 Class 组件\n- 使用命名导出，避免默认导出\n- 类型定义放在独立文件\n- CSS 使用 Tailwind CSS 或 CSS Modules\n- 测试使用 Vitest + React Testing Library"
}
```

## 组织多个 Agent 的团队

### Team Leader 模式

```json
{
  "name": "Tech Lead",
  "description": "技术负责人，协调多个专业 Agent",
  "model": "anthropic/claude-sonnet-4-20250514",
  "subagents": [
    {
      "name": "Code Reviewer",
      "trigger": "需要审查代码时",
      "agent": "code-reviewer"
    },
    {
      "name": "Test Engineer",
      "trigger": "需要编写测试时",
      "agent": "test-writer"
    },
    {
      "name": "Doc Writer",
      "trigger": "需要编写文档时",
      "agent": "doc-writer"
    },
    {
      "name": "DBA",
      "trigger": "涉及数据库操作时",
      "agent": "dba-assistant"
    }
  ],
  "systemPrompt": "你是技术负责人。当用户提出需求时：\n1. 分析需求，制定方案\n2. 根据任务类型分派给合适的 Subagent\n3. 审查各 Subagent 的输出\n4. 整合结果，确保一致性\n\n当 Subagent 完成工作后，你需要验证：\n- 代码风格一致\n- 没有重复代码\n- 接口兼容\n- 测试覆盖充分"
}
```

## 配置管理

### 推荐目录结构

```
项目根目录/
├── .opencode/
│   ├── agents/
│   │   ├── code-reviewer.json
│   │   ├── test-writer.json
│   │   └── tech-lead.json
│   ├── skills/
│   │   ├── git-workflow.md
│   │   └── api-design.md
│   ├── prompts/
│   │   ├── code-reviewer.md
│   │   └── dba-assistant.md
│   └── mcp.json
├── AGENTS.md
└── ...
```

### 版本管理

```bash
# 将 Agent 配置纳入版本管理
git add .opencode/
git commit -m "feat(opencode): 添加代码审查和测试 Agent 配置"

# 团队成员 clone 后即可使用相同配置
git clone <repo>
cd <repo>
opencode --agent "Code Reviewer"
```

## 调试 Agent

### 查看 Agent 使用了哪些信息和工具

```
/status
```

### 测试 Agent 的输出

在 Plan 模式下测试 Agent 的行为，确认无误后再切换到 Build 模式。

### 日志查看

```bash
# OpenCode 日志位置
tail -f ~/.config/opencode/logs/opencode.log
```

### 常见调优方向

| 问题 | 可能原因 | 解决方案 |
|------|---------|---------|
| Agent 输出不够专业 | systemPrompt 太简单 | 添加具体的领域知识 |
| Agent 反复询问 | prompt 缺少上下文 | 在 systemPrompt 中补充项目背景 |
| Agent 操作太激进 | 工具权限过多 | 限制 tools 列表，设置 autoApprove: false |
| 输出格式不统一 | 缺少格式要求 | 在 systemPrompt 中明确输出格式 |
| 速度太慢 | 模型太大 | Plan 阶段使用 Haiku，Build 阶段用 Sonnet |

## 最佳实践总结

1. 🎯 **一个 Agent 一个职责**：不要让 Agent 变成"万能工具"
2. 📝 **写清楚 systemPrompt**：这是决定 Agent 质量的最关键因素
3. 🔒 **最小权限**：只给 Agent 必要的工具
4. 🧪 **Plan 模式测试**：先在 Plan 模式验证，再 Build 执行
5. 📊 **持续优化**：根据实际表现不断调整配置
6. 🤝 **团队共享**：将 `.opencode/` 纳入 Git，团队共用

## 下一步

了解自定义 Agent 后，继续学习 👉 [子 Agent](02-subagents.md)
