# 阶段 8：发布到 GitHub

## 学习目标

- 初始化 Git 仓库
- 写一个清晰的 README
- 提交并推送到 GitHub

---

## 前置准备

1. 安装 Git：[https://git-scm.com/download/win](https://git-scm.com/download/win)
2. 注册 GitHub 账号：[https://github.com](https://github.com)
3. 生成 SSH Key（可选但推荐）

---

## 步骤 1：初始化仓库

```bash
cd d:/学习/从零构建HTTP-Server
git init
```

---

## 步骤 2：创建 .gitignore

创建 `.gitignore` 文件：

```
# Python
__pycache__/
*.pyc
*.pyo
*.egg-info/
.venv/

# IDE
.vscode/
.idea/

# macOS
.DS_Store

# 服务器运行时
*.log
```

---

## 步骤 3：创建 README.md

项目根目录已有 README.md，可以进一步完善：

```markdown
# HTTP Server from Scratch

用 Python 从零实现一个 HTTP 服务器。

## 功能

- [x] 监听 TCP 端口
- [x] 解析 HTTP 请求
- [x] 返回 HTML/JSON 响应
- [x] 路由系统
- [x] 静态文件服务
- [x] 多线程并发
- [ ] Gzip 压缩
- [ ] Keep-Alive

## 运行

```bash
python server.py
```

然后访问 http://localhost:8080

## 项目结构

```
.
├── server.py       # 主入口
├── router.py       # 路由
├── handlers.py     # 请求处理
├── static.py       # 静态文件
└── public/         # 静态文件目录
```

## 学习记录

本项目是我跟随 [Build Your Own X](https://github.com/codecrafters-io/build-your-own-x) 教程的学习记录。

每个阶段的学习笔记在对应目录中。
```

---

## 步骤 4：提交代码

```bash
# 添加所有文件
git add .

# 提交
git commit -m "feat: 完成 HTTP 服务器核心功能"

# 查看状态
git status
```

---

## 步骤 5：推送到 GitHub

1. 在 GitHub 上创建新仓库：https://github.com/new
   - 仓库名：`http-server-from-scratch`
   - 不要勾选 "Initialize with README"

2. 关联本地仓库：

```bash
git remote add origin https://github.com/你的用户名/http-server-from-scratch.git
git branch -M main
git push -u origin main
```

---

## 步骤 6：验证

访问 `https://github.com/你的用户名/http-server-from-scratch` 查看你的代码。

---

## 阶段成果检查

- [ ] Git 仓库初始化
- [ ] .gitignore 配置
- [ ] README 完善
- [ ] 代码提交
- [ ] 成功推送到 GitHub
- [ ] GitHub 页面正常显示

---

## 恭喜完成！

你从零实现了一个 HTTP Server！核心知识点：

- TCP Socket 编程
- HTTP 协议
- 多线程并发
- 文件 I/O
- RESTful API 设计

这是计算机基础中非常重要的内容，继续加油！

---

## 后续学习建议

1. 继续挑战其他项目（如 Build your own Git）
2. 学习 Web 框架（Flask、Django、FastAPI）
3. 学习数据库基础
4. 学习操作系统原理
