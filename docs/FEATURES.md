# 📋 功能特性

## 🎯 核心专精模块（默认加载）

| 模块 | 检测维度 | 层级 |
|------|---------|:----:|
| **SQL 注入** | 8种: error/union/boolean-blind/time-based/stacked/**二阶**/**宽字节**/**OOB** | 🟢 核心 |
| **XSS** | 5种: reflected/stored/**Polyglot**/**mXSS**/**SSTI**（DOM XSS 待 headless 验证，见 Roadmap）| 🟢 核心 |
| **OA 专项** | 12种: 泛微/通达/金蝶/蓝凌/致远/用友/禅道/万户/Nacos/Spring/Jenkins/Confluence | 🟡 Lite |
| **WebShell** | 路径扫描 + 内容特征 + 启发式检测 | 🟡 Lite |
| **弱口令** | 表单登录 + phpMyAdmin + Tomcat Manager | 🟡 Lite |
| **子域名** | DNS爆破 + crt.sh 证书透明度 | 🟡 Lite |
| CMDi / LFI / RCE / SSRF / XXE | 通用漏洞检测 | 🟡 Lite |
| sensitive / api / waf / jspathfinder | 信息收集 + 绕过 | 🟡 Lite |

## 🧩 Lite 辅助模块（--all-modules 启用）

| 模块 | 说明 |
|------|------|
| CMDi / LFI / RCE / SSRF / XXE | 通用漏洞检测 |
| sensitive / api / waf / jspathfinder | 信息收集 + 绕过 |
| mcp / graphql | MCP 工具泄露检测 · GraphQL introspection/批量查询 |
| 第三方集成 | Nuclei · sqlmap · ffuf · Wappalyzer |
| 报告格式 | HTML · JSON · CSV · Markdown · Console |

## ⚡ 架构亮点

- **Nuclei 12.5w PoC 引擎** — 扫描主流程默认启用（`--no-nuclei` 关闭）：CLI 可用走智能模板扫描，不可用走内置内容特征回退（无"可达即报"）
- **OA 三级检测链路** — 内容指纹识别（title/正文/响应头）→ 版本识别（Jenkins/Nacos/Spring…）→ 规则级响应证据验证 + 版本过滤（如 Nacos 1.x 用户列表未授权）
- **扫描断点恢复** — 30 秒间隔落盘 checkpoint，`--resume` 合并已发现漏洞并跳过已完成模块
- **误报治理基线** — 全部检测判定基于响应证据（baseline 排除/内容特征），仅路径可达不再视为漏洞
- **流式检测** — 爬取即检测，不等全部爬完（30页实战 / 150页靶机）
- **双路径自动分流** — 检测到靶机IP/路径则走靶机流程，否则走实战流程
- **三层降噪** — 内容特征 + 尺寸聚类 + 校准匹配
- **规划中** — 多引擎聚合（AWVS/Nessus/sqlmap 一键调度）、Metasploit 漏洞验证链

## 🎯 新功能速览

### 🤖 v2.2.0 — AI 复核 + MCP + GraphQL

```bash
# AI 误报复核（官方 OpenAI 兼容 API，无 key 时静默跳过）
export LLM_API_KEY=sk-xxx
python -m wvs scan https://target.com --ai-verify
# AI 报告摘要
python -m wvs ai-report scan_reports/report_xxx.json -o summary.md

# MCP Server — 让 Claude/ChatGPT 直接驱动扫描（pip install "rayscan[mcp]"）
python -m wvs mcp            # http://127.0.0.1:18000/mcp，工具: scan/list_modules/get_report

# 新增 lite 模块（--all-modules）：mcp（MCP 工具泄露检测）、graphql（introspection/批量查询）
python -m wvs scan https://target.com --all-modules

# 实验性 SPA 爬取（pip install "rayscan[jsrender]"）
python -m wvs scan https://spa-target.com --js-render
```

### 🏢 OA 专项检测
RayScan 能自动识别并检测以下 OA/中间件系统：
```
泛微Ecology · 通达OA · 金蝶Kingdee · 蓝凌Landray
致远Seeyon · 用友Yonyou · 禅道Zentao · 万户Whir
Nacos · Spring Boot · Jenkins · Confluence
```
检测类型：SQL注入 / RCE / 文件上传 / 认证绕过 / 配置泄露 / 未授权访问
> 检测链路：内容指纹识别 → 版本识别 → 规则级响应证据验证 + 版本过滤。
> 仅路径可达不再视为漏洞（S1 误报治理）。详见 [OA 检测规则](OA_RULES.md)。

### 📦 Nuclei 12.5w PoC 管理
```bash
# 一键部署 Nuclei 模板
./scripts/deploy_nuclei_templates.sh

# 扫描默认自动运行 Nuclei 阶段（智能模板选择；无 CLI 时走内置回退）
python -m wvs scan https://target.com

# 禁用 Nuclei 阶段
python -m wvs scan https://target.com --no-nuclei
```

### 💾 扫描断点恢复
```bash
# 长任务中断后，从上次 checkpoint 恢复（合并已发现漏洞 + 跳过已完成模块）
python -m wvs scan https://target.com --resume
```

### 🧭 规划中（Roadmap）
以下能力已在 `wvs/integrations/` 实现集成层，但**尚未接入主扫描流程**，当前版本不生效：
- **多引擎聚合** — AWVS / Nessus / sqlmap 一键调度 + 结果去重合并
- **Metasploit 漏洞验证链** — MSF RPC 自动匹配 exploit 模块验证漏洞真实性

接入完成后将随版本发布启用，详见 [技术演进规划](audit/rayscan-evolution-plan-2026-07-12.md)。