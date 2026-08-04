"""CLI 最小入口的测试。"""

from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def run_cli(*arguments: str) -> subprocess.CompletedProcess[str]:
    """从源码运行 CLI，验证用户实际使用的模块入口。"""

    environment = os.environ.copy()
    source_path = str(PROJECT_ROOT / "src")
    existing_path = environment.get("PYTHONPATH")
    environment["PYTHONPATH"] = (
        f"{source_path}{os.pathsep}{existing_path}" if existing_path else source_path
    )
    return subprocess.run(
        [sys.executable, "-m", "build_your_agent", *arguments],
        cwd=PROJECT_ROOT,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )


class CliTest(unittest.TestCase):
    """验证帮助、版本和默认行为。"""

    def test_help(self) -> None:
        result = run_cli("--help")

        self.assertEqual(result.returncode, 0)
        self.assertIn("usage: build-your-agent", result.stdout)
        self.assertIn("--version", result.stdout)

    def test_version(self) -> None:
        result = run_cli("--version")

        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.strip(), "build-your-agent 0.1.0")

    def test_no_arguments_shows_help(self) -> None:
        result = run_cli()

        self.assertEqual(result.returncode, 0)
        self.assertIn("usage: build-your-agent", result.stdout)


if __name__ == "__main__":
    unittest.main()
