"""终端负责输入输出，处理逻辑独立放在 reply 中。"""
import http.client
from model import call_model
from config import load_config


def reply(user_input: str, request_id: str = "") -> str:
    """处理一次输入；后续章节逐步替换回显逻辑。"""
    message = call_model([{"role": "user", "content": user_input}], request_id, [], load_config())
    content = message.get("content")
    if not isinstance(content, str):
        raise ValueError("模型没有返回文本回复。")
    return content


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
            try:
                response = reply(user_input, request_id)
            except (ValueError, OSError, http.client.HTTPException) as error:
                text = str(error) if isinstance(error, ValueError) else "连接或执行失败，请检查运行环境。"
                print(f"错误：{text}")
                continue
            print(f"Agent：{response}")
        except (EOFError, KeyboardInterrupt):
            break
    print("\n再见！")
    return 0
