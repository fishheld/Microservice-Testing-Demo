import json
from datetime import datetime
from mitmproxy import ctx, http

class HARLogger:
    def __init__(self):
        self.har_path = "/home/mitmproxy/output/output.har"

    def request(self, flow: http.HTTPFlow):
        # 如果请求有正文，将正文以适当的方式编码并添加到请求对象中
        if flow.request.method in ["POST", "PUT"] and flow.request.content:
            # 对于非文本内容，需要进行编码处理
            content_type = flow.request.headers.get("Content-Type", "")
            if content_type.startswith("application/x-www-form-urlencoded"):
                # 表单URL编码正文
                flow.request.content = http.urlencode(flow.request.decode_content())
            elif content_type.startswith("multipart/form-data"):
                # 多部分表单正文
                pass  # mitmproxy 会处理好，无需编码
            else:
                # 其他正文类型，如JSON，可以直接使用
                flow.request.content = flow.request.decode_content()

    def response(self, flow: http.HTTPFlow):
        # 创建HAR条目
        entry = {
            "startedDateTime": datetime.fromtimestamp(flow.request.timestamp_start).isoformat() + "Z",
            "time": (flow.response.timestamp_end - flow.request.timestamp_start) * 1000,
            "request": self.create_request_entry(flow),
            "response": self.create_response_entry(flow),
            "cache": {},
            "timings": self.create_timings_entry(flow)
        }

        # 将条目追加到HAR文件
        with open(self.har_path, "a", encoding="utf-8") as f:
            json.dump(entry, f, ensure_ascii=False, indent=2)
            f.write("\n")

    @staticmethod
    def create_request_entry(flow: http.HTTPFlow):
        request_entry = {
            "method": flow.request.method,
            "url": flow.request.pretty_url,
            "httpVersion": flow.request.http_version,
            "cookies": [],
            "headers": [],
            "queryString": [],
            "postData": {},
            "headersSize": -1,
            "bodySize": 0 if flow.request.content is None else len(flow.request.content),
        }

        # 添加请求头
        for name, value in flow.request.headers.items():
            request_entry["headers"].append({
                "name": name,
                "value": value,
            })

        # 添加请求参数
        for name, values in flow.request.query.items():
            for value in values:
                request_entry["queryString"].append({
                    "name": name,
                    "value": value,
                })

        # 添加请求正文
        if flow.request.method in ["POST", "PUT"] and flow.request.content:
            request_entry["postData"] = {
                "mimeType": flow.request.headers.get("Content-Type", ""),
                "text": flow.request.content.decode("utf-8", errors="ignore") if flow.request.content else "",
                "params": []  # 如果需要解析表单数据，可以在这里添加解析逻辑
            }

        return request_entry

    @staticmethod
    def create_response_entry(flow: http.HTTPFlow):
        response_entry = {
            "status": flow.response.status_code,
            "statusText": flow.response.reason,
            "httpVersion": flow.response.http_version,
            "cookies": [],
            "headers": [],
            "content": {
                "size": 0 if flow.response.content is None else len(flow.response.content),
                "mimeType": flow.response.headers.get("Content-Type", ""),
                "text": flow.response.content.decode("utf-8", errors="ignore") if flow.response.content else "",
            },
            "redirectURL": "",
            "headersSize": -1,
            "bodySize": -1,
        }

        # 添加响应头
        for name, value in flow.response.headers.items():
            response_entry["headers"].append({
                "name": name,
                "value": value,
            })

        return response_entry

    @staticmethod
    def create_timings_entry(flow: http.HTTPFlow):
        return {
            "send": 0,
            "wait": flow.response.timestamp_start - flow.request.timestamp_start,
            "receive": flow.response.timestamp_end - flow.response.timestamp_start,
        }

addons = [
    HARLogger()
]