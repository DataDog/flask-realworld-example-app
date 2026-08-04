# 基于 prometheus_client 的简单集成
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from flask import Response, request

REQUEST_COUNT = Counter('flask_request_count', 'App Request Count', ['method', 'endpoint', 'http_status'])

def after_request(response):
    try:
        REQUEST_COUNT.labels(method=request.method, endpoint=request.path, http_status=response.status_code).inc()
    except Exception:
        pass
    return response

def metrics_endpoint():
    resp = Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)
    return resp
