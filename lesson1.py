import time
from playwright.sync_api import sync_playwright

URL = "https://sfbay.craigslist.org/"

playwright = sync_playwright().start()

browser = playwright.chromium.launch(headless=False)

page = browser.new_page(java_script_enabled=True)

page.goto(URL, wait_until="load")

time.sleep(10)

# Explicitly closing page, browser, and Playwright is required for resource control in long-running or multi-job systems, 
# even though Playwright auto-cleans on process exit.”
page.close()
browser.close()
playwright.stop()