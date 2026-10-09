"""终端交互入口。"""

import argparse
import http.client
from time import perf_counter
from uuid import uuid4
from agent import run_agent
from log_event import LogEvent, log_event


def main(argv: list[str] | None = None) -> int:
    """解析启动参数并持续读取输入；返回 0 表示正常退出。"""
    # argparse 自动提供 --help；argv 为 None 时读取真实命令行参数。
    parser = argparse.ArgumentParser(description="本地 AI Agent：终端对话与 Bash 工具调用")
    parser.add_argument("--version", action="version", version="%(prog)s 0.1.0")
    parser.parse_args(argv)
    print("终端对话已启动，输入 exit 退出。Bash 工具会直接执行模型生成的命令。")
    while True:
        try:
            user_input = input("你：")
            if user_input.strip() == "exit":
                break
            # 空白输入不发送给模型，直接等待下一次输入。
            if not user_input.strip():
                continue
            # 同一次请求的所有日志共用这个 ID，便于从日志中追踪完整过程。
            request_id = uuid4().hex
            # perf_counter 适合计算耗时，不受系统时钟调整影响。
            started = perf_counter()
            log_event(request_id, LogEvent.INPUT_RECEIVED, user_input, "cli")
            try:
                response = run_agent(user_input, request_id)
            # 单次请求失败后保留交互循环；连接异常不向终端输出底层详情。
            except (ValueError, OSError, http.client.HTTPException) as error:
                log_event(request_id, LogEvent.RESULT_FAILED, {
                    "error_type": type(error).__name__,
                    "elapsed_ms": round((perf_counter() - started) * 1000, 3)}, "cli")
                text = str(error) if isinstance(error, ValueError) else "模型连接或命令执行失败，请检查运行环境。"
                print(f"错误：{text}", flush=True)
                continue
            print(f"\nAgent：\n{response}\n", flush=True)
            log_event(request_id, LogEvent.RESULT_RETURNED, {
                "elapsed_ms": round((perf_counter() - started) * 1000, 3),
                "response": response}, "cli")
        # Ctrl+D 产生 EOFError，Ctrl+C 产生 KeyboardInterrupt，均正常退出。
        except (EOFError, KeyboardInterrupt):
            break
    print("\n再见！", flush=True)
    return 0
