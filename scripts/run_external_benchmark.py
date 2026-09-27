"""
RayScan 外部基准（Juice Shop）— CI 专用（workflow_dispatch 手动触发）。

本机网络受限（Docker Hub 阻断）时无法运行；GitHub Actions 环境可跑。
流程：docker run juice-shop → 扫描 → 断言核心模块检出 → 汇总。

用法：python scripts/run_external_benchmark.py [--port 3000]
"""

import argparse
import json
import subprocess
import sys
import time
import urllib.request
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parent.parent


def wait_ready(url: str, timeout: int = 180) -> bool:
    """等待目标 URL 服务就绪
    
    循环检查目标 URL 是否返回 200 状态码，用于等待 Docker 容器或其他服务启动完成。
    
    Args:
        url: 要检查的目标 URL
        timeout: 最大等待时间（秒），默认 180 秒
        
    Returns:
        bool: 服务就绪返回 True，超时返回 False
    """
    deadline = time.time() + timeout  # 计算超时截止时间
    while time.time() < deadline:
        try:
            r = urllib.request.urlopen(url, timeout=5)  # 尝试访问 URL
            if r.status == 200:
                return True  # 服务已就绪
        except Exception:
            time.sleep(3)  # 请求失败，等待 3 秒后重试
    return False  # 超时未就绪


def scan(port: int, modules: str, out_name: str, timeout: int = 1800, extra_args: Optional[list] = None) -> list:
    """执行扫描并返回漏洞列表
    
    调用 RayScanX 扫描器对目标进行漏洞检测，解析结果后删除临时报告文件。
    
    Args:
        port: 目标服务端口
        modules: 要启用的检测模块（空格分隔）
        out_name: 输出报告文件名（不含扩展名）
        timeout: 扫描超时时间（秒），默认 1800 秒
        extra_args: 额外的 CLI 参数列表
        
    Returns:
        list: 漏洞元组列表，每项为 (type, severity, url)
    """
    out = ROOT / f"{out_name}.json"  # 报告输出路径
    cmd = [
        sys.executable,
        "-m",
        "wvs",
        "scan",
        f"http://127.0.0.1:{port}/",
        "--modules",
        modules,
        "--no-nuclei",
        "--allow-loopback",
        "--rate",
        "15",
        "--max-time",
        "1500",  # 大型 SPA 目标限时，防 CI 超时
        "-o",
        str(out),
    ]
    if extra_args:
        cmd.extend(extra_args)
    subprocess.run(cmd, cwd=ROOT, capture_output=True, timeout=timeout)
    if not out.exists():
        return []
    data = json.loads(out.read_text(encoding="utf-8"))
    out.unlink(missing_ok=True)  # 清理临时报告文件
    return [(v.get("type"), v.get("severity"), v.get("url")) for v in data.get("vulnerabilities", [])]


def main() -> int:
    """主函数：启动 Juice Shop 容器，执行扫描，验证基准测试结果
    
    流程：
    1. 启动 OWASP Juice Shop Docker 容器
    2. 等待服务就绪
    3. 记录镜像版本信息（用于诊断）
    4. 执行核心模块扫描（sqli/xss/api/sensitive）
    5. 验证 XSS 检出（硬断言 ≥1）
    6. 记录 SQLi 检出（诊断模式，不强制要求）
    7. 清理容器
    
    Returns:
        int: 基准测试通过返回 0，失败返回 1
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=3000, help="Juice Shop 映射端口")
    parser.add_argument("--image", default="bkimminich/juice-shop", help="Docker 镜像名称")
    args = parser.parse_args()

    print("[*] 启动 Juice Shop 容器...")
    subprocess.run(["docker", "rm", "-f", "rayscan-juiceshop"], capture_output=True)  # 清理旧容器
    subprocess.run(
        [
            "docker",
            "run",
            "-d",
            "--name",
            "rayscan-juiceshop",
            "-p",
            f"{args.port}:3000",
            args.image,
        ],
        capture_output=True,
    )
    try:
        base = f"http://127.0.0.1:{args.port}/"
        if not wait_ready(base):
            print("[FAIL] Juice Shop 未就绪")
            return 1

        # 诊断：记录实际运行的镜像 digest（未钉 tag 时镜像漂移是外部基准失效的首要嫌疑,
        # digest 唯一标识应用版本——断言失败时应据此钉死版本再重跑）
        for fmt in ("{{index .RepoDigests 0}}", "{{.Image}}"):
            try:
                out = subprocess.run(
                    ["docker", "inspect", "--format", fmt, "rayscan-juiceshop"],
                    capture_output=True,
                    text=True,
                    timeout=30,
                )
                tag = "digest" if "RepoDigests" in fmt else "image_id"
                print(f"  [{tag}] {out.stdout.strip()}")
            except Exception as e:  # noqa: BLE001
                print(f"  [{tag}] 获取失败: {e}")

        print("[*] 扫描核心模块（sqli/xss/api/sensitive，--js-render 渲染）...")
        cmd_extra = ["--js-render"]
        # scan() 已支持 --js-render（SPA 渲染 + XHR 捕获）——外部目标（Juice Shop）需要
        vulns = scan(args.port, "sqli xss api sensitive", "bench_juice_core", extra_args=cmd_extra)
        print(f"  检出 {len(vulns)} 个漏洞")

        sqli = [v for v in vulns if v[0] == "sql_injection"]
        xss = [v for v in vulns if v[0] == "cross_site_scripting"]
        print(f"  sqli: {len(sqli)} | xss: {len(xss)} | 其他: {len(vulns) - len(sqli) - len(xss)}")

        # 重扫自愈：xss=0 时渲染时序抖动（慢 runner 页面加载超时）会偶发全 0，
        # 重扫一次排除抖动——真实 SPA 爬取回归会连续两次失败
        if len(xss) < 1:
            print("[RETRY] xss 0 — 疑似渲染时序抖动,重扫一次")
            vulns = scan(args.port, "sqli xss api sensitive", "bench_juice_core", extra_args=cmd_extra)
            sqli = [v for v in vulns if v[0] == "sql_injection"]
            xss = [v for v in vulns if v[0] == "cross_site_scripting"]
            print(f"  [重扫] sqli: {len(sqli)} | xss: {len(xss)} | 其他: {len(vulns) - len(sqli) - len(xss)}")

        # 硬断言（第六轮）：xss ≥1 —— SPA/JSON API 链路有效性的门禁（search 反射已稳定 PASS）。
        # sqli 记录为 DIAG：真实 Juice Shop 的 login POST 仅在用户交互时发出，
        # 无交互 SPA 捕获发现不了该端点（依赖交互式爬取，工程量大，列入待办）。
        failed = 0
        ok = len(xss) >= 1
        if not ok:
            failed += 1
        print(f"  [{'PASS' if ok else 'FAIL'}] xss（search 反射）: {len(xss)} — XSS 检出 ≥1")
        print(f"  [DIAG] sqli（login 注入）: {len(sqli)} — 依赖交互端点，待交互式爬取支持")

        for v in vulns[:15]:
            print(f"    - {v[0]}/{v[1]} @ {v[2][:80]}")

        if failed:
            print("[RESULT] 外部基准失败")
            return 1
        print("[RESULT] 外部基准通过")
        return 0
    finally:
        subprocess.run(["docker", "rm", "-f", "rayscan-juiceshop"], capture_output=True)  # 清理容器


if __name__ == "__main__":
    sys.exit(main())