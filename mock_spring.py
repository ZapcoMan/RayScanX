"""S5 合成靶场：忠实模拟 Spring Boot Actuator 暴露的响应签名。

用于验证 OA 模块 Spring 检测链路（指纹 → actuator 检查 → 证据验证）。
响应内容参照真实 Spring Boot 2.x actuator 输出构造。
"""
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

PORT = 8898

ENV_JSON = {
    "activeProfiles": ["prod"],
    "propertySources": [
        {
            "name": "server.ports",
            "properties": {
                "local.server.port": {"value": 8898},
            },
        },
        {
            "name": "application.yml",
            "properties": {
                "spring.datasource.password": {"value": "s3cr3t-password"},
                "spring.redis.password": {"value": "redis-pass"},
            },
        },
    ],
}

HEAPDUMP_BYTES = bytes(range(256)) * 200  # 51KB 二进制，非 HTML


class Handler(BaseHTTPRequestHandler):
    """Spring Boot Actuator 模拟处理器"""

    def log_message(self, *args):
        """禁用默认日志输出"""
        pass

    def _send(self, code, body, ctype="application/json;charset=UTF-8"):
        """发送 HTTP 响应
        
        Args:
            code: HTTP 状态码
            body: 响应体字节数据
            ctype: Content-Type 头部值
        """
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        """处理 GET 请求，模拟 Spring Boot Actuator 端点"""
        path = self.path.split("?")[0]  # 移除查询参数
        
        if path == "/":
            # 模拟 Spring Boot 默认 404 错误页面
            html = (
                "<html><head><title>Whitelabel Error Page</title></head>"
                "<body><h1>Whitelabel Error Page</h1>"
                "<p>This application has no explicit mapping for /error, so you are seeing this as a fallback.</p>"
                "<p>Spring Boot</p></body></html>"
            ).encode()
            self._send(404, html, "text/html;charset=UTF-8")
            
        elif path == "/actuator/env":
            # 模拟环境变量端点，返回预定义的环境配置
            self._send(200, json.dumps(ENV_JSON).encode())
            
        elif path == "/actuator/heapdump":
            # 模拟堆转储端点，返回二进制堆转储数据
            self._send(200, HEAPDUMP_BYTES, "application/octet-stream")
            
        elif path == "/actuator/health":
            # 模拟健康检查端点，返回服务状态
            self._send(200, json.dumps({"status": "UP"}).encode())
            
        else:
            # 其他路径返回标准 Spring Boot 404 JSON 响应
            self._send(404, b'{"timestamp":"2026-08-24T00:00:00.000+00:00","status":404,"error":"Not Found","path":"' + path.encode() + b'"}')


if __name__ == "__main__":
    print(f"Spring Boot Actuator mock listening on :{PORT}")
    HTTPServer(("127.0.0.1", PORT), Handler).serve_forever()