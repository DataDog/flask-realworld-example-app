# Contributing to Flask RealWorld Example App

Thank you for your interest in contributing to this project! This document provides guidelines and instructions for contributing.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Code Style Guidelines](#code-style-guidelines)
- [Running Tests](#running-tests)
- [Submitting Changes](#submitting-changes)
- [Branch Naming Convention](#branch-naming-convention)
- [Commit Message Guidelines](#commit-message-guidelines)
- [Pull Request Process](#pull-request-process)

## Code of Conduct

This project follows the Datadog Code of Conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

## Getting Started

### Prerequisites

- Python 3.9 or higher
- Git
- Hatch (recommended) or pip
- PostgreSQL (optional, for testing production database features)

### Setting Up Your Development Environment

1. Fork the repository on GitHub

2. Clone your fork:

```bash
git clone https://github.com/YOUR_USERNAME/flask-realworld-example-app.git
cd flask-realworld-example-app
```

3. Add the upstream repository:

```bash
git remote add upstream https://github.com/DataDog/flask-realworld-example-app.git
```

4. Install Hatch (recommended):

```bash
pip install hatch
```

5. Install pre-commit hooks:

```bash
hooks/autohook.sh install
```

This will automatically run code formatters and linters before each commit.

## Development Workflow

### Using Hatch (Recommended)

Hatch automatically manages virtual environments and dependencies:

```bash
# Run tests
hatch run unit_tests:test

# Run tests for specific Python version
hatch run +py=3.14 unit_tests:test

# Format code
hatch run lint:fmt

# Run all linters
hatch run lint:all

# Run type checking
hatch run lint:typing
```

### Using pip (Alternative)

If you prefer not to use Hatch:

```bash
# Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements/dev.txt

# Run tests
pytest -vvv

# Format code
black .

# Run linters
flake8
mypy .
```

## Code Style Guidelines

This project follows strict code style guidelines to maintain consistency:

### Python Style

- **PEP 8**: Follow Python's PEP 8 style guide
- **Line Length**: Maximum 120 characters
- **Formatter**: Use Black for automatic formatting
- **Imports**: Use isort for import sorting
- **Type Hints**: Use type hints where appropriate (especially for public APIs)

### Formatting Tools

The project uses the following tools (automatically run by pre-commit hooks):

- **Black**: Code formatter
- **flake8**: Linting and style checking
- **mypy**: Static type checking
- **isort**: Import sorting

### Code Organization

- Keep functions and methods focused on a single responsibility
- Use descriptive variable and function names
- Add docstrings to all public functions and classes
- Keep files under 500 lines when possible

### Example Code Style

```python
# Good
def calculate_article_score(article: Article, user: User) -> float:
    """Calculate relevance score for an article.
    
    Args:
        article: The article to score
        user: The user viewing the article
        
    Returns:
        Float score between 0.0 and 1.0
    """
    base_score = article.favorite_count * 0.1
    recency_bonus = calculate_recency_bonus(article.created_at)
    return min(base_score + recency_bonus, 1.0)
```

## Running Tests

### Run All Tests

```bash
# Using hatch
hatch run unit_tests:test

# Using pytest directly
pytest -vvv -s
```

### Run Specific Tests

```bash
# Test a specific file
pytest tests/test_security.py -v

# Test a specific function
pytest tests/test_articles.py::test_get_article -v

# Run with coverage
pytest --cov=conduit --cov-report=html
```

### Run Tests for Multiple Python Versions

```bash
# Test on Python 3.14
hatch run +py=3.14 unit_tests:test

# Test on Python 3.12
hatch run +py=3.12 unit_tests:test
```

### Writing Tests

- Place tests in the `tests/` directory
- Mirror the structure of the `conduit/` package
- Use descriptive test names that explain what is being tested
- Follow the Arrange-Act-Assert pattern
- Use fixtures for common setup

Example test structure:

```python
def test_user_can_create_article(testapp, user):
    """Test that authenticated users can create articles."""
    # Arrange
    article_data = {
        "title": "Test Article",
        "body": "Test content",
        "description": "Test description"
    }
    
    # Act
    response = testapp.post_json("/api/articles", article_data)
    
    # Assert
    assert response.status_code == 201
    assert response.json["article"]["title"] == "Test Article"
```

## Submitting Changes

### Branch Naming Convention

Use the following format for branch names:

```
<username>/<ticket-id>_<short-description>
```

Examples:

- `avara1986/APPSEC-60986_python314`
- `jdoe/ISSUE-123_fix-auth-bug`
- `msmith/FEATURE-456_add-comments`

### Commit Message Guidelines

Follow the conventional commits format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks, dependency updates

**Examples:**

```
feat(security): add IAST header injection endpoint

Add new endpoint to test header injection vulnerabilities
for IAST testing purposes.

Closes #123
```

```
fix(articles): resolve SQL injection vulnerability

Update article query to use parameterized queries instead
of string concatenation.

BREAKING CHANGE: ArticleRepository.search() now requires
keyword arguments instead of positional arguments.
```

## Pull Request Process

1. **Update Your Branch**

```bash
git fetch upstream
git rebase upstream/master
```

2. **Run Tests and Linters**

```bash
hatch run lint:all
hatch run unit_tests:test
```

3. **Push to Your Fork**

```bash
git push origin your-branch-name
```

4. **Create Pull Request**

- Go to GitHub and create a Pull Request from your fork to `DataDog/flask-realworld-example-app:master`
- Fill out the PR template completely
- Link any related issues

5. **PR Title Format**

Use the same format as commit messages:

```
feat(security): add IAST header injection endpoint
fix(articles): resolve SQL injection vulnerability
```

6. **PR Description Should Include**

- **What**: What changes are being made
- **Why**: Why these changes are needed
- **How**: How to test the changes
- **Screenshots**: If applicable, include screenshots or GIFs
- **Related Issues**: Link to related issues or tickets

7. **Review Process**

- Address all review comments
- Keep your PR up to date with master
- Maintain a clean commit history (squash if needed)
- Ensure CI passes before requesting review

8. **After Approval**

- Maintainers will merge your PR
- Your changes will be included in the next release

## Questions or Need Help?

- **Issues**: Create an issue on [GitHub](https://github.com/DataDog/flask-realworld-example-app/issues)
- **Discussions**: Use GitHub Discussions for general questions
- **Security**: For security issues, see [SECURITY.md](SECURITY.md)

## License

By contributing, you agree that your contributions will be licensed under the same [MIT License](LICENSE) that covers this project.

Thank you for contributing!
