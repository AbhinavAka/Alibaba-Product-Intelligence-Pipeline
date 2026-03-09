from playwright.sync_api import Playwright, sync_playwright
import time
import random

from url_scraper.new_browser import start_browser
from url_scraper.data_saver import save_product_data

def run(playwright: Playwright) -> None:
    SL = random.uniform(8, 10)
    time.sleep(SL)

    while True:
        try:

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

                cards = page.locator("//div[@data-product_id]")
                count_ids = cards.count()

                for count in range(count_ids):
                    product_id = cards.nth(count).get_attribute("data-product_id")
                    if product_id:
                        batch.append(product_id)

                if len(batch) >= 100:
                    save_product_data(batch[:100])
                    batch = batch[100:]

                else:
                    continue

        except Exception as e:
            print(f"Error: {str(e)}")
            continue

with sync_playwright() as playwright:
    run(playwright)
