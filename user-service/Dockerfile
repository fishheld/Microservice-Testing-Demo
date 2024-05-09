FROM apache/skywalking-python:1.0.0-kafka-py3.11-slim

RUN apt update \
    && apt upgrade -y \
    && apt install -y gcc default-libmysqlclient-dev pkg-config \
    && rm -rf /var/lib/apt/lists/*

RUN pip install flask flask_sqlalchemy mysqlclient

COPY . .

EXPOSE 5001

# 设置SkyWalking Agent的环境变量
ENV SW_AGENT_NAME=user-service
ENV SW_AGENT_COLLECTOR_BACKEND_SERVICES=oap-server:11800
ENV SW_PLUGIN_SQL_PARAMETERS_MAX_LENGTH=500

# CMD python ./ui-service.py
# CMD run -p flask --app app run --host=0.0.0.0
CMD ["run", "-p", "flask", "--app", "app", "run", "--host=0.0.0.0", "--port=5001"]