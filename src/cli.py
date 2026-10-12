"""终端负责输入输出，处理逻辑独立放在 reply 中。"""


def reply(user_input: str, request_id: str = "") -> str:
    """处理一次输入；后续章节逐步替换回显逻辑。"""
    return f"hello，你输入的是：{user_input}"


def main() -> int:
    print("终端对话已启动，输入 exit 退出。")
    while True:
        try:
            user_input = input("你：")
            if user_input.strip() == "exit":
                break
            if not user_input.strip():
                continue
            request_id = ""
            response = reply(user_input, request_id)
            print(f"Agent：{response}")
        except (EOFError, KeyboardInterrupt):
            break
    print("\n再见！")
    return 0
