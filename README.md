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
| P05 模型配置 | 待发布 | 模型配置 |
| P06 日志 | 待发布 | 日志 |
| P07 Bash 工具 | 待发布 | Bash 工具 |
| P08 模型调用工具 | 待发布 | 模型调用工具 |
| P09 Agent 循环 | 待发布 | Agent 循环 |

当前阶段：P04 调用模型。

## 跟随课程

```bash
git clone https://github.com/wayss000/build-your-agent.git
cd build-your-agent
git fetch origin --tags
git switch --detach study-p04
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

本课使用环境变量 `NEW_API_KEY`、`MODEL_URL`、`MODEL_NAME`；在自己的终端设置，不把密钥提交到 Git。
MODEL_URL 是完整 HTTPS Chat Completions 地址，接口调用可能产生费用。

[教程目录](docs/user_docs/README.md) · [课程章节目录](docs/user_docs/课程章节目录.md)
