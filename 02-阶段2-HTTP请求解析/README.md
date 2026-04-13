# 阶段 2：HTTP 请求解析

## 学习目标

- 看到真实的 HTTP 请求长什么样
- 解析请求行（方法、路径、协议版本）
- 解析请求头（Host、Content-Type 等）

---

## HTTP 请求格式

一个真实的 HTTP 请求是这样的：

```
GET /hello HTTP/1.1
Host: localhost:8080
User-Agent: curl/7.68.0
Accept: */*
Connection: keep-alive


```

第一行叫**请求行**，后面是**请求头**，中间以空行分隔。

---

## 任务 1：完整读取请求

```python
# server3.py
import socket

def handle_request(client_socket):
    """处理客户端请求"""
    # 接收数据
    request = client_socket.recv(4096)

    # 打印原始请求（方便调试）
    print("=== 原始请求 ===")
    print(request.decode('utf-8', errors='replace'))
    print("==============")

    # 发送简单响应
    response = b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nReceived!"
    client_socket.send(response)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 8080))
server.listen(1)

print("服务器启动...")
client, address = server.accept()
handle_request(client)
client.close()
server.close()
```

**测试：**

```bash
python server3.py
nc localhost 8080
# 输入上面的 HTTP 请求
```

---

## 任务 2：解析请求行

```python
# server4.py
import socket

def parse_request(request_bytes):
    """解析 HTTP 请求"""
    # 解码为字符串
    request_text = request_bytes.decode('utf-8', errors='replace')

    # 按行分割
    lines = request_text.split('\r\n')

    # 第一行是请求行
    request_line = lines[0]
    print(f"请求行: {request_line}")

    # 解析请求行
    parts = request_line.split(' ')
    method = parts[0]      # GET
    path = parts[1]       # /hello
    http_version = parts[2]  # HTTP/1.1

    return method, path, http_version

def handle_request(client_socket):
    request = client_socket.recv(4096)
    method, path, version = parse_request(request)

    print(f"方法: {method}")
    print(f"路径: {path}")
    print(f"协议版本: {version}")

    response = b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nParsed!"
    client_socket.send(response)

# ... server setup same as before ...
```

---

## 任务 3：解析请求头

```python
# server5.py
import socket

def parse_headers(lines):
    """解析请求头"""
    headers = {}
    for line in lines[1:]:  # 跳过请求行
        if line == '':  # 空行结束
            break
        key, value = line.split(': ', 1)
        headers[key] = value
    return headers

def handle_request(client_socket):
    request = client_socket.recv(4096)
    lines = request.decode('utf-8', errors='replace').split('\r\n')

    # 请求行
    method, path, version = lines[0].split(' ')

    # 请求头
    headers = parse_headers(lines)

    print(f"请求: {method} {path}")
    print(f"Headers: {headers}")

    response = b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nOK"
    client_socket.send(response)

# ... server setup same as before ...
```

---

## 阶段成果检查

- [ ] 打印出原始 HTTP 请求
- [ ] 提取出请求方法（GET/POST）
- [ ] 提取出请求路径（/hello）
- [ ] 提取出所有请求头

---

## 挑战

尝试解析这个请求：

```
POST /submit HTTP/1.1
Host: localhost:8080
Content-Type: application/x-www-form-urlencoded
Content-Length: 13

name=Alice&age=25
```

你能提取出 `name=Alice&age=25` 这个请求体吗？

---

## 下一步

下一阶段我们构建完整的 HTTP 响应，让浏览器能显示页面。
