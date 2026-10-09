"""按请求 ID 记录调用过程；认证密钥不写入日志。"""

import json
from datetime import datetime
from enum import Enum
from config import ROOT


class LogEvent(str, Enum):
    """统一定义日志事件，调用时使用枚举成员，避免手写字符串。"""

    INPUT_RECEIVED = "INPUT_RECEIVED"  # 已收到用户输入，开始处理本次请求。
    ROUND_STARTED = "ROUND_STARTED"  # 开始一轮 Agent 循环，每轮调用一次模型。
    MODEL_REQUEST = "MODEL_REQUEST"  # 记录即将发送给模型的请求内容。
    MODEL_RESPONSE_WAITING = "MODEL_RESPONSE_WAITING"  # 模型请求已发送，等待响应。
    MODEL_RESPONSE = "MODEL_RESPONSE"  # 已收到模型接口响应，记录状态码和响应内容。
    TOOL_STARTED = "TOOL_STARTED"  # 开始处理模型发起的工具调用。
    TOOL_RESULT = "TOOL_RESULT"  # 记录工具执行结果或错误，随后交给模型继续处理。
    RESULT_FAILED = "RESULT_FAILED"  # 本次用户请求处理失败，记录错误类型和耗时。
    RESULT_RETURNED = "RESULT_RETURNED"  # 最终回答已输出给用户，记录回答和耗时。


def log_event(request_id: str, event: LogEvent, details: object = "", module: str = "agent") -> None:
    """追加一条事件日志；字典等结构自动格式化为易读的 JSON。"""
    path = ROOT / "logs" / "app.log"
    # 首次运行时自动创建 logs；目录已存在也不会报错。
    path.parent.mkdir(parents=True, exist_ok=True)
    # ensure_ascii=False 保留中文，indent=2 让多层数据更容易阅读。
    text = details if isinstance(details, str) else json.dumps(details, ensure_ascii=False, indent=2)
    timestamp = datetime.now().isoformat(timespec="milliseconds")
    # a 表示追加而非覆盖；with 会在写完后自动关闭文件。
    with path.open("a", encoding="utf-8") as file:
        # 使用 value 写入原始事件名，日志中不会出现 LogEvent.MODEL_REQUEST 等前缀。
        file.write(f"{timestamp} | {request_id} | {module} | {event.value}\n{text}\n\n")
