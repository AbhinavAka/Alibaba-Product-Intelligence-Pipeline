# Alibaba-Product-Intelligence-Pipeline
Agentic web-scraping pipeline that crawls Alibaba industrial machinery product pages using AI agents, extracts structured product information, normalizes the data, and stores it in a database for downstream analytics and EDA. Built with CrewAI and Firecrawl,


How to run :-

1. Run the requirement.txt file and install all the dependencies 
2. Run the scrapper first it will collect the products unique id
3. After collecting sufficient amt of products_ids run the crawler file it will crawl each product page and scrape the data
4. The data is saved in the database so you might need to set up a postgres db I will share the scema of the tables also 
5. For now I have manually downloaded the data and ran some EDA steps.
6. Download the file in system and copy the path of the file and paste it in the jupyter notebook in file_path variable 
7. Run the whole file

^_^