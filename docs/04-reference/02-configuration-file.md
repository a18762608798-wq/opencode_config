# 配置文件参考

## 配置文件位置

OpenCode 的配置分布在两个层级：

| 层级 | 路径 | 作用范围 |
|------|------|---------|
| 全局 | `~/.config/opencode/` | 所有项目 |
| 项目 | `<project>/.opencode/` | 当前项目 |

> 💡 项目级配置会覆盖全局配置中的同名项。

## 目录结构

```
~/.config/opencode/
├── config.json           # 主配置文件
├── credentials/          # API Key 存储
│   └── *.json
├── agents/               # 全局 Agent 定义
│   └── *.json
├── skills/               # 全局 Skill 定义
│   └── *.md
├── mcp.json              # 全局 MCP 服务器配置
├── sessions/             # 会话历史
│   └── *.json
└── logs/                 # 日志文件
    └── opencode.log
```

```
<project>/.opencode/
├── agents/               # 项目 Agent
│   └── *.json
├── skills/               # 项目 Skill
│   └── *.md
├── mcp.json              # 项目 MCP 配置
└── prompts/              # 提示词模板
    └── *.md
```

## config.json

### 完整配置示例

```jsonc
{
  // === 默认设置 ===
  "default_model": "anthropic/claude-sonnet-4-20250514",
  "default_provider": "anthropic",

  // === 提供商配置 ===
  "providers": {
    "anthropic": {
      "type": "anthropic",
      "api_key": "env:ANTHROPIC_API_KEY",
      "base_url": "https://api.anthropic.com"
    },
    "openai": {
      "type": "openai",
      "api_key": "env:OPENAI_API_KEY",
      "base_url": "https://api.openai.com/v1"
    },
    "openrouter": {
      "type": "openai_compatible",
      "api_key": "env:OPENROUTER_API_KEY",
      "base_url": "https://openrouter.ai/api/v1"
    },
    "ollama": {
      "type": "ollama",
      "base_url": "http://localhost:11434"
    }
  },

  // === 模型配置 ===
  "models": {
    "anthropic/claude-sonnet-4-20250514": {
      "max_tokens": 8192,
      "temperature": 0.3
    },
    "openai/gpt-5.4": {
      "max_tokens": 16384,
      "temperature": 0.5
    }
  },

  // === UI 设置 ===
  "ui": {
    "theme": "dark",              // dark | light | system
    "show_line_numbers": true,
    "show_cost": true,
    "language": "zh",             // en | zh | ja | ...
    "editor": "nvim",             // 外部编辑器
    "diff_tool": "delta"          // diff 查看工具
  },

  // === 行为设置 ===
  "behavior": {
    "auto_approve": false,         // 是否自动批准操作
    "confirm_before_delete": true,  // 删除前确认
    "max_concurrent_tasks": 3,     // 最大并发任务数
    "save_session_on_exit": true,  // 退出时保存会话
    "restore_last_session": false, // 启动时恢复上次会话
    "check_for_updates": true      // 检查更新
  },

  // === 工具设置 ===
  "tools": {
    "shell": {
      "enabled": true,              // 允许执行 shell 命令
      "timeout": 120,               // 命令超时（秒）
      "blacklist": [                // 禁止的命令
        "rm -rf /",
        "sudo rm",
        "mkfs",
        "dd if="
      ]
    },
    "filesystem": {
      "max_file_size": 1048576,    // 最大读取文件大小（字节）
      "exclude_patterns": [        // 排除模式
        "node_modules/**",
        ".git/**",
        "*.log",
        "dist/**",
        "build/**"
      ]
    }
  },

  // === 网络设置 ===
  "network": {
    "proxy": "",                    // HTTP 代理
    "timeout": 60,                  // 请求超时（秒）
    "max_retries": 3                // 最大重试次数
  },

  // === TUI 界面设置 ===
  "tui": {
    "max_history": 1000,           // 最大历史记录
    "scrollback": 10000,           // 回滚行数
    "enable_mouse": true,          // 启用鼠标
    "show_keybindings": true       // 显示快捷键提示栏
  }
}
```

## mcp.json

### 全局 MCP 配置

```jsonc
{
  "mcpServers": {
    // === 官方 MCP 服务器 ===

    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@anthropic/mcp-server-filesystem",
        "/path/to/allowed/directory"
      ]
    },

    "github": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    },

    "postgres": {
      "command": "npx",
      "args": [
        "-y",
        "@anthropic/mcp-server-postgres",
        "postgresql://localhost:5432/mydb"
      ]
    },

    "brave-search": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-server-brave-search"],
      "env": {
        "BRAVE_API_KEY": "${BRAVE_API_KEY}"
      }
    },

    "puppeteer": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-server-puppeteer"]
    },

    // === 自定义 MCP 服务器 ===

    "custom-api": {
      "command": "python",
      "args": ["/path/to/mcp/api-server.py"],
      "env": {
        "API_KEY": "${MY_API_KEY}"
      }
    },

    "docker-mcp": {
      "command": "docker",
      "args": [
        "run", "-i", "--rm",
        "-v", "/var/run/docker.sock:/var/run/docker.sock",
        "my-mcp-server"
      ]
    }
  }
}
```

### 项目级 MCP 配置

项目目录下的 `.opencode/mcp.json` 可以覆盖或扩展全局 MCP 配置：

```jsonc
{
  // "extends" 继承全局配置
  "extends": true,

  // 新增项目特定的 MCP
  "mcpServers": {
    "project-db": {
      "command": "npx",
      "args": [
        "-y",
        "@anthropic/mcp-server-postgres",
        "postgresql://localhost:5432/myproject"
      ]
    }
  }
}
```

## Agent 配置参考

见 [自定义 Agent](../03-advanced/01-custom-agents.md) 章节。

## Skill 配置参考

见 [Skills 技能](../02-core-features/03-skills.md) 章节。

## 环境变量完整列表

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `ANTHROPIC_API_KEY` | Anthropic API 密钥 | - |
| `OPENAI_API_KEY` | OpenAI API 密钥 | - |
| `GEMINI_API_KEY` | Google Gemini API 密钥 | - |
| `DEEPSEEK_API_KEY` | DeepSeek API 密钥 | - |
| `OPENROUTER_API_KEY` | OpenRouter API 密钥 | - |
| `OPENCODE_SERVER_PASSWORD` | HTTP 服务 Basic Auth 密码 | - |
| `OPENCODE_CONFIG_DIR` | 配置目录 | `~/.config/opencode` |
| `OPENCODE_LOG_LEVEL` | 日志级别 | `info` |
| `OPENCODE_NO_COLOR` | 禁用彩色输出 | `false` |
| `HTTP_PROXY` | HTTP 代理 | - |
| `HTTPS_PROXY` | HTTPS 代理 | - |
| `NO_PROXY` | 不走代理的地址 | - |
