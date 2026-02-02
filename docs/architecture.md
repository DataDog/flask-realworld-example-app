# Architecture

## Overview

This application follows a modular Flask architecture with blueprints for separation of concerns.

## Project Structure

```
flask-realworld-example-app/
├── conduit/                    # Main application package
│   ├── __init__.py
│   ├── app.py                  # Application factory
│   ├── settings.py             # Configuration classes
│   ├── extensions.py           # Flask extensions initialization
│   ├── database.py             # Database utilities
│   ├── exceptions.py           # Custom exceptions
│   ├── utils.py                # Utility functions
│   ├── commands.py             # CLI commands
│   │
│   ├── user/                   # User module
│   │   ├── models.py           # User model
│   │   ├── views.py            # User routes
│   │   └── serializers.py      # User schemas
│   │
│   ├── profile/                # Profile module
│   │   ├── models.py
│   │   ├── views.py
│   │   └── serializers.py
│   │
│   ├── articles/               # Articles module
│   │   ├── models.py
│   │   ├── views.py
│   │   └── serializers.py
│   │
│   └── security/               # Security testing module
│       ├── views.py            # IAST endpoints
│       └── vulnerabilities.py  # Test vulnerabilities
│
├── tests/                      # Test suite
│   ├── conftest.py
│   ├── test_user.py
│   ├── test_articles.py
│   └── test_security.py
│
├── requirements/               # Dependencies
│   ├── prod.txt
│   └── dev.txt
│
└── .github/                    # CI/CD workflows
    └── workflows/
        ├── unit_tests.yml
        └── check_format.yml
```

## Design Patterns

### Application Factory Pattern

The app uses the Application Factory pattern (`conduit/app.py:create_app()`), which:
- Allows multiple app instances with different configurations
- Simplifies testing
- Enables extension initialization after app creation

```python
def create_app(config_object=ProdConfig):
    app = Flask(__name__.split(".")[0])
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    return app
```

### Blueprint Architecture

Each module is a Flask Blueprint for modularity:
- `user.views.blueprint` - User authentication and registration
- `profile.views.blueprint` - User profiles and following
- `articles.views.blueprint` - Article CRUD and favorites
- `security.views.blueprint` - IAST security testing endpoints

### Repository Pattern

Models handle data persistence, views handle HTTP logic:
- Models: `conduit/*/models.py`
- Views: `conduit/*/views.py`
- Serializers: `conduit/*/serializers.py`

## Database Schema

### Users Table
- id (primary key)
- username (unique)
- email (unique)
- password (hashed with bcrypt)
- bio
- image
- created_at
- updated_at

### Articles Table
- id (primary key)
- slug (unique, auto-generated)
- title
- description
- body
- author_id (foreign key to users)
- created_at
- updated_at

### Comments Table
- id (primary key)
- body
- article_id (foreign key to articles)
- author_id (foreign key to users)
- created_at
- updated_at

### Tags Table
- id (primary key)
- tagname (unique)

### Associations
- **article_tags** - Many-to-many between articles and tags
- **followers_assoc** - Many-to-many for user following
- **favoriter_assoc** - Many-to-many for article favorites

## Configuration

Three environment configs in `conduit/settings.py`:

### DevConfig
- SQLite database
- Debug mode enabled
- Long-lived JWT tokens

### ProdConfig
- PostgreSQL database
- Debug mode disabled
- Standard JWT expiration

### TestConfig
- In-memory SQLite
- Reduced bcrypt rounds for speed

## Extensions

- **SQLAlchemy** - ORM for database operations
- **Flask-Migrate** - Database migration management
- **Flask-JWT-Extended** - JWT authentication
- **Flask-Bcrypt** - Password hashing
- **Flask-Caching** - Response caching
- **Flask-CORS** - Cross-origin resource sharing

## Request Flow

1. Request arrives at Flask app
2. Datadog ddtrace intercepts for APM
3. Route matches to blueprint view
4. JWT authentication (if required)
5. View processes request
6. Database queries (tracked by APM)
7. Response serialization
8. Response sent to client

## Security Architecture

### Authentication
- JWT tokens in `Authorization: Token <jwt>` header
- Tokens signed with `CONDUIT_SECRET`
- Optional authentication on some endpoints

### Authorization
- Article authors can update/delete their articles
- Users can only update their own profile
- Comments can only be deleted by author

### IAST Testing Endpoints
- `/iast/propagation` - Taint propagation testing
- `/iast/sqli` - SQL injection testing
- `/iast/weak_hash` - Weak cryptography testing
- These endpoints are for security testing only

## Performance Considerations

- **Caching**: Flask-Caching for frequently accessed data
- **Database Indexes**: On username, email, slug fields
- **Lazy Loading**: SQLAlchemy relationships use lazy loading
- **Connection Pooling**: SQLAlchemy connection pool

## Monitoring & Observability

### Datadog APM
- Automatic instrumentation of Flask requests
- Database query tracing
- External HTTP request tracing
- Custom spans for business logic

### Datadog IAST
- Taint tracking for user input
- Vulnerability detection at runtime
- Code-level security analysis

## Testing Strategy

- **Unit Tests**: Test individual functions and methods
- **Integration Tests**: Test full request/response cycles
- **Security Tests**: Test IAST vulnerability detection
- Test fixtures in `tests/conftest.py`
- WebTest for HTTP testing

## Future Enhancements

- GraphQL API support
- WebSocket support for real-time updates
- Redis caching layer
- Elasticsearch for full-text search
- API rate limiting
- API versioning
