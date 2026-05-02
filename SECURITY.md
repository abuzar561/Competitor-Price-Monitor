# Security Policy

## Supported Versions

The `main` branch is the supported version of this project.

## Reporting a Vulnerability

Please report security issues through GitHub Security Advisories for this repository.

## Credential Safety

- Never commit `.env` files, n8n credential exports, webhook IDs, Google Sheet URLs, or personal email addresses.
- Rotate any credential that was accidentally pushed to a public repository.
- Use n8n credential storage for Google Sheets and Gmail accounts instead of embedding secrets in workflow JSON.
- Treat product URLs and selectors as configuration when they reveal private business targets.
