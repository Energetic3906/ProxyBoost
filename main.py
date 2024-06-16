import http.server
import socketserver
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter

PORT = 30830

class ProxyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        # 解析目标URL
        url = urlparse(self.path.lstrip('/'))
        target_url = f"{url.scheme}://{url.netloc}{url.path}"

        try:
            # 创建会话并设置最大重试次数
            s = requests.Session()
            s.mount('http://', HTTPAdapter(max_retries=3))
            s.mount('https://', HTTPAdapter(max_retries=3))

            # 发起请求,设置超时时间为30秒
            response = s.get(target_url, stream=True, timeout=30)

            # 检查是否为目录列表页面
            if response.headers.get('Content-Type', '').startswith('text/html'):
                soup = BeautifulSoup(response.text, 'html.parser')
                if soup.title and soup.title.string == 'Index of ' + url.path.rstrip('/'):
                    self.handle_directory_listing(soup, target_url)
                    return

            # 如果不是目录列表页面,则按照正常方式处理响应
            self.send_response(response.status_code)
            for header, value in response.headers.items():
                self.send_header(header, value)
            self.end_headers()

            try:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        self.wfile.write(chunk)
            except (ConnectionResetError, BrokenPipeError):
                # 忽略连接被客户端中断的错误
                pass

        except Exception as e:
            print(f"Error: {e}")
            try:
                self.send_error(500, "Internal Server Error")
            except (ConnectionResetError, BrokenPipeError):
                # 忽略连接被客户端中断的错误
                pass

    # handle_directory_listing 方法保持不变

with socketserver.TCPServer(("", PORT), ProxyHandler) as httpd:
    print(f"Proxy server started at http://localhost:{PORT}/")
    httpd.serve_forever()