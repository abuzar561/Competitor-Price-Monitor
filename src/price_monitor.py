import argparse
import json
import os
import re
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any

import requests
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)


@dataclass
class PriceSnapshot:
    product_name: str
    price: float
    currency: str
    url: str
    target_price: float
    alert_type: str
    timestamp: str


def parse_price(raw_text: str) -> float:
    cleaned = raw_text.replace(",", "")
    match = re.search(r"(\d+(?:\.\d+)?)", cleaned)

    if not match:
        raise ValueError(f"Could not parse a numeric price from: {raw_text!r}")

    return float(match.group(1))


def create_driver(headless: bool = True) -> webdriver.Chrome:
    options = Options()

    if headless:
        options.add_argument("--headless=new")

    options.add_argument("--window-size=1440,1200")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument(f"user-agent={os.getenv('USER_AGENT', DEFAULT_USER_AGENT)}")
    options.page_load_strategy = "eager"

    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)


def scrape_price(url: str, selector: str, wait_seconds: int, headless: bool) -> float:
    driver = create_driver(headless=headless)

    try:
        driver.get(url)
        wait = WebDriverWait(driver, wait_seconds)
        element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
        return parse_price(element.text)
    except TimeoutException as error:
        raise RuntimeError(f"Timed out waiting for selector {selector!r}") from error
    finally:
        driver.quit()


def determine_alert_type(price: float, target_price: float) -> str:
    if price < target_price:
        return "price_drop"
    if price > target_price:
        return "price_increase"
    return "unchanged"


def send_to_webhook(webhook_url: str, payload: dict[str, Any]) -> None:
    response = requests.post(webhook_url, json=payload, timeout=30)
    response.raise_for_status()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Monitor a competitor product price and notify n8n.")
    parser.add_argument("--url", default=os.getenv("PRODUCT_URL"), help="Product page URL to monitor.")
    parser.add_argument("--selector", default=os.getenv("PRICE_SELECTOR"), help="CSS selector for the price element.")
    parser.add_argument("--product-name", default=os.getenv("PRODUCT_NAME", "Tracked Product"))
    parser.add_argument("--target-price", type=float, default=float(os.getenv("TARGET_PRICE", "999")))
    parser.add_argument("--currency", default=os.getenv("CURRENCY", "PKR"))
    parser.add_argument("--webhook-url", default=os.getenv("N8N_WEBHOOK_URL"))
    parser.add_argument("--wait-seconds", type=int, default=int(os.getenv("WAIT_SECONDS", "20")))
    parser.add_argument("--no-headless", action="store_true", help="Run Chrome with a visible browser window.")
    parser.add_argument("--dry-run", action="store_true", help="Print payload without sending it to n8n.")
    return parser


def main() -> None:
    args = build_parser().parse_args()

    if not args.url:
        raise SystemExit("Missing product URL. Provide --url or PRODUCT_URL.")

    if not args.selector:
        raise SystemExit("Missing price selector. Provide --selector or PRICE_SELECTOR.")

    price = scrape_price(
        url=args.url,
        selector=args.selector,
        wait_seconds=args.wait_seconds,
        headless=not args.no_headless,
    )

    snapshot = PriceSnapshot(
        product_name=args.product_name,
        price=price,
        currency=args.currency,
        url=args.url,
        target_price=args.target_price,
        alert_type=determine_alert_type(price, args.target_price),
        timestamp=datetime.now(timezone.utc).isoformat(),
    )
    payload = asdict(snapshot)

    print(json.dumps(payload, indent=2))

    if args.dry_run:
        return

    if not args.webhook_url:
        raise SystemExit("Missing n8n webhook URL. Provide --webhook-url or N8N_WEBHOOK_URL.")

    send_to_webhook(args.webhook_url, payload)
    print("Sent price snapshot to n8n.")


if __name__ == "__main__":
    main()
