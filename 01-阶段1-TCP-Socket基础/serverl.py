#serverl.py
import socket
import os
import threading
import json
import logging
import base64
from datetime import datetime
from pathlib import Path

# ============================================
# 配置
# ============================================
CONFIG = {
    "host": "localhost",
    "port": 8080,
    "public_dir": "public",
    "log_enabled": True,
    "username": "admin",
    "password": "123456",
}

def load_config():
    """从配置文件加载配置"""
    config_path = Path(__file__).parent / "config.json"
    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            loaded = json.load(f)
            CONFIG.update(loaded)

load_config()

# 静态文件目录
PUBLIC_DIR = Path(__file__).parent / CONFIG["public_dir"]

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(message)s',
    datefmt='%H:%M:%S',
)

def log(msg):
    """打印日志"""
    if CONFIG["log_enabled"]:
        logging.info(msg)

# ============================================
# MIME 类型表
# ============================================
MIME_TYPES = {
    '.html': 'text/html',
    '.css': 'text/css',
    '.js': 'application/javascript',
    '.json': 'application/json',
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.gif': 'image/gif',
    '.svg': 'image/svg+xml',
    '.ico': 'image/x-icon',
    '.txt': 'text/plain',
}

def get_mime_type(file_path):
    """根据文件扩展名获取 MIME 类型"""
    ext = os.path.splitext(file_path)[1].lower()
    return MIME_TYPES.get(ext, 'application/octet-stream')

def check_auth(headers):
    """检查 HTTP Basic Auth 认证"""
    auth_header = headers.get('Authorization', '')
    if not auth_header.startswith('Basic '):
        return False
    encoded = auth_header[6:]
    try:
        decoded = base64.b64decode(encoded).decode('utf-8')
        username, password = decoded.split(':', 1)
        return username == CONFIG['username'] and password == CONFIG['password']
    except:
        return False

def make_auth_response():
    """返回 401 认证挑战响应"""
    body = "<h1>401 Unauthorized</h1><p>需要登录</p>"
    body_bytes = body.encode('utf-8')
    response_line = "HTTP/1.1 401 Unauthorized\r\n"
    response_headers = "WWW-Authenticate: Basic realm=\"HTTP Server\"\r\n"
    response_headers += "Content-Type: text/html; charset=utf-8\r\n"
    response_headers += f"Content-Length: {len(body_bytes)}\r\n"
    response_headers += "Connection: close\r\n"
    response_headers += "\r\n"
    response = response_line.encode() + response_headers.encode() + body_bytes
    return response

# ============================================
# 路由处理器
# ============================================
def home_handler():
    return "<h1>首页</h1><p>欢迎访问！</p><p><a href='/index.html'>访问静态首页</a></p>"

def hello_handler():
    return "<h1>Hello!</h1><p>你好，世界！</p>"

def time_handler():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"<h1>当前时间</h1><p>{now}</p>"

def about_handler():
    return "<h1>关于</h1><p>这是2026年第一次尝试</p>"

def not_found_handler():
    return "<h1>404 Not Found</h1><p>页面不存在</p>"

# 路由表
ROUTES = {
    "/": home_handler,
    "/hello": hello_handler,
    "/time": time_handler,
    "/about": about_handler,
}

# ============================================
# 工具函数
# ============================================
def parse_request(request_text):
    """解析 HTTP 请求"""
    lines = request_text.split('\r\n')
    request_line = lines[0]
    parts = request_line.split(' ')
    method = parts[0]
    path = parts[1]
    version = parts[2]

    headers = {}
    for line in lines[1:]:
        if line == '':
            break
        key, value = line.split(': ', 1)
        headers[key] = value

    return method, path, version, headers

def make_response(body, status=200, content_type="text/html"):
    """构建 HTTP 响应"""
    status_text = "OK" if status == 200 else "Not Found"
    body_bytes = body.encode('utf-8')

    response_line = f"HTTP/1.1 {status} {status_text}\r\n"
    response_headers = f"Content-Type: {content_type}; charset=utf-8\r\n"
    response_headers += f"Content-Length: {len(body_bytes)}\r\n"
    response_headers += "Connection: close\r\n"
    response_headers += "\r\n"

    response = response_line.encode() + response_headers.encode() + body_bytes
    return response

def make_file_response(file_path, status=200):
    """返回静态文件"""
    with open(file_path, 'rb') as f:
        content = f.read()

    mime_type = get_mime_type(file_path)

    # 文本类型加上 utf-8 编码
    if mime_type.startswith('text/') or mime_type == 'application/javascript':
        mime_type += '; charset=utf-8'

    response_line = f"HTTP/1.1 {status} OK\r\n"
    response_headers = f"Content-Type: {mime_type}\r\n"
    response_headers += f"Content-Length: {len(content)}\r\n"
    response_headers += "Connection: close\r\n"
    response_headers += "\r\n"

    response = response_line.encode() + response_headers.encode() + content
    return response

# ============================================
# 请求处理（在新线程中运行）
# ============================================
def handle_request(client_socket, address):
    """处理客户端请求"""
    start_time = datetime.now()

    try:
        data = client_socket.recv(8192)

        if not data:
            return

        request_text = data.decode('utf-8', errors='replace')
        method, path, version, headers = parse_request(request_text)

        log(f"{address} {method} {path}")

        # 安全检查：认证验证
        if not check_auth(headers):
            log(f"{address} 认证失败")
            response = make_auth_response()
            client_socket.send(response)
            return

        # 静态文件服务
        if path in ['/index.html', '/style.css', '/script.js'] or path.startswith('/static/'):
            if '..' in path:
                response = make_response("<h1>403 Forbidden</h1><p>禁止访问</p>", 403)
                client_socket.send(response)
                return

            file_path = path.lstrip('/')
            full_path = PUBLIC_DIR / file_path

            try:
                response = make_file_response(full_path)
                client_socket.send(response)
            except FileNotFoundError:
                response = make_response("<h1>404</h1><p>文件不存在</p>", 404)
                client_socket.send(response)
            return

        # 动态路由
        handler = ROUTES.get(path, not_found_handler)
        body = handler()
        response = make_response(body)
        client_socket.send(response)

        # 记录响应状态
        status = 200

    except Exception as e:
        log(f"{address} 错误: {e}")
        try:
            response = make_response("<h1>500 Internal Server Error</h1>", 500)
            client_socket.send(response)
        except:
            pass

    finally:
        client_socket.close()
        duration = (datetime.now() - start_time).total_seconds() * 1000
        log(f"{address} 关闭 (耗时 {duration:.1f}ms)")

# ============================================
# 主循环
# ============================================
def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((CONFIG["host"], CONFIG["port"]))
    server.listen(5)

    print("=" * 50)
    print("  HTTP Server from Scratch")
    print("=" * 50)
    print(f"  主机: {CONFIG['host']}")
    print(f"  端口: {CONFIG['port']}")
    print(f"  静态目录: {PUBLIC_DIR}")
    print("=" * 50)
    print("按 Ctrl+C 停止服务器")
    print("")

    log("服务器启动")

    while True:
        try:
            client, address = server.accept()
            log(f"{address} 新连接")

            # 启动新线程处理请求
            thread = threading.Thread(target=handle_request, args=(client, address))
            thread.start()

        except KeyboardInterrupt:
            log("服务器关闭")
            print("\n服务器已停止")
            break
        except Exception as e:
            log(f"服务器错误: {e}")

if __name__ == "__main__":
    main()
