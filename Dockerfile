# 基于官方 Python 镜像
FROM python:3.11-slim

WORKDIR /app

# 安装系统依赖（如需编译某些 Python 包，可在此添加 apt 包）
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖并安装
COPY requirements.txt .
# requirements.txt 引用了 requirements/prod.txt —— 把 requirements/ 目录也一并复制，
# 否则 pip 在解析 -r requirements/prod.txt 时会找不到该文件。
COPY requirements/ ./requirements/

RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1

# 使用仓库中的 autoapp.py 作为 gunicorn 的入口（仓库中没有顶级 app.py）
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "autoapp:app"]
