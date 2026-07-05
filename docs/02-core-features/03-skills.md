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

一个 Skill 由一个 Markdown 文件定义：

```
.opencode/skills/
├── git-workflow.md
├── api-design.md
├── docker-deploy.md
└── database-migration.md
```

### Skill 文件格式

````markdown
---
name: Git Workflow
description: 规范化的 Git 工作流程操作
triggers:
  - "提交代码"
  - "commit"
  - "创建分支"
  - "merge"
  - "rebase"
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

## 内置 Skills

OpenCode 自带一些常用 Skills：

| Skill | 功能 |
|-------|------|
| `file-editor` | 文件编辑能力 |
| `code-searcher` | 代码搜索能力 |
| `command-runner` | 命令执行能力 |
| `web-researcher` | 网络搜索能力 |

## 创建自定义 Skill

### 示例一：API 设计 Skill

````markdown
---
name: API Design
description: RESTful API 设计规范和最佳实践
triggers:
  - "设计 API"
  - "创建接口"
  - "REST"
  - "endpoint"
---

# API Design Skill

## RESTful 规范

### URL 设计
- 使用复数名词：`/users` ✓  `/getUsers` ✗
- 层级关系：`/users/{id}/posts`
- 小写 + 连字符：`/user-profiles` ✓  `/userProfiles` ✗

### HTTP 方法
| 方法   | 操作   | 示例              |
|--------|--------|-------------------|
| GET    | 查询   | GET /users        |
| POST   | 创建   | POST /users       |
| PUT    | 全量更新 | PUT /users/{id}  |
| PATCH  | 部分更新 | PATCH /users/{id}|
| DELETE | 删除   | DELETE /users/{id}|

### 状态码
- 200: 成功
- 201: 创建成功
- 400: 请求参数错误
- 401: 未认证
- 403: 无权限
- 404: 资源不存在
- 500: 服务器错误

### 响应格式
```json
{
  "code": 0,
  "message": "success",
  "data": {},
  "timestamp": "2026-01-01T00:00:00Z"
}
```

### 错误响应
```json
{
  "code": 40001,
  "message": "用户名已存在",
  "details": {
    "field": "username",
    "reason": "duplicate"
  }
}
```
````

### 示例二：Docker 部署 Skill

````markdown
---
name: Docker Deploy
description: Docker 容器化部署流程
triggers:
  - "docker"
  - "部署"
  - "容器化"
  - "Dockerfile"
---

# Docker Deploy Skill

## Dockerfile 最佳实践

### 多阶段构建
```dockerfile
# 构建阶段
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

# 运行阶段
FROM node:20-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
EXPOSE 3000
CMD ["node", "dist/index.js"]
```

### docker-compose.yml 模板
```yaml
version: "3.8"
services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
    depends_on:
      - db
      - redis
    restart: unless-stopped

  db:
    image: postgres:16-alpine
    volumes:
      - pgdata:/var/lib/postgresql/data
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: user
      POSTGRES_PASSWORD: ${DB_PASSWORD}

  redis:
    image: redis:7-alpine
    volumes:
      - redisdata:/data

volumes:
  pgdata:
  redisdata:
```

## 安全注意事项

- ❌ 不要在 Dockerfile 中硬编码密钥
- ✅ 使用 Docker secrets 或环境变量
- ✅ 以非 root 用户运行容器
- ✅ 定期更新基础镜像
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
