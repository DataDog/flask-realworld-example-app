# Flask RealWorld Example App - Datadog APM & IAST Testing

[![Check-Format](https://github.com/DataDog/flask-realworld-example-app/actions/workflows/check_format.yml/badge.svg)](https://github.com/DataDog/flask-realworld-example-app/actions/workflows/check_format.yml)
![Python Versions](https://img.shields.io/badge/python-3.9%20%7C%203.10%20%7C%203.12%20%7C%203.14-blue)
![License](https://img.shields.io/badge/license-MIT-green)

A Flask-based implementation of the RealWorld API specification, instrumented with [Datadog APM](https://docs.datadoghq.com/tracing/) for testing and demonstrating:

- **Application Performance Monitoring (APM)** - Distributed tracing and performance metrics
- **Application Security Management (ASM)** - Runtime application security monitoring
- **Application Vulnerability Management (IAST)** - Interactive Application Security Testing for vulnerability detection

This project is maintained by Datadog and serves as a reference implementation for testing APM features, security vulnerabilities, and IAST capabilities in a real-world Flask application.

![image](image.png)

## Table of Contents

- [Features](#features)
- [Quick Start](#quick-start)
- [Development Setup](#development-setup)
- [Running the Application](#running-the-application)
- [Testing](#testing)
- [Datadog Integration](#datadog-integration)
- [Security Testing Endpoints](#security-testing-endpoints)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Modern Flask Stack**: Flask 3.x with SQLAlchemy, Flask-Migrate, Flask-JWT-Extended
- **RESTful API**: Implements the [RealWorld API spec](https://realworld-docs.netlify.app/docs/specs/backend-specs/endpoints)
- **Security Testing**: Dedicated endpoints for testing IAST vulnerability detection
- **Datadog Instrumentation**: Pre-configured with ddtrace for APM and security monitoring
- **Multiple Python Versions**: Supports Python 3.9, 3.10, 3.12, and 3.14
- **Modern Tooling**: Uses Hatch for dependency management and task running

## Quick Start

### Prerequisites

- Python 3.9 or higher
- PostgreSQL (for production) or SQLite (for development)
- [Hatch](https://hatch.pypa.io/) package manager

### Installation

1. Clone the repository:

```bash
git clone https://github.com/DataDog/flask-realworld-example-app.git
cd flask-realworld-example-app
```

2. Install Hatch (if not already installed):

```bash
pip install hatch
```

3. Set required environment variables:

```bash
export CONDUIT_SECRET='your-secret-key-here'
export FLASK_APP=autoapp.py
export FLASK_DEBUG=1
```

4. Initialize the database:

```bash
flask db init
flask db migrate
flask db upgrade
```

5. Run the development server:

```bash
flask run --with-threads
```

The application will be available at `http://localhost:5000`

## Development Setup

### Using Hatch (Recommended)

Hatch manages virtual environments and dependencies automatically:

```bash
# Run tests for specific Python version
hatch run +py=3.14 unit_tests:test

# Run tests for all Python versions
hatch run unit_tests:test

# Check code formatting
hatch run lint:fmt

# Run linting
hatch run lint:all
```

### Pre-commit Hooks

The project uses pre-commit hooks to ensure code quality. Initialize them with:

```bash
hooks/autohook.sh install
```

This will automatically run `black`, `flake8`, and `mypy` on each commit.

## Running the Application

### Development Mode

```bash
export FLASK_DEBUG=1
flask run --with-threads
```

### With Datadog APM

To enable Datadog tracing:

```bash
export DD_SERVICE=flask-realworld-app
export DD_ENV=development
export DD_VERSION=1.0.0

ddtrace-run flask run --with-threads
```

### Using uWSGI

```bash
ddtrace-run uwsgi --http 0.0.0.0:3000 --enable-threads --module autoapp:app
```

## Testing

### Run All Tests

```bash
# Using pytest directly
python -m pytest -vvv -s

# Using hatch
hatch run unit_tests:test

# Run tests for specific Python version
hatch run +py=3.12 unit_tests:test
```

### Run Specific Tests

```bash
pytest tests/test_security.py -v
pytest tests/test_articles.py::test_get_article -v
```

## Datadog Integration

This application is instrumented with Datadog's `ddtrace` library. Key integration points:

- **Automatic Instrumentation**: Flask, SQLAlchemy, and other libraries are automatically instrumented
- **Custom Spans**: Security testing endpoints create custom spans for vulnerability detection
- **IAST Support**: Application Vulnerability Management features are enabled in security endpoints

### Configuration

Set these environment variables for Datadog integration:

```bash
export DD_SERVICE=flask-realworld-app       # Service name in Datadog
export DD_ENV=production                     # Environment (dev, staging, prod)
export DD_VERSION=1.0.0                      # Application version
export DD_TRACE_ENABLED=true                 # Enable tracing
export DD_IAST_ENABLED=true                  # Enable IAST vulnerability detection
```

## Security Testing Endpoints

The application includes dedicated endpoints for testing security vulnerabilities:

### IAST Propagation Testing

```bash
GET /iast/propagation?string1=test&password=secret
```

Tests taint propagation through:
- String operations (concatenation, slicing, formatting)
- Path operations
- Regular expressions
- Multiple vulnerability types (Path Traversal, Command Injection, SSRF)

### SQL Injection Testing

```bash
GET /iast/sqli?q=test
```

### Weak Hash Testing

```bash
GET /iast/weak_hash?q=test
```

### Articles with IAST

```bash
GET /iast/articles?tag=testing&limit=10
```

For more details, see [conduit/security/views.py](conduit/security/views.py).

## Deployment

### Heroku

The project includes a `Procfile` for easy Heroku deployment:

```bash
heroku create your-app-name
heroku addons:create heroku-postgresql:mini
git push heroku main
heroku run flask db upgrade
```

### Production Configuration

Ensure these environment variables are set:

```bash
export FLASK_DEBUG=0
export DATABASE_URL=postgresql://user:password@host:port/database
export CONDUIT_SECRET=your-production-secret-key
export DD_SERVICE=flask-realworld-app
export DD_ENV=production
```

## Database Migrations

### Create a New Migration

```bash
flask db migrate -m "Description of changes"
```

### Apply Migrations

```bash
flask db upgrade
```

### Rollback Migration

```bash
flask db downgrade
```

For more migration commands:

```bash
flask db --help
```

## Interactive Shell

Open an interactive shell with Flask app context:

```bash
flask shell
```

Available objects: `app`, `db`, `User`, `UserProfile`, `Article`, `Tag`, `Comment`

## Project Structure

```
.
├── conduit/                 # Main application package
│   ├── articles/           # Articles module (models, views, schemas)
│   ├── profile/            # User profiles module
│   ├── security/           # Security testing views and vulnerabilities
│   ├── user/               # User authentication module
│   ├── app.py              # Application factory
│   ├── settings.py         # Configuration classes
│   └── extensions.py       # Flask extensions
├── tests/                   # Test suite
├── requirements/            # Dependencies (prod, dev)
├── .github/workflows/       # CI/CD pipelines
├── hooks/                   # Git pre-commit hooks
└── docs/                    # Documentation
```

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details on:

- Setting up your development environment
- Code style guidelines
- Submitting pull requests
- Reporting issues

## Security

For security concerns, please see our [Security Policy](SECURITY.md).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Original implementation by Mohamed Aziz Knani. Maintained by Datadog, Inc.

## Resources

- [Datadog APM Documentation](https://docs.datadoghq.com/tracing/)
- [Datadog ASM Documentation](https://docs.datadoghq.com/security/application_security/)
- [Datadog IAST Documentation](https://docs.datadoghq.com/security/application_security/vulnerability_management/)
- [RealWorld API Spec](https://realworld-docs.netlify.app/docs/specs/backend-specs/endpoints)
- [Flask Documentation](https://flask.palletsprojects.com/)

## Support

- **Issues**: [GitHub Issues](https://github.com/DataDog/flask-realworld-example-app/issues)
- **Datadog Support**: [https://www.datadoghq.com/support/](https://www.datadoghq.com/support/)
