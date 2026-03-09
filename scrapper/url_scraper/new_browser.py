# This file defines a function to start a Playwright browser instance. The start_browser function launches a Chromium browser in non-headless mode, creates a new browser context, and opens a new page. It returns the browser, context, and page objects for further use in web scraping tasks.
def start_browser(playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    return browser, context, page