"""支持通过 ``python -m build_your_agent`` 启动命令行。"""

from .cli import main


if __name__ == "__main__":
    raise SystemExit(main())

