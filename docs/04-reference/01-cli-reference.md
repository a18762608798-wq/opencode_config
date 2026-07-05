# CLI 命令参考

## 全局选项

这些选项可以用于所有 OpenCode 命令：

| 选项 | 简写 | 说明 |
|------|------|------|
| `--help` | `-h` | 显示帮助信息 |
| `--version` | `-v` | 显示版本号 |
| `--model` | `-m` | 指定模型（格式：provider/model） |
| `--agent` | | 指定 Agent |

## opencode（默认命令）

启动 TUI 交互界面。

```bash
opencode [options] [path]
```

| 参数 | 说明 |
|------|------|
| `path` | 项目路径（默认为当前目录） |

```bash
# 示例
opencode                           # 在当前目录启动
opencode /path/to/project          # 在指定目录启动
opencode --model openai/gpt-4o     # 指定模型启动
opencode --agent "Code Reviewer"   # 指定 Agent 启动
```

---

## opencode run

单次执行模式，无 TUI 界面。

```bash
opencode run [options]
```

| 选项 | 简写 | 说明 |
|------|------|------|
| `--prompt` | | 提示词（必需） |
| `--model` | `-m` | 模型 |
| `--agent` | | Agent |
| `--file` | `-f` | 引用文件（可重复使用） |
| `--format` | | 输出格式：`default`（默认）或 `json` |
| `--continue` | `-c` | 继续上次会话 |
| `--session` | `-s` | 指定会话 ID |
| `--fork` | | Fork 会话 |
| `--title` | | 会话标题 |
| `--attach` | | 连接到运行中的 opencode server |
| `--password` | `-p` | 密码（连接 server 时使用） |

### 示例

```bash
# 基本使用
opencode run --prompt "解释这个项目"

# 指定模型 + 引用文件
opencode run --model openai/gpt-4o --file src/main.go --prompt "审查代码"

# JSON 输出
opencode run --prompt "列出所有 TODO" --format json

# 继续会话
opencode run --continue --prompt "继续上次的任务"

# Fork 会话
opencode run --session abc123 --fork --prompt "尝试另一种方案"

# 带标题
opencode run --prompt "重构认证模块" --title "认证模块重构"
```

---

## opencode serve

启动 HTTP 服务。

```bash
opencode serve [options]
```

| 选项 | 说明 |
|------|------|
| `--port` | 监听端口（默认 3000） |
| `--hostname` | 监听主机名（默认 localhost） |
| `--mdns` | 启用 mDNS 发现 |
| `--mdns-domain` | 自定义 mDNS 域名 |
| `--cors` | 允许的 CORS 来源 |

### 示例

```bash
# 基本启动
opencode serve

# 自定义端口
opencode serve --port 8080

# 允许外部访问
opencode serve --hostname 0.0.0.0 --port 3000

# 带 CORS
opencode serve --cors "https://myapp.com"

# 带密码保护
OPENCODE_SERVER_PASSWORD="secret" opencode serve
```

---

## opencode agent

管理 Agent。

```bash
opencode agent [command]
```

### opencode agent create

创建新 Agent。

```bash
opencode agent create
```

交互式创建，会引导你完成 Agent 配置。

### opencode agent list

列出所有 Agent。

```bash
opencode agent list
```

### opencode agent edit

编辑 Agent。

```bash
opencode agent edit <agent-name>
```

---

## opencode session

管理会话。

### opencode session list

列出所有会话。

```bash
opencode session list
```

输出示例：

```
┌──────────────────────┬──────────────────┬─────────────────────┐
│ Session ID           │ Title            │ Last Active         │
├──────────────────────┼──────────────────┼─────────────────────┤
│ abc123-def456        │ 重构认证模块      │ 2026-07-05 14:30   │
│ ghi789-jkl012        │ 修复登录 Bug      │ 2026-07-05 09:15   │
└──────────────────────┴──────────────────┴─────────────────────┘
```

### opencode session delete

删除会话。

```bash
opencode session delete <session-id>
```

### opencode session export

导出会话。

```bash
opencode session export <session-id> [--format json|markdown]
```

### opencode session info

查看会话详情。

```bash
opencode session info <session-id>
```

---

## opencode skill

管理 Skills。

```bash
opencode skill [command]
```

### opencode skill list

列出可用 Skills。

```bash
opencode skill list
```

### opencode skill create

创建 Skill。

```bash
opencode skill create
```

### opencode skill edit

编辑 Skill。

```bash
opencode skill edit <skill-name>
```

---

## opencode connect

管理 LLM 提供商连接。

```bash
opencode connect [command]
```

### opencode connect list

列出已配置的提供商。

```bash
opencode connect list
```

### opencode connect add

添加提供商。

```bash
opencode connect add
```

### opencode connect remove

移除提供商。

```bash
opencode connect remove <provider-name>
```

---

## opencode config

管理配置。

```bash
opencode config [command]
```

### opencode config show

显示当前配置。

```bash
opencode config show
```

### opencode config set

设置配置项。

```bash
opencode config set <key> <value>
```

示例：

```bash
opencode config set default_model "anthropic/claude-sonnet-4-20250514"
opencode config set default_provider "anthropic"
```

### opencode config get

获取配置项。

```bash
opencode config get <key>
```

---

## opencode init

初始化项目（等同于 TUI 中的 `/init`）。

```bash
opencode init [path]
```

分析项目并生成 `AGENTS.md`。

---

## opencode update

更新 OpenCode。

```bash
opencode update
```

---

## 环境变量

| 变量 | 说明 |
|------|------|
| `ANTHROPIC_API_KEY` | Anthropic API Key |
| `OPENAI_API_KEY` | OpenAI API Key |
| `GEMINI_API_KEY` | Google Gemini API Key |
| `DEEPSEEK_API_KEY` | DeepSeek API Key |
| `OPENCODE_SERVER_PASSWORD` | HTTP 服务密码 |
| `OPENCODE_CONFIG_DIR` | 配置目录（默认 ~/.config/opencode） |
| `OPENCODE_LOG_LEVEL` | 日志级别（debug/info/warn/error） |
| `HTTP_PROXY` / `HTTPS_PROXY` | 代理设置 |

## 退出码

| 退出码 | 说明 |
|--------|------|
| 0 | 成功 |
| 1 | 一般错误 |
| 2 | 配置错误 |
| 3 | 网络错误 |
| 130 | 被 Ctrl+C 中断 |
