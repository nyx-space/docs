
from playwright.sync_api import sync_playwright
import time

def run(playwright):
    browser = playwright.chromium.launch()
    page = browser.new_page()
    time.sleep(5)  # Add a 5-second delay
    page.goto("http://127.0.0.1:8000")
    page.screenshot(path="homepage_screenshot.png")
    browser.close()

with sync_playwright() as playwright:
    run(playwright)
