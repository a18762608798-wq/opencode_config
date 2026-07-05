# MCP Server 示例

这里展示如何创建自定义 MCP Server。

## Python MCP Server 示例

### 天气查询 Server

```python
#!/usr/bin/env python3
"""
一个简单的天气查询 MCP Server 示例。
通过 MCP 协议让 OpenCode Agent 可以查询天气信息。
"""

import json
import sys


def get_weather(city: str) -> dict:
    """
    模拟天气查询。实际使用中应替换为真实 API 调用。
    """
    # 模拟数据
    weather_data = {
        "北京": {"temp": 28, "weather": "晴", "humidity": 45},
        "上海": {"temp": 32, "weather": "多云", "humidity": 70},
        "深圳": {"temp": 30, "weather": "阵雨", "humidity": 85},
    }

    info = weather_data.get(city, {"temp": 25, "weather": "未知", "humidity": 60})
    return {
        "content": [
            {
                "type": "text",
                "text": f"{city}天气：{info['weather']}，温度 {info['temp']}°C，湿度 {info['humidity']}%"
            }
        ]
    }


def list_tools() -> dict:
    """返回可用的工具列表"""
    return {
        "tools": [
            {
                "name": "get_weather",
                "description": "查询指定城市的天气信息",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "city": {
                            "type": "string",
                            "description": "城市名称，如：北京、上海"
                        }
                    },
                    "required": ["city"]
                }
            }
        ]
    }


def handle_request(request: dict) -> dict:
    """处理 MCP 请求"""
    method = request.get("method")

    if method == "tools/list":
        return list_tools()

    elif method == "tools/call":
        tool_name = request["params"]["name"]
        arguments = request["params"].get("arguments", {})

        if tool_name == "get_weather":
            return get_weather(arguments.get("city", "北京"))

    return {"error": f"Unknown method: {method}"}


def main():
    """主循环：通过 stdio 与 OpenCode 通信"""
    for line in sys.stdin:
        try:
            request = json.loads(line.strip())
            response = handle_request(request)
            print(json.dumps(response), flush=True)
        except json.JSONDecodeError:
            print(json.dumps({"error": "Invalid JSON"}), flush=True)
        except Exception as e:
            print(json.dumps({"error": str(e)}), flush=True)


if __name__ == "__main__":
    main()
```

### 配置使用

在 `.opencode/mcp.json` 中：

```json
{
  "mcpServers": {
    "weather": {
      "command": "python",
      "args": ["./mcp/weather-server.py"]
    }
  }
}
```

---

## Node.js MCP Server 示例

### 待办事项 Server

```javascript
#!/usr/bin/env node
/**
 * 一个简单的待办事项 MCP Server。
 * 让 OpenCode Agent 可以管理待办事项列表。
 */

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

// 内存中的待办列表
const todos = [];

// 创建 MCP Server
const server = new Server(
  {
    name: "todo-server",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// 注册：列出可用工具
server.setRequestHandler("tools/list", async () => ({
  tools: [
    {
      name: "add_todo",
      description: "添加新的待办事项",
      inputSchema: {
        type: "object",
        properties: {
          title: {
            type: "string",
            description: "待办事项标题",
          },
          priority: {
            type: "string",
            enum: ["high", "medium", "low"],
            description: "优先级",
          },
        },
        required: ["title"],
      },
    },
    {
      name: "list_todos",
      description: "列出所有待办事项",
      inputSchema: {
        type: "object",
        properties: {},
      },
    },
    {
      name: "complete_todo",
      description: "完成一个待办事项",
      inputSchema: {
        type: "object",
        properties: {
          index: {
            type: "number",
            description: "待办事项的序号（从 1 开始）",
          },
        },
        required: ["index"],
      },
    },
  ],
}));

// 注册：调用工具
server.setRequestHandler("tools/call", async (request) => {
  const { name, arguments: args } = request.params;

  switch (name) {
    case "add_todo": {
      const todo = {
        title: args.title,
        priority: args.priority || "medium",
        completed: false,
        createdAt: new Date().toISOString(),
      };
      todos.push(todo);
      return {
        content: [
          {
            type: "text",
            text: `✅ 已添加待办 #${todos.length}：[${todo.priority}] ${todo.title}`,
          },
        ],
      };
    }

    case "list_todos": {
      if (todos.length === 0) {
        return {
          content: [{ type: "text", text: "📝 待办列表为空" }],
        };
      }

      const list = todos
        .map(
          (t, i) =>
            `${t.completed ? "✅" : "⬜"} #${i + 1} [${t.priority}] ${t.title}`
        )
        .join("\n");

      return {
        content: [
          {
            type: "text",
            text: `📝 待办列表（共 ${todos.length} 项）：\n${list}`,
          },
        ],
      };
    }

    case "complete_todo": {
      const idx = args.index - 1;
      if (idx < 0 || idx >= todos.length) {
        return {
          content: [{ type: "text", text: "❌ 无效的序号" }],
        };
      }
      todos[idx].completed = true;
      return {
        content: [
          {
            type: "text",
            text: `✅ 已完成：#${args.index} ${todos[idx].title}`,
          },
        ],
      };
    }

    default:
      throw new Error(`Unknown tool: ${name}`);
  }
});

// 启动 Server
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("Todo MCP Server running on stdio");
}

main().catch(console.error);
```

### 配置使用

```json
{
  "mcpServers": {
    "todo": {
      "command": "node",
      "args": ["./mcp/todo-server.js"]
    }
  }
}
```

---

## 更多 MCP Server 资源

- [MCP 官方文档](https://modelcontextprotocol.io/)
- [Awesome MCP Servers](https://github.com/punkpeye/awesome-mcp-servers)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [MCP TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk)
