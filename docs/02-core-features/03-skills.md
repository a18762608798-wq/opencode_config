# Skills 技能

## 什么是 Skill？

Skill（技能）是 OpenCode 中的**可复用能力模块**。它像是给 Agent 装载的专业工具包，让 Agent 在需要时获得特定领域的知识和操作能力。

### Skill vs Agent

| 维度 | Agent | Skill |
|------|-------|-------|
| 定位 | 定义「谁来做」 | 定义「会做什么」 |
| 复用 | Agent 内使用 | 跨 Agent 复用 |
| 触发 | 用户手动选择 | Agent 按需加载 |
| 粒度 | 粗粒度（角色级） | 细粒度（能力级） |

## Skill 的结构

一个 Skill 由一个 文件夹定义, 至少需要一个SKILL.md文件：

```
opencode/skills/
├── git_workflow/SKILL.md
├── api-design/SKILL.md
├── docker_deploy/SKILL.md
└── database_migration/SKILL.md
```

## 内置 Skills

OpenCode 自带一些常用 Skills：

| Skill | 功能 |
|-------|------|
| `file-editor` | 文件编辑能力 |
| `code-searcher` | 代码搜索能力 |
| `command-runner` | 命令执行能力 |
| `web-researcher` | 网络搜索能力 |


## Skill 文件格式

### 文件名

必须是小写字母、数字和连字符，并且与目录名一致：

### 有效字段

```text
name
description
license
compatibility
metadata:
  author: mintusr
  category: scientific-computing
  audience: researchers
  version: "1.0"
```

最少包括前两个；后两个分别是写运行环境或依赖以及自定义的标签

### case

````markdown
---
name: git_workflow
description: 规范化 Git 工作流程。用于提交代码、创建或切换分支、生成 Conventional Commit、执行 merge 或 rebase，以及准备推送和 Pull Request。
---

# Git Workflow Skill

## 分支命名规范

- `feat/` — 新功能
- `fix/` — Bug 修复
- `refactor/` — 重构
- `docs/` — 文档

## Commit 规范

使用 Conventional Commits 格式：

```
<type>(<scope>): <description>

[optional body]
```

类型：
- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档
- `style`: 格式调整
- `refactor`: 重构
- `test`: 测试
- `chore`: 构建/工具

## 操作流程

### 开始新功能
1. 从 main 创建分支：`git checkout -b feat/xxx`
2. 开发完成后运行测试
3. 提交代码
4. 推送并创建 PR

### 提交代码
1. `git add <files>`
2. `git commit -m "feat(scope): description"`
3. `git push origin feat/xxx`
````

## Skill 的触发机制

Agent 会根据以下条件自动判断是否需要加载 Skill：

1. **触发器关键词**：配置中的 `triggers` 列表匹配用户输入
2. **上下文相关性**：Agent 判断当前任务是否与 Skill 相关
3. **显式调用**：用户可以明确要求使用某个 Skill

```
# 显式调用 Skill
使用 API Design skill 帮我设计用户管理接口
```

## 管理 Skills

### 查看可用 Skills

```
/skills
```

### 加载 Skill

```
/skill load api-design
```

### 卸载 Skill

```
/skill unload api-design
```

### 列出已加载 Skills

```
/skill list
```

## 最佳实践

1. 📦 **保持 Skill 单一职责**：一个 Skill 只做一件事
2. 🏷️ **写好 triggers**：覆盖足够的关键词让 Agent 能自动发现
3. 📚 **提供示例**：好的示例比长篇说明更有效
4. 🔄 **持续迭代**：根据使用反馈优化 Skill 内容
5. 🗂️ **版本管理**：将 Skills 纳入 Git，团队共享

## 下一步

了解了 Skills，接下来学习 👉 [Plan 模式](04-plan-mode.md)
