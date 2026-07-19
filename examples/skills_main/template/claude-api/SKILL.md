---
name: claude-api
description: |-
  Claude API / Anthropic SDK 参考——模型 ID、定价、参数、流式传输、工具使用、MCP、智能体、缓存、Token 计数、模型迁移。
  触发条件——在打开目标文件之前阅读；不要因为"看起来像一行代码"就跳过——每当：提示中提及 Claude/Anthropic 的任何形式（Claude、Anthropic、Fable、Opus、Sonnet、Haiku、`anthropic`、`@anthropic-ai`、`claude-*`、`us.anthropic.*`、`[1m]`）；用户询问关于 LLM 的问题（定价/模型选择/限制/缓存）——绝不要凭记忆回答；或者任务是 LLM 形式的但未说明提供商（agent/MCP/工具定义/多智能体/RAG/LLM 评判/计算机使用；生成/摘要/提取/分类/重写/通过自然语言对话；调试拒绝/截断/流式/工具调用/token）。
  仅在正在使用其他提供商时跳过（覆盖所有触发条件）：查询中明确命名了 OpenAI/GPT/Gemini/Llama/Mistral/Cohere/Ollama；或对项目运行 `grep -rE 'openai|langchain_openai|google.generativeai|genai|mistralai|cohere|ollama'` 命中（如果没有命名提供商，先运行此 grep——不要读取文件）。
license: Complete terms in LICENSE.txt
---

# 使用 Claude 构建 LLM 驱动的应用程序

此技能帮助你使用 Claude 构建 LLM 驱动的应用程序。根据需求选择合适的接口，检测项目语言，然后阅读相关的语言特定文档。

## 开始之前

扫描目标文件（或如果没有目标文件，扫描提示和项目）中是否存在非 Anthropic 提供商标记——`import openai`、`from openai`、`langchain_openai`、`OpenAI(`、`gpt-4`、`gpt-5`，文件名如 `agent-openai.py` 或 `*-generic.py`，或任何明确指示保持代码提供商中立的指令。如果发现，停止并告诉用户此技能生成 Claude/Anthropic SDK 代码；询问他们是希望将文件切换到 Claude 还是需要非 Claude 的实现。不要用 Anthropic SDK 调用编辑非 Anthropic 文件。

## 输出要求

当用户要求添加、修改或实现 Claude 功能时，你的代码必须通过以下方式之一调用 Claude：

1. **项目语言的官方 Anthropic SDK**（`anthropic`、`@anthropic-ai/sdk`、`com.anthropic.*` 等）。这是一个受支持的 SDK 存在时项目的默认选择。
2. **原始 HTTP**（`curl`、`requests`、`fetch`、`httpx` 等）——仅在用户明确要求 cURL/REST/原始 HTTP、项目是 shell/cURL 项目，或语言没有官方 SDK 时使用。

绝不要混用两者——不要因为在 Python 或 TypeScript 项目中觉得更轻量就使用 `requests`/`fetch`。绝不回退到 OpenAI 兼容垫片。

**绝不要猜测 SDK 用法。** 函数名、类名、命名空间、方法签名和导入路径必须来自明确的文档——要么是本技能中的 `{lang}/` 文件，要么是 `shared/live-sources.md` 中列出的官方 SDK 仓库或文档链接。如果你需要的绑定在技能文件中没有明确记载，在编写代码之前，从 `shared/live-sources.md` 中 WebFetch 相关 SDK 仓库。不要从 cURL 形状或其他语言的 SDK 推断 Ruby/Java/Go/PHP/C# API。

**如果 WebFetch 或仓库访问失败**（网络受限、超时、克隆被阻止）：不要继续重试——根据 `{lang}/` 文件中的模式和命名空间/包表编写代码，运行编译器或解释器，并迭代错误输出。对于静态类型 SDK（C#、Java、Go），编译-修复循环比被阻止的网络研究更快地达到有效代码。

## 默认值

除非用户另有要求：

对于 Claude 模型版本，请使用 Claude Opus 4.8，可以通过精确的模型字符串 `claude-opus-4-8` 访问。对于任何远程复杂的事情，请默认使用自适应思考（`thinking: {type: "adaptive"}`）。最后，对于任何可能涉及长输入、长输出或高 `max_tokens` 的请求，请默认使用流式传输——它可以防止请求超时。如果你不需要处理单个流事件，使用 SDK 的 `.get_final_message()` / `.finalMessage()` 辅助函数获取完整响应。

## ⚠️ API 变动——你的训练先验可能已过时

几个常见的 Claude API 形态在 2025-2026 年间发生了变化。如果你从训练中回忆起某个模式，请在编写之前对照本技能中的 `{lang}/` 文件进行验证——以下几行是最常见的变更点：

| 领域 | 过时先验 | 当前 API |
|---|---|---|
| 扩展思考 | `thinking: {type: "enabled", budget_tokens: N}` | 在 Claude 4.6+ 模型上：`thinking: {type: "adaptive"}`。`budget_tokens` 在 Opus 4.6 / Sonnet 4.6 上已弃用，在 Fable 5 / Sonnet 5 / Opus 4.8 / 4.7 上会**返回 400 错误**。4.6 之前的模型仍使用 `budget_tokens`。 |
| Web 搜索 / Web 抓取工具类型 | `web_search_20250305`、`web_fetch_20250910` | `web_search_20260209`、`web_fetch_20260209`（动态筛选）在 Opus 4.8/4.7/4.6、Sonnet 5 和 Sonnet 4.6 上。旧模型保留基本变体；在 Vertex AI 上仅有基本 `web_search_20250305` 可用（Web 抓取不在 Vertex 上）——参见下方 Server Tools 快速参考。 |
| PHP 参数名 | 蛇形命名 wire 名作为命名参数（`max_tokens`） | 顶层命名参数使用驼峰命名（`maxTokens`）。嵌套数组键因功能而异（如 `'taskBudget'`、`'skillID'`、`'mcp_server_name'`）——从文档示例中复制确切键名；不要批量转换。 |

本技能中的 `{lang}/` 文件比回忆的模式更具权威性。

---

## 子命令

如果本提示底部的用户请求是一个裸子命令字符串（无散文），搜索本文档中的每个**子命令**表——包括下方附加的任何部分——并直接遵循匹配的操作列。这使用户可以通过 `/claude-api <subcommand>` 调用特定流程。如果文档中没有任何表匹配，将该请求视为普通散文。

| 子命令 | 操作 |
|---|---|
| `migrate` | 将现有 Claude API 代码迁移到较新模型。**立即读取 `shared/model-migration.md`** 并按顺序遵循：第 0 步（确认范围——在任何编辑之前询问哪些文件/目录），第 1 步（分类每个文件），然后是按目标的破坏性更改部分。不要总结指南——执行它。如果用户没有命名目标模型，在与范围问题相同的轮次中询问迁移到哪个模型。 |

---

## 语言检测

在阅读代码示例之前，确定用户正在使用哪种语言：

1. **查看项目文件**来推断语言：

   - `*.py`、`requirements.txt`、`pyproject.toml`、`setup.py`、`Pipfile` → **Python**——从 `python/` 读取
   - `*.ts`、`*.tsx`、`package.json`、`tsconfig.json` → **TypeScript**——从 `typescript/` 读取
   - `*.js`、`*.jsx`（没有 `.ts` 文件存在）→ **TypeScript**——JS 使用相同的 SDK，从 `typescript/` 读取
   - `*.java`、`pom.xml`、`build.gradle` → **Java**——从 `java/` 读取
   - `*.kt`、`*.kts`、`build.gradle.kts` → **Java**——Kotlin 使用 Java SDK，从 `java/` 读取
   - `*.scala`、`build.sbt` → **Java**——Scala 使用 Java SDK，从 `java/` 读取
   - `*.go`、`go.mod` → **Go**——从 `go/` 读取
   - `*.rb`、`Gemfile` → **Ruby**——从 `ruby/` 读取
   - `*.cs`、`*.csproj` → **C#**——从 `csharp/` 读取
   - `*.php`、`composer.json` → **PHP**——从 `php/` 读取

2. **如果检测到多种语言**（例如，Python 和 TypeScript 文件同时存在）：

   - 检查用户当前文件或问题与哪种语言有关
   - 如果仍然模糊，询问："我同时检测到 Python 和 TypeScript 文件。你为 Claude API 集成使用哪种语言？"

3. **如果无法推断语言**（空项目、无源文件或不支持的语言）：

   - 使用 AskUserQuestion，选项为：Python、TypeScript、Java、Go、Ruby、cURL/原始 HTTP、C#、PHP
   - 如果 AskUserQuestion 不可用，默认使用 Python 示例并说明："展示 Python 示例。如果你需要其他语言，请告诉我。"

4. **如果检测到不支持的语言**（Rust、Swift、C++、Elixir 等）：

   - 建议从 `curl/` 获取 cURL/原始 HTTP 示例，并说明社区 SDK 可能存在
   - 提供展示 Python 或 TypeScript 示例作为参考实现

5. **如果用户需要 cURL/原始 HTTP 示例**，从 `curl/` 读取。

### 语言特定功能支持

| 语言   | Tool Runner | Managed Agents | 说明                                 |
| ------ | ----------- | -------------- | ------------------------------------- |
| Python     | 是（beta）  | 是（beta）     | 完整支持——`@beta_tool` 装饰器 |
| TypeScript | 是（beta）  | 是（beta）     | 完整支持——`betaZodTool` + Zod    |
| Java       | 是（beta）  | 是（beta）     | 带注解类的 Beta 工具使用  |
| Go         | 是（beta）  | 是（beta）     | `toolrunner` 包中的 `BetaToolRunner`  |
| Ruby       | 是（beta）  | 是（beta）     | Beta 中的 `BaseTool` + `tool_runner`    |
| C#         | 是（beta）  | 是（beta）     | `BetaToolRunner` + 原始 JSON schema    |
| PHP        | 是（beta）  | 是（beta）     | `BetaRunnableTool` + `toolRunner()`   |
| cURL       | N/A         | 是（beta）     | 原始 HTTP，无 SDK 功能             |

> **Managed Agents 代码示例**：为 Python、TypeScript、Go、Ruby、PHP、Java 和 cURL 提供了专用的语言特定 README（`{lang}/managed-agents/README.md`、`curl/managed-agents.md`）。阅读你的语言的 README 以及语言无关的 `shared/managed-agents-*.md` 概念文件。**Agent 是持久化的——创建一次，通过 ID 引用。** 存储 `agents.create` 返回的 agent ID 并将其传递给每个后续的 `sessions.create`；不要在请求路径中调用 `agents.create`。Anthropic CLI（`ant`）是从版本控制的 YAML 创建 agent 和 environment 的一种便捷方式——参见 `shared/anthropic-cli.md`。如果你需要的绑定在 README 中没有展示，WebFetch `shared/live-sources.md` 中相关条目而不是猜测。C# 通过 `client.Beta.Agents` 和相关命名空间支持 Beta Managed Agents。

---

## 应使用哪种接口？

> **从简单开始。** 默认使用满足你需求的最简单层级。单个 API 调用和工作流处理大多数用例——仅在任务真正需要开放式、模型驱动的探索时才使用 agent。

| 用例                                        | 层级            | 推荐接口       | 原因                                                          |
| ----------------------------------------------- | --------------- | ------------------------- | ------------------------------------------------------------ |
| 分类、摘要、提取、问答  | 单个 LLM 调用 | **Claude API**            | 一次请求，一次响应                                    |
| 批量处理或嵌入                  | 单个 LLM 调用 | **Claude API**            | 专用端点                                        |
| 带有代码控制逻辑的多步骤管道 | 工作流        | **Claude API + 工具使用** | 你来编排循环                                     |
| 带有自己工具的自定义 agent                | Agent           | **Claude API + 工具使用** | 最大灵活性                                          |
| 带有工作区的服务器托管有状态 agent    | Agent           | **Managed Agents**        | Anthropic 运行循环并托管工具执行沙箱 |
| 持久化、版本化的 agent 配置              | Agent           | **Managed Agents**        | Agent 是存储的对象；sessions 固定到版本         |
| 带有文件挂载的长时间运行多轮 agent  | Agent           | **Managed Agents**        | 每个 session 的容器，SSE 事件流，Skills + MCP       |

> **注意：** Managed Agents 是当你希望 Anthropic 运行 agent 循环*并*托管工具执行容器时的正确选择——文件操作、bash、代码执行都在每个 session 的工作区中运行。如果你想自己托管计算或运行自己的自定义工具运行时，Claude API + 工具使用是正确的选择——使用 tool runner 自动处理循环，或使用手动循环实现精细控制（审批关卡、自定义日志、条件执行）。

> **云提供商访问。** **Claude Platform on AWS** 由 Anthropic 运营，具有同日 API 对等——参见 `shared/claude-platform-on-aws.md` 了解客户端设置。关于 **Claude Platform on AWS**、**Amazon Bedrock**、**Google Vertex AI** 和 **Microsoft Foundry** 的每个功能可用性，参见 `shared/platform-availability.md`——该表是本技能中唯一的真实来源；不要从其他地方推断可用性。

### 决策树

```
你的应用需要什么？

0. 哪个提供商？
   ├── 第一方 API 或 Claude Platform on AWS → 继续（完整接口可用；每个功能例外参见 shared/platform-availability.md）。
   └── Amazon Bedrock、Google Vertex AI 或 Microsoft Foundry → Claude API（+ 工具使用用于 agent）；参见 shared/platform-availability.md 了解每个功能的支持情况。

1. 单个 LLM 调用（分类、摘要、提取、问答）
   └── Claude API——一次请求，一次响应

2. 你希望 Anthropic 运行 agent 循环并托管每个 session 的
   容器，Claude 在其中执行工具（bash、文件操作、代码）吗？
   └── 是 → Managed Agents——服务器管理的 sessions，持久化的 agent 配置，
       SSE 事件流，Skills + MCP，文件挂载。
       示例："每个任务有工作区的有状态编码 agent"、
                 "将事件流式传输到 UI 的长时间运行研究 agent"、
                 "跨多个 sessions 使用的带有持久化、版本化配置的 agent"

3. 工作流（多步骤、代码编排、使用你自己的工具）
   └── 带有工具使用的 Claude API——你控制循环

4. 开放式 agent（模型决定自己的轨迹，你自己的工具，你托管计算）
   └── Claude API agentic 循环（最大灵活性）
```

### 应构建 Agent 吗？

在选择 agent 层级之前，检查所有四个标准：

- **复杂性**——任务是多步骤的且难以提前完全指定吗？（例如"将此设计文档变成 PR"vs"从此 PDF 中提取标题"）
- **价值**——结果是否能证明更高的成本和延迟？
- **可行性**——Claude 在此任务类型上有能力吗？
- **错误成本**——错误是否可以被捕获和恢复？（测试、审查、回滚）

如果对任何这些的回答是"否"，保持在更简单的层级（单个调用或工作流）。

---

## 架构

一切通过 `POST /v1/messages`。工具和输出约束是这个单一端点的功能——不是单独的 API。

**用户定义的工具**——你定义工具（通过装饰器、Zod schema 或原始 JSON），SDK 的 tool runner 处理调用 API、执行你的函数和循环直到 Claude 完成。为了完全控制，你可以手动编写循环。

**服务器端工具**——Anthropic 托管的工具，运行在 Anthropic 的基础设施上。代码执行完全是服务器端的（在 `tools` 中声明它，Claude 自动运行代码）。计算机使用可以是服务器托管或自托管。

**结构化输出**——约束 Messages API 响应格式（`output_config.format`）和/或工具参数验证（`strict: true`）。推荐的方法是 `client.messages.parse()`，它自动根据你的 schema 验证响应。注意：旧的 `output_format` 参数已弃用；在 `messages.create()` 上使用 `output_config: {format: {...}}`。

**辅助端点**——批处理（`POST /v1/messages/batches`）、文件（`POST /v1/files`）、Token 计数（`POST /v1/messages/count_tokens`——参见 `shared/token-counting.md`）和模型（`GET /v1/models`、`GET /v1/models/{id}`——实时能力/上下文窗口发现）为 Messages API 请求提供数据或支持。

---

## 当前模型（缓存：2026-06-24）

| 模型             | 模型 ID            | 上下文        | 输入 $/1M | 输出 $/1M |
| ----------------- | ------------------- | -------------- | ---------- | ----------- |
| Claude Fable 5    | `claude-fable-5`      | 1M             | $10.00     | $50.00      |
| Claude Mythos 5（仅限 Project Glasswing） | `claude-mythos-5` | 1M | $10.00     | $50.00      |
| Claude Opus 4.8   | `claude-opus-4-8`   | 1M             | $5.00      | $25.00      |
| Claude Opus 4.7   | `claude-opus-4-7`   | 1M             | $5.00      | $25.00      |
| Claude Opus 4.6   | `claude-opus-4-6`   | 1M             | $5.00      | $25.00      |
| Claude Sonnet 5   | `claude-sonnet-5`   | 1M             | $3.00（$2.00 首发至 2026-08-31） | $15.00（$10.00 首发） |
| Claude Sonnet 4.6 | `claude-sonnet-4-6` | 1M             | $3.00      | $15.00      |
| Claude Haiku 4.5  | `claude-haiku-4-5`  | 200K           | $1.00      | $5.00       |

**始终使用 `claude-opus-4-8`，除非用户明确命名了不同的模型。** 这是不可妥协的。不要使用 `claude-sonnet-5`、`claude-sonnet-4-6` 或任何其他模型，除非用户明确说"用 sonnet"或"用 haiku"。绝不要为了成本而降级——那是用户的决定，不是你的。仅在用户明确要求 Claude Fable 5、"fable" 或 Anthropic 最强大的模型时才使用 `claude-fable-5`——它与 Opus 家族有不同的 API 行为（见下文）和超出 Opus 层级的定价。

### Claude Fable 5 (`claude-fable-5`)——最强大的广泛发布模型

Claude Fable 5 是 Anthropic 最强大的广泛发布模型，用于最苛刻的推理和长时间 horizon 的 agent 工作。**Claude Mythos 5** (`claude-mythos-5`) 通过 Project Glasswing 提供相同能力、定价和 API 接口（参与是访问它的唯一方式），接替仅限邀请的 Claude Mythos Preview (`claude-mythos-preview`)——以下内容适用于两个模型。1M 上下文窗口（最大值也是默认值），128K 最大输出。与 Opus 层级的主要 API 差异——详情参见 `shared/model-migration.md` → 迁移到 Claude Fable 5：

- **思考始终开启**——完全省略 `thinking` 参数（或发送 `{type: "adaptive"}`）。任何其他显式配置都会被拒绝：`{type: "disabled"}` 和 `{type: "enabled", budget_tokens: N}` 都返回 400。使用 `output_config.effort`（支持 `low` 到 `xhigh` 和 `max`）控制深度。
- **原始思考链从不返回**——响应携带常规 `thinking` 块（不是 `redacted_thinking`）：`display: "summarized"` 返回可读摘要，`"omitted"`（默认）将 `thinking` 字段留空。重放规则：在相同模型上原样传回 thinking 块（包括空文本块——API 拒绝*修改过的*块，而非读取的块）；**不同**模型从提示中**丢弃**它们（通常静默地——不是错误；丢弃发生在计费之前，因此丢弃的块不收费，也没有需要剥离的内容）。来自其他模型的常规 thinking 块可以在模型之间自由重放。
- **分词器**——与 Opus 4.8 相同的分词器（在 Opus 4.7 中引入）。从 Opus 4.7/4.8 迁移时 Token 计数大致不变；每 Token 定价不同。从 Opus 4.6、Sonnet、Haiku 或更早版本迁移时，使用 `count_tokens` 重新基线。
- **`refusal` 停止原因——处理它，并默认选择回退**——安全分类器可能拒绝请求（HTTP 200，`stop_reason: "refusal"`，带有 `stop_details` 类别）。预输出拒绝具有空 `content` 数组且完全不收费；中间流式拒绝会收取已流式输出的费用——丢弃部分输出。在读取 `content` 之前始终检查 `stop_reason`。恢复是**在 API 上主动选择的**：大多数 Claude 消费端界面内置了 Claude Opus 4.8 回退，但不选择加入的 API 请求会在拒绝时直接停止——而良性相邻工作（安全工具、生命科学任务）上的误报确实发生。**当你编写 `claude-fable-5` 代码时，默认包含服务器端 `fallbacks` 参数**（`betas: ["server-side-fallback-2026-06-01"]` + `fallbacks: [{"model": "claude-opus-4-8"}]`；Claude API 和 Claude Platform on AWS）：被拒绝的请求在同一个调用中由回退模型透明地重新服务，自动应用信用式重新定价（输出前的拒绝不收费；救援按回退模型自身费率计费）。告诉用户你已经启用它；仅在他们拒绝时才删除。GA SDK 的客户端 `BetaRefusalFallbackMiddleware` + `BetaFallbackState` 处理所有服务器端回退不支持的地方的重试（包括 Amazon Bedrock、Vertex AI、Microsoft Foundry）；回退信用退还客户端重试的缓存切换成本。代码示例：你的语言的 claude-api 文档的回退拒绝部分；完整语义参见迁移指南的拒绝部分。
- **无 assistant prefill**——与 4.6+ 家族的其他模型相同。
- **需要 30 天数据保留**——Claude Fable 5 在零数据保留下不可用；来自保留配置不满足要求的组织的请求返回 `400 invalid_request_error`。
- **更长的回合，不同的提示**——困难任务上的单个请求可能运行数分钟（规划超时/流式/进度 UX）；effort 扫描应包括低/中用于常规工作；为先前模型编写的提示通常过于预设，会降低输出质量。参见 `shared/model-migration.md` → 迁移到 Fable 5 → 行为转变（提示可调）获取推荐的提示片段（反过度规划、不整理、有根据的进展声明、边界、异步子 agent、记忆、`send_to_user`）。

**关键：仅使用上表中的确切模型 ID 字符串——它们已经是完整的。不要追加日期后缀。** 例如，使用 `claude-sonnet-4-6`，绝不要使用 `claude-sonnet-4-6-20251114` 或你可能从训练数据中回忆起的任何其他带日期后缀的变体。如果用户请求表中没有的较旧模型（例如"opus 4.5"、"sonnet 3.7"），读取 `shared/models.md` 获取确切 ID——不要自己构建。

注意：如果上面的任何模型字符串对你来说不熟悉，那是预料之中的——只是意味着它们是在你的训练数据截止日期之后发布的。请放心，它们是真实模型；我们不会那样忽悠你。

**实时能力查询：** 上表是缓存的。当用户问"X 的上下文窗口是多少"、"X 是否支持 vision/thinking/effort"或"哪些模型支持 Y"时，查询 Models API（`client.models.retrieve(id)` / `client.models.list()`）——参见 `shared/models.md` 了解字段参考和能力筛选示例。

---

## 认证（快速参考）

**未设置的 `ANTHROPIC_API_KEY` 并不意味着没有凭据。** SDK 和 `ant` CLI 按此顺序解析凭据（先匹配者胜）：`ANTHROPIC_API_KEY` → `ANTHROPIC_AUTH_TOKEN` → `ANTHROPIC_PROFILE` 选择的或活动的 OAuth 配置文件来自 `ant auth login` → Workload Identity Federation 环境变量 → 磁盘上的默认配置文件。一个裸 `Anthropic()` / `new Anthropic()` / `anthropic.NewClient()` 在 `ant auth login` 后即使没有环境变量也能工作。

**当你需要调用 API 且 `ANTHROPIC_API_KEY` 未设置时，不要向用户索要密钥。** 首先运行 `ant auth status`——它显示活动的凭据源和配置文件。如果它报告有活动配置文件：

- **SDK 代码或 `ant` CLI：** 直接运行。零参数客户端构造函数和每个 `ant …` 子命令自动选取配置文件——无需环境变量。
- **原始 `curl` / HTTP：** 使用 `ant auth print-credentials --access-token` 获取短期令牌，并将其作为 `Authorization: Bearer <token>` 发送，**加上**头部 `anthropic-beta: oauth-2025-04-20`（OAuth 令牌在 `Authorization: Bearer` 上，而非 `x-api-key:`——将 curl 从 API 密钥转换是头部更改，而非密钥交换）。始终传入 `--access-token`；无标志形式打印 JSON，而非裸令牌。

仅当 `ant auth status` 报告没有活动凭据源（或 `ant` 本身未安装）时才向用户索要密钥。建议 `ant auth login` 作为首选——它存储配置文件在 `~/.config/anthropic/` 下，SDK 自动读取——而导出的 `ANTHROPIC_API_KEY` 作为替代方案。

完整认证详情（命名配置文件、作用域、API 密钥遮蔽配置文件陷阱、刷新令牌过期）：`shared/anthropic-cli.md`。

---

## 思考与努力（快速参考）

**Fable 5 / Opus 4.8 / 4.7 / Sonnet 5——仅自适应思考：** 使用 `thinking: {type: "adaptive"}`。`thinking: {type: "enabled", budget_tokens: N}` 返回 400——自适应是唯一的开启模式。在 Opus 4.8、Opus 4.7 和 Sonnet 5 上，`{type: "disabled"}` 和省略 `thinking` 都有效（在 Sonnet 5 上，省略运行自适应；在 Opus 4.7/4.8 上，省略无思考运行——显式设置 `{type: "adaptive"}`）；在 Fable 5 上，显式 `{type: "disabled"}` 返回 400——改为省略 `thinking` 参数。采样参数（`temperature`、`top_p`、`top_k`）也被移除并将 400。Opus 4.8 保持与 4.7 相同的请求接口（无新破坏性更改）——参见 `shared/model-migration.md` → 迁移到 Opus 4.8 了解行为重调，→ 迁移到 Opus 4.7 了解从 4.6 或更早版本迁移的完整破坏性更改列表。注意：在禁用 `thinking` 时，Opus 4.8 可能将更长的推理写入可见响应——保持自适应思考开启，或添加仅最终答案指令（参见迁移指南）。
**Opus 4.6——自适应思考（推荐）：** 使用 `thinking: {type: "adaptive"}`。Claude 动态决定何时思考以及思考多少。无需 `budget_tokens`——`budget_tokens` 在 Opus 4.6 和 Sonnet 4.6 上已弃用，不应在新增代码中使用。自适应思考也会自动启用交错思考（无需 beta 头部）。**当用户要求"扩展思考"、"思考预算"或 `budget_tokens`：始终使用 Fable 5、Opus 4.8、4.7 或 4.6 配合 `thinking: {type: "adaptive"}`。固定 Token 预算用于思考的概念已弃用——自适应思考取代了它。不要为新 4.6/4.7/4.8 代码使用 `budget_tokens`，也不要切换到旧模型。** *渐进迁移例外：* `budget_tokens` 在 Opus 4.6 和 Sonnet 4.6 上仍然作为迁移过渡的逃生口可用——如果你在调整 `effort` 之前迁移现有代码并需要硬 Token 上限，参见 `shared/model-migration.md` → 过渡逃生口。注意：此例外**不适用于** Fable 5、Opus 4.7 或 4.8——`budget_tokens` 在那里完全移除。
**Effort 参数（GA，无 beta 头部）：** 通过 `output_config: {effort: "low"|"medium"|"high"|"max"}`（在 `output_config` 内部，非顶层）控制思考深度和总体 Token 消耗。默认是 `high`（相当于省略）。`max` 在 Fable 5、Opus 4.6 及更高版本、Sonnet 5 和 Sonnet 4.6 上受支持（不在 Haiku 或更早的 Sonnets 上）。Opus 4.7 添加了 `"xhigh"`（介于 `high` 和 `max` 之间）——在 Fable 5 / Opus 4.7/4.8 / Sonnet 5 上是大多数编码和 agentic 用例的最佳设置，也是 Claude Code 中的默认设置；对于大多数对智能敏感的工作至少使用 `high`。在 Fable 5、Opus 4.5、Opus 4.6、Opus 4.7、Opus 4.8、Sonnet 5 和 Sonnet 4.6 上有效。在 Sonnet 4.5 / Haiku 4.5 上会出错。在 Fable 5、Opus 4.7/4.8 和 Sonnet 5 上，effort 比之前任何同类模型都更重要——迁移时重新调整它，并在 `high`/`xhigh` 下以完整的任务规格预先运行长时间 horizon/agentic 任务。结合自适应思考获得最佳成本-质量权衡。较低的 effort 意味着更少且更整合的工具调用、更少的前言和更简洁的确认——`high` 通常是平衡质量和 Token 效率的最佳点；当正确性比成本更重要时使用 `max`；用于子 agent 或简单任务时使用 `low`。

**思考显示——Fable 5 / Mythos 5 / Opus 4.8 / 4.7 / Sonnet 5 默认 `"omitted"`：** `display: "summarized"` 返回推理的可读摘要；`"omitted"`（所有五个的默认值——在 Opus 4.6 和 Sonnet 4.6 上是 `"summarized"` 的静默更改）以空文本流式传输 `thinking` 块。`display` 仅控制可见性——思考在任何设置下都发生且计费相同；原始思考链在任何模型上绝不暴露。如果你将推理流式传输给用户，默认看起来像是输出前的长时间暂停——显式设置 `thinking: {type: "adaptive", display: "summarized"}`。（与 display 无关，在继续相同模型时将 thinking 块原样回传；其他模型静默忽略它们——参见迁移指南。）

**任务预算（beta，Fable 5 / Opus 4.7 / 4.8 / Sonnet 5）：** `output_config: {task_budget: {type: "tokens", total: N}}` 告诉模型它对完整 agentic 循环有多少 Token——它看到运行倒计时并自我调节（最小 20,000；beta 头部 `task-budgets-2026-03-13`）。与 `max_tokens` 不同，后者是模型不知道的强制每响应上限。参见 `shared/model-migration.md` → 任务预算。

**Sonnet 4.6：** 支持自适应思考（`thinking: {type: "adaptive"}`）。`budget_tokens` 在 Sonnet 4.6 上已弃用——改用自适应思考。

**较旧模型（仅在明确要求时）：** 如果用户特别要求 Sonnet 4.5 或其他较旧模型，使用 `thinking: {type: "enabled", budget_tokens: N}`。`budget_tokens` 必须小于 `max_tokens`（最小 1024）。绝不要仅因为用户提到 `budget_tokens` 而选择较旧模型——改用 Opus 4.8 配合自适应思考。

---

## 压缩（快速参考）

**Beta，Fable 5、Opus 4.8、Opus 4.7、Opus 4.6、Sonnet 5 和 Sonnet 4.6。** 对于可能超过 1M 上下文窗口的长时间对话，启用服务器端压缩。当上下文接近触发阈值（默认：150K Token）时，API 自动摘要早期上下文。需要 Beta 头部 `compact-2026-01-12`。

**关键：** 在每一轮将 `response.content`（而不仅仅是文本）追加回你的消息。响应中的压缩块必须保留——API 使用它们在下一次请求时替换压缩的历史。仅提取文本字符串并追加将静默丢失压缩状态。

有关代码示例，参见 `{lang}/claude-api/README.md`（压缩部分）。通过 WebFetch 获取完整文档：`shared/live-sources.md`。

---

## 提示缓存（快速参考）

**前缀匹配。** 前缀中任何位置的任何字节更改会使之后的所有内容失效。渲染顺序是 `tools` → `system` → `messages`。将稳定内容放在前面（冻结的系统提示、确定性的工具列表），将易变内容（时间戳、每请求 ID、变化的问题）放在最后一个 `cache_control` 断点之后。

**中间对话操作员指令**（仅 Claude Opus 4.8；无 beta 头部）：将 `{"role": "system", ...}` 追加到 `messages[]` 中，而不是编辑顶层的 `system`。保留缓存的历史前缀，并且是防止提示注入安全的操作员通道。参见 `shared/prompt-caching.md` § 中间对话系统消息。

**顶层自动缓存**（在 `messages.create()` 上设置 `cache_control: {type: "ephemeral"}`）是最简单的选项，当你不需要精细放置时使用。每个请求最多 4 个断点。最小可缓存前缀约为 1024 Token——更短的前缀将静默不缓存。

**使用 `usage.cache_read_input_tokens` 验证**——如果在重复请求中为零，则存在静默失效因素（`datetime.now()` 在系统提示中、未排序的 JSON、变化的工具集）。

放置模式、架构指导和静默失效因素审计清单：阅读 `shared/prompt-caching.md`。语言特定语法：`{lang}/claude-api/README.md`（提示缓存部分）。

---

## 快速模式（快速参考）

**研究预览，仅 Opus 4.8 / 4.7。** Opus 4.7 快速模式已弃用——移除后，4.7 上的 `speed: "fast"` 返回错误。Opus 4.8 是持久的快速支持层级。快速模式以高级定价以最高 2.5 倍的输出 Token/秒速度运行同一模型。每个请求需要三件事：使用 **beta** 消息端点（`client.beta.messages.…`）、传递 beta 标志 `fast-mode-2026-02-01`，并设置 `speed: "fast"` 作为顶层请求参数（不是头部，不在 `extra_body` 中）。

```python
client.beta.messages.create(
    model="claude-opus-4-8", max_tokens=4096,
    speed="fast", betas=["fast-mode-2026-02-01"],
    messages=[...],
)
```

| 语言 | Beta 标志 | Speed 参数 |
|---|---|---|
| Python | `betas=["fast-mode-2026-02-01"]` | `speed="fast"` |
| TypeScript / Ruby | `betas: ["fast-mode-2026-02-01"]` | `speed: "fast"` |
| Go | `[]anthropic.AnthropicBeta{anthropic.AnthropicBetaFastMode2026_02_01}` | `Speed: anthropic.BetaMessageNewParamsSpeedFast` |
| Java | `.addBeta(AnthropicBeta.FAST_MODE_2026_02_01)` | `.speed(MessageCreateParams.Speed.FAST)` |
| C# | `Betas = ["fast-mode-2026-02-01"]` | `Speed = Speed.Fast`（`Anthropic.Models.Beta.Messages`） |
| PHP | `betas: ['fast-mode-2026-02-01']` | `speed: 'fast'` |
| cURL | `anthropic-beta: fast-mode-2026-02-01` 头部 | 正文中 `"speed": "fast"` |

`response.usage.speed` 报告使用了哪种速度。快速模式有独立于标准 Opus 的速率限制；在 429 时，要么在 `retry-after` 延迟后重试，要么删除 `speed` 并回退到标准（注意：切换速度会失效提示缓存）。不支持批处理 API、优先层级、Claude Platform on AWS 或第三方平台。

---

## 任务预算（快速参考）

**Beta，Fable 5 / Sonnet 5 / Opus 4.8 / 4.7。** 任务预算给 Claude 一个 agentic 循环的 Token 上限，使其能够自我调节并在优雅完成而非被截断。在 `client.beta.messages.stream(...)` 的 `output_config` 内设置 `task_budget`，使用 beta 标志 `task-budgets-2026-03-13`——使用流式传输，以便大的 `max_tokens` 不会触发 HTTP 超时：

```python
with client.beta.messages.stream(
    model="claude-opus-4-8", max_tokens=128000,
    output_config={"effort": "high", "task_budget": {"type": "tokens", "total": 64000}},
    betas=["task-budgets-2026-03-13"],
    messages=[...], tools=[...],
) as stream:
    response = stream.get_final_message()
```

`task_budget` 字段：`type`（始终为 `"tokens"`）、`total` 和可选的 `remaining`（默认为 `total`）。服务器注入一个 Claude 在生成期间看到的倒计时标记；预算计算 Claude 生成的内容和本轮它读取的工具结果——**而不是**你每次请求重新发送的完整历史。

**观察花费：** 跨循环迭代累积 `response.usage.output_tokens`（加上你追加的工具结果块的 Token 计数），如果你想显示进度。在正常循环中，不设置 `remaining`——服务器自己跟踪倒计时，而传递客户端计算的 `remaining` 同时重新发送完整历史会少报预算。**仅当你两次请求之间压缩或重写历史**且服务器无法再推导先前花费时，才传递 `remaining`。

---

## 提供商客户端（快速参考）

当在第三方平台上针对 Claude 时，使用该平台的专用客户端类——而不是带有 `base_url` 覆盖的的第一方 `Anthropic()` 客户端。构建后，客户端暴露与第一方 SDK 相同的 `messages.create` / `.stream` 接口。

### Amazon Bedrock

使用 **Mantle** 客户端（Messages-API Bedrock 终端节点）。Bedrock 模型 ID 使用 `anthropic.` 前缀（例如 `"anthropic.claude-opus-4-8"`）。区域（Region）是必需的。

| 语言 | 客户端 |
|---|---|
| Python | `from anthropic import AnthropicBedrockMantle` → `AnthropicBedrockMantle(aws_region="…")` |
| TypeScript | `import { AnthropicBedrockMantle } from "@anthropic-ai/bedrock-sdk"` → `new AnthropicBedrockMantle({ awsRegion: "…" })` |
| Go | `bedrock.NewMantleClient(ctx, bedrock.MantleClientConfig{ AWSRegion: "…" })` |
| Java | `AnthropicOkHttpClient.builder().backend(BedrockMantleBackend.fromEnv()).build()`（来自 `com.anthropic.bedrock.backends`） |
| C# | `new AnthropicBedrockMantleClient(new() { AwsRegion = "…" })`（包 `Anthropic.Bedrock`） |
| PHP | `use Anthropic\Bedrock\MantleClient;` → `new MantleClient(awsRegion: '…')` |
| Ruby | `Anthropic::BedrockMantleClient.new(aws_region: "…")` |

`AnthropicBedrock` / `BedrockClient` / `BedrockBackend`（不带 `Mantle`）是传统的 `bedrock-runtime` InvokeModel 路径——对于新代码建议使用 Mantle 客户端。

### Microsoft Foundry

| 语言 | 客户端 |
|---|---|
| Python | `from anthropic import AnthropicFoundry` → `AnthropicFoundry(api_key=…, resource="…")` |
| TypeScript | `import AnthropicFoundry from "@anthropic-ai/foundry-sdk"` → `new AnthropicFoundry({ … })` |
| Java | `AnthropicOkHttpClient.builder().backend(FoundryBackend.fromEnv()).build()`（来自 `com.anthropic.foundry.backends`） |
| C# | `new AnthropicFoundryClient(new AnthropicFoundryApiKeyCredentials(…))`（包 `Anthropic.Foundry`） |
| PHP | `Foundry\Client::withCredentials(…)` |

Go 和 Ruby SDK 当前不支持 Foundry。对于 Ruby，使用标准 `Anthropic::Client.new(base_url: "<foundry endpoint>")` 作为备选（Entra ID 认证未内置）。关于 Claude Platform on AWS，参见 `shared/claude-platform-on-aws.md`。

### Google Cloud Vertex AI

两个必需的构造参数：GCP `project_id` 和 `region`。Vertex 模型 ID **无前缀**——当前代模型（Opus 4.8/4.7/4.6、Sonnet 5、Sonnet 4.6）使用裸的第一方 ID（如 `"claude-opus-4-8"`）；日期快照模型使用 `@` 版本分隔符（如 `claude-opus-4-5@20251101`，**不是** `claude-opus-4-5-20251101`）。认证是 GCP ADC（`gcloud auth application-default login`）；无需 Anthropic API 密钥。`region` 可以是 `"global"`（推荐）、多区域（`"us"`/`"eu"`）或特定区域。构建后，使用相同的 `messages.create` / `.stream` 接口。

| 语言 | 客户端 |
|---|---|
| Python | `from anthropic import AnthropicVertex` → `AnthropicVertex(project_id="…", region="…")`（安装 `"anthropic[vertex]"`） |
| TypeScript | `import { AnthropicVertex } from "@anthropic-ai/vertex-sdk"` → `new AnthropicVertex({ projectId, region })` |
| Go | `import "github.com/anthropics/anthropic-sdk-go/vertex"` → `anthropic.NewClient(vertex.WithGoogleAuth(ctx, region, projectID))` |
| Java | `AnthropicOkHttpClient.builder().backend(VertexBackend.builder().region("…").project("…").build()).build()`（来自 `com.anthropic.vertex.backends`） |
| C# | `new AnthropicClient { Backend = new VertexBackend(projectId, region) }`（包 `Anthropic.Vertex`） |
| PHP | `use Anthropic\Vertex;` → `Vertex\Client::fromEnvironment(location: '…', projectId: '…')`——注意是 `location`，不是 `region` |
| Ruby | `Anthropic::VertexClient.new(region: "…", project_id: "…")` |

---

## 上下文编辑（快速参考）

**Beta。** 上下文编辑**清除**模型看到之前的旧工具结果或思考块；它不是**压缩**（压缩是摘要）。在 `client.beta.messages.*` 上使用 beta `context-management-2025-06-27`，传入带有策略类型的 `context_management.edits`：

```python
client.beta.messages.create(
    model="claude-opus-4-8", max_tokens=4096,
    betas=["context-management-2025-06-27"],
    context_management={"edits": [{"type": "clear_tool_uses_20250919"}]},
    tools=[...], messages=[...],
)
```

策略类型：`clear_tool_uses_20250919`（清除旧工具结果；可选的 `clear_tool_inputs: true` 也清除 tool_use 参数）和 `clear_thinking_20251015`（清除思考块）。**不要**使用 `compact_20260112` 或 beta `compact-2026-01-12`——那些是独立的压缩功能。

---

## 中间对话系统消息（快速参考）

**仅 Claude Opus 4.8；无 beta 头部。** 将 `{"role": "system", "content": "…"}` 追加到 `messages` 数组（不是顶层 `system` 字段）以在中间对话中添加操作员指令，而不导致缓存前缀失效。使用常规 `client.messages.create`——没有 beta。中间对话系统消息必须跟在 `user` 消息（或以服务器工具使用结束的 `assistant` 消息）之后，且必须是 `messages` 中的最后一条或被 `assistant` 轮次跟随——不能是 `messages[0]`。可用性：`shared/platform-availability.md`。参见 `shared/prompt-caching.md` § 中间对话系统消息。

---

## Managed Agents（Beta）

**Managed Agents** 是第三个接口：服务器管理的状态化 Agent 配合 Anthropic 托管的工具执行。你创建一个持久化、版本化的 Agent 配置（`POST /v1/agents`），然后启动引用它的 Sessions。每个 session 分配一个容器作为 agent 的工作区——bash、文件操作和代码执行在此运行；agent 循环本身在 Anthropic 的编排层运行，并通过工具对容器进行操作。session 流式传输事件；你发送消息和工具结果回来。

可用性：`shared/platform-availability.md`。对于 Bedrock / Vertex / Foundry 上的 agent（不支持 Managed Agents），使用 Claude API + 工具使用。

**强制性流程：** Agent（一次）→ Session（每次运行）。`model`/`system`/`tools` 存在于 agent 上，从不在 session 上。参见 `shared/managed-agents-overview.md` 了解完整阅读指南、beta 头部和陷阱。

**Beta 头部：** `managed-agents-2026-04-01`——SDK 自动为所有 `client.beta.{agents,environments,sessions,vaults,memory_stores,deployments,deployment_runs}.*` 调用设置此头部。Skills API 使用 `skills-2025-10-02`，Files API 使用 `files-api-2025-04-14`，但除了 `/v1/skills` 和 `/v1/files` 端点外，你不需要显式传入它们。

**子命令**——直接使用 `/claude-api <subcommand>` 调用：

| 子命令 | 操作 |
|---|---|
| `managed-agents-onboard` | 引导用户从头设置 Managed Agent。**立即读取 `shared/managed-agents-onboarding.md`** 并遵循其访谈脚本：**描述 → 配置 agent（提议，不要盘问）→ 环境 → 会话**（与控制台快速入门相同的流程，认证推迟到会话步骤）——默认值和内联建议承担工作，在任何代码发出之前有静默可行性关口（工作 vs 工具/凭据/数据）。不要总结——执行访谈。 |

**阅读指南：** 首先阅读 `shared/managed-agents-overview.md`，然后阅读主题性的 `shared/managed-agents-*.md` 文件（core、environments、tools、events、outcomes、multiagent、webhooks、memory、scheduled-deployments、client-patterns、onboarding、api-reference）。对于 Python、TypeScript、Go、Ruby、PHP 和 Java，阅读 `{lang}/managed-agents/README.md` 获取代码示例。对于 cURL，阅读 `curl/managed-agents.md`。**Agent 是持久化的——创建一次，通过 ID 引用。** 存储 `agents.create` 返回的 agent ID 并将其传递给每个后续的 `sessions.create`；不要在请求路径中调用 `agents.create`。Anthropic CLI（`ant`）是从版本控制的 YAML 创建 agent 和 environment 的一种便捷方式——参见 `shared/anthropic-cli.md`。如果你需要的绑定在语言 README 中没有展示，WebFetch `shared/live-sources.md` 中的相关条目而不是猜测。C# 通过 `client.Beta.Agents` 和相关命名空间支持 Beta Managed Agents。

**当用户想要从头设置 Managed Agent**（例如"我如何开始"、"引导我创建一个"、"设置一个新 agent"）：阅读 `shared/managed-agents-onboarding.md` 并运行其访谈——与 `managed-agents-onboard` 子命令相同。

**当用户询问"如何为 X 编写客户端代码"：** 使用 `shared/managed-agents-client-patterns.md`——涵盖无损流重连、`processed_at` 队列/已处理闸门、中断、`tool_confirmation` 往返、正确的空闲/已终止中断闸门、空闲后状态竞争、流优先排序、文件挂载陷阱、通过自定义工具保持凭据在宿主端等。

**当用户想要 agent 按计划运行**（cron、"每晚"、"周报"）：阅读 `shared/managed-agents-scheduled-deployments.md`——部署按 cron 节奏自主触发会话，具有每次触发的运行记录和生命周期控制（暂停/取消暂停/归档）。

---

## 服务器工具（快速参考）

服务器端工具运行在 Anthropic 的基础设施上——无需客户端执行循环。在 `tools` 中声明；结果作为内容块在同一个响应中到达。**无需 beta 头部**，除非另有说明。**优先使用你的模型支持的最新类型变体。** 下方的 `_20260209` Web 搜索 / Web 抓取变体（动态筛选）需要 Opus 4.8/4.7/4.6、Sonnet 5 或 Sonnet 4.6；旧模型的基本变体列在表后。

| 工具 | `type` | `name` | 关键可选参数 | 结果块类型 |
|---|---|---|---|---|
| Web 搜索 | `web_search_20260209` | `web_search` | `max_uses`、`allowed_domains`/`blocked_domains`、`user_location` | `web_search_tool_result` → `.content` 是 `web_search_result` 的列表 |
| Web 抓取 | `web_fetch_20260209` | `web_fetch` | `max_uses`、`allowed_domains`/`blocked_domains`、`citations`、`max_content_tokens` | `web_fetch_tool_result` → `.content` 是带有 `document` 块的 `web_fetch_result` |
| 代码执行 | `code_execution_20260521` | `code_execution` | none | `bash_code_execution_tool_result` → `.content.stdout` / `.stderr` / `.return_code` |
| 工具搜索（正则） | `tool_search_tool_regex_20251119` | `tool_search_tool_regex` | 将其他工具标记为 `defer_loading: true` | `tool_search_tool_result` |
| 工具搜索（BM25） | `tool_search_tool_bm25_20251119` | `tool_search_tool_bm25` | 将其他工具标记为 `defer_loading: true` | `tool_search_tool_result` |

`web_search_20260209` / `web_fetch_20260209` 内置动态筛选——代码执行在底层运行，因此**不要**在 `tools` 中单独声明 `code_execution`（第二个执行环境会混淆模型）。对于早于 Opus 4.6 / Sonnet 4.6 的模型，改为使用基本变体 `web_search_20250305` / `web_fetch_20250910`；在 Vertex AI 上仅有基本 `web_search_20250305` 可用。`code_execution_20260120`（REPL 持久化 + 程序化工具调用）在 Opus 4.5+ / Sonnet 4.5+ 上运行。**仅 Go SDK**：`code_execution_20260521` 存在于 `client.Beta.Messages.New` 下，使用 `Betas: []anthropic.AnthropicBeta{"code-execution-2025-08-25"}`（其他语言使用普通的 `client.messages.create`）；`code_execution_20260120` 在 Go 中像其他语言一样使用非 beta 的 `client.Messages.New`。Web 抓取仅抓取对话中已存在的 URL。提供商可用性因工具而异——参见 `shared/platform-availability.md`。参见 `shared/tool-use-concepts.md` 了解 `pause_turn` 处理。

## 文档与文件输入（快速参考）

**PDF（base64，无 beta）：** 用户内容中的 `{"type": "document", "source": {"type": "base64", "media_type": "application/pdf", "data": <b64 string>}}`，放在文本块之前。Base64 字符串必须无换行。限制：32 MB 请求，600 页（200k 上下文模型为 100 页）。Java：`ContentBlockParam.ofDocument(DocumentBlockParam... Base64PdfSource.builder().data(...))`。

**Files API（beta `files-api-2025-04-14`）：** 通过 `client.beta.files.upload(...)` 上传 → 响应的 `id` 是 `file_id`。将其引用为 `{"type": "document", "source": {"type": "file", "file_id": "..."}}` 用于 PDF/文本，或 `{"type": "image", ...}` 用于图片——内容块类型必须匹配文件的 MIME 类型。beta 头部在**上传和引用该文件的 `messages.create`** 上都需要。可用性：`shared/platform-availability.md`。

**引用（无 beta）：** 在每个 `document` 内容块上设置 `citations: {enabled: true}`（全部或全不）。响应拆分为多个 `text` 块；引用的块携带 `citations` 数组。每个引用有 `cited_text`、`document_index`、`document_title`，以及按 `type` 的位置：`char_location`（`start_char_index`/`end_char_index`）用于纯文本，`page_location`（`start_page_number`/`end_page_number`，1 索引）用于 PDF，`content_block_location` 用于自定义内容。与 `output_config.format` 不兼容。

## 工具使用模式（快速参考）

**严格工具使用（无 beta）：** 在工具定义上将 `strict: true` 设置为顶层字段（与 `name`/`description`/`input_schema` 同级），**而不是**在 `tool_choice` 上。Schema 必须有 `additionalProperties: false` + `required`。保证 `tool_use.input` 验证精确。Go：`Strict: anthropic.Bool(true)` + 通过 `InputSchema.ExtraFields` 设置 `additionalProperties`；Java：`.strict(true)` + `.putAdditionalProperty("additionalProperties", JsonValue.from(false))`。

**并行工具使用（默认开启）：** 一个 assistant 消息可包含多个 `tool_use` 块。并发执行它们，然后在**单个** user 消息中返回**所有** `tool_result` 块（不要拆分到多个消息）。对于失败的工具，返回带有 `is_error: true` 的 `tool_result`——不要丢弃它。

**Tool Runner（SDK beta 辅助）：** 通过 `client.beta.messages.*` 为你驱动工具调用循环。Python：`@beta_tool` 装饰器 + `client.beta.messages.tool_runner(...)` → `runner.until_done()`。TypeScript：来自 `@anthropic-ai/sdk/helpers/beta/zod` 的 `betaZodTool({...})` + `client.beta.messages.toolRunner(...)` → `await runner`。Go：`toolrunner.NewBetaToolFromJSONSchema(...)` + `client.Beta.Messages.NewToolRunner(...)` → `.RunToCompletion(ctx)`。Java 需要 `.addBeta("structured-outputs-2025-11-13")`。Ruby：`Anthropic::BaseTool` 子类 + `client.beta.messages.tool_runner(...)`。PHP：`BetaRunnableTool` + `->toolRunner(...)`。C#：原始 JSON schema 工具 + 通过 `client.Beta.Messages.ToolRunner(...)` 的 `BetaToolRunner`。

**程序化工具调用（无 beta 头部）：** Claude 从代码执行内部调用你的自定义工具。添加 `{"type": "code_execution_20260120", "name": "code_execution"}` **并**在你的自定义工具上设置 `"allowed_callers": ["code_execution_20260120"]`。Opus 4.5+ / Sonnet 4.5+（可用性：`shared/platform-availability.md`）。当响应挂起的程序化调用时，user 消息必须包含**仅** `tool_result` 块（无文本）。与 `strict: true`、`disable_parallel_tool_use`、强制 `tool_choice` 或 MCP 工具不兼容。

## 其他 API 接口（快速参考）

**消息批处理（无 beta；可用性：`shared/platform-availability.md`）：** `client.messages.batches.create(requests=[{custom_id, params}, ...])` → 轮询 `client.messages.batches.retrieve(id).processing_status` 直到 `"ended"` → 流式 `client.messages.batches.results(id)`。每个结果有 `.custom_id` + `.result.type`（`succeeded`/`errored`/`canceled`/`expired`）；成功后读取 `.result.message.content`。Python 将请求包装为 `Request(custom_id=..., params=MessageCreateParamsNonStreaming(...))`。结果以**任何顺序**到达——通过 `custom_id` 键控，绝不要按位置。

**Models API（无 beta；可用性：`shared/platform-availability.md`）：** `client.models.list()`（自动分页）和 `client.models.retrieve("claude-opus-4-8")`。每个模型对象有 `id`、`display_name`、`created_at`，以及自 2026 年 3 月以来——`max_input_tokens`（上下文窗口）、`max_tokens`（输出上限）和 `capabilities`。没有 `context_window` 字段。

**停止详情（GA，Opus 4.7+）：** `response.stop_details` 仅在 `stop_reason == "refusal"` 时填充（字段：`type: "refusal"`、`category: "cyber"|"bio"|null`、`explanation`）。对于其他每个 `stop_reason`（`end_turn`、`max_tokens`、`tool_use`、`pause_turn` 等）为 `null`——始终在读取前守卫。

**客户端配置（无 beta）：** `timeout` 默认 10 分钟；**单位因 SDK 而异**——Python/Ruby：秒；TypeScript：**毫秒**；Go `option.WithRequestTimeout(time.Duration)`；Java `Duration`；C# `TimeSpan`。TS 在非流式请求上对大的 `max_tokens` 将默认值扩展到 60 分钟；Java 对流式请求执行同样操作（Java 非流式在 30 秒-10 分钟之间缩放）。`max_retries`/`maxRetries` 默认 2（重试 408/409/429/5xx + 连接错误）。`base_url`（或 `ANTHROPIC_BASE_URL` 环境变量）。每请求覆盖：Python `client.with_options(timeout=5.0).messages.create(...)`；TS `client.messages.create({...}, {timeout: 5_000})`；Ruby `request_options: {timeout: 5}`。超时可重试——实际墙钟时间可达 `timeout × (max_retries+1)`。

## Workload Identity Federation（快速参考）

**GA，无 beta 头部。** 构建普通的零参数客户端（`Anthropic()` / `new Anthropic()` / `anthropic.NewClient()` / `AnthropicOkHttpClient.fromEnv()`）；SDK 在**所有**的 `ANTHROPIC_FEDERATION_RULE_ID`、`ANTHROPIC_ORGANIZATION_ID`、`ANTHROPIC_SERVICE_ACCOUNT_ID` 和 `ANTHROPIC_IDENTITY_TOKEN_FILE`（或 `ANTHROPIC_IDENTITY_TOKEN`）设置时自动检测 WIF，在 `/v1/oauth/token` 交换 JWT，并自动刷新。`ANTHROPIC_WORKSPACE_ID` 不决定激活——仅当联合规则跨越多个工作区时需要（否则 400 `workspace_id_required`），对于单工作区规则是可选的。`ANTHROPIC_API_KEY` 或 `ANTHROPIC_AUTH_TOKEN`（即使为空）优先级高于 WIF，而设置的 `ANTHROPIC_PROFILE` 也胜于联合环境变量（缺失的命名配置文件是错误，不是回退）——取消设置所有三个。

---

## 阅读指南

检测语言后，根据用户需求阅读相关文件。

**所有 SDK 语言使用相同的多文件布局**——目录 `{lang}/claude-api/` 包含 `README.md`（安装、客户端初始化、基本请求、思考、缓存、停止详情、杂项）、`tool-use.md`（工具定义、agent 循环、Anthropic 定义的的工具、结构化输出）、`streaming.md`、`batches.md`、`files-api.md`。并非每种语言都有每个文件（例如，Ruby 没有 `batches.md`）；如果某个文件缺失，该功能的示例尚未为该语言提供文档——回退到 cURL 形状或从 `shared/live-sources.md` WebFetch SDK 仓库。**cURL** → `curl/examples.md`。

下面的快速任务参考对所有语言使用 `{lang}/claude-api/FILE.md` 路径符号。

### 快速任务参考

**单文本分类/摘要/提取/问答：**
→ 仅阅读 `{lang}/claude-api/README.md`

**聊天 UI 或实时响应显示：**
→ 阅读 `{lang}/claude-api/README.md` + `{lang}/claude-api/streaming.md`

**长时间对话（可能超过上下文窗口）：**
→ 阅读 `{lang}/claude-api/README.md`——参见压缩部分
**迁移到较新模型（Fable 5 / Opus 4.8 / Opus 4.7 / Opus 4.6 / Sonnet 5 / Sonnet 4.6）或替换已退役模型：**
→ 阅读 `shared/model-migration.md`
**Fable 5 的提示或调整（长回合、effort、冗长度、自主运行、子 agent）：**
→ 阅读 `shared/model-migration.md` → 迁移到 Fable 5 → 行为转变（提示可调）+ 长时间运行 agent 建议
**提示缓存 / 优化缓存 / "为什么我的缓存命中率低"：**
→ 阅读 `shared/prompt-caching.md` + `{lang}/claude-api/README.md`（提示缓存部分）
**统计文件 / 提示 / diff 中的 Token（"X 有多少 token"）：**
→ 阅读 `shared/token-counting.md`——使用 `messages.count_tokens`，绝不用 `tiktoken`

**函数调用 / 工具使用 / agent：**
→ 阅读 `{lang}/claude-api/README.md` + `shared/tool-use-concepts.md` + `{lang}/claude-api/tool-use.md`

**Agent 设计（工具接口、上下文管理、缓存策略）：**
→ 阅读 `shared/agent-design.md`

**批处理（非延迟敏感）：**
→ 阅读 `{lang}/claude-api/README.md` + `{lang}/claude-api/batches.md`

**跨多个请求的文件上传：**
→ 阅读 `{lang}/claude-api/README.md` + `{lang}/claude-api/files-api.md`

**Managed Agents（服务器管理的带工作区的有状态 agent）：**
→ 阅读 `shared/managed-agents-overview.md` + 其他 `shared/managed-agents-*.md` 文件。对于 Python、TypeScript、Go、Ruby、PHP 和 Java，阅读 `{lang}/managed-agents/README.md` 获取代码示例。对于 cURL，阅读 `curl/managed-agents.md`。**Agent 是持久化的——创建一次，通过 ID 引用。** 存储 `agents.create` 返回的 agent ID 并将其传递给每个后续的 `sessions.create`；不要在请求路径中调用 `agents.create`。Anthropic CLI（`ant`）是从版本控制的 YAML 创建 agent 和 environment 的一种便捷方式——参见 `shared/anthropic-cli.md`。如果你需要的绑定在语言 README 中没有展示，WebFetch `shared/live-sources.md` 中的相关条目而不是猜测。C# 支持 Beta Managed Agents——参见 `csharp/claude-api/README.md` 了解详情，或 `curl/managed-agents.md` 获取原始 HTTP 参考。

### Claude API（完整文件参考）

阅读**语言特定的 Claude API 源**——每个 SDK 语言的 `{language}/claude-api/`，cURL 的 `curl/examples.md`：

1. **`{language}/claude-api/README.md`**——**首先阅读。** 安装、快速入门、常见模式、错误处理。
2. **`shared/tool-use-concepts.md`**——当用户需要函数调用、代码执行、内存或结构化输出时阅读。涵盖概念基础。
3. **`shared/agent-design.md`**——设计 agent 时阅读：bash vs. 专用工具、程序化工具调用、工具搜索/skills、上下文编辑 vs. 压缩 vs. 内存、缓存原则。
4. **`{language}/claude-api/tool-use.md`**——阅读了解语言特定的工具使用代码示例（tool runner、手动循环、代码执行、内存、结构化输出）。
5. **`{language}/claude-api/streaming.md`**——构建聊天 UI 或递增显示响应的界面时阅读。
6. **`{language}/claude-api/batches.md`**——脱机处理许多请求（非延迟敏感）时阅读。以 50% 成本异步运行。
7. **`{language}/claude-api/files-api.md`**——跨多个请求发送相同文件而无需重复上传时阅读。
8. **`shared/prompt-caching.md`**——添加或优化提示缓存时阅读。涵盖前缀稳定性设计、断点放置和静默失效缓存的防反模式。
9. **`shared/error-codes.md`**——调试 HTTP 错误或实现错误处理时阅读。包括每种 SDK 类型的异常类表和 Go `errors.As` 模式。
10. **`shared/model-migration.md`**——升级到较新模型、替换已退役模型或将 `budget_tokens` / prefill 模式转换为当前 API 时阅读。
11. **`shared/live-sources.md`**——用于获取最新官方文档的 WebFetch URL。

并非每种语言都有每个文件（例如，Ruby 没有 `batches.md`）；如果文件缺失，该功能的示例尚未为该语言提供文档。

> **注意：** 关于 Managed Agents 文件参考，参见上述 `## Managed Agents (Beta)` 部分——它列出了每个 `shared/managed-agents-*.md` 文件和语言特定的 README。

---

## 何时使用 WebFetch

在以下情况下使用 WebFetch 获取最新文档：

- 用户要求"最新"或"当前"信息
- 缓存数据似乎不正确
- 用户询问此处未涵盖的功能

实时文档 URL 在 `shared/live-sources.md` 中。

## 常见陷阱

- **没有 `ANTHROPIC_API_KEY` ≠ 没有凭据。** 不要因为环境变量未设置就放弃或向用户索要密钥——先运行 `ant auth status`。在 `ant auth login` 之后，裸 `Anthropic()` 客户端和 `ant …` 即使没有环境变量也能工作；对于原始 curl，使用 `Authorization: Bearer $(ant auth print-credentials --access-token)` 加上头部 `anthropic-beta: oauth-2025-04-20`。参见上述认证快速参考和 `shared/anthropic-cli.md`。
- 不要截断向 API 传递文件或内容时的输入。如果内容太长无法放入上下文窗口，通知用户并讨论选项（分块、摘要等），而不是静默截断。
- **Fable 5 / Sonnet 5 / Opus 4.8 / 4.7 思考：** 仅自适应。`thinking: {type: "enabled", budget_tokens: N}` 返回 400——`budget_tokens` 完全移除（连同 `temperature`、`top_p`、`top_k`）。使用 `thinking: {type: "adaptive"}`。Opus 4.8 继承 4.7 的此接口，无新的破坏性更改；Fable 5 增加一项——显式 `thinking: {type: "disabled"}` 返回 400（在 Sonnet 5 / 4.7 / 4.8 上接受）；改为省略该参数。
- **Opus 4.6 / Sonnet 4.6 思考：** 使用 `thinking: {type: "adaptive"}`——不要为新 4.6 代码使用 `budget_tokens`（在 Opus 4.6 和 Sonnet 4.6 上均已弃用；对于现有代码的逐步迁移，参见 `shared/model-migration.md` 中的过渡逃生口——注意此例外不适用于 Fable 5、Opus 4.7 或 4.8）。对于较旧模型，`budget_tokens` 必须小于 `max_tokens`（最小 1024）。如果设置错误将会抛出错误。
- **Prefill 已移除（Fable 5 和 4.6/4.7/4.8 家族）：** Assistant 消息 prefill（最后 assistant 轮次 prefill）在 Fable 5、Opus 4.6、Opus 4.7、Opus 4.8 和 Sonnet 4.6 上返回 400 错误。改用结构化输出（`output_config.format`）或系统提示指令来控制响应格式。（一个例外：回退信用 prefill 声明——当使用 `fallback_has_prefill_claim: true` 兑换信用时，服务器接受回传的 assistant 消息；参见迁移指南的拒绝部分。）
- **Fable 5 `refusal` 停止原因：** 安全分类器可能拒绝请求——成功的 HTTP 200 带有 `stop_reason: "refusal"`（预输出：空 `content`，不收费；中间流式：部分输出已计费——丢弃它）。在读取 `response.content[0]` 之前检查 `stop_reason`，否则在拒绝的请求上会遇到索引错误。要在另一个模型上重试，原样重放历史——其他模型从提示中丢弃已拒绝模型的思考块，不收费；无需剥离（而回退信用兑换无论如何必须原样回传拒绝体，思考块包含在内）。回退是**主动选择的**——新 `claude-fable-5` 代码应默认包含服务器端 `fallbacks` 参数，以便拒绝不会直接导致请求失败；参见上述 Claude Fable 5 部分。
- **Fable 5 分词器：** 与 Opus 4.8 相同的分词器——从 Opus 4.7/4.8 迁移时 Token 计数大致不变。从 Opus 4.6、Sonnet、Haiku 或更早版本迁移时，Token 计数不同（Opus 4.7 分词器使用约 1×–1.35× 的 Token）——通过在每个模型上调用一次 `count_tokens` 并比较 `input_tokens` 重新测量。
- **编辑前确认迁移范围：** 当用户要求将代码迁移到较新 Claude 模型而未命名特定文件、目录或文件列表时，**首先询问应用范围**——整个工作目录、特定子目录或一组特定文件。在用户确认之前不要开始编辑。命令式措辞如"迁移我的代码库"、"将我的项目迁移到 X"、"升级到 Sonnet 4.6"或裸"迁移到 Opus 4.8"**仍然模糊**——它们告诉你做什么但没说在哪里，所以要询问。仅当提示命名了确切文件、特定目录或显式文件列表时才无需询问继续（"迁移 `app.py`"、"迁移 `services/` 下的一切"、"更新 `a.py` 和 `b.py`"）。参见 `shared/model-migration.md` 第 0 步。
- **`max_tokens` 默认值：** 不要低估 `max_tokens`——达到上限会在思考中途截断输出，需要重试。对于非流式请求，默认设为 `~16000`（保持响应在 SDK HTTP 超时内）。对于流式请求，默认设为 `~64000`（超时不关心，因此给模型更多空间）。仅在有明确理由时才降低：分类（`~256`）、成本上限、故意短输出，或缓存预热的 **`max_tokens: 0`**（参见 `shared/prompt-caching.md` → 预热）。
- **128K 输出 Token：** Fable 5、Opus 4.6、Opus 4.7、Opus 4.8、Sonnet 5 和 Sonnet 4.6 支持高达 128K `max_tokens`，但 SDK 需要流式传输以避免 HTTP 超时。使用 `.stream()` 配合 `.get_final_message()` / `.finalMessage()`。
- **工具调用 JSON 解析（Fable 5 和 4.6/4.7/4.8 家族）：** Fable 5、Opus 4.6、Opus 4.7、Opus 4.8 和 Sonnet 4.6 可能在工具调用 `input` 字段中产生不同的 JSON 字符串转义（例如，Unicode 或正斜杠转义）。始终使用 `json.loads()` / `JSON.parse()` 解析工具输入——绝不要对序列化的输入进行原始字符串匹配。
- **结构化输出（所有模型）：** 使用 `output_config: {format: {...}}` 而不是已弃用的 `output_format` 参数在 `messages.create()` 上。这是一般的 API 更改，不是 4.6 特有。
- **不要重新实现 SDK 功能：** SDK 提供高级辅助函数——使用它们而不是从头构建。具体来说：使用 `stream.finalMessage()` 而不是将 `.on()` 事件包装在 `new Promise()` 中；使用类型化异常类（`Anthropic.RateLimitError` 等）而不是字符串匹配错误消息；使用 SDK 类型（`Anthropic.MessageParam`、`Anthropic.Tool`、`Anthropic.ToolUseBlock` / `Anthropic.ToolResultBlockParam`、`Anthropic.Message` 等）而不是重新定义等效接口。
- **错误处理——捕获链，不要一个宽泛类。** 单个 `except APIStatusError` / `catch (AnthropicServiceException)` / `rescue APIError` 丢失了可重试（429、≥500、网络）和不可重试（400/404）失败之间的区分。编写最具体优先的链——例如 `NotFoundError` → `RateLimitError` → `APIStatusError` → `APIConnectionError`（或 Go 等效：`errors.As` 到 `*anthropic.Error` 然后 `switch apierr.StatusCode { case 404: …; case 429: …; default: … }`）。每种语言的类名和命名空间在 `shared/error-codes.md` 中。
- **不要研究 SDK 类型——先写。** 如果此技能包含的文档中没有显示类型名，从语言特定文档中的命名空间/包表编写代码文件，让编译器的错误指给你正确的名称。不要花费轮次在 WebFetch、SDK 仓库克隆或编译运行单独的反射程序来在编写之前发现类型名——先生成源文件，然后修复编译器报告的内容。对已安装的 SDK 运行 `strings` / `jar tf` / `javap` 来定位名称是可以接受的（几秒内返回），但不要超过此范围。带错误类型名的文件是可恢复的；在发现上花费 session 却没有写出文件则不可恢复。
- **Bash 和文本编辑器工具是 Anthropic 定义的，无 schema。** 声明 `{"type": "bash_20250124", "name": "bash"}` / `{"type": "text_editor_20250728", "name": "str_replace_based_edit_tool"}`——无 `input_schema`。带有你自己 schema 命名为 `"bash"` 的自定义工具是不同的工具。处理路径和安全检查在 `shared/tool-use-concepts.md` § 客户端工具中。
- **Advisor 工具模型配对。** advisor 工具的 `model` 必须至少与请求的顶层 `model` 一样强大——例如执行者 `claude-sonnet-5` → advisor `claude-opus-4-8` 或 `claude-opus-4-7`。无效配对返回 400。配对表在 `shared/tool-use-concepts.md` § Advisor 中。可用性：`shared/platform-availability.md`。
- **Agent Skills ≠ Managed Agents。** 要通过 Agent Skills 让 Claude 生成 `.pptx`/`.xlsx`/等，调用 `client.beta.messages.create` 配合 `container={"skills": [...]}`、`code_execution_20260521` 工具和 `code-execution-2025-08-25` + `skills-2025-10-02` 两个 beta。不要在此使用 `client.beta.agents` / `sessions` / `environments`——那些是 Managed Agents 接口，不是 Agent Skills。
- **MCP 连接器需要两个部分。** 单独的 `mcp_servers=[{type:"url", url, name}]` 会作为验证错误被拒绝——还要添加 `tools=[{type:"mcp_toolset", mcp_server_name:<same name>}]` 配合 beta `mcp-client-2025-11-20`。可用性：`shared/platform-availability.md`。
- **上下文编辑 ≠ 压缩。** 上下文编辑*清除*工具结果和思考块；压缩*摘要*历史。对于上下文编辑，在 `client.beta.messages.*` 上使用 `context_management.edits` 配合类型 `clear_tool_uses_20250919`（或 `clear_thinking_20251015`），beta 为 `context-management-2025-06-27`——不是 `compact_20260112` 类型或 `compact-2026-01-12` beta，那是压缩。
- **`inference_geo` 是直接顶层请求参数**——`client.messages.create(..., inference_geo="us")` / `.inferenceGeo("us")`。不要将其放在 `extra_body` / `putAdditionalBodyProperty` 中。在 Opus 4.6 / Sonnet 4.6 及更高版本上支持；可用性：`shared/platform-availability.md`。`response.usage.inference_geo` 报告推理运行的位置。
- **细粒度工具流式传输不是 beta 功能。** 在工具定义上设置 `eager_input_streaming: true` 并调用常规 `client.messages.stream(...)`。没有 beta 头部和 `client.beta.*` 路径。
- **缓存诊断是 beta。** 使用 `client.beta.messages.*` 配合 beta `cache-diagnosis-2026-04-07`。在第一轮传入 `diagnostics: {previous_message_id: null}`，在后续轮次传入 `diagnostics: {previous_message_id: <previous response id>}`；结果在 `response.diagnostics` 上。可用性：`shared/platform-availability.md`。
- **Memory 工具类型是 `memory_20250818`。** 声明 `{"type": "memory_20250818", "name": "memory"}`。Go 在 `client.Beta.Messages.New` 上使用 beta 命名空间类型 `{OfMemoryTool20250818: &anthropic.BetaMemoryTool20250818Param{}}`；Python/TypeScript/Ruby/PHP/C# 使用非 beta 的 `client.messages.create`；Java 同时有非 beta `MemoryTool20250818` 和 beta tool-runner 路径。Python/TypeScript 提供 `BetaAbstractMemoryTool` / `betaMemoryTool` 辅助函数实现后端。
- **使用功能实际支持的模型。** 某些功能限制在特定模型层级——快速模式仅 Opus 4.8 / 4.7，任务预算仅 Fable 5 / Sonnet 5 / Opus 4.8 / 4.7，advisor 工具需要有效的执行者↔advisor 配对。如果用户提示命名了该功能不支持的模型，改用支持的模型并在输出中注明替换。
- **Bedrock / Foundry：使用平台客户端类。** 对于 Bedrock，使用 `…BedrockMantle…` 客户端（如 Python `AnthropicBedrockMantle`、Java `BedrockMantleBackend`）配合 `anthropic.` 前缀的模型 ID；不带 `Mantle` 的 `AnthropicBedrock`/`BedrockBackend` 是传统路径。对于 Foundry，在 SDK 支持的地方使用 `AnthropicFoundry` / `FoundryBackend` / `AnthropicFoundryClient`（C#、Java、PHP、Python、TypeScript）；Go 和 Ruby 没有 Foundry 客户端——Ruby 已记录的回退是带自定义 `base_url` 的第一方客户端。各语言表见上。
- **不要为 SDK 数据结构定义自定义类型：** SDK 为所有 API 对象导出类型。对消息使用 `Anthropic.MessageParam`，对工具定义使用 `Anthropic.Tool`，对工具结果使用 `Anthropic.ToolUseBlock` / `Anthropic.ToolResultBlockParam`，对响应使用 `Anthropic.Message`。定义你自己的 `interface ChatMessage { role: string; content: unknown }` 会重复 SDK 已提供的内容并丢失类型安全。
- **报告和文档输出：** 对于生成报告、文档或可视化的任务，代码执行沙箱预装了 `python-docx`、`python-pptx`、`matplotlib`、`pillow` 和 `pypdf`。Claude 可以生成格式化文件（DOCX、PDF、图表）并通过 Files API 返回——在"报告"或"文档"类型请求时考虑这一点，而不仅是纯 stdout 文本。
- **服务器工具错误不抛出。** Web 搜索和 Web 抓取错误返回 HTTP 200，其 `web_search_tool_result` / `web_fetch_tool_result` 块的 `content` 是单个错误对象（如 `{error_code: "max_uses_exceeded"}`）——不是抛出的异常。对于 Web 搜索，成功 `content` 是*列表*；错误 `content` 是*对象*——在索引之前根据此分支。
- **代码执行输出块类型：** `code_execution_20260521` 返回 `bash_code_execution_tool_result`（带有 `.content.stdout`），**不是**旧式的裸 `code_execution_tool_result`。迭代 `response.content` 并匹配正确的类型。
- **工具搜索：绝不要全部延迟。** 搜索工具本身不能有 `defer_loading: true`，且 `tools` 中必须至少有一个工具是非延迟的，否则 API 返回 400 `All tools have defer_loading set`。
- **`strict: true` 放在工具上，而非 `tool_choice`。** 将 `strict` 放在 `tool_choice` 上无效；它是工具定义上与 `name`/`description`/`input_schema` 同级的字段。
- **并行工具结果放在一个 user 消息中。** 将 `tool_result` 块拆分到多个 user 消息会静默地训练 Claude 停止进行并行调用。一个 assistant 消息的 `tool_use` 块 → 一个 user 消息的 `tool_result` 块。
- **引用 + 结构化输出不兼容。** 在文档上启用 `citations: {enabled: true}` 同时设置 `output_config.format` 返回 400。
- **批处理结果无序。** 通过 `custom_id` 匹配，绝不要按结果流中的位置匹配。
- **Vertex 模型 ID 无前缀。** 与 Bedrock 的 `anthropic.` 前缀 ID 不同，Vertex 对当前代模型使用裸第一方 ID（如 `"claude-opus-4-8"`）；日期快照模型使用 `@` 分隔符（如 `claude-haiku-4-5@20251001`）。
- **`stop_details` 除非 `stop_reason == "refusal"` 否则为 `null`。** 对于 `max_tokens`、`end_turn` 等，`stop_details` 为 `null`——读取 `.category` 前守卫。
- **WIF 认证：取消设置 `ANTHROPIC_API_KEY`、`ANTHROPIC_AUTH_TOKEN` 和 `ANTHROPIC_PROFILE`。** `ANTHROPIC_API_KEY` 和 `ANTHROPIC_AUTH_TOKEN`（即使设为 `""`）在 SDK 的优先级链中高于 Workload Identity Federation 并静默胜出；设置的 `ANTHROPIC_PROFILE` 也会胜出（缺失的命名配置文件是错误，不是回退）。`unset` 它们，不要置空。
