"""按请求 ID 记录调用过程；认证密钥不写入日志。"""

import json
from datetime import datetime
from config import ROOT


def log_event(request_id: str, event: str, details: object = "", module: str = "agent") -> None:
    """追加一条事件日志；字典等结构自动格式化为易读的 JSON。"""
    path = ROOT / "logs" / "app.log"
    # 首次运行时自动创建 logs；目录已存在也不会报错。
    path.parent.mkdir(parents=True, exist_ok=True)
    # ensure_ascii=False 保留中文，indent=2 让多层数据更容易阅读。
    text = details if isinstance(details, str) else json.dumps(details, ensure_ascii=False, indent=2)
    timestamp = datetime.now().isoformat(timespec="milliseconds")
    # a 表示追加而非覆盖；with 会在写完后自动关闭文件。
    with path.open("a", encoding="utf-8") as file:
        file.write(f"{timestamp} | {request_id} | {module} | {event}\n{text}\n\n")
