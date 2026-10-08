"""按请求 ID 记录调用过程；认证密钥不写入日志。"""

import json
from datetime import datetime
from config import ROOT


def log_event(request_id: str, event: str, details: object = "", module: str = "agent") -> None:
    path = ROOT / "logs" / "app.log"
    path.parent.mkdir(parents=True, exist_ok=True)
    text = details if isinstance(details, str) else json.dumps(details, ensure_ascii=False, indent=2)
    timestamp = datetime.now().isoformat(timespec="milliseconds")
    with path.open("a", encoding="utf-8") as file:
        file.write(f"{timestamp} | {request_id} | {module} | {event}\n{text}\n\n")
