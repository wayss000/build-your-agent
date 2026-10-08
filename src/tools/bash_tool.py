"""在当前工作目录执行 Bash 命令。"""

import subprocess
from dataclasses import dataclass

# 按模型接口约定描述工具名称、用途和参数，供模型生成工具调用。
# required 要求提供 command；additionalProperties 禁止生成额外参数。
TOOL = {"type": "function", "function": {
    "name": "bash", "description": "在当前工作目录执行 Bash 命令，返回 stdout、stderr 和退出码。每次调用独立运行，cd 不会影响下一次调用。",
    "parameters": {"type": "object", "properties": {
        "command": {"type": "string", "description": "要执行的 Bash 命令"}},
        "required": ["command"], "additionalProperties": False},
}}


@dataclass
class BashResult:
    """数据类自动生成初始化方法，统一保存命令执行的三个结果字段。"""

    # stdout 为正常输出，stderr 为错误输出，returncode 通常为 0 表示成功。
    stdout: str
    stderr: str
    returncode: int


def execute(command: str, timeout: float = 30) -> BashResult:
    """执行命令并捕获输出；超时异常由 Agent 处理。"""
    if not isinstance(command, str) or not command.strip():
        raise ValueError("command 必须是非空字符串。")
    # bash -c 支持管道等 shell 语法；每次都是新进程，cd 不影响下次调用。
    # DEVNULL 关闭子进程输入，避免它抢占 CLI；capture_output 捕获两种输出。
    # text/encoding 将输出解码成字符串，errors=replace 替换无法解码的字节。
    # timeout 限制等待时间；不使用 check=True，以便将非零退出码回传给模型。
    result = subprocess.run(["bash", "-c", command], stdin=subprocess.DEVNULL,
                            capture_output=True, text=True, encoding="utf-8",
                            errors="replace", timeout=timeout)
    return BashResult(result.stdout, result.stderr, result.returncode)
