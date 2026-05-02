# n8n Workflow Guide

The workflow template lives at `workflow/competitor-price-monitor.json`.

## Nodes

| Node | Purpose |
| --- | --- |
| `Price Update Webhook` | Receives price snapshots from the Python scraper. |
| `Log Price Snapshot` | Writes the snapshot into Google Sheets. |
| `Price Below Target?` | Compares current price against target price. |
| `Send Price Drop Alert` | Sends an alert when the current price is below target. |
| `Send Status Email` | Sends a status email when the price is not below target. |

## Import Steps

1. Open n8n and import `workflow/competitor-price-monitor.json`.
2. Open `Log Price Snapshot` and connect your Google Sheets credential.
3. Replace `YOUR_GOOGLE_SHEET_ID` with your spreadsheet ID.
4. Create a sheet named `Price Monitor` or update the node to match your tab name.
5. Create these columns: `Product Name`, `Price`, `Target Price`, `Alert Type`, `Currency`, `Timestamp`, `URL`.
6. Open the Gmail nodes and connect your Gmail credential.
7. Replace `price-alerts@example.com` with your alert recipient.
8. Activate the workflow and copy the production webhook URL.
9. Set `N8N_WEBHOOK_URL` in your runtime environment.

## Sheet Behavior

The workflow uses `URL` as the matching column. This keeps one latest row per tracked product URL. If you want historical rows for every check, switch the Google Sheets operation to append mode inside n8n.

## Public Export Notes

The workflow is intentionally exported without:

- n8n credential bindings
- webhook IDs
- private sheet URLs
- personal email addresses
- instance metadata
