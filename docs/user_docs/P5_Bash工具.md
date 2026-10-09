# 执行 Bash 工具

> 状态：已实现。

## 本章开发目标

先独立执行命令，理解工具输入与输出，再交给模型调用。

## 实现步骤

1. 阅读 `src/tools/bash_tool.py`，用 `TOOL` 描述名称、用途和 `command` 参数。
2. `execute()` 校验命令为非空字符串，再使用 `bash -c` 执行。
3. 捕获 stdout、stderr 和退出码，放入 `BashResult` 数据类。
4. 默认等待 30 秒，关闭子进程标准输入，避免抢占 CLI。
5. 每次调用启动独立进程；一次调用中的 `cd` 不影响下一次调用。

## 运行方式

独立调用示例：
```bash
PYTHONPATH=src python3 -c "from tools.bash_tool import execute; print(execute('pwd'))"
```

## 验收检查点

1. `pwd` 返回当前目录且退出码为 0。
2. 不存在的命令返回错误输出和非零退出码。

## 本章边界

当前工具直接执行命令，没有沙箱或审批，仅在可信本地环境练习；超时不保证清理所有派生进程。
