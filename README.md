# 🔬 RayScanX 2.3.0

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)
![License](https://img.shields.io/badge/License-MIT-green)
![Version](https://img.shields.io/badge/Version-2.3.0-blue)
![Status](https://img.shields.io/badge/Status-Beta-yellow)

**🎯 中文 OA / 国产中间件专项 Web 漏洞检测器 | 三级检测链路 · 规则级证据 · 低误报**

[快速开始](#-快速开始) • [功能特性](#-核心特性) • [文档导航](#-文档导航) • [免责声明](#-免责声明)

</div>

---

## 📜 项目说明

> RayScanX 是基于 [RayScan](https://github.com/xiabai2008/rayscan) 项目的二次开发版本。
> 在此向原作者 [xiabai2008](https://github.com/xiabai2008) 致敬，感谢其在 Web 漏洞扫描领域的杰出贡献。
> 原项目从 WVS 19 个大版本的迭代成长为一个功能强大的扫描器，RayScanX 在此基础上继续进化。

---

## 📋 项目简介

RayScanX 是一款开箱即用的 Web 漏洞扫描器，专注于中文 OA 系统和国产中间件的专项漏洞检测。支持 CLI 和 Web UI 双模式，一条命令即可输出可复核的扫描报告。

### ✨ 核心特性

- 🎯 **OA 专项检测**：泛微/通达/金蝶/蓝凌/致远/用友/禅道/万户/Nacos/Spring/Jenkins/Confluence
- 🔍 **三级检测链路**：内容指纹识别 → 版本识别 → 规则级响应证据验证
- 📊 **低误报设计**：基于响应证据判定，仅路径可达不再视为漏洞
- 🧩 **18 个检测模块**：SQL 注入/XSS/CMDi/LFI/RCE/SSRF/XXE/WebShell/弱口令/子域名
- ⚡ **流式检测**：爬取即检测，不等全部爬完（30页实战 / 150页靶机）
- 🔄 **断点恢复**：30 秒间隔落盘 checkpoint，`--resume` 从上次中断处继续
- 🤖 **AI 误报复核**：集成 LLM API，自动复核疑似误报的漏洞
- 🌐 **双模式运行**：CLI 命令行 + Web UI 图形界面
- 📦 **Nuclei 12.5w PoC**：智能模板扫描，无 CLI 时走内置回退
- 🎨 **三层降噪**：内容特征 + 尺寸聚类 + 校准匹配

### 🛠️ 技术栈

| 分类 | 技术 |
|------|------|
| **核心** | Python 3.8+, asyncio, aiohttp, BeautifulSoup4 |
| **检测引擎** | 自研扫描框架 + Nuclei PoC 引擎 |
| **AI 集成** | OpenAI 兼容 API (LLM 误报复核) |
| **Web UI** | Flask, Bootstrap, 实时日志流 |
| **第三方集成** | Nuclei, sqlmap, ffuf, Wappalyzer |
| **报告格式** | HTML, JSON, CSV, Markdown, Console |

---

## 🚀 快速开始

### ⚡ 方式一：从源码安装（推荐）

```bash
git clone https://github.com/xiabai2008/rayscanx
cd RayScanX
pip install -e ".[dev]"
```

### 💻 方式二：Docker 部署

```bash
docker build -t rayscanx .
docker run rayscanx scan http://example.com

# 或使用 docker-compose
TARGET_URL=http://example.com docker-compose up
```

### 🎯 开始扫描

```bash
# CLI 扫描（快速模式）
python -m wvs scan https://target.com --insecure --rate 10

# 全量扫描（含所有 Lite 模块）
python -m wvs scan https://target.com --all-modules

# Web UI 模式（推荐新手使用）
python web_ui/app.py
# 浏览器访问 http://localhost:5000
```

---

## 📁 项目结构

```
RayScanX/
├── 📄 README.md                    # 项目说明（本文件）
├── 📄 LICENSE                      # MIT 许可证
├── 📄 pyproject.toml               # 项目配置
├── 📄 Dockerfile                   # Docker 镜像构建
├── 📄 docker-compose.yml           # Docker 服务编排
├── 📂 wvs/                         # 核心扫描库
│   ├── core/                       # 扫描引擎（scanner/orchestrator/stages/爬虫/会话/限速/OOB/被动代理）
│   ├── modules/                    # 18 个检测模块（sqli/xss/oa/webshell/weakpass/subdomain…）
│   ├── integrations/               # 第三方集成（Nuclei/sqlmap/ffuf/AWVS…）
│   ├── reporting/                  # 报告（HTML/JSON/CSV/Markdown/Console）
│   ├── profiles/                   # 扫描配置 Profile
│   └── plugins/                    # 认证插件
├── 📂 web_ui/                      # Web UI（Flask）
├── 📂 rules/                       # 检测规则
├── 📂 scripts/                     # 脚本
├── 📂 scan_reports/                # 扫描报告输出（本地）
├── 📂 examples/                    # 示例代码
├── 📂 docs/                        # 技术文档
└── 📂 tests/                       # 测试
```

---

## 🎯 核心功能

### 🔐 漏洞检测能力

| 模块 | 检测维度 | 状态 |
|------|---------|:----:|
| **SQL 注入** | error/union/boolean-blind/time-based/stacked/二阶/宽字节/OOB | ✅ |
| **XSS** | reflected/stored/Polyglot/mXSS/SSTI | ✅ |
| **OA 专项** | 泛微/通达/金蝶/蓝凌/致远/用友/禅道/万户/Nacos/Spring/Jenkins/Confluence | ✅ |
| **CMDi** | 命令注入 | ✅ |
| **LFI** | 本地文件包含 | ✅ |
| **RCE** | 远程代码执行 | ✅ |
| **SSRF** | 服务端请求伪造 | ✅ |
| **XXE** | XML 外部实体注入 | ✅ |
| **WebShell** | 路径扫描 + 内容特征 + 启发式检测 | ✅ |
| **弱口令** | 表单登录 + phpMyAdmin + Tomcat Manager | ✅ |
| **子域名** | DNS爆破 + crt.sh 证书透明度 | ✅ |

### 🏢 OA 专项检测

RayScanX 能自动识别并检测以下 OA/中间件系统：

```
泛微Ecology · 通达OA · 金蝶Kingdee · 蓝凌Landray
致远Seeyon · 用友Yonyou · 禅道Zentao · 万户Whir
Nacos · Spring Boot · Jenkins · Confluence
```

**检测链路**：内容指纹识别 → 版本识别 → 规则级响应证据验证 + 版本过滤

> 仅路径可达不再视为漏洞（S1 误报治理）。详见 [OA检测规则](docs/OA检测规则.md)。

---

## 📖 文档导航

| 文档 | 说明 |
|------|------|
| [使用指南](docs/使用指南.md) | 详细安装和使用说明、CLI 参数、配置方法 |
| [功能特性](docs/功能特性.md) | 完整功能列表、架构亮点、新功能速览 |
| [检测模块](docs/检测模块.md) | 所有检测模块的功能介绍 |
| [工具集成](docs/工具集成.md) | 第三方工具和检测能力状态 |
| [OA检测规则](docs/OA检测规则.md) | OA 专项检测规则说明 |
| [架构设计](docs/架构设计.md) | 系统架构和技术栈 |
| [项目结构](docs/项目结构.md) | 目录结构和模块组织 |
| [版本历史](docs/版本历史详细.md) | 详细的版本更新记录 |
| [演进规划](docs/项目演进规划.md) | 未来发展方向 |
| [领域词汇表](docs/领域词汇表.md) | 项目术语定义 |
| [贡献指南](docs/贡献指南.md) | 如何参与项目开发 |
| [行为准则](docs/行为准则.md) | 社区行为准则 |
| [贡献者致谢](docs/贡献者致谢.md) | 贡献者致谢 |
| [更名记录](docs/更名记录.md) | 项目更名历史 |

---

## ⚙️ 常用 CLI 参数

| 参数 | 说明 | 默认值 |
|------|------|:-----:|
| `--rate` | 请求速率（req/s） | 10 |
| `--all-modules` | 启用全部 Lite 模块 | 关 |
| `--insecure` | 跳过 SSL 证书校验 | 关 |
| `--no-nuclei` | 关闭 Nuclei 阶段 | 开（默认启用） |
| `--resume` | 从上次 checkpoint 恢复 | 关 |
| `-o / -f` | 报告输出路径 / 格式 | json |
| `--timeout` | 扫描总超时（分钟） | — |

---

## 🧪 测试

项目包含完整的测试套件，覆盖核心扫描引擎和检测模块。

```bash
# 运行所有测试
pytest tests/

# 运行特定测试
pytest tests/test_sqli.py
pytest tests/test_xss.py
```

---

## 🔐 安全机制

- **三级检测链路**：内容指纹 → 版本识别 → 规则级证据验证
- **误报治理基线**：基于响应证据判定，非仅路径可达
- **三层降噪**：内容特征 + 尺寸聚类 + 校准匹配
- **AI 误报复核**：集成 LLM API 自动复核疑似误报
- **扫描限速**：可配置请求速率，避免对目标造成过大压力
- **SSL 选项**：支持跳过证书校验（`--insecure`）

---

## ❓ 常见问题

### 1. 如何启用 AI 误报复核？

```bash
export LLM_API_KEY=sk-xxx
python -m wvs scan https://target.com --ai-verify
```

### 2. 如何禁用 Nuclei？

```bash
python -m wvs scan https://target.com --no-nuclei
```

### 3. 如何从断点恢复扫描？

```bash
python -m wvs scan https://target.com --resume
```

### 4. Web UI 无法启动？

确保已安装 Flask：
```bash
pip install flask
python web_ui/app.py
```

---

## 🤝 贡献指南

1. Fork 本仓库
2. 创建特性分支：`git checkout -b feature/AmazingFeature`
3. 提交更改：`git commit -m 'Add some AmazingFeature'`
4. 推送分支：`git push origin feature/AmazingFeature`
5. 提交 Pull Request

详见 [贡献指南](docs/贡献指南.md)

---

## ⚠️ 免责声明

本工具**仅供**获得明确授权的安全测试、渗透测试及漏洞研究使用。

**未经授权扫描、攻击他人系统属于违法行为，使用者需自行承担一切法律责任。**

---

## 📄 许可证

MIT License — Copyright (c) 2026 xiabai2008

---

## 📞 联系方式

如有问题或建议，欢迎提 Issue

---

*最后更新时间：2026-09-27*