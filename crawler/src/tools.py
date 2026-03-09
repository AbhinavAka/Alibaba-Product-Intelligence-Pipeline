from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from firecrawl import Firecrawl
from firecrawl.types import ScrapeOptions
import os


# This file defines the FirecrawlScraperTool, which is a custom tool for scraping web pages using the Firecrawl API. The tool takes a product URL as input and returns the scraped content in markdown format. It also includes error handling to manage any issues that arise during the scraping process.
class FirecrawlInput(BaseModel):
    product_url: str = Field(description="URL of the webpage to scrape")

# This tool uses the Firecrawl API to scrape the provided product URL and returns the content in markdown format. It handles any exceptions that may occur during the scraping process and provides an error message if the scraping fails.
class FirecrawlScraperTool(BaseTool):

    name: str = "Firecrawl Web Scraper"

    description: str = (
        "Visits a webpage using Firecrawl and returns clean markdown content. "
        "Useful for scraping product pages or listing pages."
    )

    args_schema: type[BaseModel] = FirecrawlInput

    def _run(self, product_url: str):

        try:
            firecrawl = Firecrawl(api_key=os.getenv("FIRECRAWL_API_KEY"))

            # Scrape the webpage and get markdown content
            response = firecrawl.crawl(
                product_url,
                limit=1,
                scrape_options=ScrapeOptions(formats=['markdown'])
            )

            return response

        except Exception as e:
            return f"Firecrawl scraping failed: {str(e)}"