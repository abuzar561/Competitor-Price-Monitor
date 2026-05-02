# Troubleshooting

## Selenium Cannot Start Chrome

- Make sure Google Chrome is installed.
- Update Chrome to a current version.
- Delete any stale local ChromeDriver binary and run again so `webdriver-manager` can download a matching version.

## Price Selector Times Out

- Confirm the selector still exists on the page.
- Increase `WAIT_SECONDS`.
- Run with `--no-headless` to see what the browser renders.
- Check whether the page requires region selection, login, age gates, or cookie consent.

## Parsed Price Is Incorrect

- Choose a selector that contains only the current price.
- Avoid parent containers that include old prices, discounts, ratings, or shipping text.
- Test with `--dry-run` until the payload is correct.

## n8n Does Not Receive Data

- Use the production webhook URL, not the test URL, when running outside the n8n editor.
- Confirm `N8N_WEBHOOK_URL` is set.
- Check n8n execution logs for validation or credential errors.

## Google Sheets or Gmail Fails

- Reconnect credentials inside n8n after importing the workflow.
- Replace `YOUR_GOOGLE_SHEET_ID` with your own sheet ID.
- Replace `price-alerts@example.com` with the alert recipient.
- Confirm the sheet has columns matching the workflow mapping.
