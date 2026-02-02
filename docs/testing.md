# Testing Guide

## Testing Strategy

This project uses a comprehensive testing approach with pytest and WebTest.

## Test Structure

```
tests/
├── conftest.py           # Test fixtures and configuration
├── factories.py          # Factory Boy factories
├── test_user.py          # User authentication tests
├── test_profile.py       # User profile tests
├── test_articles.py      # Article CRUD tests
└── test_security.py      # IAST security tests
```

## Running Tests

### All Tests

```bash
# Using hatch (recommended)
hatch run unit_tests:test

# Using pytest directly
pytest -vvv -s
```

### Specific Test Files

```bash
pytest tests/test_security.py -v
pytest tests/test_articles.py -v
```

### Specific Test Functions

```bash
pytest tests/test_user.py::test_register_user -v
pytest tests/test_articles.py::test_create_article -v
```

### With Coverage

```bash
# Using hatch
hatch run unit_tests:cov

# Using pytest directly
pytest --cov=conduit --cov-report=html --cov-report=term
```

View coverage report:
```bash
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

### Multiple Python Versions

```bash
# Test on Python 3.14
hatch run +py=3.14 unit_tests:test

# Test on Python 3.12
hatch run +py=3.12 unit_tests:test

# Test on all supported versions
hatch run unit_tests:test
```

## Writing Tests

### Test Fixtures

Common fixtures are defined in `tests/conftest.py`:

```python
@pytest.fixture
def app():
    """Flask application for testing"""
    return create_app(TestConfig)

@pytest.fixture
def testapp(app):
    """WebTest TestApp wrapper"""
    return TestApp(app)

@pytest.fixture
def db(app):
    """Database with tables"""
    with app.app_context():
        _db.create_all()
        yield _db
        _db.drop_all()

@pytest.fixture
def user(db):
    """Test user"""
    user = User(username='test', email='test@example.com')
    user.set_password('password')
    db.session.add(user)
    db.session.commit()
    return user
```

### Example Test

```python
def test_user_can_register(testapp):
    """Test user registration."""
    # Arrange
    user_data = {
        "user": {
            "username": "newuser",
            "email": "new@example.com",
            "password": "securepassword"
        }
    }
    
    # Act
    response = testapp.post_json("/api/users", user_data)
    
    # Assert
    assert response.status_code == 201
    assert "user" in response.json
    assert response.json["user"]["username"] == "newuser"
    assert "token" in response.json["user"]
```

### Using Factories

Factory Boy is used for test data generation:

```python
from tests.factories import UserFactory, ArticleFactory

def test_article_creation(db):
    user = UserFactory()
    article = ArticleFactory(author=user)
    
    assert article.author == user
    assert article.slug is not None
```

## Test Categories

### Unit Tests
Test individual functions and methods in isolation.

```python
def test_slug_generation():
    article = Article(title="Test Article")
    assert article.slug == "test-article"
```

### Integration Tests
Test full request/response cycles.

```python
def test_create_and_get_article(testapp, user):
    # Create article
    create_response = testapp.post_json(
        "/api/articles",
        {"article": {"title": "Test", "body": "Content"}},
        headers={"Authorization": f"Token {user.token}"}
    )
    
    slug = create_response.json["article"]["slug"]
    
    # Get article
    get_response = testapp.get(f"/api/articles/{slug}")
    assert get_response.status_code == 200
```

### Security Tests
Test IAST vulnerability detection.

```python
def test_iast_weak_hash(testapp):
    resp = testapp.get("/iast/weak_hash?q=test")
    assert resp.status_code == 200
```

## Testing Best Practices

### 1. Use Descriptive Names

```python
# Good
def test_authenticated_user_can_create_article():
    pass

# Bad
def test_article():
    pass
```

### 2. Follow Arrange-Act-Assert

```python
def test_user_login():
    # Arrange
    user = UserFactory()
    credentials = {"email": user.email, "password": "password"}
    
    # Act
    response = testapp.post_json("/api/users/login", {"user": credentials})
    
    # Assert
    assert response.status_code == 200
    assert "token" in response.json["user"]
```

### 3. Test Edge Cases

```python
def test_article_title_too_long(testapp, user):
    long_title = "x" * 300
    response = testapp.post_json(
        "/api/articles",
        {"article": {"title": long_title}},
        headers=auth_headers(user),
        expect_errors=True
    )
    assert response.status_code == 422
```

### 4. Use Parametrize for Multiple Inputs

```python
@pytest.mark.parametrize("invalid_email", [
    "notanemail",
    "@example.com",
    "user@",
    ""
])
def test_invalid_email_rejected(testapp, invalid_email):
    response = testapp.post_json(
        "/api/users",
        {"user": {"username": "test", "email": invalid_email}},
        expect_errors=True
    )
    assert response.status_code == 422
```

## Coverage Goals

- **Overall Coverage**: > 80%
- **Critical Paths**: > 95% (authentication, data modification)
- **Security Code**: 100%

### Viewing Coverage

```bash
# Generate coverage report
pytest --cov=conduit --cov-report=html

# Open in browser
open htmlcov/index.html
```

### Coverage Configuration

Coverage settings in `pyproject.toml`:

```toml
[tool.coverage.run]
source = ["conduit"]
omit = [
    "*/tests/*",
    "*/migrations/*",
    "*/__pycache__/*"
]

[tool.coverage.report]
precision = 2
show_missing = true
skip_covered = false
```

## Continuous Integration

Tests run automatically on:
- Every pull request
- Every push to master
- Multiple Python versions (3.9, 3.10, 3.12, 3.14)

See `.github/workflows/unit_tests.yml` for CI configuration.

## Debugging Tests

### Run with Debug Output

```bash
pytest -vvv -s --log-cli-level=DEBUG
```

### Drop into Debugger on Failure

```bash
pytest --pdb
```

### Run Only Failed Tests

```bash
pytest --lf  # Last failed
pytest --ff  # Failed first
```

## Performance Testing

For load testing, use tools like:
- **Locust**: `pip install locust`
- **Apache Bench**: `ab -n 1000 -c 10 http://localhost:5000/`

## Security Testing

### IAST Testing

```bash
DD_IAST_ENABLED=true ddtrace-run pytest tests/test_security.py -v
```

### Dependency Scanning

```bash
# Using safety
pip install safety
safety check

# Using bandit
pip install bandit
bandit -r conduit/
```

## Test Maintenance

- Review tests when code changes
- Remove obsolete tests
- Keep fixtures DRY
- Update tests before refactoring
- Maintain test documentation
