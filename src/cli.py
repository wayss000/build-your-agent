"""终端交互入口。"""

import argparse
import http.client
from time import perf_counter
from uuid import uuid4
from agent import run_agent
from log_event import log_event


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="本地 AI Agent：终端对话与 Bash 工具调用")
    parser.add_argument("--version", action="version", version="%(prog)s 0.1.0")
    parser.parse_args(argv)
    print("终端对话已启动，输入 exit 退出。Bash 工具会直接执行模型生成的命令。")
    while True:
        try:
            user_input = input("你：")
            if user_input.strip() == "exit":
                break
            if not user_input.strip():
                continue
            request_id = uuid4().hex
            started = perf_counter()
            log_event(request_id, "INPUT_RECEIVED", user_input, "cli")
            try:
                response = run_agent(user_input, request_id)
            except (ValueError, OSError, http.client.HTTPException) as error:
                log_event(request_id, "RESULT_FAILED", {
                    "error_type": type(error).__name__,
                    "elapsed_ms": round((perf_counter() - started) * 1000, 3)}, "cli")
                text = str(error) if isinstance(error, ValueError) else "模型连接或命令执行失败，请检查运行环境。"
                print(f"错误：{text}", flush=True)
                continue
            print(f"\nAgent：\n{response}\n", flush=True)
            log_event(request_id, "RESULT_RETURNED", {
                "elapsed_ms": round((perf_counter() - started) * 1000, 3),
                "response": response}, "cli")
        except (EOFError, KeyboardInterrupt):
            break
    print("\n再见！", flush=True)
    return 0
