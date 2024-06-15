import http.server
import socketserver
import requests
from urllib.parse import urlparse

PORT = 30830

class ProxyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        # 解析目标URL
        url = urlparse(self.path.lstrip('/'))
        target_url = f"{url.scheme}://{url.netloc}{url.path}"

        try:
            # 发起并发请求
            responses = [requests.get(target_url, stream=True) for _ in range(3)]  # 可根据需要调整并发数量

            # 合并响应
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')  # 设置响应内容类型为 HTML
            self.send_header('Access-Control-Allow-Origin', '*')  # 允许跨域访问
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type, Content-Length, Authorization, Accept, X-Requested-With')
            self.send_header('Access-Control-Allow-Credentials', 'true')
            self.end_headers()

            for resp in responses:
                for chunk in resp.iter_content(chunk_size=1024):
                    if chunk:
                        self.wfile.write(chunk)

        except Exception as e:
            print(f"Error: {e}")
            self.send_error(500, "Internal Server Error")

with socketserver.TCPServer(("", PORT), ProxyHandler) as httpd:
    print(f"Proxy server started at http://localhost:{PORT}/")
    httpd.serve_forever()