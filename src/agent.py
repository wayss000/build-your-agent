"""最小模型—工具—模型循环；每次用户请求使用独立上下文。"""

import json
import subprocess
from dataclasses import asdict
from config import load_config
from log_event import log_event
from model import call_model
from tools.bash_tool import TOOL, execute


def run_agent(user_input: str, request_id: str) -> str:
    config = load_config()
    messages = [
        {"role": "system", "content": "你是一个简洁的本地助手。需要操作本地环境时调用 bash 工具，根据实际执行结果回答。命令在用户当前工作目录执行。"},
        {"role": "user", "content": user_input},
    ]
    for round_number in range(1, config["AGENT_MAX_ROUNDS"] + 1):
        log_event(request_id, "ROUND_STARTED", {"round": round_number})
        message = call_model(messages, request_id, [TOOL], config)
        calls = message.get("tool_calls") or []
        if not isinstance(calls, list):
            raise ValueError("模型返回的工具调用格式异常。")
        if not calls:
            content = message.get("content")
            if not isinstance(content, str):
                raise ValueError("模型没有返回文本回复。")
            return content
        if round_number == config["AGENT_MAX_ROUNDS"]:
            raise ValueError("已达到模型调用轮数上限，请缩小任务后重试。")
        messages.append(message)
        for call in calls:
            if not isinstance(call, dict) or not isinstance(call.get("id"), str):
                raise ValueError("模型返回的工具调用缺少有效 ID。")
            try:
                function = call["function"]
                if function["name"] != "bash":
                    raise ValueError("模型请求了未知工具。")
                arguments = json.loads(function["arguments"])
                command = arguments["command"]
                log_event(request_id, "TOOL_STARTED", {"command": command}, "bash")
                output = asdict(execute(command))
            except subprocess.TimeoutExpired:
                output = {"error": "命令执行超过 30 秒，已停止等待。"}
            except (ValueError, KeyError, TypeError, OSError) as error:
                output = {"error": str(error)}
            log_event(request_id, "TOOL_RESULT", output, "bash")
            messages.append({"role": "tool", "tool_call_id": call["id"],
                             "content": json.dumps(output, ensure_ascii=False)})
    raise ValueError("已达到模型调用轮数上限。")
