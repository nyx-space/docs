from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('http://127.0.0.1:8000')
    page.screenshot(path='jules-scratch/verification/staggered_layout.png')
    browser.close()
