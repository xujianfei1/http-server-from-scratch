# 阶段 3：HTTP 响应

## 学习目标

- 理解 HTTP 响应格式
- 返回 HTML 页面
- 返回 404 错误页面
- 设置正确的 Header

---

## HTTP 响应格式

```
HTTP/1.1 200 OK
Content-Type: text/html
Content-Length: 13

Hello, World!
```

- 第一行：协议版本 + 状态码 + 状态文本
- 请求头：Content-Type、Content-Length 等
- 空行：分隔 header 和 body
- Body：实际内容

---

## 任务 1：返回 HTML 页面

```python
# server6.py
import socket

def handle_request(client_socket):
    request = client_socket.recv(4096)

    # 简单的路由逻辑（后面会完善）
    html = """
<!DOCTYPE html>
<html>
<head>
    <title>我的服务器</title>
</head>
<body>
    <h1>Hello, World!</h1>
    <p>这是我的第一个 HTTP 服务器</p>
</body>
</html>
"""

    # 构建响应
    response_line = "HTTP/1.1 200 OK\r\n"
    response_headers = "Content-Type: text/html; charset=utf-8\r\n"
    response_headers += f"Content-Length: {len(html.encode('utf-8'))}\r\n"
    response_headers += "\r\n"

    response = response_line.encode() + response_headers.encode() + html.encode()
    client_socket.send(response)

# ... server setup ...
```

**测试：** 用浏览器访问 `http://localhost:8080`

---

## 任务 2：返回 404 页面

```python
# server7.py
import socket

def handle_request(client_socket, request_path):
    """根据路径返回不同响应"""

    if request_path == "/":
        html = "<h1>首页</h1><p>欢迎！</p>"
        status = "200 OK"
    elif request_path == "/hello":
        html = "<h1>Hello!</h1><p>你好，世界！</p>"
        status = "200 OK"
    else:
        html = "<h1>404 Not Found</h1><p>页面不存在</p>"
        status = "404 Not Found"

    # 构建响应
    response_line = f"HTTP/1.1 {status}\r\n"
    response_headers = "Content-Type: text/html; charset=utf-8\r\n"
    response_headers += f"Content-Length: {len(html.encode('utf-8'))}\r\n"
    response_headers += "\r\n"

    response = response_line.encode() + response_headers.encode() + html.encode()
    client_socket.send(response)
```

---

## 任务 3：返回 JSON

现代 Web 开发 JSON 比 HTML 更常见：

```python
import json

def handle_json_request(client_socket):
    data = {"message": "Hello!", "status": "ok"}

    json_str = json.dumps(data)
    response_line = "HTTP/1.1 200 OK\r\n"
    response_headers = "Content-Type: application/json\r\n"
    response_headers += f"Content-Length: {len(json_str.encode('utf-8'))}\r\n"
    response_headers += "\r\n"

    response = response_line.encode() + response_headers.encode() + json_str.encode()
    client_socket.send(response)
```

---

## 常用状态码

| 状态码 | 含义 | 何时使用 |
|--------|------|----------|
| 200 | OK | 成功 |
| 301 | Moved Permanently | 重定向 |
| 400 | Bad Request | 请求格式错误 |
| 404 | Not Found | 资源不存在 |
| 500 | Internal Server Error | 服务器错误 |

---

## 常用 Content-Type

| 类型 | 用途 |
|------|------|
| `text/html` | HTML 页面 |
| `text/plain` | 纯文本 |
| `application/json` | JSON 数据 |
| `image/png` | PNG 图片 |
| `image/jpeg` | JPEG 图片 |
| `text/css` | CSS 文件 |
| `application/javascript` | JS 文件 |

---

## 阶段成果检查

- [ ] 浏览器能显示 HTML 页面
- [ ] 访问不存在的路径返回 404
- [ ] 能返回 JSON 数据
- [ ] Content-Length 正确

---

## 下一步

下一阶段我们实现一个完整的路由系统，让代码更清晰。
