# Deployment Guide

## Heroku Deployment

### Quick Deploy

```bash
heroku create your-app-name
heroku addons:create heroku-postgresql:mini
heroku config:set CONDUIT_SECRET='your-secret-key'
heroku config:set DD_API_KEY='your-datadog-api-key'
heroku config:set DD_SERVICE='flask-realworld-app'
heroku config:set DD_ENV='production'
git push heroku main
heroku run flask db upgrade
```

## Docker Deployment

### Dockerfile

```dockerfile
FROM python:3.14-slim

WORKDIR /app
COPY requirements/prod.txt .
RUN pip install --no-cache-dir -r prod.txt

COPY . .

ENV FLASK_APP=autoapp.py
ENV FLASK_DEBUG=0

CMD ["ddtrace-run", "gunicorn", "-b", "0.0.0.0:8000", "autoapp:app"]
```

### Docker Compose

```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/conduit
      - DD_AGENT_HOST=datadog-agent
      - DD_SERVICE=flask-realworld-app
    depends_on:
      - db
      - datadog-agent
  
  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=conduit
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
  
  datadog-agent:
    image: datadog/agent:latest
    environment:
      - DD_API_KEY=${DD_API_KEY}
      - DD_SITE=datadoghq.com
      - DD_APM_ENABLED=true
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
```

## Production Checklist

- [ ] Set FLASK_DEBUG=0
- [ ] Use strong CONDUIT_SECRET
- [ ] Configure PostgreSQL
- [ ] Enable HTTPS
- [ ] Remove/disable IAST endpoints
- [ ] Configure proper CORS
- [ ] Set up database backups
- [ ] Configure logging
- [ ] Set up monitoring alerts
- [ ] Enable Datadog ASM
- [ ] Configure rate limiting
- [ ] Review security settings

## Environment Variables

```bash
# Required
export FLASK_DEBUG=0
export DATABASE_URL=postgresql://user:pass@host:port/db
export CONDUIT_SECRET='strong-secret-key'

# Datadog
export DD_API_KEY='your-api-key'
export DD_SERVICE='flask-realworld-app'
export DD_ENV='production'
export DD_VERSION='1.0.0'

# Optional
export DD_APPSEC_ENABLED=true
export DD_TRACE_SAMPLE_RATE=0.1
```

## Database Migrations

```bash
# Run migrations on deployment
flask db upgrade
```

## Monitoring

Set up Datadog monitors for:
- Error rate > 5%
- Response time p95 > 1s
- Database connection errors
- Critical IAST vulnerabilities
