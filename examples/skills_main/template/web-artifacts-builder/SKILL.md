---
name: web-artifacts-builder
description: 使用现代前端 Web 技术（React、Tailwind CSS、shadcn/ui）创建复杂的多组件 claude.ai HTML 制品的工具集。用于需要状态管理、路由或 shadcn/ui 组件的复杂制品——不用于简单的单文件 HTML/JSX 制品。
license: Complete terms in LICENSE.txt
---

# Web 制品构建器

构建强大的前端 claude.ai 制品，按以下步骤操作：
1. 使用 `scripts/init-artifact.sh` 初始化前端仓库
2. 通过编辑生成的代码来开发制品
3. 使用 `scripts/bundle-artifact.sh` 将所有代码打包成单个 HTML 文件
4. 向用户展示制品
5. （可选）测试制品

**技术栈**：React 18 + TypeScript + Vite + Parcel（打包）+ Tailwind CSS + shadcn/ui

## 设计与风格指南

非常重要：为避免常被称为"AI 套路"的问题，避免使用过度居中的布局、紫色渐变、统一圆角和 Inter 字体。

## 快速开始

### 第 1 步：初始化项目

运行初始化脚本创建新的 React 项目：
```bash
bash scripts/init-artifact.sh <project-name>
cd <project-name>
```

这会创建一个完全配置好的项目，包含：
- ✅ React + TypeScript（通过 Vite）
- ✅ Tailwind CSS 3.4.1 及 shadcn/ui 主题系统
- ✅ 路径别名（`@/`）已配置
- ✅ 40+ shadcn/ui 组件预装
- ✅ 所有 Radix UI 依赖已包含
- ✅ Parcel 已配置用于打包（通过 .parcelrc）
- ✅ Node 18+ 兼容性（自动检测并固定 Vite 版本）

### 第 2 步：开发制品

编辑生成的文件来构建制品。参见下方**常见开发任务**获取指导。

### 第 3 步：打包为单个 HTML 文件

将 React 应用打包为单个 HTML 制品：
```bash
bash scripts/bundle-artifact.sh
```

这会创建 `bundle.html`——一个自包含的制品，所有 JavaScript、CSS 和依赖都已内联。此文件可直接在 OpenCode 对话中作为制品分享。

**要求**：项目根目录必须有 `index.html`。

**脚本功能**：
- 安装打包依赖（parcel、@parcel/config-default、parcel-resolver-tspaths、html-inline）
- 创建带路径别名支持的 `.parcelrc` 配置
- 使用 Parcel 构建（无 source maps）
- 使用 html-inline 将所有资源内联到单个 HTML 中

### 第 4 步：与用户分享制品

最后，在对话中与用户分享打包好的 HTML 文件，以便他们将其作为制品查看。

### 第 5 步：测试/可视化制品（可选）

注意：这完全是可选步骤。仅在必要时或被要求时才执行。

使用可用工具（包括其他技能或内置工具如 Playwright 或 Puppeteer）测试/可视化制品。通常，避免一开始就测试制品，因为这会增加从请求到看到成品之间的延迟。后续如果有请求或出现问题时再测试。

## 参考

- **shadcn/ui 组件**：https://ui.shadcn.com/docs/components
