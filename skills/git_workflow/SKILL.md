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
