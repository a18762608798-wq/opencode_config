# 第一次使用

## 启动你的第一个会话

### 1. 进入项目目录

```bash
cd /path/to/your/project
```

### 2. 启动 OpenCode

```bash
opencode
```

你会看到 TUI（文本用户界面）启动，显示类似以下内容：

```
┌─ OpenCode ──────────────────────────────────────────┐
│  Agent: Build     Model: claude-sonnet-4             │
│  Provider: anthropic                                 │
│                                                      │
│  > _                                                 │
│                                                      │
│  ctrl+t 切换模型    / 命令    esc 退出               │
└──────────────────────────────────────────────────────┘
```

### 3. 初始化项目（重要！）

首次在一个项目中使用 OpenCode 时，建议运行初始化命令：

```
/init
```

这会分析你的项目结构和代码风格，生成一个 `AGENTS.md` 文件。

## AGENTS.md — 项目的 AI 说明书

`AGENTS.md` 是 OpenCode 理解你项目的关键文件。它包含：

- 📁 项目结构说明
- 🛠️ 技术栈信息
- 📝 编码规范
- 🎨 设计模式偏好

## 基本交互

### 引用文件

使用 `@` 符号可以**模糊搜索**并引用文件：

```
@README.md 把这个文件翻译成中文
```

输入 `@` 后会弹出文件搜索框，输入文件名即可。

### 斜杠命令

| 命令 | 功能 |
|------|------|
| `/help` | 显示帮助 |
| `/init` | 初始化项目（生成 AGENTS.md） |
| `/connect` | 配置 LLM 提供商 |
| `/model` | 切换模型 |
| `/sessions` | 查看/切换会话 |
| `/new` | 新建会话 |
| `/timeline` | 查看会话时间线 |
| `/compact` | 压缩会话上下文 |
| `/undo` | 撤销上一个操作 |
| `/redo` | 重做被撤销的操作 |
| `/clear` | 清空对话历史（同 `/new`） |
| `/cost` | 查看当前会话花费 |
| `/export` | 导出对话记录 |
| `/quit` 或 `/exit` | 退出 OpenCode |

### 快捷键

| 快捷键 | 功能 |
|--------|------|
| `Tab` | 切换 Plan / Build 模式 |
| `Ctrl+T` | 切换模型变体 |
| `Ctrl+C` | 中断当前操作 |
| `Ctrl+X N` | 新建会话 |
| `Ctrl+X L` | 会话列表 |
| `Ctrl+X G` | 会话时间线 |
| `Ctrl+X C` | 压缩上下文 |
| `Ctrl+X X` | 导出会话 |
| `Esc` | 取消 / 返回 |

## Plan 模式 vs Build 模式

OpenCode 有**两种工作模式**：

### Plan 模式（规划）

- 用于讨论方案、分析需求
- AI **只会读**代码，不会修改
- 适合：需求分析、架构设计、代码审查

### Build 模式（构建）

- 用于实际编写代码
- AI 会**读写**文件
- 适合：功能开发、Bug 修复、重构

按 `Tab` 键在两个模式间切换。

## 会话管理

OpenCode 的每个对话称为一个**会话 (Session)**，支持多会话管理。

### 查看和切换会话

在 TUI 中输入 `/sessions` 打开会话列表面板：

### 新建会话

输入 `/new`（别名：`/clear`），创建全新会话——AI 记忆清空，从零开始。

快捷键：`Ctrl+X N`

### 查看会话时间线

输入 `/timeline` 查看当前会话的完整对话历史时间线。

快捷键：`Ctrl+X G`

### 压缩会话上下文

当会话很长、token 消耗过高时，输入 `/compact`（别名：`/summarize`），AI 会自动总结历史对话，压缩上下文窗口。

快捷键：`Ctrl+X C`

### 导出会话

输入 `/export` 将当前对话导出为 Markdown 文件。

快捷键：`Ctrl+X X`

### Fork 会话

从当前会话的某个节点分叉出一个新会话（保留历史上下文，独立发展）。需要在 `config.json` 中配置快捷键：

```json
{
  "keybinds": {
    "session_fork": "<leader>f"
  }
}
```

### 命令行启动选项

以下操作在启动 OpenCode 时通过命令行参数完成：

| 命令 | 说明 |
|------|------|
| `opencode --continue` | 继续上次会话 |
| `opencode --session <id>` | 继续指定会话 |
| `opencode --session <id> --fork` | Fork 指定会话后进入 |
| `opencode session list` | 在终端列出所有会话 |

## 下一步

掌握基础操作后，深入学习 👉 [TUI 基础操作](../02-core-features/01-tui-basics.md)
