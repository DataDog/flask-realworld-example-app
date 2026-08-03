# 基于官方 Python 镜像
FROM python:3.11-slim

WORKDIR /app

# 安装系统依赖（如需编译某些 Python 包，可在此添加 apt 包）
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖并安装
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1

# 监听 8080（Cloud Run / 容器友好端口），注意：按项目实际 app 对象调整 app:app
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
