# Workflow Template

`competitor-price-monitor.json` is a sanitized n8n workflow template for public repository use.

## Before Activating

1. Import the JSON file into n8n.
2. Connect Google Sheets credentials in `Log Price Snapshot`.
3. Replace `YOUR_GOOGLE_SHEET_ID` with your spreadsheet ID.
4. Create or select a tab named `Price Monitor`.
5. Connect Gmail credentials in both email nodes.
6. Replace `price-alerts@example.com` with your alert recipient.
7. Activate the workflow and copy the production webhook URL.

The template does not include credentials, webhook IDs, private sheet URLs, or personal email addresses.
