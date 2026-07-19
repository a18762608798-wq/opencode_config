---
name: mcp-builder
description: 创建高质量 MCP（Model Context Protocol）服务器的指南，使 LLM 能够通过设计良好的工具与外部服务交互。在构建 MCP 服务器以集成外部 API 或服务时使用，无论是 Python（FastMCP）还是 Node/TypeScript（MCP SDK）。
license: Complete terms in LICENSE.txt
---

# MCP 服务器开发指南

## 概述

创建 MCP（Model Context Protocol）服务器，使 LLM 能够通过设计良好的工具与外部服务交互。MCP 服务器的质量取决于它使 LLM 完成现实任务的能力。

---

# 流程

## 🚀 高级工作流

创建高质量的 MCP 服务器涉及四个主要阶段：

### 阶段 1：深入调研与规划

#### 1.1 理解现代 MCP 设计

**API 覆盖率 vs. 工作流工具：**
平衡全面的 API 端点覆盖与专门的工作流工具。工作流工具对特定任务可能更方便，而全面的覆盖率让智能体能够灵活组合操作。性能因客户端而异——有些客户端受益于结合基础工具的代码执行，而另一些客户端更适合高层次工作流。不确定时，优先采用全面的 API 覆盖。

**工具命名与可发现性：**
清晰、描述性的工具名称帮助智能体快速找到正确的工具。使用一致的前缀（如 `github_create_issue`、`github_list_repos`）和以操作为导向的命名。

**上下文管理：**
智能体受益于简洁的工具描述以及筛选/分页结果的能力。设计返回聚焦、相关数据的工具。某些客户端支持代码执行，可以帮助智能体高效筛选和处理数据。

**可操作的错误消息：**
错误消息应引导智能体找到解决方案，提供具体的建议和下一步。

#### 1.2 学习 MCP 协议文档

**导航 MCP 规范：**

首先使用站点地图找到相关页面：`https://modelcontextprotocol.io/sitemap.xml`

然后使用 `.md` 后缀获取 markdown 格式的特定页面（如 `https://modelcontextprotocol.io/specification/draft.md`）。

需要查阅的关键页面：
- 规范概述与架构
- 传输机制（streamable HTTP、stdio）
- 工具、资源和提示定义

#### 1.3 学习框架文档

**推荐技术栈：**
- **语言**：TypeScript（高质量的 SDK 支持和在许多执行环境中的良好兼容性，如 MCPB。此外，AI 模型擅长生成 TypeScript 代码，受益于其广泛使用、静态类型和良好的 lint 工具）
- **传输**：远程服务器使用 Streamable HTTP，使用无状态 JSON（比有状态会话和流式响应更易扩展和维护）。本地服务器使用 stdio。

**加载框架文档：**

- **MCP 最佳实践**：[📋 查看最佳实践](./reference/mcp_best_practices.md) - 核心指南

**TypeScript（推荐）：**
- **TypeScript SDK**：使用 WebFetch 加载 `https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/main/README.md`
- [⚡ TypeScript 指南](./reference/node_mcp_server.md) - TypeScript 模式和示例

**Python：**
- **Python SDK**：使用 WebFetch 加载 `https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/README.md`
- [🐍 Python 指南](./reference/python_mcp_server.md) - Python 模式和示例

#### 1.4 规划实现

**理解 API：**
查阅服务的 API 文档，识别关键端点、认证要求和数据模型。按需使用网络搜索和 WebFetch。

**工具选择：**
优先采用全面的 API 覆盖。列出要实现的端点，从最常见的操作开始。

---

### 阶段 2：实现

#### 2.1 设置项目结构

参见各语言指南了解项目设置：
- [⚡ TypeScript 指南](./reference/node_mcp_server.md) - 项目结构、package.json、tsconfig.json
- [🐍 Python 指南](./reference/python_mcp_server.md) - 模块组织、依赖

#### 2.2 实现核心基础设施

创建共享工具：
- 带认证的 API 客户端
- 错误处理辅助函数
- 响应格式化（JSON/Markdown）
- 分页支持

#### 2.3 实现工具

对于每个工具：

**输入 Schema：**
- 使用 Zod（TypeScript）或 Pydantic（Python）
- 包含约束和清晰的描述
- 在字段描述中添加示例

**输出 Schema：**
- 在可能时定义 `outputSchema` 用于结构化数据
- 在工具响应中使用 `structuredContent`（TypeScript SDK 功能）
- 帮助客户端理解和处理工具输出

**工具描述：**
- 功能的简洁摘要
- 参数描述
- 返回类型 schema

**实现：**
- I/O 操作使用 Async/await
- 适当的错误处理，提供可操作的错误消息
- 在适用时支持分页
- 使用现代 SDK 时返回文本内容和结构化数据

**注解：**
- `readOnlyHint`：true/false
- `destructiveHint`：true/false
- `idempotentHint`：true/false
- `openWorldHint`：true/false

---

### 阶段 3：审查与测试

#### 3.1 代码质量

审查以下方面：
- 无重复代码（DRY 原则）
- 一致的错误处理
- 完整的类型覆盖
- 清晰的工具描述

#### 3.2 构建与测试

**TypeScript：**
- 运行 `npm run build` 验证编译
- 使用 MCP Inspector 测试：`npx @modelcontextprotocol/inspector`

**Python：**
- 验证语法：`python -m py_compile your_server.py`
- 使用 MCP Inspector 测试

参见各语言指南了解详细的测试方法和质量检查清单。

---

### 阶段 4：创建评估

实现 MCP 服务器后，创建全面的评估来测试其有效性。

**加载 [✅ 评估指南](./reference/evaluation.md) 获取完整的评估指南。**

#### 4.1 理解评估目的

使用评估来检验 LLM 是否能有效地使用你的 MCP 服务器来回答现实、复杂的问题。

#### 4.2 创建 10 个评估问题

创建有效的评估，遵循评估指南中概述的流程：

1. **工具检查**：列出可用工具并了解其能力
2. **内容探索**：使用只读操作探索可用数据
3. **问题生成**：创建 10 个复杂、现实的问题
4. **答案验证**：自己解答每个问题以验证答案

#### 4.3 评估要求

确保每个问题：
- **独立**：不依赖其他问题
- **只读**：仅需非破坏性操作
- **复杂**：需要多次工具调用和深入探索
- **现实**：基于人类关心的真实用例
- **可验证**：单一、清晰的答案，可通过字符串比较验证
- **稳定**：答案不会随时间改变

#### 4.4 输出格式

创建具有以下结构的 XML 文件：

```xml
<evaluation>
  <qa_pair>
    <question>查找关于带有动物代号的 AI 模型发布的讨论。一个模型需要特定安全等级，使用 ASL-X 格式。以斑点野猫命名的模型正在确定数字 X 是多少？</question>
    <answer>3</answer>
  </qa_pair>
<!-- 更多 qa_pairs... -->
</evaluation>
```

---

# 参考文件

## 📚 文档库

在开发过程中按需加载这些资源：

### 核心 MCP 文档（首先加载）
- **MCP 协议**：从 `https://modelcontextprotocol.io/sitemap.xml` 的站点地图开始，然后使用 `.md` 后缀获取特定页面
- [📋 MCP 最佳实践](./reference/mcp_best_practices.md) - 通用 MCP 指南，包括：
  - 服务器和工具命名约定
  - 响应格式指南（JSON vs Markdown）
  - 分页最佳实践
  - 传输选择（streamable HTTP vs stdio）
  - 安全和错误处理标准

### SDK 文档（在阶段 1/2 加载）
- **Python SDK**：从 `https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/README.md` 获取
- **TypeScript SDK**：从 `https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/main/README.md` 获取

### 各语言实现指南（在阶段 2 加载）
- [🐍 Python 实现指南](./reference/python_mcp_server.md) - 完整的 Python/FastMCP 指南，包含：
  - 服务器初始化模式
  - Pydantic 模型示例
  - 使用 `@mcp.tool` 注册工具
  - 完整的工作示例
  - 质量检查清单

- [⚡ TypeScript 实现指南](./reference/node_mcp_server.md) - 完整的 TypeScript 指南，包含：
  - 项目结构
  - Zod schema 模式
  - 使用 `server.registerTool` 注册工具
  - 完整的工作示例
  - 质量检查清单

### 评估指南（在阶段 4 加载）
- [✅ 评估指南](./reference/evaluation.md) - 完整的评估创建指南，包含：
  - 问题创建指南
  - 答案验证策略
  - XML 格式规范
  - 示例问题和答案
  - 使用提供的脚本运行评估
