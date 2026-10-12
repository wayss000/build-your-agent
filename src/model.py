"""使用标准库调用兼容 Chat Completions 的 HTTPS 接口。"""

import http.client
import json
from urllib.parse import urlsplit


def call_model(messages: list[dict], request_id: str, tools: list[dict], config: dict) -> dict:
    """发送一次非流式请求，返回响应中的 assistant 消息。"""
    # 拆开主机、端口与路径，供标准库 HTTPSConnection 使用。
    url = urlsplit(config["MODEL_URL"])
    # tools 只是工具说明，模型不会执行 Python 代码；实际执行发生在 agent.py。
    payload = {"model": config["MODEL_NAME"], "messages": messages,
               "temperature": config["MODEL_TEMPERATURE"]}
    if tools:
        payload["tools"] = tools
    # 网络调用设置超时，避免连接或读取长期阻塞终端。
    connection = http.client.HTTPSConnection(url.hostname, url.port, timeout=60)
    try:
        path = url.path or "/"
        if url.query:
            path += "?" + url.query
        # 请求体先转成 JSON 再编码成字节；密钥放在认证头中。
        connection.request("POST", path, body=json.dumps(payload).encode("utf-8"), headers={
            "Authorization": f"Bearer {config['NEW_API_KEY']}",
            "Content-Type": "application/json",
        })
        # request 返回仅表示请求已发送；此处等待响应并读取完整内容。
        response = connection.getresponse()
        raw = response.read().decode("utf-8", errors="replace")
        # 响应保留用于排障，但不记录服务端可能回显的认证密钥。
        raw = raw.replace(config["NEW_API_KEY"], "[REDACTED]")
        # HTTP 成功状态码为 2xx；失败响应已记录，终端只显示简明提示。
        if not 200 <= response.status < 300:
            raise ValueError(f"模型接口返回 HTTP {response.status}。")
        try:
            # Chat Completions 的回复位于 choices 列表的第一项中。
            message = json.loads(raw)["choices"][0]["message"]
            if not isinstance(message, dict) or message.get("role") != "assistant":
                raise ValueError
            return message
        except (ValueError, KeyError, IndexError, TypeError):
            raise ValueError("模型响应格式异常。") from None
    # 无论成功还是异常都关闭连接，避免资源泄漏。
    finally:
        connection.close()
