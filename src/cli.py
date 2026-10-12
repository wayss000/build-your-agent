"""终端负责输入输出，处理逻辑独立放在 reply 中。"""
import http.client
from model import call_model
from config import load_config
from time import perf_counter
from uuid import uuid4
from log_event import LogEvent, log_event
from agent import run_agent


def reply(user_input: str, request_id: str = "") -> str:
    """处理一次输入；后续章节逐步替换回显逻辑。"""
    return run_agent(user_input, request_id)


def main() -> int:
    print("终端对话已启动，输入 exit 退出。")
    while True:
        try:
            user_input = input("你：")
            if user_input.strip() == "exit":
                break
            if not user_input.strip():
                continue
            request_id = uuid4().hex
            started = perf_counter()
            log_event(request_id, LogEvent.INPUT_RECEIVED, user_input, "cli")
            try:
                response = reply(user_input, request_id)
            except (ValueError, OSError, http.client.HTTPException) as error:
                log_event(request_id, LogEvent.RESULT_FAILED, {
                    "error_type": type(error).__name__,
                    "elapsed_ms": round((perf_counter() - started) * 1000, 3)}, "cli")
                text = str(error) if isinstance(error, ValueError) else "连接或执行失败，请检查运行环境。"
                print(f"错误：{text}")
                continue
            print(f"Agent：{response}")
            log_event(request_id, LogEvent.RESULT_RETURNED, {
                "response": response,
                "elapsed_ms": round((perf_counter() - started) * 1000, 3)}, "cli")
        except (EOFError, KeyboardInterrupt):
            break
    print("\n再见！")
    return 0
