# 阶段 1：TCP Socket 基础

## 学习目标

- 理解 TCP Socket 是什么
- 学会用 Python 监听端口
- 用 `nc` 或 `telnet` 连接并测试

---

## 核心概念

### 什么是 Socket？

Socket 是**网络通信的端点**。就像打电话需要电话机一样，计算机之间通信需要 Socket。

```
计算机 A (Server)                    计算机 B (Client)
┌─────────────┐                    ┌─────────────┐
│   Socket    │ ←──── TCP 连接 ──→ │   Socket    │
│  监听 :8080  │                    │  连接 :8080  │
└─────────────┘                    └─────────────┘
```

### 服务器流程

```python
import socket

# 1. 创建 socket 对象
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 2. 绑定端口
server.bind(('localhost', 8080))

# 3. 开始监听
server.listen(5)

print("服务器运行在 :8080 ...")
```

---

## 任务 1：最简单的服务器

```python
# server1.py
import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 8080))
server.listen(1)

print("服务器启动，监听 8080 端口...")

while True:
    client, address = server.accept()
    print(f"收到来自 {address} 的连接")
    client.close()
```

**测试：**

```bash
# 终端 1：运行服务器
python server1.py

# 终端 2：连接服务器
nc localhost 8080
# 或
telnet localhost 8080
```

---

## 任务 2：收发数据

```python
# server2.py
import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 8080))
server.listen(1)

print("服务器启动，监听 8080 端口...")

while True:
    client, address = server.accept()
    print(f"收到来自 {address} 的连接")

    # 接收数据
    data = client.recv(1024)
    print(f"收到数据: {data}")

    # 发送响应
    client.send(b"Hello from server!")

    client.close()
```

**测试：**

```bash
python server2.py
nc localhost 8080
# 随便输入文字，会收到服务器响应
```

---

## 任务 3：用 nc 手动发 HTTP 请求

这是关键一步！先运行服务器，然后用 nc 发送原始 HTTP 请求：

```bash
python server2.py &
nc localhost 8080
```

输入以下内容（注意换行）：

```
GET /hello HTTP/1.1
Host: localhost

```

你会看到服务器打印出原始请求内容。

---

## 阶段成果检查

- [ ] 能运行服务器
- [ ] 能用 nc 连接
- [ ] 能看到接收到的数据
- [ ] 用 nc 发送了 HTTP 请求格式的数据

---

## 常见问题

**Q: `Address already in use` 怎么办？**

端口被占用，等一会再试，或换端口：

```python
server.bind(('localhost', 8081))  # 换端口
```

**Q: 程序卡住了？**

`server.accept()` 和 `client.recv()` 都是阻塞的，这是正常的。

**Q: `nc` 找不到？**

Windows 可以用 PowerShell 测试，或者安装 [Git Bash](https://git-scm.com/downloads)（自带 nc）。

---

## 下一步

下一阶段我们解析 HTTP 请求，把 `GET /hello HTTP/1.1` 这样的字符串拆解成有用信息。
