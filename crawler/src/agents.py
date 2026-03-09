from textwrap import dedent
from crewai import LLM, Agent
from dotenv import load_dotenv
from src.tools import FirecrawlScraperTool
import os


load_dotenv()

# Initialize the LLM.
llm = LLM(
    model=os.getenv("OPENAI_MODEL_NAME"),
    temperature=0.1
)

# This file defines the AlibabaCrawler class, which contains two methods: crawler_agent and formatter_agent. The crawler_agent method creates an agent that is responsible for crawling Alibaba product pages using the Firecrawl tool and extracting raw product information. The formatter_agent method creates an agent that formats the extracted product information into a structured JSON format that matches a predefined schema. Both agents are designed to work together in a workflow where the crawler agent extracts data and the formatter agent structures it for further use.
class AlibabaCrawler:
    
    def crawler_agent(self):

        Firecrawl_Scraper_Tool = FirecrawlScraperTool()

        "This is the Agent for crawling the Alibaba Website"
        return Agent(
            role = "Alibaba Product Information Extractor",
            goal=dedent("""
                Visit Alibaba product pages using the Firecrawl tool and extract raw product information from the generated
                markdown content.
            """),   

            backstory = dedent("""
                You are an expert web scraping specialist focused on Alibaba industrial machinery product pages.

                Your job is to visit the provided product page URL, use the Firecrawl tool to scrape the page, generate
                markdown content, and extract relevant product specifications, supplier details, and pricing information.

                Ignore navigation menus, advertisements, and unrelated sections.   
                """),
            allow_delegation = False,
            verbose = True,
            tools = [Firecrawl_Scraper_Tool],
            llm = llm

        )
    
    def formatter_agent(self):
        "This the agent which format the output given by the crawler agent"
        return Agent(
            role="Industrial Machinery Data Structuring Specialist",

            goal=dedent("""
                Convert extracted product information into a structured JSON format that matches the
                industrial machinery product schema.
            """),

            backstory=dedent("""
                You are a data engineer responsible for converting unstructured product data into clean structured
                datasets.

                Your output must strictly follow the required Pydantic schema and contain no explanations.
            """), 
            allow_delegation = False,
            verbose = True,
            llm = llm
        )