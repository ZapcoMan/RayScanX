# 🔗 外部工具集成

## 支持的检测模块

| 模块 | 检测类型 |
|------|----------|
| `sqli` | SQL 注入 (error-based / union / boolean-blind / time-based / stacked) |
| `xss` | 跨站脚本 (反射型/存储型) |
| `cmdi` | 命令注入 |
| `lfi` | 本地文件包含 |
| `rce` | 远程代码执行 |
| `ssrf` | 服务端请求伪造 |
| `xxe` | XML 外部实体注入 |
| `api` | API 安全检测 |
| `sensitive` | 敏感信息泄露 |
| `waf` | WAF 检测与绕过 |
| `jspathfinder` | JavaScript 端点发现 |

## 第三方工具集成

| 工具 | 用途 | 安装方式 |
|------|------|----------|
| Nuclei | 漏洞模板扫描 | `pip install nuclei-python` |
| sqlmap | SQL 注入深度利用 | 需单独安装 |
| ffuf | 模糊测试 | 需单独安装 |
| Wappalyzer | 技术栈识别 | `pip install python-Wappalyzer` |

## 检测能力状态

| 能力 | 状态 | 靶机验证 |
|------|------|:--------:|
| SQL 注入 | ✅ error-based / union / boolean-blind / time-based | ✅ Metasploitable 2 — UNION 注入提取 5 用户密码 |
| XSS | ✅ 反射型 / 存储型 | ✅ 靶机验证通过（security=low） |
| 命令注入 | ✅ 高精度 | ⬜ 靶机未开放，但检测引擎就绪 |
| LFI | ✅ 本地文件包含 | ✅ Metasploitable 2 — 读取 /etc/passwd 成功 |
| SSRF | ✅ 服务端请求伪造 | ⬜ 待验证 |
| XXE | ✅ XML 外部实体注入 | ⬜ 待验证 |
| RCE | ✅ 远程代码执行 | ⬜ 待验证 |
| 敏感信息泄露 | ✅ 高覆盖 | ✅ Metasploitable 2 — 发现 /test/、phpinfo.php、phpMyAdmin 密码泄露 |
| WAF 绕过 | ✅ 多策略 | ⬜ 待验证 |
| API 扫描 | ✅ API 安全检测 | ✅ Metasploitable 2 — 80 个 Server 版本泄露 + 密码字段发现 |
| 第三方集成 | ✅ Nuclei, sqlmap, ffuf, Wappalyzer | ⬜ 需要独立安装第三方工具 |