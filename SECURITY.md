# Security Policy

## Supported Versions

We release patches for security vulnerabilities for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| Latest  | :white_check_mark: |
| < Latest| :x:                |

## Reporting a Vulnerability

We take security seriously. If you discover a security vulnerability, please follow these steps:

### 1. **Do Not** Open a Public Issue
Security vulnerabilities should not be reported through public GitHub issues.

### 2. Report Privately
Please report security vulnerabilities by:
- Opening a private security advisory on GitHub (preferred)
- Or emailing the maintainers directly

### 3. Include These Details
- Type of vulnerability
- Full paths of affected source files
- Location of the affected code (tag/branch/commit)
- Step-by-step instructions to reproduce
- Proof-of-concept or exploit code (if possible)
- Impact of the issue

### 4. What to Expect
- We will acknowledge receipt within 48 hours
- We will provide a detailed response within 7 days
- We will work on a fix and keep you updated
- We will notify you when the vulnerability is fixed
- We will publicly credit you (if desired) after the fix is released

## Security Best Practices

When deploying this application:

1. **Use HTTPS** in production
2. **Set appropriate CORS** policies (don't use `allow_origins=["*"]` in production)
3. **Implement rate limiting** to prevent abuse
4. **Validate and sanitize** all user inputs
5. **Keep dependencies updated** regularly
6. **Use environment variables** for sensitive configuration
7. **Monitor logs** for suspicious activity
8. **Limit file upload sizes** to prevent DoS attacks

## Known Security Considerations

- This application processes user-provided HTML/Markdown content
- WeasyPrint renders HTML which could potentially include malicious content
- Always validate and sanitize inputs in production
- Consider running in a sandboxed environment for untrusted content

## Updates

Security updates will be released as soon as possible after a vulnerability is confirmed and fixed. Users are encouraged to upgrade to the latest version.
