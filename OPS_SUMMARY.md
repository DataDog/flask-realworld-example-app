# 已添加的运维/容器化改动

此分支包含为 flask-realworld-example-app 添加的运维相关文件：

- Dockerfile
- docker-compose.yml
- docker-compose-monitoring.yml
- .github/workflows/ci.yml
- app_health.py
- metrics.py
- prometheus.yml
- docs/run-local.md
- docs/monitoring.md

请在合入前检查并根据仓库实际 app 名称调整 Dockerfile 中的 gunicorn 启动参数（app:app）。
