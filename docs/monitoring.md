# 监控 (Prometheus + Grafana)

1. 使用本仓库的 docker-compose-monitoring.yml 启动监控栈：
docker-compose -f docker-compose-monitoring.yml up --build

2. 打开 Prometheus:
http://localhost:9090

3. 打开 Grafana (默认账号 admin/admin):
http://localhost:3000

4. 在 Grafana 中添加数据源：
- 类型：Prometheus
- URL: http://prometheus:9090  （如果在容器网络内）
或 http://localhost:9090（如果在宿主机上访问）

5. 导入/创建 Dashboard，查看 /metrics 与自定义指标（示例：flask_request_count）。
