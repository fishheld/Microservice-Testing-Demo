from mitmproxy import http
import json
from datetime import datetime

class RecordTraffic:
    def __init__(self):
        # 定义日志文件路径
        self.logfile_path = "/home/mitmproxy/filter-oap.txt"
        # 打开文件流，以追加模式打开
        self.logfile = open(self.logfile_path, "a")

    def get_timestamp(self):
        # 获取当前时间的ISO 8601格式字符串
        return datetime.now().isoformat()

    def request(self, flow: http.HTTPFlow) -> None:
        # 检查请求是否是发送到oap-server的
        if "oap-server" not in flow.request.pretty_host:
            # 记录更多请求信息，包括时间戳
            request_info = {
                "timestamp": self.get_timestamp(),
                "method": flow.request.method,
                "url": flow.request.url,
                "http_version": flow.request.http_version,
                "headers": dict(flow.request.headers)
            }
            self.logfile.write(f"Request: {json.dumps(request_info, indent=2)}\n\n")
            # 确保实时写入到文件中
            self.logfile.flush()

    def response(self, flow: http.HTTPFlow) -> None:
        # 与请求检查相同，确保响应不是来自oap-server
        if "oap-server" not in flow.request.pretty_host:
            # 记录更多响应信息，包括时间戳
            response_info = {
                "timestamp": self.get_timestamp(),
                "status_code": flow.response.status_code,
                "reason": flow.response.reason,
                "http_version": flow.response.http_version,
                "headers": dict(flow.response.headers)
            }
            self.logfile.write(f"Response: {json.dumps(response_info, indent=2)}\n\n")
            # 确保实时写入到文件中
            self.logfile.flush()

    def done(self):
        # 当mitmproxy退出时关闭文件流
        self.logfile.close()

# 注册addon
addons = [
    RecordTraffic()
]
