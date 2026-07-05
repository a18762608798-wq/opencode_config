# 子 Agent (Subagent)

## 什么是 Subagent？

Subagent 是由**父 Agent 自动调用的子任务处理器**。当用户提出复杂需求时，父 Agent 可以将任务分解并分派给专门的 Subagent 处理。

```
用户: "给这个项目加上完整的用户认证系统"

         ┌──────────────┐
         │  Tech Lead   │  ← 父 Agent（协调者）
         │  (Agent)     │
         └──────┬───────┘
                │
      ┌─────────┼─────────┐
      │         │         │
      ▼         ▼         ▼
┌──────────┐ ┌──────────┐ ┌──────────┐
│Frontend  │ │Backend   │ │DBA       │
│Specialist│ │Specialist│ │Assistant │
└──────────┘ └──────────┘ └──────────┘
     ↑            ↑            ↑
  前端 UI      API 逻辑    数据库表
```

## Subagent 配置

### 在 Agent JSON 中定义

```json
{
  "name": "Full-Stack Lead",
  "description": "全栈技术负责人",
  "subagents": [
    {
      "name": "Frontend Dev",
      "description": "React 前端开发",
      "trigger": "涉及 UI、组件、样式、前端路由",
      "agent": "frontend-specialist",
      "prompt": "请专注于前端实现，使用项目已有的组件库和样式方案"
    },
    {
      "name": "Backend Dev",
      "description": "Node.js 后端开发",
      "trigger": "涉及 API、数据库、服务端逻辑、中间件",
      "agent": "backend-specialist",
      "prompt": "请实现对应的后端逻辑，遵循项目的 API 设计规范"
    }
  ]
}
```

### Subagent 配置字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `name` | string | Subagent 显示名称 |
| `description` | string | Subagent 描述 |
| `trigger` | string | 触发条件（关键词匹配） |
| `agent` | string | 引用的 Agent 名称 |
| `prompt` | string | 调用时附加的提示词 |
| `autoApprove` | boolean | 是否自动批准该 Subagent 的操作 |

## Subagent 的调用流程

```
1. 用户向父 Agent 提出需求
       │
2. 父 Agent 分析需求
       │
3. 父 Agent 匹配 trigger，决定调用哪些 Subagent
       │
4. Subagent 1 处理子任务 → 返回结果
       │
5. Subagent 2 处理子任务 → 返回结果
       │
6. 父 Agent 整合结果，反馈给用户
```

### 示例对话

```
用户: 我需要一个用户管理页面，包括列表、新增、编辑、删除功能

Agent (Tech Lead):
  收到需求，我将分解为以下几个部分：

  1. 数据库 — 设计 users 表（交给 DBA）
  2. 后端 — 实现 CRUD API（交给 Backend）
  3. 前端 — 实现管理页面（交给 Frontend）

  [自动调用 Frontend Subagent]
  Frontend: 正在创建用户管理页面组件...
  - UserList.tsx ✓
  - UserForm.tsx ✓
  - 路由配置 ✓

  [自动调用 Backend Subagent]
  Backend: 正在创建 API 接口...
  - GET /api/users ✓
  - POST /api/users ✓
  - PUT /api/users/:id ✓
  - DELETE /api/users/:id ✓

  [自动调用 DBA Subagent]
  DBA: 正在创建数据库迁移...
  - users 表 ✓
  - 索引 ✓

  ====================================
  ✅ 全部完成！以下是变更摘要：
  - 新建 5 个文件
  - 修改 2 个文件
  - 创建 1 个数据库迁移
```

## 实战场景

### 场景一：全栈功能开发

```json
{
  "name": "Feature Developer",
  "description": "功能开发协调者",
  "subagents": [
    {
      "name": "UI Builder",
      "trigger": "用户界面|组件|页面|样式|布局",
      "agent": "frontend-architect",
      "prompt": "请根据项目设计规范实现 UI。完成后告知后端需要哪些 API。"
    },
    {
      "name": "API Builder",
      "trigger": "接口|API|端点|路由|控制器",
      "agent": "backend-specialist",
      "prompt": "根据前端需求实现 API。返回标准的 JSON 响应格式。"
    },
    {
      "name": "Test Writer",
      "trigger": "测试完成后|验证功能",
      "agent": "test-writer",
      "prompt": "对新增的代码编写单元测试和集成测试。"
    }
  ]
}
```

### 场景二：代码迁移

```json
{
  "name": "Migration Lead",
  "description": "代码迁移协调者",
  "subagents": [
    {
      "name": "JS to TS Converter",
      "trigger": "转换为TypeScript|加类型",
      "agent": "typescript-specialist",
      "prompt": "将 JavaScript 代码转换为 TypeScript，确保类型安全。"
    },
    {
      "name": "Linter",
      "trigger": "代码风格检查|格式化",
      "agent": "code-reviewer",
      "prompt": "检查代码是否符合项目 ESLint 和 Prettier 配置。"
    }
  ]
}
```

### 场景三：文档生成

```json
{
  "name": "Documentation Lead",
  "description": "文档生成协调者",
  "subagents": [
    {
      "name": "API Doc Generator",
      "trigger": "API文档|接口文档",
      "agent": "doc-writer",
      "prompt": "分析 API 代码，生成 OpenAPI/Swagger 格式的 API 文档。"
    },
    {
      "name": "Readme Generator",
      "trigger": "README|项目说明",
      "agent": "doc-writer",
      "prompt": "根据项目结构生成 README.md，包括安装、使用、贡献指南。"
    }
  ]
}
```

## Subagent 通信

### 父 Agent 向 Subagent 传递信息

父 Agent 在调用 Subagent 时，可以传递上下文：

```json
{
  "subagents": [
    {
      "name": "API Builder",
      "agent": "backend-specialist",
      "prompt": "当前项目使用 Express + TypeScript，
               认证中间件在 @src/middleware/auth.ts，
               数据库 ORM 是 Prisma，
               请遵循这些约束实现 API。"
    }
  ]
}
```

### Subagent 向父 Agent 返回结果

Subagent 返回的结果会包含：
- 做了什么操作
- 创建/修改了哪些文件
- 有什么注意事项
- 父 Agent 需要做什么整合工作

## 限制与注意事项

### Subagent 的局限性

1. **独立上下文**：每个 Subagent 有独立的对话上下文，不共享记忆
2. **无法互相通信**：Subagent 之间不能直接通信，必须通过父 Agent 中转
3. **触发依赖关键词**：trigger 是简单的关键词匹配，不是语义理解
4. **串行执行**：默认情况下 Subagent 是串行执行的

### 避免的问题

```json
// ❌ 不好：trigger 太宽泛
{
  "trigger": "代码"  // 几乎所有请求都包含"代码"
}

// ✅ 好：trigger 精确
{
  "trigger": "React 组件|JSX|hooks|useState|useEffect"
}
```

```json
// ❌ 不好：Subagent 之间职责重叠
{
  "subagents": [
    { "name": "Coder", "trigger": "写代码|实现" },
    { "name": "Developer", "trigger": "开发|编程" }  // 与 Coder 重叠
  ]
}
```

```json
// ✅ 好：职责分明
{
  "subagents": [
    { "name": "Frontend", "trigger": "UI|组件|样式|页面" },
    { "name": "Backend", "trigger": "API|数据库|服务端" },
    { "name": "DevOps", "trigger": "部署|Docker|CI/CD" }
  ]
}
```

## 调试 Subagent

### 查看调用链

```
/status

# 显示当前会话的 Subagent 调用历史
```

### 强制调用特定 Subagent

```
使用 Frontend Subagent 重新设计导航栏
```

### 禁用某个 Subagent

在 TUI 中临时禁用：

```
/subagent disable "Frontend Dev"
```

## 最佳实践

1. 🎯 **精确的 trigger**：避免过于宽泛或过于狭窄的关键词
2. 📋 **明确的职责边界**：每个 Subagent 只做一类事
3. 📝 **清晰的 prompt**：告诉 Subagent 项目的约束和规范
4. 🔗 **父子协作**：父 Agent 负责协调和审查，Subagent 负责执行
5. 🧪 **逐步构建**：先从一个 Subagent 开始，验证效果后再添加更多

## 下一步

了解 Subagent 后，继续学习 👉 [无头模式](03-headless-mode.md)
