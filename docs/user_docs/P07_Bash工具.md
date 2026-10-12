# P07 Bash工具

> 使用 study-p07：独立工具，尚未接入模型。

## 本章目标

先独立执行命令，理解工具参数与结果。

## 实现步骤

1. 用 TOOL 描述工具名称、用途及 command 参数。
2. 校验非空命令，通过 `bash -c` 执行。
3. 捕获 stdout、stderr、returncode，返回 BashResult。
4. 默认超时 30 秒，关闭子进程输入，每次启动独立进程。

## 运行方式

```bash
PYTHONPATH=src python3 -c "from tools.bash_tool import execute; print(execute('pwd'))"
```

## 验收检查

1. 执行 `pwd` 得到当前目录，退出码为 0。
2. 不存在的命令返回错误输出及非零退出码。

## 本章边界

Bash 直接执行命令，没有沙箱；在可信本地目录练习。cd 不跨调用保留，超时不保证清理所有派生进程。
