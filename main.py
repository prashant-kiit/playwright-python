import time
from playwright.sync_api import Page, sync_playwright
from dotenv import load_dotenv
import os

load_dotenv()

URL = os.getenv("URL")
HEADLESS = os.getenv("HEADLESS") == "true"
TIMEOUT = int(os.getenv("TIMEOUT"))

def run_task(page: Page, output: str):
    page.goto(URL, wait_until="load")

    page.wait_for_selector("input[placeholder='search craigslist']", state="visible", timeout=TIMEOUT)
    input_element = page.locator('input[placeholder="search craigslist"]')

    input_element.type("apartment")
    input_element.press("Enter")

    page.wait_for_selector('input[type="checkbox"][name="postedToday"]', state="visible", timeout=TIMEOUT)
    psoted_today_checkbox = page.locator('input[type="checkbox"][name="postedToday"]')
    psoted_today_checkbox.check()

    page.wait_for_selector("select[name='availabilityMode']", state="visible", timeout=TIMEOUT)
    availability_select = page.locator('select[name="availabilityMode"]')
    availability_select.select_option(label="within 30 days")

    filters_panel = page.locator(".cl-search-filters-panel")
    filters_panel.evaluate("(el) => { el.scrollTop = el.scrollHeight }")

    apply_button = page.locator('.cl-search-filters-panel button.cl-exec-search')
    apply_button.click()

    page.wait_for_selector("#search-results-1", state="visible", timeout=TIMEOUT)

    page.screenshot(path=output, full_page=True)

    time.sleep(2)

def main():
    try: 
        playwright = sync_playwright().start()

        browser = playwright.chromium.launch(headless=HEADLESS)
        browser_context_1 = browser.new_context(java_script_enabled=True)
        page1 = browser_context_1.new_page()

        browser_context_2 = browser.new_context(java_script_enabled=True)
        page2 = browser_context_2.new_page()

        run_task(page1, "page1.png")
        run_task(page2, "page2.png")
    except Exception as e:
        print(e)
    finally:
        # Explicitly closing page, browser, and Playwright is required for resource control in long-running or multi-job systems, 
        # even though Playwright auto-cleans on process exit.
        page1.close()
        page2.close()
        browser.close()
        playwright.stop()

if __name__ == "main":
    main()