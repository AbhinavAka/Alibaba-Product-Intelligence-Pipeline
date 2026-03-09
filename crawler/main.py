from crewai import Crew, Process
from src.agents import AlibabaCrawler
from src.task import IndustrialMachineryTasks, TaskOutput
from dml.data_fetcher import fetch_product_data
from dml.data_saver import save_data_in_db


def main_crew(product_url):

    try:
        # Initialize the agent class
        agents = AlibabaCrawler()

        # Initialize task class
        tasks = IndustrialMachineryTasks(agent=None, product_url = product_url)

        # Creating agents
        alibaba_crawler_agent = agents.crawler_agent()
        output_formatter_agent = agents.formatter_agent()

        # Creating tasks
        alibaba_crawler_agent_task = tasks.crawl_alibaba_task(alibaba_crawler_agent)
        output_formatter_agent_task = tasks.format_data_task(output_formatter_agent, alibaba_crawler_agent_task)

        # Initialize Crew with agents and tasks
        crew = Crew(
            agents = [alibaba_crawler_agent, output_formatter_agent],
            tasks = [alibaba_crawler_agent_task, output_formatter_agent_task],
            verbose = True,
            process = Process.sequential,
            max_rpm = 29
        ) 

        # Kickoff the Crew and get results
        result = crew.kickoff()
        output = result.raw
        parsed_output = TaskOutput.parse_raw(output)

        return parsed_output

    except Exception as e:
        print(f"error:{str(e)}")

if __name__ == "__main__": 
    
    # Fetch product IDs from the database
    data = fetch_product_data()

    for product_id in data:
        print(f"Processing product_id: {product_id}")
        product_url = f"https://www.alibaba.com/product-detail/_{product_id}.html"

        # Call the main crew function
        result = main_crew(product_url)
        if result and result.products:

            # Save the extracted data back to the database
            save_data_in_db(product_id, result.products)
            print(f"Data for product_id {product_id} saved successfully.")
