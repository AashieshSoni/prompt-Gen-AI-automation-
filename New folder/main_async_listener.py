import asyncio
import json
import os
import logging
from datetime import datetime
from logging.handlers import RotatingFileHandler
from playwright.async_api import async_playwright

TARGET_DOMAIN = "https://automation.us7.map.net/api/customerapi"
OUTPUT_DIR = "captured_xh"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# -----------------------------
# Logging Configuration
# -----------------------------
LOG_FILE = "listener.log"

logger = logging.getLogger("XHRListener")
logger.setLevel(logging.INFO)

handler = RotatingFileHandler(
    LOG_FILE,
    maxBytes=5 * 1024 * 1024,   # 5 MB per file
    backupCount=5               # keep last 5 logs
)
formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(message)s"
)
handler.setFormatter(formatter)
logger.addHandler(handler)


# -----------------------------
# Helpers
# -----------------------------
def timestamp():
    return datetime.now().strftime("%Y%m%d_%H%M%S_%f")


async def save_json_with_retry(data, filename, retries=3, delay=0.5):
    """
    Async JSON writer with retry support.
    """
    path = os.path.join(OUTPUT_DIR, filename)

    for attempt in range(1, retries + 1):
        try:
            # Safe synchronous file write wrapped in thread executor
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(
                None,
                lambda: json.dump(data, open(path, "w", encoding="utf-8"), indent=4)
            )

            logger.info(f"Saved {filename} (attempt {attempt})")
            return True

        except Exception as e:
            logger.error(f"Failed to save {filename} on attempt {attempt}: {e}")

            if attempt < retries:
                await asyncio.sleep(delay)
            else:
                logger.error(f"Giving up on {filename} after {retries} retries.")
                return False


# -----------------------------
# Request Handler
# -----------------------------
async def handle_request(request):
    url = request.url
    if not url.startswith(TARGET_DOMAIN):
        return

    method = request.method
    headers = request.headers

    try:
        post_data = request.post_data_json
    except:
        post_data = request.post_data

    filename = f"Request-{method}_{timestamp()}.json"

    req_json = {
        "url": url,
        "method": method,
        "headers": headers,
        "payload": post_data,
    }

    logger.info(f"[REQUEST] Capturing {method} {url}")
    await save_json_with_retry(req_json, filename)


# -----------------------------
# Response Handler
# -----------------------------
async def handle_response(response):
    url = response.url
    if not url.startswith(TARGET_DOMAIN):
        return

    try:
        body = await response.json()
    except:
        body = await response.text()

    headers = await response.all_headers()
    status = response.status

    filename = f"Response-{status}_{timestamp()}.json"

    res_json = {
        "url": url,
        "status": status,
        "headers": headers,
        "body": body,
    }

    logger.info(f"[RESPONSE] Capturing {status} {url}")
    await save_json_with_retry(res_json, filename)


# -----------------------------
# Main Runner
# -----------------------------
async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        page.on("request", lambda req: asyncio.create_task(handle_request(req)))
        page.on("response", lambda res: asyncio.create_task(handle_response(res)))

        logger.info(f"🚀 Listener started for: {TARGET_DOMAIN}")
        await page.goto("https://automation.us7.map.net")

        # Run listener for 1 hour
        await asyncio.sleep(3600)

        logger.info("⏹ Listener session ended.")
        await context.close()
        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
