# MCP 协议

## 什么是 MCP？

**MCP（Model Context Protocol）** 是由 Anthropic 提出的一种开放协议，用于标准化 AI 模型与外部工具/服务的交互方式。

简单来说，MCP 就像是 AI 的 **"USB 接口"** — 只要实现了这个协议，AI 就能连接任何工具。

```
┌──────────┐     MCP 协议      ┌──────────────┐
│ OpenCode │ ◄──────────────▶ │  MCP Server   │
│ (Client) │                   │  (Tool/Service)│
└──────────┘                   └──────────────┘
                                     │
                           ┌─────────┼─────────┐
                           ▼         ▼         ▼
                       Database    API      File System
```

## MCP 的核心概念

### Client（客户端）

OpenCode 本身就是一个 MCP Client。它负责：
- 发现可用的 MCP Server
- 管理与 Server 的连接
- 将工具调用请求发送给 Server

### Server（服务器）

MCP Server 是一个实现了 MCP 协议的服务程序，提供具体的工具能力。例如：

- 数据库查询 Server
- 文件系统操作 Server
- 第三方 API 集成 Server
- 浏览器自动化 Server

### Tool（工具）

Server 暴露的具体能力单元。例如一个 GitHub Server 可能提供：

- `create_issue` — 创建 Issue
- `list_prs` — 列出 Pull Request
- `search_code` — 搜索代码

## 配置 MCP Server

### 全局配置

在 `~/.config/opencode/mcp.json` 中配置：

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-server-filesystem", "/path/to/allowed/dir"]
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
      "args": ["-y", "@anthropic/mcp-server-postgres", "postgresql://localhost/mydb"]
    }
  }
}
```

### 项目级配置

在项目根目录创建 `.opencode/mcp.json`：

```json
{
  "mcpServers": {
    "project-db": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-server-postgres", "postgresql://localhost/myproject"]
    },
    "project-api": {
      "command": "python",
      "args": ["./mcp/api-server.py"]
    }
  }
}
```

## 常用 MCP Server

### 1. 文件系统 (Filesystem)

提供安全的文件操作能力：

```json
{
  "filesystem": {
    "command": "npx",
    "args": [
      "-y",
      "@anthropic/mcp-server-filesystem",
      "/home/user/projects"
    ]
  }
}
```

可用工具：
- `read_file` — 读取文件
- `write_file` — 写入文件
- `list_directory` — 列出目录
- `search_files` — 搜索文件

### 2. GitHub

集成 GitHub 操作：

```json
{
  "github": {
    "command": "npx",
    "args": ["-y", "@anthropic/mcp-server-github"],
    "env": {
      "GITHUB_TOKEN": "${GITHUB_TOKEN}"
    }
  }
}
```

可用工具：
- `create_issue` — 创建 Issue
- `create_pr` — 创建 Pull Request
- `search_repositories` — 搜索仓库
- `get_file_contents` — 获取文件内容

### 3. PostgreSQL

直接查询数据库：

```json
{
  "postgres": {
    "command": "npx",
    "args": [
      "-y",
      "@anthropic/mcp-server-postgres",
      "postgresql://user:pass@localhost:5432/mydb"
    ]
  }
}
```

可用工具：
- `query` — 执行 SQL 查询
- `list_tables` — 列出表
- `describe_table` — 查看表结构

### 4. Brave Search

网络搜索能力：

```json
{
  "brave-search": {
    "command": "npx",
    "args": ["-y", "@anthropic/mcp-server-brave-search"],
    "env": {
      "BRAVE_API_KEY": "${BRAVE_API_KEY}"
    }
  }
}
```

### 5. Puppeteer（浏览器自动化）

```json
{
  "puppeteer": {
    "command": "npx",
    "args": ["-y", "@anthropic/mcp-server-puppeteer"]
  }
}
```

可用工具：
- `navigate` — 导航到网页
- `screenshot` — 截图
- `click` — 点击元素
- `fill` — 填写表单

## 在 Agent 中使用 MCP

### 为 Agent 绑定 MCP Server

```json
// .opencode/agents/fullstack-dev.json
{
  "name": "Full-Stack Developer",
  "description": "全栈开发 Agent",
  "mcpServers": ["github", "postgres", "filesystem"],
  "tools": ["read_file", "write_file", "run_command"]
}
```

### 在对话中使用 MCP 工具

```
# Agent 会自动调用 MCP 工具
帮我查一下数据库中 users 表的结构

# 也可以明确指定
使用 github MCP，帮我在这个仓库创建一个 Issue：
标题：「修复登录页面样式问题」
描述：在移动端，登录按钮位置偏移...
```

## 编写自定义 MCP Server

### Python 示例

```python
# mcp/weather-server.py
import json
import sys
from urllib.request import urlopen

def handle_request(request):
    """处理 MCP 请求"""
    method = request.get("method")

    if method == "tools/list":
        return {
            "tools": [
                {
                    "name": "get_weather",
                    "description": "获取指定城市的天气信息",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "city": {
                                "type": "string",
                                "description": "城市名称"
                            }
                        },
                        "required": ["city"]
                    }
                }
            ]
        }

    elif method == "tools/call":
        tool_name = request["params"]["name"]
        arguments = request["params"]["arguments"]

        if tool_name == "get_weather":
            city = arguments["city"]
            # 这里可以调用真实的天气 API
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"{city}的天气：晴，25°C，湿度 60%"
                    }
                ]
            }

    return {"error": "Unknown method"}

if __name__ == "__main__":
    # MCP 使用 stdio 通信
    for line in sys.stdin:
        request = json.loads(line)
        response = handle_request(request)
        print(json.dumps(response), flush=True)
```

### Node.js 示例

```javascript
// mcp/todo-server.js
import { Server } from "@anthropic/mcp-sdk/server";
import { StdioServerTransport } from "@anthropic/mcp-sdk/server/stdio.js";

const server = new Server({
  name: "todo-server",
  version: "1.0.0",
});

// 注册工具
server.setRequestHandler("tools/list", async () => ({
  tools: [
    {
      name: "add_todo",
      description: "添加待办事项",
      inputSchema: {
        type: "object",
        properties: {
          title: { type: "string", description: "待办标题" },
          priority: {
            type: "string",
            enum: ["high", "medium", "low"],
          },
        },
        required: ["title"],
      },
    },
  ],
}));

const todos = [];

server.setRequestHandler("tools/call", async (request) => {
  const { name, arguments: args } = request.params;

  if (name === "add_todo") {
    todos.push({ title: args.title, priority: args.priority || "medium" });
    return {
      content: [{ type: "text", text: `已添加待办: ${args.title}` }],
    };
  }
});

// 启动 Server
const transport = new StdioServerTransport();
await server.connect(transport);
```

### 配置自定义 MCP Server

```json
{
  "mcpServers": {
    "weather": {
      "command": "python",
      "args": ["./mcp/weather-server.py"]
    },
    "todo": {
      "command": "node",
      "args": ["./mcp/todo-server.js"]
    }
  }
}
```

## MCP 最佳实践

1. 🔒 **最小权限原则**：只给 Agent 必要的工具权限
   ```json
   // ✅ 好：限制文件系统访问范围
   { "args": ["-y", "@anthropic/mcp-server-filesystem", "/home/user/projects/myapp"] }

   // ❌ 坏：开放整个文件系统
   { "args": ["-y", "@anthropic/mcp-server-filesystem", "/"] }
   ```

2. ⚡ **保持工具简单**：一个工具只做一件事

3. 📝 **写好工具描述**：清晰的描述帮助 AI 正确使用工具

4. 🧪 **充分测试**：确保 MCP Server 在各种输入下都稳定

5. 🚫 **避免副作用**：工具应该是幂等的，多次调用结果一致

## 下一步

掌握了 MCP，进入进阶玩法 👉 [自定义 Agent](../03-advanced/01-custom-agents.md)
