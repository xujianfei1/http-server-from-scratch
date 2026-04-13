# 阶段 6：并发支持

## 学习目标

- 理解阻塞 vs 并发
- 用 threading 处理多连接
- 理解线程安全基础

---

## 问题：当前的服务器有什么问题？

当前代码只能**一次处理一个请求**：

```
请求 A ──────→ [服务器] ───→ 响应 A
                          ↑
请求 B ─── (等待中...) ────┘
                          ↑
请求 C ─── (等待中...) ────┘
```

如果 A 耗时很长，B 和 C 都要等着，体验很差。

---

## 解决方案：多线程

每个连接用一个线程处理：

```
请求 A ──→ [线程 1] ──→ 响应 A
请求 B ──→ [线程 2] ──→ 响应 B
请求 C ──→ [线程 3] ──→ 响应 C
```

---

## 任务 1：基础多线程

```python
# server9.py
import socket
import threading

def handle_request(client_socket, address):
    """在新线程中处理请求"""
    print(f"[{address}] 新连接")

    request = client_socket.recv(4096)

    # 解析并响应...
    response = b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nOK"
    client_socket.send(response)

    print(f"[{address}] 处理完成")
    client_socket.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 8080))
    server.listen(5)

    print("服务器启动，支持并发...")

    while True:
        client, address = server.accept()
        # 每收到一个连接，启动一个新线程处理
        thread = threading.Thread(target=handle_request, args=(client, address))
        thread.start()

if __name__ == '__main__':
    main()
```

---

## 任务 2：处理长时间请求

模拟一个耗时操作：

```python
import time

def handle_request(client_socket, address):
    print(f"[{address}] 新连接")

    request = client_socket.recv(4096)
    lines = request.decode('utf-8', errors='replace').split('\r\n')
    method, path, version = lines[0].split(' ')

    # 模拟耗时操作
    if path == '/slow':
        print(f"[{address}] 执行慢操作...")
        time.sleep(5)  # 模拟 5 秒处理时间
        body = "慢操作完成！"
    else:
        body = "快速响应"

    response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(body)}\r\n\r\n{body}"
    client_socket.send(response.encode())

    print(f"[{address}] 处理完成")
    client_socket.close()
```

**测试：**

1. 打开浏览器访问 `/slow`
2. 同时用另一个标签访问 `/fast`
3. 如果是并发的，`/fast` 应该立即返回

---

## 任务 3：线程池（可选）

频繁创建线程有开销，用线程池复用：

```python
from concurrent.futures import ThreadPoolExecutor

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 8080))
    server.listen(5)

    # 最多同时处理 10 个请求
    with ThreadPoolExecutor(max_workers=10) as executor:
        while True:
            client, address = server.accept()
            executor.submit(handle_request, client, address)
```

---

## 常见问题

**Q：多线程会有安全问题吗？**

对于这个简单的服务器，不太会有。但如果你：
- 共享全局变量（如缓存）
- 读写同一个文件

就要注意线程安全。可以用 `threading.Lock()` 保护。

**Q：Windows 上报错？**

确保用 `if __name__ == '__main__':` 包裹主代码，Windows 需要这个。

---

## 阶段成果检查

- [ ] 用 threading 处理多连接
- [ ] 同时访问 /slow 和 /fast，验证并发
- [ ] 理解阻塞和并发的区别

---

## 下一步

下一阶段加入日志、错误处理等工程化功能。
