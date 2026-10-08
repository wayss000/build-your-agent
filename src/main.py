"""终端 Agent 启动入口。"""

from cli import main

# 直接运行本文件时启动 CLI；被其他模块导入时不会自动进入交互循环。
if __name__ == "__main__":
    # 将 CLI 的返回值作为进程退出码，0 表示正常结束。
    raise SystemExit(main())
