# 🔬 RayScanX 2.3.0

> 📜 **项目说明**：RayScanX 是基于 [RayScan](https://github.com/xiabai2008/rayscan) 项目的二次开发版本。
> 在此向原作者 [xiabai2008](https://github.com/xiabai2008) 致敬，感谢其在 Web 漏洞扫描领域的杰出贡献。
> 原项目从 WVS 19 个大版本的迭代成长为一个功能强大的扫描器，RayScanX 在此基础上继续进化。

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)
![License](https://img.shields.io/badge/License-MIT-green)
![Version](https://img.shields.io/badge/Version-2.3.0-blue)
![Status](https://img.shields.io/badge/Status-Beta-yellow)

**🎯 中文 OA / 国产中间件专项 Web 漏洞检测器 | 三级检测链路 · 规则级证据 · 低误报**

</div>

## 📖 简介

RayScanX 是一款开箱即用的 Web 漏洞扫描器，专注于中文 OA 系统和国产中间件的专项漏洞检测。支持 CLI 和 Web UI 双模式，一条命令即可输出可复核的扫描报告。

## 🚀 快速开始

### 安装

```bash
git clone https://github.com/xiabai2008/rayscanx
cd RayScanX
pip install -e ".[dev]"
```

### 使用

```bash
# CLI 扫描
python -m wvs scan https://target.com --insecure --rate 10

# Web UI（推荐）
python web_ui/app.py
# 浏览器访问 http://localhost:5000
```

## 🎯 核心功能

| 模块 | 检测能力 |
|------|----------|
| **SQL 注入** | error/union/boolean-blind/time-based/stacked/二阶/宽字节/OOB |
| **XSS** | reflected/stored/Polyglot/mXSS/SSTI |
| **OA 专项** | 泛微/通达/金蝶/蓝凌/致远/用友/禅道/万户/Nacos/Spring/Jenkins/Confluence |
| **通用漏洞** | CMDi / LFI / RCE / SSRF / XXE / WebShell / 弱口令 / 子域名 |

## 📚 文档

- [快速上手指南](docs/getting-started.md) — 详细安装和使用说明
- [检测模块说明](docs/modules.md) — 所有检测模块的功能介绍
- [OA 检测规则](docs/OA_RULES.md) — OA 专项检测规则说明
- [架构设计](docs/architecture.md) — 系统架构和技术栈
- [版本历史](docs/CHANGELOG.md) — 详细的版本更新记录
- [项目演进规划](docs/rayscan_evolution_roadmap.md) — 未来发展方向

## ⚠️ 免责声明

本工具**仅供**获得明确授权的安全测试、渗透测试及漏洞研究使用。
**未经授权扫描、攻击他人系统属于违法行为，使用者需自行承担一切法律责任。**

## 📄 License

MIT License — Copyright (c) 2026 xiabai2008