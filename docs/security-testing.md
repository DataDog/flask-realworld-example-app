# Security Testing Guide

## IAST Testing

### Overview

This application includes intentional vulnerabilities for testing Datadog IAST capabilities.

**Warning**: IAST endpoints should NEVER be deployed to production.

### Test Endpoints

#### 1. Taint Propagation Test

```bash
curl "http://localhost:5000/iast/propagation?string1=hello&password=world"
```

Tests:
- String operations (concat, slice, format)
- Path traversal vulnerability
- Command injection vulnerability
- SSRF vulnerability
- Weak randomness
- Insecure cookie
- Header injection

#### 2. SQL Injection Test

```bash
curl "http://localhost:5000/iast/sqli?q=' OR '1'='1"
```

#### 3. Weak Cryptography Test

```bash
curl "http://localhost:5000/iast/weak_hash?q=password123"
```

### Running with IAST Enabled

```bash
DD_IAST_ENABLED=true ddtrace-run flask run
```

### Viewing Results

1. Navigate to Datadog UI
2. Security > Application Vulnerability Management
3. Filter by service: flask-realworld-app
4. View detected vulnerabilities

### Disabling IAST Endpoints for Production

Remove or comment out the security blueprint registration in `conduit/app.py`:

```python
# app.register_blueprint(security.views.blueprint)  # Remove this line
```

## Security Best Practices

1. Never deploy IAST endpoints to production
2. Use strong secret keys in production
3. Enable HTTPS
4. Configure CORS properly
5. Implement rate limiting
6. Keep dependencies updated
7. Monitor Datadog ASM for threats
