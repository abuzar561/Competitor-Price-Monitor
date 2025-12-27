# 🛒 Automated E-Commerce Price Monitor (Python + n8n)

An intelligent automation tool built to track product prices on dynamic e-commerce websites (like Daraz.pk) and send real-time alerts via n8n webhooks.

## 🚀 Project Overview
I wanted to track specific product prices (triggering alerts if the price rises above or drops below Rs. 999). However, standard HTTP requests often fail due to:
1. Dynamic JavaScript rendering (React.js).
2. Bot detection/Anti-scraping mechanisms.

**The Solution:** I built a Python script using **Selenium** to mimic real user behavior, extract the accurate price, and trigger an **n8n workflow** to log data to Google Sheets and send email alerts.

## 🛠️ Tech Stack
- **Python:** Core scripting language.
- **Selenium:** For headless browser automation and rendering JavaScript.
- **n8n:** For workflow automation (Webhook -> Google Sheets -> Email).
- **Windows Task Scheduler:** To run the script automatically every day.

## ⚙️ How It Works
1. **Scraping:** The script launches a headless Chrome browser with a custom mobile User-Agent.
2. **Extraction:** It navigates to the target URL, waits for the DOM to load, and extracts the current price using CSS Selectors and Regex.
3. **Logic:** It compares the detected price with the target price.
4. **Alerting:** If the data is valid, it sends a JSON payload to an n8n Webhook.

## 📦 Installation & Usage

1. **Clone the Repo**
   ```bash
   git clone [https://github.com/yourusername/price-monitor.git](https://github.com/yourusername/price-monitor.git)
   cd price-monitor
