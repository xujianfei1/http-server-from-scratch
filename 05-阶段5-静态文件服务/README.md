# 阶段 5：静态文件服务

## 学习目标

- 读取文件并返回
- 识别文件类型（MIME）
- 防止路径遍历漏洞

---

## 什么是静态文件服务？

让服务器托管真实文件：

```
/index.html    → 读取 ./public/index.html
/style.css     → 读取 ./public/style.css
/script.js     → 读取 ./public/script.js
/image.png     → 读取 ./public/image.png
```

---

## 任务 1：基础文件读取

```python
import os

def serve_static_file(client_socket, path):
    """返回静态文件"""

    # 移除开头的 /
    file_path = path.lstrip('/')

    # 安全检查：防止路径遍历
    # 攻击者可能访问 /../../../etc/passwd
    if '..' in file_path:
        send_404(client_socket)
        return

    # 默认文件
    if file_path == '':
        file_path = 'index.html'

    # 读取文件
    full_path = os.path.join('public', file_path)

    try:
        with open(full_path, 'rb') as f:
            content = f.read()

        # 根据扩展名判断 MIME 类型
        content_type = get_mime_type(full_path)

        # 发送响应
        response_line = "HTTP/1.1 200 OK\r\n"
        response_headers = f"Content-Type: {content_type}\r\n"
        response_headers += f"Content-Length: {len(content)}\r\n"
        response_headers += "\r\n"

        response = response_line.encode() + response_headers.encode() + content
        client_socket.send(response)

    except FileNotFoundError:
        send_404(client_socket)
```

---

## 任务 2：MIME 类型表

```python
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
    '.pdf': 'application/pdf',
    '.txt': 'text/plain',
}

def get_mime_type(file_path):
    """根据扩展名获取 MIME 类型"""
    ext = os.path.splitext(file_path)[1].lower()
    return MIME_TYPES.get(ext, 'application/octet-stream')
```

---

## 任务 3：创建静态文件目录

先创建测试文件：

```bash
mkdir public
```

创建 `public/index.html`：

```html
<!DOCTYPE html>
<html>
<head>
    <title>我的静态网站</title>
    <link rel="stylesheet" href="/style.css">
</head>
<body>
    <h1>欢迎！</h1>
    <p>这是我的第一个静态网站</p>
    <img src="/image.png" alt="示例图片">
    <script src="/script.js"></script>
</body>
</html>
```

创建 `public/style.css`：

```css
body {
    font-family: Arial, sans-serif;
    max-width: 800px;
    margin: 50px auto;
    padding: 20px;
}
h1 { color: #333; }
```

创建 `public/script.js`：

```javascript
console.log("Hello from static file!");
alert("页面加载完成！");
```

---

## 重要：路径安全

**路径遍历攻击**：

攻击者访问：`/../../../etc/passwd`

```python
# 危险！
full_path = '/public/' + path

# 安全做法：realpath 检查
full_path = os.path.realpath(os.path.join('public', path))
if not full_path.startswith(os.path.realpath('public')):
    # 有人试图跳出目录
    return 403 Forbidden
```

---

## 阶段成果检查

- [ ] 能返回 HTML、CSS、JS 文件
- [ ] 能返回图片
- [ ] 不存在的文件返回 404
- [ ] 防止了路径遍历漏洞
- [ ] 创建了 `public/` 目录放测试文件

---

## 扩展挑战

尝试实现：

1. **目录列表** — 访问 `/files/` 时列出目录下所有文件
2. **缓存** — 读取一次后缓存到内存
3. **压缩** — 返回 gzip 压缩的内容

---

## 下一步

下一阶段加入并发支持，让服务器能同时处理多个请求。
