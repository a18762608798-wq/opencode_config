# 自定义 Skill 示例

这里展示如何创建自定义 Skill。

## Git Workflow Skill

文件名：`git-workflow.md`

```markdown
---
name: Git Workflow
description: 规范化的 Git 工作流程
triggers:
  - "提交"
  - "commit"
  - "分支"
  - "branch"
  - "merge"
  - "rebase"
  - "PR"
---

# Git Workflow

## 分支命名

- `feat/xxx` — 新功能
- `fix/xxx` — Bug 修复
- `refactor/xxx` — 重构
- `docs/xxx` — 文档
- `chore/xxx` — 杂项

## Commit 格式

使用 Conventional Commits：

```
<type>(<scope>): <subject>

<body>
```

类型：
- `feat` — 新功能
- `fix` — 修复
- `docs` — 文档
- `refactor` — 重构
- `test` — 测试
- `chore` — 构建

## 工作流程

1. 从 main 创建功能分支
2. 完成开发后运行测试
3. 提交代码
4. 推送到远端
5. 创建 Pull Request
```

---

## API Design Skill

文件名：`api-design.md`

```markdown
---
name: API Design
description: RESTful API 设计规范
triggers:
  - "API"
  - "接口"
  - "REST"
  - "endpoint"
  - "路由"
---

# API Design Rules

## URL 规范
- 使用复数名词：`/users`
- 小写 + 连字符：`/user-profiles`
- 层级不超过 3 层

## HTTP 方法
| 方法 | 用途 |
|------|------|
| GET | 查询 |
| POST | 创建 |
| PUT | 全量更新 |
| PATCH | 部分更新 |
| DELETE | 删除 |

## 响应格式
```json
{
  "code": 0,
  "message": "success",
  "data": {}
}
```

## 分页
- 参数：`?page=1&pageSize=20`
- 响应包含：`total`, `page`, `pageSize`, `list`
```

---

## 使用方式

1. 将 `.md` 文件放入 `.opencode/skills/` 目录
2. 在 TUI 中使用 `/skill load <name>` 加载
3. Agent 会在匹配 trigger 关键词时自动使用
