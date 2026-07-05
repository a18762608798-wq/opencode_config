# 常见问题

## 安装相关

### Q: 安装脚本报错 "permission denied"

```bash
# 使用 sudo 运行
sudo bash -c "$(curl -fsSL https://opencode.ai/install.sh)"

# 或手动安装
curl -L https://github.com/sst/opencode/releases/latest/download/opencode-linux-amd64 -o opencode
chmod +x opencode
sudo mv opencode /usr/local/bin/
```

### Q: 安装成功但运行 `opencode` 提示 command not found

```bash
# 检查 PATH
echo $PATH

# 如果 /usr/local/bin 不在 PATH 中，添加到 shell 配置文件
echo 'export PATH="/usr/local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### Q: Windows 怎么安装？

推荐通过 WSL2 安装：

```powershell
# 安装 WSL2
wsl --install

# 进入 WSL 后按 Linux 方式安装
```

也可以在 Docker 中运行：

```powershell
docker run -it --rm -v ${PWD}:/workspace ghcr.io/sst/opencode:latest
```

---

## 配置相关

### Q: 如何使用本地模型（Ollama）？

```bash
# 1. 安装并启动 Ollama
ollama serve

# 2. 拉取模型
ollama pull qwen2.5-coder:7b

# 3. 在 OpenCode TUI 中
/connect
# 选择 ollama
```

### Q: 如何切换模型？

在 TUI 中：
- 按 `Ctrl+T` 快速切换
- 或使用 `/model` 命令

命令行指定：
```bash
opencode --model openai/gpt-4o
```

### Q: API Key 保存在哪里？

```
~/.config/opencode/credentials/
```

建议使用环境变量而非直接写入文件，更安全：

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

### Q: 如何配置多个提供商？

在 TUI 中多次使用 `/connect` 命令即可添加多个提供商，使用时用 `/model` 切换。

---

## 使用相关

### Q: AI 修改了我不想要的代码，怎么撤销？

```
/undo
```

会撤销上一次 AI 的操作。多次 `/undo` 可撤销更多操作。

也可以用 `/redo` 重做被撤销的操作。

### Q: 如何让 AI 只读不写？

切换到 Plan 模式（按 `Tab` 键）。Plan 模式下 AI 不会修改任何文件。

### Q: 对话历史太长，怎么清理？

```
/clear
```

这会清空当前对话，但不会影响已修改的文件。

### Q: 如何导出对话记录？

```
/export to-file.md
```

支持格式：
- `markdown` — Markdown 格式
- `json` — JSON 格式

### Q: 如何查看 API 调用花费？

```
/cost
```

显示当前会话的 token 使用量和预估费用。

---

## 项目配置

### Q: AGENTS.md 应该写什么？

写「AI 需要知道的关于项目的一切」：

- 项目是做什么的
- 技术栈和版本
- 代码规范和约定
- 架构约束和设计决策
- 当前开发状态

越具体越好。参考 [上下文工程](../03-advanced/04-context-engineering.md)。

### Q: 如何在团队中共享 OpenCode 配置？

将 `.opencode/` 目录提交到 Git：

```bash
git add .opencode/
git commit -m "feat: 添加 OpenCode 项目配置"
```

团队成员 clone 项目后即可使用相同的 Agent、Skills 和 MCP 配置。

---

## 模型相关

### Q: 支持哪些模型？

OpenCode 支持几乎所有主流模型：

| 提供商 | 支持模型 |
|--------|---------|
| Anthropic | Claude 全系列 |
| OpenAI | GPT-4o, GPT-5 全系列 |
| Google | Gemini 全系列 |
| DeepSeek | V3, R1 |
| 本地 | Ollama 运行的任意模型 |
| OpenRouter | 200+ 模型 |

### Q: 哪个模型最好？

取决于场景：

| 场景 | 推荐模型 |
|------|---------|
| 日常编码 | Claude Sonnet 4 |
| 复杂架构 | Claude Opus / GPT-5.4 |
| 轻量任务 | Claude Haiku / GPT-4o-mini |
| 中文场景 | DeepSeek-V3 / Qwen |
| 省钱 | DeepSeek-V3 |
| 隐私敏感 | 本地 Ollama 模型 |

### Q: 如何控制花费？

1. Plan 阶段使用便宜模型（Haiku），Build 阶段用强模型（Sonnet）
2. 使用本地模型处理非关键任务
3. 定期 `/cost` 查看花费
4. 在提供商控制台设置每月花费上限

---

## 故障排除

### Q: 提示 "API key not found"

检查：
1. 是否已配置提供商：`/connect`
2. 环境变量是否正确设置
3. API Key 是否过期

### Q: 连接超时

```bash
# 检查网络
curl -I https://api.anthropic.com

# 如需要代理
export HTTPS_PROXY=http://your-proxy:port
```

### Q: 响应很慢

1. 检查是否使用了太大的模型
2. 对话历史是否过长（`/clear` 清理）
3. 网络延迟
4. 考虑切换到更快的模型

### Q: AI 反复修改同一个文件不停止

按 `Ctrl+C` 中断，然后给更明确的指令：

```
不要反复修改，先给出修改计划让我确认
```

---

## 安全相关

### Q: OpenCode 会上传我的代码吗？

**不会**。OpenCode 是本地工具，代码只发送给你选择的 LLM 提供商（如 OpenAI、Anthropic）。

如果你担心代码隐私：
- 使用本地模型（Ollama）
- 或使用企业版的私有部署方案

### Q: 如何防止 AI 执行危险命令？

1. 在配置中设置命令黑名单：

```json
{
  "tools": {
    "shell": {
      "blacklist": ["rm -rf /", "sudo", "mkfs", "dd"]
    }
  }
}
```

2. 关闭 `auto_approve`，每次操作需手动确认
3. Plan 模式下测试后再 Build

### Q: 如何保护我的 API Key？

- 使用环境变量，不要硬编码在代码中
- 不要在对话中粘贴 API Key（会被记录在会话历史中）
- 定期轮换密钥
- 使用 `.gitignore` 排除 `.env` 文件
