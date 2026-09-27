# 📂 项目结构

```
RayScanX/
├── wvs/                       # 核心扫描库
│   ├── core/                  # 扫描引擎（scanner/orchestrator/stages/爬虫/会话/限速/OOB/被动代理）
│   ├── modules/               # 18 个检测模块（sqli/xss/oa/webshell/weakpass/subdomain…）
│   ├── integrations/          # 第三方集成（Nuclei/sqlmap/ffuf/AWVS…）
│   ├── reporting/             # 报告（HTML/JSON/CSV/Markdown/Console）
│   ├── profiles/              # 扫描配置 Profile
│   └── plugins/               # 认证插件
├── web_ui/                    # Web UI（Flask）
├── rules/                     # 检测规则
├── scripts/                   # 脚本
├── scan_reports/              # 扫描报告输出（本地）
├── examples/                  # 示例代码
├── docs/                      # 技术文档（adr/ audit/ agents/）
├── tests/                     # 测试
├── CONTEXT.md                 # 领域词汇表
├── pyproject.toml             # 项目配置
└── LICENSE                    # MIT 许可证
```