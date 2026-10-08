"""读取简单的 .env 配置，环境变量优先。"""

import os
from pathlib import Path
from urllib.parse import urlsplit

# __file__ 是当前文件路径；src 的上一级就是项目根目录。
ROOT = Path(__file__).resolve().parents[1]


def load_config() -> dict:
    """合并默认值、.env 和环境变量，再校验并转换配置类型。"""
    # 覆盖顺序：默认值 < .env < 环境变量。文件缺失时也可只用环境变量。
    values = {"MODEL_TEMPERATURE": "0.7", "AGENT_MAX_ROUNDS": "5"}
    path = ROOT / ".env"
    if path.exists():
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                raise ValueError(f".env 第 {number} 行需要使用 KEY=VALUE 格式。")
            # 只按第一个等号分割，允许配置值本身含有等号。
            key, value = line.split("=", 1)
            values[key.strip()] = value.strip().strip("\"'")
    # 仅覆盖程序支持的配置项，不把整个系统环境混入配置。
    for key in ("NEW_API_KEY", "MODEL_URL", "MODEL_NAME", "MODEL_TEMPERATURE", "AGENT_MAX_ROUNDS"):
        if key in os.environ:
            values[key] = os.environ[key]
    for key in ("NEW_API_KEY", "MODEL_URL", "MODEL_NAME"):
        if not values.get(key):
            raise ValueError(f"请在 .env 或环境变量中配置 {key}。")
    # URL 需要包含完整接口路径；这里仅允许 HTTPS，并排除嵌入式账号密码。
    url = urlsplit(values["MODEL_URL"])
    if url.scheme != "https" or not url.hostname or url.username or url.password or url.fragment:
        raise ValueError("MODEL_URL 必须是完整的 HTTPS 接口地址。")
    # 文件和环境变量读出的都是字符串，使用前转换为浮点数和整数。
    try:
        values["MODEL_TEMPERATURE"] = float(values["MODEL_TEMPERATURE"])
        values["AGENT_MAX_ROUNDS"] = int(values["AGENT_MAX_ROUNDS"])
    except ValueError:
        raise ValueError("MODEL_TEMPERATURE 必须是数字，AGENT_MAX_ROUNDS 必须是整数。") from None
    if values["AGENT_MAX_ROUNDS"] < 1:
        raise ValueError("AGENT_MAX_ROUNDS 必须大于零。")
    return values
