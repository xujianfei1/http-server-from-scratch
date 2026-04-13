# 从零构建 HTTP Server

> 通过手写一个 HTTP 服务器，深入理解 Web 底层原理。

## 项目简介

本项目参考 [build-your-own-x](https://github.com/codecrafters-io/build-your-own-x) 教程，用 Python 从零实现一个 HTTP Server。

## 学习目标

- 理解 TCP/IP 协议栈
- 理解 HTTP 协议本质
- 理解 Web 服务器工作原理
- 掌握 Socket 编程
- 理解并发编程基础

## 目录结构

```
从零构建HTTP-Server/
├── README.md                          # 项目说明
├── 00-学习计划/                        # 整体学习计划
│   └── README.md
├── 01-阶段1-TCP-Socket基础/           # 监听端口、收发数据
├── 02-阶段2-HTTP请求解析/              # 解析请求行、请求头
├── 03-阶段3-HTTP响应/                  # 返回响应
├── 04-阶段4-路由系统/                  # 多端点路由
├── 05-阶段5-静态文件服务/               # 静态文件托管
├── 06-阶段6-并发支持/                  # 多线程并发
├── 07-阶段7-美化与扩展/                # 日志、错误处理
└── 08-发布到GitHub/                    # 上线项目
```

## 学习顺序

建议按阶段顺序学习，每天一个阶段：

1. 阶段1 → 阶段2 → 阶段3（核心三件套）
2. 阶段4 → 阶段5（功能完善）
3. 阶段6 → 阶段7（工程化）
4. 阶段8（收尾）

## 推荐教程

- [Codecrafters HTTP Server (Python)](https://github.com/codecrafters-io/build-your-own-http-server)
- [Python Socket 官方文档](https://docs.python.org/3/library/socket.html)

## 最终效果

```bash
$ python server.py
# 浏览器访问 http://localhost:8080/hello
# 浏览器显示：Hello, World!
```
