# 安装指南

## 支持平台

OpenCode 支持以下平台：

| 平台 | 安装方式 |
|------|---------|
| macOS | Homebrew / 脚本安装 |
| Linux | 脚本安装 / 二进制下载 |
| Windows | WSL2 / Docker |
| Docker | 容器化运行 |

## 脚本安装

```bash
curl -fsSL https://opencode.ai/install.sh | bash
```

然后激活变量：

```bash
source ~/.bashrc
```

## 验证安装

安装完成后，验证是否成功：

```bash
opencode --version
```

## 查看帮助

```bash
# 查看所有命令
opencode --help

# 查看子命令帮助
opencode agent --help
opencode session --help
opencode run --help
```

## 升级

```bash
# 使用安装脚本升级
curl -fsSL https://opencode.ai/install.sh | bash
```

## 卸载

```bash
# 删除二进制文件
sudo rm /usr/local/bin/opencode

# 删除配置目录（可选）
rm -rf ~/.config/opencode
```

## 下一步

安装完成后，接下来 👉 [配置 OpenCode](03-configuration.md)
