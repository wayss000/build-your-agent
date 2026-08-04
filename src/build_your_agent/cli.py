"""Build Your Agent 的命令行入口。"""

from __future__ import annotations

import argparse
from collections.abc import Sequence
import sys

from . import __version__


def build_parser() -> argparse.ArgumentParser:
    """创建 CLI 参数解析器，让参数定义与程序入口可以分别测试。"""

    parser = argparse.ArgumentParser(
        prog="build-your-agent",
        description="从最小 CLI 开始，逐步构建自己的 AI Agent。",
        add_help=False,
    )
    parser.add_argument(
        "-h",
        "--help",
        action="help",
        help="显示帮助信息并退出",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
        help="显示当前版本号并退出",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """解析命令行参数；无参数时展示帮助信息。"""

    parser = build_parser()
    arguments = list(argv) if argv is not None else sys.argv[1:]

    if arguments == []:
        parser.print_help()
        return 0

    parser.parse_args(arguments)
    return 0
