# Contributing

Thanks for improving Competitor Price Monitor.

## Development Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Quality Checks

Run these checks before opening a pull request:

```bash
node scripts/validate-project.js
python -m py_compile src/price_monitor.py
```

## Pull Request Guidelines

- Keep changes focused and explain the reason for the change.
- Do not commit `.env` files, exported credentials, webhook IDs, private sheet URLs, or personal email addresses.
- Update documentation when setup steps, payload fields, or workflow behavior changes.
- Test with `--dry-run` before sending data to a live n8n workflow.
