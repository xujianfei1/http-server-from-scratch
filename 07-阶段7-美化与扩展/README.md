# 阶段 7：美化与扩展

## 学习目标

- 添加请求日志
- 错误处理
- 配置化管理
- 代码重构

---

## 任务 1：请求日志

记录每个请求的访问时间、路径、状态码：

```python
import datetime

def log_request(address, method, path, status):
    """记录请求日志"""
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] {address} {method} {path} -> {status}")

# 使用
log_request("127.0.0.1", "GET", "/hello", 200)
# 输出: [2024-01-15 10:30:45] 127.0.0.1 GET /hello -> 200
```

---

## 任务 2：错误处理

让服务器不崩溃：

```python
def handle_request(client_socket):
    try:
        request = client_socket.recv(4096)

        if not request:  # 空请求
            return

        # 解析并响应...

    except Exception as e:
        print(f"处理请求出错: {e}")
        send_500(client_socket)
    finally:
        try:
            client_socket.close()
        except:
            pass
```

---

## 任务 3：配置文件

把端口、目录等做成可配置的：

创建 `config.py`：

```python
import json

with open('config.json', 'r') as f:
    CONFIG = json.load(f)
```

创建 `config.json`：

```json
{
    "host": "localhost",
    "port": 8080,
    "public_dir": "public",
    "max_connections": 10,
    "log_enabled": true
}
```

---

## 任务 4：模块化重构

整理代码结构：

```
server/
├── server.py          # 主入口
├── config.py          # 配置
├── router.py          # 路由逻辑
├── handlers.py        # 请求处理函数
├── static.py          # 静态文件服务
├── utils.py           # 工具函数
├── public/            # 静态文件目录
└── config.json        # 配置文件
```

---

## 阶段成果检查

- [ ] 每个请求打印日志
- [ ] 错误不会让服务器崩溃
- [ ] 端口和目录可配置
- [ ] 代码结构清晰

---

## 扩展挑战

尝试添加这些功能：

1. **Gzip 压缩** — 减少传输大小
2. **连接 Keep-Alive** — 复用 TCP 连接
3. **CORS 头** — 支持跨域请求
4. **Basic 认证** — 简单的密码保护

---

## 下一步

最后一阶段，把代码发布到 GitHub！
