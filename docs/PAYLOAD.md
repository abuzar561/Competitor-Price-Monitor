# Payload Contract

The Python scraper sends one JSON object to the n8n webhook for each price check.

## Fields

| Field | Type | Description |
| --- | --- | --- |
| `product_name` | string | Human-friendly product name. |
| `price` | number | Current parsed price. |
| `currency` | string | Currency label used in logs and emails. |
| `url` | string | Product URL that was checked. |
| `target_price` | number | Threshold used for the alert decision. |
| `alert_type` | string | `price_drop`, `price_increase`, or `unchanged`. |
| `timestamp` | string | UTC ISO-8601 timestamp from the scraper. |

## Example

```json
{
  "product_name": "Competitor Product",
  "price": 899,
  "currency": "PKR",
  "url": "https://example.com/product",
  "target_price": 999,
  "alert_type": "price_drop",
  "timestamp": "2026-05-02T08:00:00+00:00"
}
```

## n8n Mapping

The workflow maps the payload into these Google Sheets columns:

| Sheet Column | Payload Expression |
| --- | --- |
| `Product Name` | `body.product_name` |
| `Price` | `body.price` |
| `Target Price` | `body.target_price` |
| `Alert Type` | `body.alert_type` |
| `Currency` | `body.currency` |
| `Timestamp` | `body.timestamp` |
| `URL` | `body.url` |
