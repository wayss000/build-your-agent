#!/usr/bin/env bash

# 任一步骤失败就退出，避免拉取失败后继续启动旧代码。
set -euo pipefail

# 切换到脚本所在的仓库目录，支持从其他目录调用此脚本。
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd -- "$SCRIPT_DIR"

# 拉取当前分支的更新；仅允许快进，分支分叉时交由用户处理。
git pull --ff-only

# 使用当前 Python 环境运行程序，可先在终端激活本地虚拟环境。
# exec 让程序直接接收 Ctrl+C 等信号，并保留程序退出码。
exec python src/main.py
