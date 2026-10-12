# Build Your Agent：循序渐进的教学分支

面向新手，从终端程序逐步写出自己的 Agent。本分支只开发到 P09。

## 选择版本

- main：现有完整实现。
- study_step：按课程顺序开发，每个代码章节完成后打 tag。
- 原理课没有独立 tag；P00、P02 可使用 study-p01。
- P10 实践可使用 study-p09；后续 Skill、记忆暂不实现。

| 章节 | tag | 能力 |
| --- | --- | --- |
| P01 环境准备 | `study-p01` | 环境准备 |
| P03 开发 CLI | `study-p03` | 开发 CLI |
| P04 调用模型 | `study-p04` | 调用模型 |
| P05 模型配置 | `study-p05` | 模型配置 |
| P06 日志 | `study-p06` | 日志 |
| P07 Bash 工具 | `study-p07` | Bash 工具 |
| P08 模型调用工具 | `study-p08` | 模型调用工具 |
| P09 Agent 循环 | `study-p09` | Agent 循环 |

当前阶段：P09 Agent 循环。

## 跟随课程

```bash
git clone https://github.com/wayss000/build-your-agent.git
cd build-your-agent
git fetch origin --tags
git switch --detach study-p09
# 想修改本课代码，创建自己的练习分支
git switch -c my-lesson
```

切换章节前先提交自己的修改。tag 是固定快照；`git switch study_step` 查看教学最新版。
Python 需要 3.10+；P07 起需要 Bash，Windows 建议使用 WSL。

## 运行

```bash
python3 src/main.py
```

输入 `exit` 或按 Ctrl+C / Ctrl+D 退出。

先复制 `.env.example` 为 `.env`，填写密钥、完整 HTTPS 接口地址和模型名称。
环境变量优先于文件；不提交 `.env`，接口调用可能产生费用。

日志追加到 `logs/app.log`，使用请求 ID 追踪；日志包含对话和命令输出，分享前检查敏感内容。

Bash 直接执行命令，没有沙箱，仅在可信本地环境练习；默认超时 30 秒。
每次命令独立启动，`cd` 不影响下一次调用。

工具结果回传模型继续处理，默认最多调用模型 5 轮；每次输入仍使用独立上下文。

[教程目录](docs/user_docs/README.md) · [课程章节目录](docs/user_docs/课程章节目录.md)
