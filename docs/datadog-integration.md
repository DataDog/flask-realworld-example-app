# Datadog Integration Guide

## Overview

This application is instrumented with Datadog's `ddtrace` library for comprehensive observability and security monitoring.

## Features

- **APM (Application Performance Monitoring)** - Distributed tracing and performance metrics
- **ASM (Application Security Management)** - Runtime threat detection and protection
- **IAST (Interactive Application Security Testing)** - Vulnerability detection through code analysis

## Setup

### Prerequisites

- Datadog account
- Datadog Agent running (or using agentless mode)
- `ddtrace` library installed (included in `requirements/dev.txt`)

### Environment Variables

```bash
# Core APM Configuration
export DD_SERVICE=flask-realworld-app
export DD_ENV=production
export DD_VERSION=1.0.0
export DD_TRACE_ENABLED=true

# IAST Configuration
export DD_IAST_ENABLED=true

# ASM Configuration (optional)
export DD_APPSEC_ENABLED=true

# Agent Configuration
export DD_AGENT_HOST=localhost
export DD_TRACE_AGENT_PORT=8126

# Optional: API Key for agentless mode
export DD_API_KEY=your_api_key_here
```

### Running with ddtrace

#### Development

```bash
ddtrace-run flask run --with-threads
```

#### Production (uWSGI)

```bash
ddtrace-run uwsgi --http 0.0.0.0:3000 --enable-threads --module autoapp:app
```

#### Production (Gunicorn)

```bash
ddtrace-run gunicorn -b 0.0.0.0:8000 autoapp:app
```

## APM Features

### Automatic Instrumentation

The following are automatically instrumented:
- Flask routes and views
- SQLAlchemy database queries
- External HTTP requests (urllib3, requests)
- Template rendering
- Cache operations

### Custom Spans

Add custom spans for specific operations:

```python
from ddtrace import tracer

@tracer.wrap('custom.operation', service='flask-realworld-app')
def my_function():
    # Your code here
    pass
```

### Tagging Requests

Add custom tags to traces:

```python
from ddtrace import tracer

span = tracer.current_span()
if span:
    span.set_tag('user.id', user_id)
    span.set_tag('article.slug', slug)
```

## IAST Features

### What is IAST?

IAST (Interactive Application Security Testing) analyzes your application's behavior at runtime to detect vulnerabilities:
- SQL Injection
- Command Injection
- Path Traversal
- Cross-Site Scripting (XSS)
- Weak Cryptography
- Insecure Cookies
- Header Injection

### IAST Test Endpoints

This application includes dedicated endpoints for testing IAST capabilities:

#### 1. Propagation Testing (`/iast/propagation`)

Tests taint propagation through various operations:

```bash
curl "http://localhost:5000/iast/propagation?string1=test&password=secret"
```

Detects:
- Path Traversal
- Command Injection
- SSRF (Server-Side Request Forgery)
- Weak Randomness
- Insecure Cookies
- Header Injection

#### 2. SQL Injection Testing (`/iast/sqli`)

```bash
curl "http://localhost:5000/iast/sqli?q=test"
```

#### 3. Weak Hash Testing (`/iast/weak_hash`)

```bash
curl "http://localhost:5000/iast/weak_hash?q=test"
```

#### 4. Combined Testing (`/iast/articles`)

```bash
curl "http://localhost:5000/iast/articles?tag=testing"
```

### Viewing IAST Results

1. Go to Datadog UI > Security > Application Vulnerability Management
2. Filter by service: `flask-realworld-app`
3. View detected vulnerabilities with:
   - Source code location
   - Attack vector
   - Remediation suggestions

## ASM Features

### Threat Detection

ASM monitors for:
- SQL injection attempts
- Command injection attempts
- SSRF attacks
- Local File Inclusion (LFI)
- Remote Code Execution (RCE)

### Blocking Mode

Enable blocking to automatically block malicious requests:

```bash
export DD_APPSEC_ENABLED=true
export DD_APPSEC_RULES=/path/to/rules.json
```

### Attack Flow Visualization

View attack attempts in Datadog UI:
1. Go to Security > Application Security > Traces
2. Filter by attack type
3. View full request details and context

## Performance Configuration

### Sampling

Control trace sampling rate:

```bash
export DD_TRACE_SAMPLE_RATE=1.0  # 100% sampling (default for testing)
export DD_TRACE_SAMPLE_RATE=0.1  # 10% sampling (production)
```

### Debug Logging

Enable debug logging:

```bash
export DD_TRACE_DEBUG=true
export DD_IAST_DEBUG=true
```

View logs:

```bash
ddtrace-run flask run 2>&1 | grep ddtrace
```

## Metrics

### Application Metrics

Automatically collected:
- Request rate
- Error rate
- Request duration (p50, p75, p95, p99)
- Database query duration

### Custom Metrics

Send custom metrics:

```python
from ddtrace import tracer

# Increment counter
tracer.current_span().set_metric('article.created', 1)

# Set gauge
tracer.current_span().set_metric('article.count', article_count)
```

## Dashboard Examples

### Key Metrics to Monitor

1. **Request Throughput**
   - `trace.flask.request.hits`
   - Grouped by endpoint

2. **Error Rate**
   - `trace.flask.request.errors`
   - Grouped by error type

3. **Database Performance**
   - `trace.sqlalchemy.query.duration`
   - Grouped by query type

4. **IAST Vulnerabilities**
   - Vulnerability count by severity
   - New vulnerabilities over time

## Troubleshooting

### ddtrace Not Working

1. Check if ddtrace is installed:
   ```bash
   pip show ddtrace
   ```

2. Verify environment variables:
   ```bash
   env | grep DD_
   ```

3. Enable debug mode:
   ```bash
   DD_TRACE_DEBUG=true ddtrace-run flask run
   ```

### No Traces in Datadog

1. Verify Datadog Agent is running:
   ```bash
   curl http://localhost:8126/info
   ```

2. Check connectivity:
   ```bash
   telnet localhost 8126
   ```

3. Verify service name:
   ```bash
   echo $DD_SERVICE
   ```

### IAST Not Detecting Vulnerabilities

1. Ensure IAST is enabled:
   ```bash
   echo $DD_IAST_ENABLED
   ```

2. Use test endpoints:
   ```bash
   curl "http://localhost:5000/iast/propagation?string1=test&password=secret"
   ```

3. Check Datadog logs for IAST events

## Best Practices

1. **Always set service, env, and version tags**
2. **Use consistent naming conventions**
3. **Sample traces appropriately in production** (10-25%)
4. **Monitor IAST vulnerability trends**
5. **Set up alerts for critical vulnerabilities**
6. **Review ASM attack patterns regularly**
7. **Keep ddtrace library updated**

## Additional Resources

- [Datadog APM Documentation](https://docs.datadoghq.com/tracing/)
- [Datadog ASM Documentation](https://docs.datadoghq.com/security/application_security/)
- [Datadog IAST Documentation](https://docs.datadoghq.com/security/application_security/vulnerability_management/)
- [ddtrace Python Library](https://ddtrace.readthedocs.io/)
