# 本地运行（本仓库示例）

前提：
- 已安装 Docker、docker-compose
- 在仓库根目录

一、用 docker-compose 启动（包含数据库）
docker-compose up --build

服务启动后访问：
http://localhost:8080/

检查健康：
curl http://localhost:8080/health

二、本地 Python 虚拟环境运行（若需要）
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export FLASK_APP=app.py   # 若入口不同请替换
flask run --host=0.0.0.0 --port=5000
