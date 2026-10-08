"""在当前工作目录执行 Bash 命令。"""

import subprocess
from dataclasses import dataclass

TOOL = {"type": "function", "function": {
    "name": "bash", "description": "在当前工作目录执行 Bash 命令，返回 stdout、stderr 和退出码。每次调用独立运行，cd 不会影响下一次调用。",
    "parameters": {"type": "object", "properties": {
        "command": {"type": "string", "description": "要执行的 Bash 命令"}},
        "required": ["command"], "additionalProperties": False},
}}


@dataclass
class BashResult:
    stdout: str
    stderr: str
    returncode: int


def execute(command: str, timeout: float = 30) -> BashResult:
    if not isinstance(command, str) or not command.strip():
        raise ValueError("command 必须是非空字符串。")
    result = subprocess.run(["bash", "-c", command], stdin=subprocess.DEVNULL,
                            capture_output=True, text=True, encoding="utf-8",
                            errors="replace", timeout=timeout)
    return BashResult(result.stdout, result.stderr, result.returncode)
