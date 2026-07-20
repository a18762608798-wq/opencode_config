# set_up

## reps

这东西类似一个skills市场，需要 `javascript` 环境.

### nvm

主要是为了安装 `Node.js 24 LTS`

nvm 全称是 Node Version Manager，也就是 Node.js 版本管理器。它本身不负责运行 JavaScript，而是负责安装、切换和管理多个 Node.js 版本。
Node.js 是运行 JavaScript 的程序。平时浏览器负责运行网页里的 JavaScript，而 Node.js 让你可以在终端、服务器、本地开发环境里运行 JavaScript

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.4/install.sh | bash
source ~/.bashrc

nvm install 24
nvm alias default 24
```

## skills-CIL

```bash
rm -rf ~/.npm/_npx
# npx skills add https://github.com/vercel-labs/skills --skill find-skills # 不指定具体设置.

# opencode 全局设置
npx skills add https://github.com/vercel-labs/skills \
  --skill find-skills \
  --agent opencode \
  --global \
  --copy.
# claude 全局设置
npx skills add https://github.com/vercel-labs/skills \
  --skill find-skills \
  --agent claude-code \
  --global \
  --copy \
  --yes
# codex 全局设置
npx skills add https://github.com/vercel-labs/skills \
  --skill find-skills \
  --agent codex \
  --global \
  --copy \
  --yes
```
