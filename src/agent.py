"""最小模型—工具—模型循环；每次用户请求使用独立上下文。"""

import json
import subprocess
from dataclasses import asdict
from config import load_config
from log_event import LogEvent, log_event
from model import call_model
from tools.bash_tool import TOOL, execute


def run_agent(user_input: str, request_id: str) -> str:
    """处理一次用户请求，返回最终文本；工具结果只在本次请求中保留。"""
    config = load_config()
    # system 规定助手的行为，user 保存用户的问题。每次请求重新建立上下文。
    messages = [
        {"role": "system", "content": "你是一个简洁的本地助手。需要操作本地环境时调用 bash 工具，根据实际执行结果回答。命令在用户当前工作目录执行。"},
        {"role": "user", "content": user_input},
    ]
    # 一轮代表一次模型请求；执行工具后需要再请求模型，让它理解执行结果。
    for round_number in range(1, config["AGENT_MAX_ROUNDS"] + 1):
        log_event(request_id, LogEvent.ROUND_STARTED, {"round": round_number})
        message = call_model(messages, request_id, [TOOL], config)
        # 模型既可以直接回答，也可以返回 tool_calls，要求程序代它执行工具。
        calls = message.get("tool_calls") or []
        if not isinstance(calls, list):
            raise ValueError("模型返回的工具调用格式异常。")
        # 没有工具调用时，将文本作为最终回答交给 CLI。
        if not calls:
            content = message.get("content")
            if not isinstance(content, str):
                raise ValueError("模型没有返回文本回复。")
            return content
        # 为工具结果预留下一轮模型调用；最后一轮不再执行新命令。
        if round_number == config["AGENT_MAX_ROUNDS"]:
            raise ValueError("已达到模型调用轮数上限，请缩小任务后重试。")
        # 先保存 assistant 的工具调用，再追加对应的 tool 结果，保持消息顺序。
        messages.append(message)
        for call in calls:
            if not isinstance(call, dict) or not isinstance(call.get("id"), str):
                raise ValueError("模型返回的工具调用缺少有效 ID。")
            try:
                function = call["function"]
                if function["name"] != "bash":
                    raise ValueError("模型请求了未知工具。")
                # arguments 是 JSON 字符串，需要先解析成字典才能读取 command。
                arguments = json.loads(function["arguments"])
                command = arguments["command"]
                log_event(request_id, LogEvent.TOOL_STARTED, {"command": command}, "bash")
                # asdict 将 BashResult 数据类转换成可序列化的普通字典。
                output = asdict(execute(command))
            # 工具错误也作为结果交给模型，让它解释原因或调整下一步。
            except subprocess.TimeoutExpired:
                output = {"error": "命令执行超过 30 秒，已停止等待。"}
            except (ValueError, KeyError, TypeError, OSError) as error:
                output = {"error": str(error)}
            log_event(request_id, LogEvent.TOOL_RESULT, output, "bash")
            # tool_call_id 把结果与原调用关联；content 按接口要求使用字符串。
            messages.append({"role": "tool", "tool_call_id": call["id"],
                             "content": json.dumps(output, ensure_ascii=False)})
    raise ValueError("已达到模型调用轮数上限。")
