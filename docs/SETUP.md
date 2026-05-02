# Setup Guide

## 1. Install Requirements

Create a virtual environment and install the Python dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

The first run downloads a compatible ChromeDriver through `webdriver-manager`.

## 2. Find the Price Selector

Open the product page in Chrome, inspect the visible price element, and copy a stable CSS selector. Prefer selectors tied to semantic classes or data attributes.

Example:

```text
.product-price
```

## 3. Run a Dry Run

```bash
python src/price_monitor.py \
  --url "https://example.com/product" \
  --selector ".product-price" \
  --product-name "Competitor Product" \
  --target-price 999 \
  --dry-run
```

The command prints the JSON payload without calling n8n.

## 4. Connect n8n

Import `workflow/competitor-price-monitor.json`, configure the Google Sheets and Gmail nodes, then copy the production webhook URL into `N8N_WEBHOOK_URL`.

```bash
N8N_WEBHOOK_URL="https://your-n8n-instance/webhook/price-update" \
python src/price_monitor.py \
  --url "https://example.com/product" \
  --selector ".product-price" \
  --product-name "Competitor Product" \
  --target-price 999
```

## 5. Schedule the Monitor

Use cron, Windows Task Scheduler, GitHub Actions, or another scheduler that can run the Python command on a sensible interval. Keep frequency respectful for the website you are checking.
