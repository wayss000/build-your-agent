"""在终端向用户提问，把回答交回 Agent 循环。"""

# 模型只负责生成问题；真正的终端交互由 execute 完成。
TOOL = {"type": "function", "function": {
    "name": "ask_user", "description": "需要用户补充信息或作出选择时，在终端提问并等待回答。返回用户输入的文本。",
    "parameters": {"type": "object", "properties": {
        "question": {"type": "string", "description": "向用户提出的问题"}},
        "required": ["question"], "additionalProperties": False},
}}


def execute(question: str) -> dict[str, str]:
    """显示问题并等待一行回答；空白回答会提示用户重新输入。"""
    if not isinstance(question, str) or not question.strip():
        raise ValueError("question 必须是非空字符串。")
    print(f"\nAgent 提问：{question.strip()}", flush=True)
    while True:
        # Ctrl+C 和 Ctrl+D 继续向外传递，由 CLI 统一处理退出。
        answer = input("你的回答：").strip()
        if answer:
            return {"answer": answer}
        print("回答不能为空，请重新输入。", flush=True)
