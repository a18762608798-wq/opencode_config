# OpenCode 全局配置

这是我的 [OpenCode](https://opencode.ai) 全局配置目录 (`~/.config/opencode`)。

## 使用

1. 将此目录放在 `~/.config/opencode`
2. 运行 `npm install` 安装插件依赖
3. 编辑 `opencode.jsonc` 配置模型和提供商

## Skills

> **说明**：OpenCode 会自动加载以下两个目录的 skills：
> - `~/.config/opencode/skills/` — 原生 skills（自写 / OpenCode 适配）
> - `~/.claude/skills/` — Claude Code 生态 skills（`npx skills add` 安装；路径硬编码为 `~/.claude/skills/`，放在此处无需修改即可正常工作）

### 学术写作（位于 `~/.claude/skills/`）

通过 `npx skills add` 安装，SKILL.md 命令路径写死为 `~/.claude/skills/`，OpenCode 兼容加载。

| Skill | 用途 | 来源 |
|-------|------|------|
| latex-thesis-zh | 中文 LaTeX 学位论文（硕博） | [bahayonghang/academic-writing-skills](https://github.com/bahayonghang/academic-writing-skills) |
| latex-paper-en | 英文 LaTeX 期刊/会议论文 | [bahayonghang/academic-writing-skills](https://github.com/bahayonghang/academic-writing-skills) |
| typst-paper | Typst 格式论文（中/英） | [bahayonghang/academic-writing-skills](https://github.com/bahayonghang/academic-writing-skills) |
| paper-audit | 论文审稿与自查 | [bahayonghang/academic-writing-skills](https://github.com/bahayonghang/academic-writing-skills) |
| bib-search-citation | BibTeX 文献检索与引用 | [bahayonghang/academic-writing-skills](https://github.com/bahayonghang/academic-writing-skills) |
| cover-letter | 投稿信（cover letter） | [bahayonghang/academic-writing-skills](https://github.com/bahayonghang/academic-writing-skills) |
| humanize-academic-writing | 学术文本去 AI 化 | [momo2young/humanize-academic-writing](https://github.com/momo2young/humanize-academic-writing) |

### 开发辅助（位于 `~/.config/opencode/skills/`）

| Skill | 用途 | 来源 |
|-------|------|------|
| [find-skills](skills/find-skills/SKILL.md) | 发现和安装 skills | [vercel-labs/skills](https://github.com/vercel-labs/skills) |
| [skill-creator](skills/skill-creator/SKILL.md) | 创建和优化 skills | [anthropics/skills](https://github.com/anthropics/skills) |
| [git-workflow](skills/git-workflow/SKILL.md) | 规范化 Git 工作流程 | 自写 |

### 知识管理（位于 `~/.config/opencode/skills/`）

| Skill | 用途 | 来源 |
|-------|------|------|
| [knowledge-organizer](skills/knowledge-organizer/SKILL.md) | 对话知识点归档到 Obsidian | 自写 |

## 参考

- [docs/index.md](docs/index.md) — 入门教程
- [docs/04-reference/02-configuration-file.md](docs/04-reference/02-configuration-file.md) — 完整配置参考
- [examples/01-basic-agents.md](examples/01-basic-agents.md) — Agent 配置示例


