# 阶段 4：路由系统

## 学习目标

- 用字典管理路由映射
- 支持 GET 参数解析
- 代码结构更清晰

---

## 什么是路由？

路由就是**把 URL 路径映射到处理函数**：

```
/          → show_homepage()
/hello     → say_hello()
/time      → show_time()
/not-found → show_404()
```

---

## 任务 1：基础路由字典

```python
# server8.py
import socket
import datetime

# 路由表：用字典存储路径→函数的映射
ROUTES = {
    '/': 'homepage',
    '/hello': 'hello',
    '/time': 'time',
}

def route_handler(path):
    """根据路径返回响应"""
    handler = ROUTES.get(path, 'not_found')

    if handler == 'homepage':
        return """
<!DOCTYPE html>
<html>
<body>
    <h1>首页</h1>
    <ul>
        <li><a href="/hello">Hello</a></li>
        <li><a href="/time">当前时间</a></li>
    </ul>
</body>
</html>
"""
    elif handler == 'hello':
        return "<h1>Hello!</h1><p>你好，世界！</p>"

    elif handler == 'time':
        now = datetime.datetime.now()
        return f"<h1>当前时间</h1><p>{now}</p>"

    else:
        return "<h1>404</h1><p>页面不存在</p>"

def handle_request(client_socket):
    request = client_socket.recv(4096)
    lines = request.decode('utf-8', errors='replace').split('\r\n')
    method, path, version = lines[0].split(' ')

    print(f"请求: {method} {path}")

    html = route_handler(path)

    response_line = "HTTP/1.1 200 OK\r\n"
    response_headers = "Content-Type: text/html; charset=utf-8\r\n"
    response_headers += f"Content-Length: {len(html.encode('utf-8'))}\r\n"
    response_headers += "\r\n"

    response = response_line.encode() + response_headers.encode() + html.encode()
    client_socket.send(response)
```

---

## 任务 2：支持 GET 参数

URL 可以带参数：`/search?q=python&lang=zh`

```python
from urllib.parse import urlparse, parse_qs

def parse_get_params(path):
    """解析 URL 中的 GET 参数"""
    # 分离路径和查询字符串
    parsed = urlparse(path)
    query_string = parsed.query  # 'q=python&lang=zh'

    # 解析为字典
    params = parse_qs(query_string)

    return parsed.path, params

# 使用
path, params = parse_get_params("/search?q=python&lang=zh")
print(path)      # /search
print(params)    # {'q': ['python'], 'lang': ['zh']}
```

---

## 任务 3：RESTful 路由（可选挑战）

支持不同 HTTP 方法：

```python
ROUTES = {
    ('GET', '/'): homepage,
    ('GET', '/hello'): hello,
    ('POST', '/submit'): submit,
    ('GET', '/user/<id>'): user_profile,  # 动态路由
}

def match_route(method, path):
    """匹配路由"""
    for (m, p), handler in ROUTES.items():
        if m == method and p == path:
            return handler

    # 尝试动态路由
    for (m, p), handler in ROUTES.items():
        if m == method and match_dynamic(p, path):
            return handler

    return not_found
```

---

## 阶段成果检查

- [ ] 用字典管理路由
- [ ] /hello 返回问候页面
- [ ] /time 返回当前时间
- [ ] 访问未知路径返回 404
- [ ] （可选）支持 GET 参数

---

## 下一步

下一阶段实现静态文件服务，让服务器能托管真实网站文件。
