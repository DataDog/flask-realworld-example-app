# Security Policy

## Supported Versions

We actively support the following Python versions with security updates:

| Python Version | Supported          |
| -------------- | ------------------ |
| 3.14           | :white_check_mark: |
| 3.13           | :white_check_mark: |
| 3.12           | :white_check_mark: |
| 3.11           | :white_check_mark: |
| 3.10           | :white_check_mark: |
| 3.9            | :white_check_mark: |
| < 3.9          | :x:                |

## Reporting a Vulnerability

**Please do not report security vulnerabilities through public GitHub issues.**

If you discover a security vulnerability in this project, please report it privately to the Datadog Security Team.

### How to Report

1. **Email**: Send details to [security@datadoghq.com](mailto:security@datadoghq.com)
2. **Include**: 
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if available)

### What to Expect

- **Acknowledgment**: We will acknowledge receipt within 48 hours
- **Assessment**: We will assess the vulnerability and determine severity
- **Updates**: We will keep you informed of progress
- **Fix Timeline**: Critical vulnerabilities will be addressed within 7 days
- **Credit**: We will credit you in the security advisory (unless you prefer to remain anonymous)

## Security Features

This application includes intentional security vulnerabilities for testing purposes. These are clearly marked in the codebase:

### Test Vulnerabilities (Intentional)

The following endpoints contain **intentional vulnerabilities** for IAST testing:

- `/iast/propagation` - Path traversal, command injection, SSRF testing
- `/iast/sqli` - SQL injection testing
- `/iast/weak_hash` - Weak cryptographic hash testing
- `/iast/articles` - Combined vulnerability testing

**Warning**: These endpoints should NEVER be deployed to production environments. They are for security testing and research only.

### Production Security

When deploying this application:

1. **Do NOT expose IAST endpoints** - Remove or disable the `security` blueprint
2. **Set secure environment variables**:
   ```bash
   export FLASK_DEBUG=0
   export CONDUIT_SECRET='<strong-random-secret>'
   ```
3. **Use HTTPS** in production
4. **Enable Datadog ASM** for runtime security monitoring
5. **Configure proper CORS** settings
6. **Use strong JWT secrets**
7. **Enable database encryption** at rest
8. **Implement rate limiting**

## Known Security Considerations

### Development vs Production

- **SQLite in Development**: Default development uses SQLite. Use PostgreSQL in production.
- **JWT Token Expiry**: Development uses long-lived tokens (10^6 seconds). Configure appropriately for production.
- **Debug Mode**: Debug mode must be disabled in production (`FLASK_DEBUG=0`)
- **Secret Keys**: Use strong, random secret keys in production

### Dependencies

We monitor dependencies for known vulnerabilities:

- Dependabot alerts are enabled
- Regular dependency updates are performed
- Security patches are prioritized

### Datadog ddtrace

This application uses Datadog's `ddtrace` library for APM and security monitoring. Security features include:

- **IAST**: Vulnerability detection through code analysis
- **ASM**: Runtime application attack detection
- **Software Composition Analysis**: Dependency vulnerability scanning

## Security Best Practices

When contributing to this project:

1. **Never commit secrets** - Use environment variables
2. **Validate user input** - Even for test endpoints
3. **Use parameterized queries** - Prevent SQL injection
4. **Sanitize output** - Prevent XSS
5. **Keep dependencies updated** - Monitor for vulnerabilities
6. **Review security changes carefully** - Extra scrutiny for auth/security code

## Security Testing

### Running Security Tests

```bash
# Run security-specific tests
pytest tests/test_security.py -v

# Run with IAST enabled
DD_IAST_ENABLED=true ddtrace-run pytest tests/test_security.py
```

### Security Scanning

We recommend running these security tools:

```bash
# Bandit - Python security linter
bandit -r conduit/

# Safety - Dependency vulnerability scanner
safety check

# Trivy - Container scanning (if using Docker)
trivy image your-image-name
```

## Disclosure Policy

- We follow coordinated vulnerability disclosure
- Security issues are fixed before public disclosure
- Public disclosure occurs after:
  1. Fix is available
  2. Sufficient time for users to update (typically 90 days)
  3. Coordination with the reporter

## Security Champions

Current security maintainers:

- Datadog Security Team - [security@datadoghq.com](mailto:security@datadoghq.com)

## Additional Resources

- [Datadog Security](https://www.datadoghq.com/product/security-platform/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CWE Top 25](https://cwe.mitre.org/top25/)

## Security Updates

Security updates will be announced through:

- GitHub Security Advisories
- Release notes in [CHANGELOG.md](CHANGELOG.md)
- Datadog Security Bulletins

Thank you for helping keep this project secure!
