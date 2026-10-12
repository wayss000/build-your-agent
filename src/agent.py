"""一次模型请求，执行其工具调用；下一章才把结果回传模型。"""
import json
import subprocess
from dataclasses import asdict
from config import load_config
from model import call_model
from log_event import LogEvent, log_event
from tools.bash_tool import TOOL, execute


def run_agent(user_input: str, request_id: str) -> str:
    messages = [{"role": "user", "content": user_input}]
    message = call_model(messages, request_id, [TOOL], load_config())
    calls = message.get("tool_calls") or []
    if not isinstance(calls, list):
        raise ValueError("工具调用格式异常。")
    if not calls:
        content = message.get("content")
        if not isinstance(content, str):
            raise ValueError("模型没有返回文本。")
        return content
    results = []
    for call in calls:
        try:
            function = call["function"]
            if function["name"] != "bash":
                raise ValueError("未知工具。")
            arguments = json.loads(function["arguments"])
            if not isinstance(arguments, dict):
                raise ValueError("工具参数必须是对象。")
            log_event(request_id, LogEvent.TOOL_STARTED, arguments, "bash")
            output = asdict(execute(arguments["command"]))
        except subprocess.TimeoutExpired:
            output = {"error": "命令执行超过 30 秒。"}
        except (ValueError, KeyError, TypeError, OSError) as error:
            output = {"error": str(error)}
        log_event(request_id, LogEvent.TOOL_RESULT, output, "bash")
        results.append(output)
    # 直接显示结果，尚未让模型理解工具输出。
    return json.dumps(results, ensure_ascii=False, indent=2)
