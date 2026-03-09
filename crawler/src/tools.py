from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from firecrawl import Firecrawl
from firecrawl.types import ScrapeOptions
import os


class FirecrawlInput(BaseModel):
    product_url: str = Field(description="URL of the webpage to scrape")


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

            response = firecrawl.crawl(
                product_url,
                limit=1,
                scrape_options=ScrapeOptions(formats=['markdown'])
            )

            return response

        except Exception as e:
            return f"Firecrawl scraping failed: {str(e)}"