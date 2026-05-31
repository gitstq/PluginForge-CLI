<!-- Language Switcher -->
<p align="center">
  <a href="#english">English</a> •
  <a href="#简体中文">简体中文</a> •
  <a href="#繁體中文">繁體中文</a>
</p>

---

<a name="english"></a>
# 🦞 PluginForge-CLI

<div align="center">

**Lightweight Terminal AI IDE Plugin Intelligent Management & Publishing Engine**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

</div>

---

## 🎉 Project Introduction

**PluginForge-CLI** is a **zero-dependency-core** terminal tool for managing AI IDE plugins. It provides a complete workflow for creating, validating, building, and publishing plugins for popular AI-powered development environments like Claude Code, Cursor, Codex, and more.

### 💡 Why PluginForge-CLI?

- **🔥 Hot Topic**: AI IDEs are rapidly evolving - Claude Code, Cursor, and similar tools are transforming how developers work
- **⚡ Zero Core Dependencies**: Minimal footprint, fast execution
- **🛡️ Security First**: Built-in security scanning for dangerous code patterns
- **📊 TUI Dashboard**: Beautiful terminal interface with Rich library
- **🔧 Multi-Platform Support**: Works with Claude Code, Cursor, Codex, Copilot, and generic plugins

---

## ✨ Core Features

| Feature | Description |
|---------|-------------|
| 🆕 **Plugin Creation** | Create plugins from templates with one command |
| ✅ **Validation** | Validate structure, manifest, and security |
| 📦 **Building** | Package plugins into distributable archives |
| 📤 **Export** | Export to ZIP/TAR formats |
| 📋 **Management** | List, info, config, and delete plugins |
| 📊 **Dashboard** | Interactive TUI dashboard |
| 🔒 **Security Scan** | Detect dangerous code patterns |
| 🎨 **Templates** | Built-in templates for Claude Code, Cursor, etc. |

---

## 🚀 Quick Start

### Requirements

- Python 3.8+
- pip

### Installation

```bash
# Install from PyPI (coming soon)
pip install pluginforge-cli

# Or install from source
git clone https://github.com/gitstq/PluginForge-CLI.git
cd PluginForge-CLI
pip install -e .
```

### Basic Usage

```bash
# Show help
pluginforge --help

# Create a new plugin
pluginforge create my-plugin --type claude-code --description "My awesome plugin"

# List all plugins
pluginforge list

# Validate a plugin
pluginforge validate my-plugin --security

# Build plugin package
pluginforge build my-plugin

# Launch dashboard
pluginforge dashboard
```

---

## 📖 Detailed Usage Guide

### Creating Plugins

```bash
# Create a Claude Code plugin
pluginforge create my-claude-plugin --type claude-code

# Create a Cursor plugin
pluginforge create my-cursor-plugin --type cursor

# Create with custom template
pluginforge create my-plugin --template claude-code
```

### Plugin Types

| Type | Description |
|------|-------------|
| `claude-code` | Claude Code IDE plugin with hooks support |
| `cursor` | Cursor IDE plugin |
| `codex` | OpenAI Codex plugin |
| `copilot` | GitHub Copilot plugin |
| `generic` | Generic plugin template |

### Validation

```bash
# Basic validation
pluginforge validate my-plugin

# With security scan
pluginforge validate my-plugin --security
```

### Building & Exporting

```bash
# Build to dist/
pluginforge build my-plugin

# Export to specific format
pluginforge export my-plugin --format tar

# Export to specific directory
pluginforge build my-plugin --output ./releases
```

---

## 💡 Design Philosophy

### Why Zero Core Dependencies?

PluginForge-CLI is designed to be **lightweight and portable**. The core functionality works with only Python standard library. Optional features use minimal, well-maintained packages.

### Architecture

```
pluginforge/
├── core.py          # Core plugin management logic
├── cli.py           # Click-based CLI interface
└── templates/       # Built-in plugin templates
```

### Future Roadmap

- [ ] Plugin marketplace integration
- [ ] Auto-update mechanism
- [ ] Plugin dependency resolution
- [ ] Test runner integration
- [ ] CI/CD templates

---

## 📦 Packaging & Deployment

### Build Package

```bash
# Install build tools
pip install build

# Build distribution
python -m build
```

### Publish to PyPI

```bash
pip install twine
twine upload dist/*
```

---

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'feat: add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Commit Convention

We follow [Angular Commit Convention](https://gist.github.com/stephenparish/9941e89d80e2bc58a153):

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `refactor:` Code refactoring
- `test:` Tests
- `chore:` Maintenance

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

<p align="center">
  Made with ❤️ by PluginForge Team
</p>

---

<a name="简体中文"></a>
# 🦞 PluginForge-CLI

<div align="center">

**轻量级终端AI IDE插件智能管理与发布引擎**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

</div>

---

## 🎉 项目介绍

**PluginForge-CLI** 是一款**零依赖核心**的终端工具，用于管理AI IDE插件。它提供了完整的插件创建、验证、构建和发布工作流，支持Claude Code、Cursor、Codex等热门AI开发环境。

### 💡 为什么选择 PluginForge-CLI？

- **🔥 热门领域**：AI IDE正在快速发展 - Claude Code、Cursor等工具正在改变开发者的工作方式
- **⚡ 零核心依赖**：最小化占用，快速执行
- **🛡️ 安全优先**：内置危险代码模式安全扫描
- **📊 TUI仪表盘**：使用Rich库构建的精美终端界面
- **🔧 多平台支持**：支持Claude Code、Cursor、Codex、Copilot和通用插件

---

## ✨ 核心特性

| 特性 | 描述 |
|------|------|
| 🆕 **插件创建** | 一键从模板创建插件 |
| ✅ **验证检测** | 验证结构、清单和安全问题 |
| 📦 **构建打包** | 打包为可分发的压缩包 |
| 📤 **导出功能** | 导出为ZIP/TAR格式 |
| 📋 **插件管理** | 列表、详情、配置、删除插件 |
| 📊 **仪表盘** | 交互式TUI仪表盘 |
| 🔒 **安全扫描** | 检测危险代码模式 |
| 🎨 **模板系统** | 内置Claude Code、Cursor等模板 |

---

## 🚀 快速开始

### 环境要求

- Python 3.8+
- pip

### 安装方式

```bash
# 从PyPI安装（即将发布）
pip install pluginforge-cli

# 或从源码安装
git clone https://github.com/gitstq/PluginForge-CLI.git
cd PluginForge-CLI
pip install -e .
```

### 基本使用

```bash
# 显示帮助
pluginforge --help

# 创建新插件
pluginforge create my-plugin --type claude-code --description "我的插件"

# 列出所有插件
pluginforge list

# 验证插件
pluginforge validate my-plugin --security

# 构建插件包
pluginforge build my-plugin

# 启动仪表盘
pluginforge dashboard
```

---

## 📖 详细使用指南

### 创建插件

```bash
# 创建Claude Code插件
pluginforge create my-claude-plugin --type claude-code

# 创建Cursor插件
pluginforge create my-cursor-plugin --type cursor

# 使用自定义模板创建
pluginforge create my-plugin --template claude-code
```

### 插件类型

| 类型 | 描述 |
|------|------|
| `claude-code` | Claude Code IDE插件，支持钩子 |
| `cursor` | Cursor IDE插件 |
| `codex` | OpenAI Codex插件 |
| `copilot` | GitHub Copilot插件 |
| `generic` | 通用插件模板 |

### 验证检测

```bash
# 基础验证
pluginforge validate my-plugin

# 包含安全扫描
pluginforge validate my-plugin --security
```

### 构建与导出

```bash
# 构建到dist/目录
pluginforge build my-plugin

# 导出为指定格式
pluginforge export my-plugin --format tar

# 导出到指定目录
pluginforge build my-plugin --output ./releases
```

---

## 💡 设计思路

### 为什么采用零核心依赖？

PluginForge-CLI 设计为**轻量且可移植**。核心功能仅依赖Python标准库即可运行。可选功能使用最小化、维护良好的第三方包。

### 架构设计

```
pluginforge/
├── core.py          # 核心插件管理逻辑
├── cli.py           # Click命令行界面
└── templates/       # 内置插件模板
```

### 后续规划

- [ ] 插件市场集成
- [ ] 自动更新机制
- [ ] 插件依赖解析
- [ ] 测试运行器集成
- [ ] CI/CD模板

---

## 📦 打包与部署

### 构建包

```bash
# 安装构建工具
pip install build

# 构建分发包
python -m build
```

### 发布到PyPI

```bash
pip install twine
twine upload dist/*
```

---

## 🤝 贡献指南

欢迎贡献代码！请遵循以下步骤：

1. Fork本仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'feat: 添加新功能'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建Pull Request

### 提交规范

我们遵循 [Angular提交规范](https://gist.github.com/stephenparish/9941e89d80e2bc58a153)：

- `feat:` 新功能
- `fix:` 修复问题
- `docs:` 文档更新
- `refactor:` 代码重构
- `test:` 测试相关
- `chore:` 维护工作

---

## 📄 开源协议

本项目采用 **MIT协议** 开源 - 详见 [LICENSE](LICENSE) 文件。

---

<p align="center">
  由 PluginForge Team 用 ❤️ 打造
</p>

---

<a name="繁體中文"></a>
# 🦞 PluginForge-CLI

<div align="center">

**輕量級終端AI IDE插件智能管理與發布引擎**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

</div>

---

## 🎉 專案介紹

**PluginForge-CLI** 是一款**零依賴核心**的終端工具，用於管理AI IDE插件。它提供了完整的插件創建、驗證、構建和發布工作流程，支援Claude Code、Cursor、Codex等熱門AI開發環境。

### 💡 為什麼選擇 PluginForge-CLI？

- **🔥 熱門領域**：AI IDE正在快速發展 - Claude Code、Cursor等工具正在改變開發者的工作方式
- **⚡ 零核心依賴**：最小化佔用，快速執行
- **🛡️ 安全優先**：內建危險程式碼模式安全掃描
- **📊 TUI儀表板**：使用Rich庫構建的精美終端界面
- **🔧 多平台支援**：支援Claude Code、Cursor、Codex、Copilot和通用插件

---

## ✨ 核心特性

| 特性 | 描述 |
|------|------|
| 🆕 **插件創建** | 一鍵從模板創建插件 |
| ✅ **驗證檢測** | 驗證結構、清單和安全問題 |
| 📦 **構建打包** | 打包為可分發的壓縮包 |
| 📤 **導出功能** | 導出為ZIP/TAR格式 |
| 📋 **插件管理** | 列表、詳情、配置、刪除插件 |
| 📊 **儀表板** | 互動式TUI儀表板 |
| 🔒 **安全掃描** | 檢測危險程式碼模式 |
| 🎨 **模板系統** | 內建Claude Code、Cursor等模板 |

---

## 🚀 快速開始

### 環境要求

- Python 3.8+
- pip

### 安裝方式

```bash
# 從PyPI安裝（即將發布）
pip install pluginforge-cli

# 或從原始碼安裝
git clone https://github.com/gitstq/PluginForge-CLI.git
cd PluginForge-CLI
pip install -e .
```

### 基本使用

```bash
# 顯示幫助
pluginforge --help

# 創建新插件
pluginforge create my-plugin --type claude-code --description "我的插件"

# 列出所有插件
pluginforge list

# 驗證插件
pluginforge validate my-plugin --security

# 構建插件包
pluginforge build my-plugin

# 啟動儀表板
pluginforge dashboard
```

---

## 📖 詳細使用指南

### 創建插件

```bash
# 創建Claude Code插件
pluginforge create my-claude-plugin --type claude-code

# 創建Cursor插件
pluginforge create my-cursor-plugin --type cursor

# 使用自定義模板創建
pluginforge create my-plugin --template claude-code
```

### 插件類型

| 類型 | 描述 |
|------|------|
| `claude-code` | Claude Code IDE插件，支援鉤子 |
| `cursor` | Cursor IDE插件 |
| `codex` | OpenAI Codex插件 |
| `copilot` | GitHub Copilot插件 |
| `generic` | 通用插件模板 |

### 驗證檢測

```bash
# 基礎驗證
pluginforge validate my-plugin

# 包含安全掃描
pluginforge validate my-plugin --security
```

### 構建與導出

```bash
# 構建到dist/目錄
pluginforge build my-plugin

# 導出為指定格式
pluginforge export my-plugin --format tar

# 導出到指定目錄
pluginforge build my-plugin --output ./releases
```

---

## 💡 設計思路

### 為什麼採用零核心依賴？

PluginForge-CLI 設計為**輕量且可移植**。核心功能僅依賴Python標準庫即可運行。可選功能使用最小化、維護良好的第三方套件。

### 架構設計

```
pluginforge/
├── core.py          # 核心插件管理邏輯
├── cli.py           # Click命令列界面
└── templates/       # 內建插件模板
```

### 後續規劃

- [ ] 插件市集整合
- [ ] 自動更新機制
- [ ] 插件依賴解析
- [ ] 測試執行器整合
- [ ] CI/CD模板

---

## 📦 打包與部署

### 構建套件

```bash
# 安裝構建工具
pip install build

# 構建分發套件
python -m build
```

### 發布到PyPI

```bash
pip install twine
twine upload dist/*
```

---

## 🤝 貢獻指南

歡迎貢獻程式碼！請遵循以下步驟：

1. Fork本倉庫
2. 創建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交變更 (`git commit -m 'feat: 添加新功能'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 創建Pull Request

### 提交規範

我們遵循 [Angular提交規範](https://gist.github.com/stephenparish/9941e89d80e2bc58a153)：

- `feat:` 新功能
- `fix:` 修復問題
- `docs:` 文檔更新
- `refactor:` 程式碼重構
- `test:` 測試相關
- `chore:` 維護工作

---

## 📄 開源協議

本專案採用 **MIT協議** 開源 - 詳見 [LICENSE](LICENSE) 文件。

---

<p align="center">
  由 PluginForge Team 用 ❤️ 打造
</p>
