# 上下文工程

## 什么是上下文工程？

**上下文工程（Context Engineering）** 是设计和优化 AI 所见信息的过程，目的是让 AI 在有限上下文窗口内获得最相关、最有价值的信息。

对于 OpenCode 来说，上下文工程直接决定了 Agent 的输出质量。

## 为什么上下文工程很重要？

### LLM 的上下文窗口限制

每个模型都有上下文窗口上限：

| 模型 | 上下文窗口 |
|------|-----------|
| Claude Sonnet 4 | 200K tokens |
| GPT-5.4 | 256K tokens |
| Gemini 2.5 Pro | 1M tokens |
| DeepSeek-V3 | 128K tokens |

上下文窗口越大 ≠ 效果越好。关键在**信息的密度和相关性**。

### 垃圾进，垃圾出

```
┌─────────────────────────────────────┐
│  上下文质量      →    AI 输出质量    │
│                                     │
│  混乱的上下文    →   混乱的回答      │
│  精确的上下文    →   精准的回答      │
└─────────────────────────────────────┘
```

## 上下文工程的层次

### 第一层：AGENTS.md

`AGENTS.md` 是最基础的上下文工程，定义项目的全局信息。

**高质量 AGENTS.md 的特征：**

````markdown
## 项目概述

这是 xxx 系统，服务于 xxx 用户，核心功能是 xxx。

## 技术决策

我们使用 PostgreSQL 而不是 MongoDB 是因为需要强事务支持。
缓存层使用 Redis，策略是 Cache-Aside。

## 架构约束

- 不允许在 Controller 中直接操作数据库，必须通过 Service 层
- 所有 API 响应格式为 `{ code, message, data }`
- 错误处理统一使用自定义异常类

## 代码约定

- 函数不超过 50 行
- 文件不超过 300 行
- 测试文件与源文件同目录
- 提交信息遵循 Conventional Commits

## 当前状态

- 正在从 REST 迁移到 GraphQL
- 支付模块正在重构，暂时不要修改
- 部署在 K8s 集群，使用 Helm charts
````

> 💡 **关键原则**：写「为什么」而不仅仅是「是什么」。

### 第二层：目录级 AGENTS.md

在大型项目中，可以在子目录放置更具体的 `AGENTS.md`：

```
project/
├── AGENTS.md                 # 全局约束
├── frontend/
│   └── AGENTS.md             # 前端特定约束
├── backend/
│   └── AGENTS.md             # 后端特定约束
└── infrastructure/
    └── AGENTS.md             # 基础设施约束
```

**frontend/AGENTS.md 示例：**

```markdown
## 前端技术栈

- React 18 + TypeScript
- 状态管理：Zustand
- 样式：Tailwind CSS
- 组件库：基于 Radix UI 的自定义组件

## 组件规范

- 每个组件一个文件
- Props 必须定义 interface
- 使用 named export
- 组件文件命名：PascalCase.tsx
```

### 第三层：选择性文件引用（@）

使用 `@` 符号精确引用相关文件，而不是盲目引用整个项目。

```
# ✅ 好：精确引用
@src/services/auth.ts @src/middleware/auth.ts
帮我分析认证流程

# ❌ 差：过度引用
@src/
帮我分析认证流程     # 会把整个 src 目录读入上下文
```

### 第四层：Prompt 工程

在每次对话中，通过 prompt 精确控制 AI 的行为。

#### 结构化 Prompt 模板

```
## 任务
{具体任务描述}

## 约束
- {约束1}
- {约束2}

## 上下文
- @{相关文件1}
- @{相关文件2}

## 输出要求
- 格式：{期望格式}
- 语言：{中文/英文}

## 示例（可选）
{提供期望输出的示例}
```

#### 实例对比

```
# ❌ 模糊的 prompt
帮我改一下登录

# ✅ 结构化的 prompt
## 任务
在 @src/auth/login.ts 中添加账号锁定功能：
连续 5 次登录失败后锁定账号 30 分钟

## 约束
- 不改变现有 API 签名
- 锁定状态存储在 Redis
- 失败次数记录也要存在 Redis（key 格式：login:attempts:{userId}）

## 输出要求
- 只修改 login.ts，不创建新文件
- 添加必要的日志
- 用中文写注释
```

## AGENTS.md 进阶技巧

### 1. 使用模板变量

OpenCode 支持在 `AGENTS.md` 中使用一些模板变量：

```markdown
## 项目信息

- 项目名称：{{PROJECT_NAME}}
- 主分支：{{DEFAULT_BRANCH}}
- 包管理器：{{PACKAGE_MANAGER}}
```

### 2. 条件规则

```markdown
## 代码规则

### 对于 TypeScript 文件
- 严格模式开启
- 禁止使用 any
- 优先使用 interface 而非 type

### 对于测试文件
- 使用 describe/it 模式
- 测试文件后缀：.test.ts
- Mock 放在 __mocks__ 目录

### 对于配置文件
- 使用 .env.example 作为模板
- 敏感信息使用环境变量
```

### 3. 添加入门指南

```markdown
## 新人入门

### 项目启动
```bash
git clone <repo>
cd project
pnpm install
cp .env.example .env
pnpm dev
```

### 关键文档
- 架构设计：[ARCHITECTURE.md](./docs/ARCHITECTURE.md)
- API 文档：[API.md](./docs/API.md)
- 部署指南：[DEPLOY.md](./docs/DEPLOY.md)
```

## 上下文窗口管理

### 精简原则

1. **引用的文件不要超过实际需要**：多余的文件消耗 token 且分散注意力
2. **拆分大文件**：单个文件超过 1000 行时考虑拆分
3. **清除无关历史**：用 `/clear` 清理不再需要的对话历史

### Token 估算

```
英文：1 token ≈ 4 个字符 ≈ 0.75 个单词
中文：1 token ≈ 1.5-2 个字符
代码：1 token ≈ 3-4 个字符
```

### 上下文预算分配

对于 200K 窗口，建议分配：

```
├── AGENTS.md: ~2K tokens (1%)
├── 引用文件: ~50K tokens (25%)
├── 对话历史: ~30K tokens (15%)
├── 系统提示词: ~5K tokens (2.5%)
└── 输出预留: ~113K tokens (56.5%)
```

## Skills 作为上下文注入

Skills 也是一种上下文工程手段——将高频使用的知识和规则封装为 Skill，按需注入：

```markdown
---
name: Project Rules
description: 项目特定规则
triggers: ["写代码", "修改文件", "创建组件"]
---

# 项目规则

## 目录结构
...
## 命名规范
...
## 禁止事项
...
```

## 实战：优化一个混乱的上下文

### Before（混乱）

```
用户：帮我加个功能

AGENTS.md 内容：
# 项目
这是一个项目
```

引用了 15 个不相关的文件，对话历史有 50 轮，包括闲聊。

### After（优化后）

```
用户：在用户设置页面添加「深色模式」切换开关

AGENTS.md 内容：
## 项目：SaaS Dashboard
- 前端 React 18 + Tailwind CSS
- 主题系统使用 CSS 变量，定义在 @src/styles/theme.css
- 用户偏好存储在 localStorage，通过 @src/hooks/usePreference.ts 读写

@src/pages/Settings.tsx @src/hooks/usePreference.ts @src/styles/theme.css
```

只引用了 3 个相关文件，AGENTS.md 提供了精准的约束。

## 最佳实践总结

1. 📝 **写好 AGENTS.md**：这是上下文工程的基石
2. 🎯 **精确引用**：用 `@` 精确引用需要的文件
3. 🗂️ **分层配置**：全局 AGENTS.md + 子目录 AGENTS.md
4. 📋 **结构化 Prompt**：用模板确保 prompt 质量
5. 🔄 **定期清理**：用 `/clear` 清除无用对话历史
6. 📊 **关注 token 使用**：用 `/cost` 查看消耗
7. 🏷️ **善用 Skills**：把重复使用的规则封装为 Skill

## 下一步

完成了所有教程内容，可以查阅 👉 [CLI 命令参考](../04-reference/01-cli-reference.md)
