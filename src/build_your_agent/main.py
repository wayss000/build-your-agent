"""第 1 章：一个最小可运行的终端对话程序。"""

import logging


logger = logging.getLogger(__name__)


def main() -> None:
    """持续读取终端输入，并把输入内容返回给用户。"""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    print("终端对话已启动，输入 exit 退出。")

    while True:
        try:
            user_input = input("你：")
        except (EOFError, KeyboardInterrupt):
            print("\n再见！")
            break

        if user_input == "exit":
            print("再见！")
            break

        # 先记录后台日志，再把用户的输入回显到终端。
        logger.info("收到用户输入：%s", user_input)
        print(f"你刚才输入的是：{user_input}")


if __name__ == "__main__":
    main()
