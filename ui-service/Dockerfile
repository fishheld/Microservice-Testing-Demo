FROM apache/skywalking-python:1.0.0-kafka-py3.11-slim

COPY . .

RUN pip install flask requests

EXPOSE 5000

# 设置SkyWalking Agent的环境变量
ENV SW_AGENT_NAME=ui-service
ENV SW_AGENT_COLLECTOR_BACKEND_SERVICES=oap-server:11800
ENV SW_PLUGIN_SQL_PARAMETERS_MAX_LENGTH=500

# CMD python ./ui-service.py
# CMD run -p flask --app app run --host=0.0.0.0
CMD ["run", "-p", "flask", "--app", "app", "run", "--host=0.0.0.0"]