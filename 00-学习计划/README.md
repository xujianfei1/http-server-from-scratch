# 学习计划 — 从零构建 HTTP Server

## 阶段总览

| 阶段 | 内容 | 核心技能 | 预计时间 |
|------|------|----------|----------|
| 0 | 环境准备 | Python 基础语法 | 0.5 天 |
| 1 | TCP Socket 基础 | 网络编程、socket 监听 | 1 天 |
| 2 | HTTP 请求解析 | 协议解析、字符串处理 | 1 天 |
| 3 | HTTP 响应 | 状态码、Header、Body | 1 天 |
| 4 | 路由系统 | 字典映射、请求分发 | 1 天 |
| 5 | 静态文件服务 | 文件 I/O、MIME 类型 | 1 天 |
| 6 | 并发支持 | 多线程、并发与阻塞 | 1-2 天 |
| 7 | 美化与扩展 | 日志、错误处理、配置化 | 0.5 天 |
| 8 | 发布到 GitHub | Git 操作、README 编写 | 0.5 天 |

**总计：约 8-10 天**

---

## 每日目标

### 阶段 0：环境准备
- [ ] 安装 Python 3.10+
- [ ] 验证安装：`python --version`
- [ ] 了解基础语法：变量、函数、import、with 语句

### 阶段 1：TCP Socket 基础
- [ ] 用 `socket` 模块监听端口
- [ ] 用 `telnet` 或 `nc` 连接服务器
- [ ] 手动发送数据，理解"连接"本质

### 阶段 2：HTTP 请求解析
- [ ] 接收并打印浏览器请求
- [ ] 解析请求行：`GET /hello HTTP/1.1`
- [ ] 解析请求头：`Host: localhost`
- [ ] 看到真实的 HTTP 长什么样

### 阶段 3：HTTP 响应
- [ ] 返回 `200 OK` + HTML 页面
- [ ] 返回 `404 Not Found`
- [ ] 设置 `Content-Type`、`Content-Length`
- [ ] 浏览器能显示你写的页面

### 阶段 4：路由系统
- [ ] `GET /` → 首页
- [ ] `GET /hello` → 返回 "Hello!"
- [ ] `GET /time` → 返回当前时间
- [ ] 其他路径 → 404

### 阶段 5：静态文件服务
- [ ] `GET /index.html` → 读取并返回文件
- [ ] 支持 CSS/JS/图片
- [ ] 能跑一个真实静态网站

### 阶段 6：并发支持
- [ ] 用 `threading` 处理多连接
- [ ] 理解"阻塞"和"并发"的区别
- [ ] 多浏览器标签同时访问

### 阶段 7：美化与扩展
- [ ] 请求日志（打印来访路径）
- [ ] 错误页面定制
- [ ] 端口/目录可配置

### 阶段 8：发布到 GitHub
- [ ] Git 初始化
- [ ] 写 README
- [ ] 提交并推送

---

## 学习原则

1. **不要抄代码** — 先自己试，碰到问题再查
2. **多用 nc/telnet 测试** — 手动发请求，深刻理解 HTTP
3. **每阶段都 commit** — 记录学习过程
4. **不懂就问** — 查 Google/ChatGPT，问老师

---

## 参考资源

- [Python Socket 官方文档](https://docs.python.org/3/library/socket.html)
- [HTTP 协议 rfc2616](https://www.rfc-editor.org/rfc/rfc2616)
- [Codecrafters HTTP Server 教程](https://github.com/codecrafters-io/build-your-own-http-server)
