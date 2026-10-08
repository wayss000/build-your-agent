"""读取简单的 .env 配置，环境变量优先。"""

import os
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]


def load_config() -> dict:
    values = {"MODEL_TEMPERATURE": "0.7", "AGENT_MAX_ROUNDS": "5"}
    path = ROOT / ".env"
    if path.exists():
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                raise ValueError(f".env 第 {number} 行需要使用 KEY=VALUE 格式。")
            key, value = line.split("=", 1)
            values[key.strip()] = value.strip().strip("\"'")
    for key in ("NEW_API_KEY", "MODEL_URL", "MODEL_NAME", "MODEL_TEMPERATURE", "AGENT_MAX_ROUNDS"):
        if key in os.environ:
            values[key] = os.environ[key]
    for key in ("NEW_API_KEY", "MODEL_URL", "MODEL_NAME"):
        if not values.get(key):
            raise ValueError(f"请在 .env 或环境变量中配置 {key}。")
    url = urlsplit(values["MODEL_URL"])
    if url.scheme != "https" or not url.hostname or url.username or url.password or url.fragment:
        raise ValueError("MODEL_URL 必须是完整的 HTTPS 接口地址。")
    try:
        values["MODEL_TEMPERATURE"] = float(values["MODEL_TEMPERATURE"])
        values["AGENT_MAX_ROUNDS"] = int(values["AGENT_MAX_ROUNDS"])
    except ValueError:
        raise ValueError("MODEL_TEMPERATURE 必须是数字，AGENT_MAX_ROUNDS 必须是整数。") from None
    if values["AGENT_MAX_ROUNDS"] < 1:
        raise ValueError("AGENT_MAX_ROUNDS 必须大于零。")
    return values
