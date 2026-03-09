from playwright.sync_api import Playwright, sync_playwright
import time
import random

from url_scraper.new_browser import start_browser
from url_scraper.data_saver import save_product_data


# This file defines a web scraping script that uses Playwright to scrape product IDs from Alibaba's industrial machinery category pages. The script launches a browser, navigates through multiple pages of product listings, extracts product IDs from the page's HTML structure, and saves the extracted product IDs into a database using the save_product_data function. The script includes error handling to ensure that it continues running even if it encounters issues while scraping or saving data.
def run(playwright: Playwright) -> None:
    SL = random.uniform(8, 10)
    time.sleep(SL)

    while True:
        try:

            # Start the browser and navigate to the target URL.
            browser, context, page = start_browser(playwright)
            base_url = "https://www.alibaba.com/showroom/industrial-machinery"
            batch = []

            for page_num in range(1,100):

                if page_num == 1:
                    url = f"{base_url}.html"

                else:
                    url = f"{base_url}_{page_num}.html"

                print(f"Scraping {url}")
                
                page.goto(url, wait_until="domcontentloaded")

                # Extract product IDs from the page using the specified locator for product cards.
                cards = page.locator("//div[@data-product_id]")
                count_ids = cards.count()

                for count in range(count_ids):
                    product_id = cards.nth(count).get_attribute("data-product_id")
                    if product_id:

                        # Append the product ID to the batch list for later saving.
                        batch.append(product_id)

                if len(batch) >= 100:

                    # Save the batch of product IDs to the database and clear the batch list for the next set of IDs.
                    save_product_data(batch[:100])
                    batch = batch[100:]

                else:
                    continue

        except Exception as e:
            print(f"Error: {str(e)}")
            continue

with sync_playwright() as playwright:
    run(playwright)
