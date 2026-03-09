from textwrap import dedent
from crewai import Task
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class Product(BaseModel):

    product_name: Optional[str]
    machine_type: Optional[str]
    model: Optional[str]
    brand: Optional[str]
    power: Optional[str]
    capacity: Optional[str]
    price: Optional[str]
    min_order: Optional[str]
    supplier_name: Optional[str]
    supplier_type: Optional[str]
    rating: Optional[str]
    years_in_business: Optional[str]
    city: Optional[str]
    state: Optional[str]
    delivery_time: Optional[str]
    warranty: Optional[str]
    url: Optional[str]
    platform: str
    scrape_date: str

class TaskOutput(BaseModel):
    products: List[Product]

class IndustrialMachineryTasks:

    def __init__(self, agent, product_url):
     
        self.product_url = product_url
        self.agent = agent

    def crawl_alibaba_task(self, agent):

        return Task(

            description=dedent(f"""
                Visit the following Alibaba product page:

                URL:
                {self.product_url}

                Use the Firecrawl tool to scrape the webpage and generate markdown content.

                From the markdown, extract the following information:

                PRODUCT DETAILS
                - product_name
                - machine_type
                - model
                - brand
                - power
                - capacity
                - price
                - min_order

                SUPPLIER DETAILS
                - supplier_name
                - supplier_type
                - rating
                - years_in_business

                LOCATION & LOGISTICS
                - city
                - state
                - delivery_time
                - warranty

                Focus on sections like:
                - Product title
                - Key attributes
                - Specifications
                - Supplier information
                - Pricing tiers
                - Lead time

                Ignore:
                - navigation menus
                - ads
                - related searches
                - icons/images
                """ ), 
                
                expected_output=dedent(""" 
                    A clean textual summary of extracted product specifications, supplier details, and logistics
                    information from the scraped markdown. 
                """ ), 
                    
                agent = agent, 
                verbose=True
                )
    
    def format_data_task(self, agent, crawl_task):

        today = datetime.now().strftime("%Y-%m-%d")

        return Task(

            description=dedent(f"""
                Convert the extracted product information into
                structured JSON format.

                Use ONLY the information from the previous task.

                Fill the following schema fields:

                PRODUCT DETAILS
                - product_name
                - machine_type
                - model
                - brand
                - power
                - capacity
                - price
                - min_order

                SUPPLIER DETAILS
                - supplier_name
                - supplier_type
                - rating
                - years_in_business

                LOCATION & LOGISTICS
                - city
                - state
                - delivery_time
                - warranty

                META DATA
                - url = {self.product_url}
                - platform = Alibaba
                - scrape_date = {today}

                If information is missing return null.

                RULES:
                - If data is missing, use null
                - Never invent information
                - Normalize formats where possible
                - Keep original currency format

                IMPORTANT FORMATTING RULES:

                - If price contains multiple tiers, convert them into ONE string.
                Example:
                "1 set: $27,500 | 2-4 sets: $25,500 | >=5 sets: $21,500"

                - If delivery time contains tiers, convert them into ONE string.
                Example:
                "1 set: 45 days | 2 sets: 60 days | >2 sets: Negotiable"

                - ALL fields must be strings OR null
                - DO NOT return dictionaries or lists
            """),

            expected_output=dedent(f"""
                    Return all products in JSON format inside "products" array.
                    Do not include explanations.

                    {{
                        "products":[
                            {{
                                "product_name": null,
                                "machine_type": null,
                                "model": null,
                                "brand": null,
                                "power": null,
                                "capacity": null,
                                "price": null,
                                "min_order": null,
                                "supplier_name": null,
                                "supplier_type": null,
                                "rating": null,
                                "years_in_business": null,
                                "city": null,
                                "state": null,
                                "delivery_time": null,
                                "warranty": null,
                                "url": "{self.product_url}",
                                "platform": "Alibaba",
                                "scrape_date": "{today}"
                            }}
                        ]
                    }}
                """),
            agent=agent,
            context=[crawl_task],
            output_json=TaskOutput,
            verbose=True
        )