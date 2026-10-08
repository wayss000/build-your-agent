"""使用标准库调用兼容 Chat Completions 的 HTTPS 接口。"""

import http.client
import json
from urllib.parse import urlsplit
from log_event import log_event


def call_model(messages: list[dict], request_id: str, tools: list[dict], config: dict) -> dict:
    url = urlsplit(config["MODEL_URL"])
    payload = {"model": config["MODEL_NAME"], "messages": messages,
               "tools": tools, "temperature": config["MODEL_TEMPERATURE"]}
    log_event(request_id, "MODEL_REQUEST", payload, "model")
    connection = http.client.HTTPSConnection(url.hostname, url.port, timeout=60)
    try:
        path = url.path or "/"
        if url.query:
            path += "?" + url.query
        connection.request("POST", path, body=json.dumps(payload).encode("utf-8"), headers={
            "Authorization": f"Bearer {config['NEW_API_KEY']}",
            "Content-Type": "application/json",
        })
        log_event(request_id, "MODEL_RESPONSE_WAITING", module="model")
        response = connection.getresponse()
        raw = response.read().decode("utf-8", errors="replace")
        # 响应保留用于排障，但不记录服务端可能回显的认证密钥。
        raw = raw.replace(config["NEW_API_KEY"], "[REDACTED]")
        log_event(request_id, "MODEL_RESPONSE", f"HTTP {response.status}\n{raw}", "model")
        if not 200 <= response.status < 300:
            raise ValueError(f"模型接口返回 HTTP {response.status}，详情见 logs/app.log。")
        try:
            message = json.loads(raw)["choices"][0]["message"]
            if not isinstance(message, dict) or message.get("role") != "assistant":
                raise ValueError
            return message
        except (ValueError, KeyError, IndexError, TypeError):
            raise ValueError("模型响应格式异常，详情见 logs/app.log。") from None
    finally:
        connection.close()
