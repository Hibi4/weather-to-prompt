import base64
from playwright.async_api import async_playwright

async def scrape_website(url: str) -> dict:
    """
    Scrapes the target URL using headless Chromium.
    Returns raw HTML, a base64 JPEG screenshot, and detected API calls.
    """
    detected_apis = set()

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={"width": 1440, "height": 900},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        )
        page = await context.new_page()

        # Listen to XHR/Fetch requests to help the AI deduce the backend
        def handle_request(request):
            if request.resource_type in ["xhr", "fetch"]:
                detected_apis.add(f"{request.method} {request.url[:100]}")

        page.on("request", handle_request)

        # Navigate to the page and wait for network to settle
        await page.goto(url, wait_until="domcontentloaded", timeout=45000)
        await page.wait_for_timeout(3000)  # Wait 3s for JS animations/frameworks

        # Capture compressed JPEG screenshot for the Vision LLM
        screenshot_bytes = await page.screenshot(type="jpeg", quality=60, full_page=False)
        screenshot_b64 = base64.b64encode(screenshot_bytes).decode("utf-8")

        # Extract rendered DOM
        raw_html = await page.content()

        await browser.close()

    return {
        "raw_html": raw_html,
        "screenshot_b64": screenshot_b64,
        "detected_apis": list(detected_apis)[:20]  # Keep top 20 API calls
    }