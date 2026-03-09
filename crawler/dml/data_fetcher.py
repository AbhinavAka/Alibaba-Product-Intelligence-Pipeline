import psycopg2
from psycopg2.extras import RealDictCursor
import os


# This file defines functions for saving extracted product data into a PostgreSQL database. It includes a function to create a database connection and a function to save product data based on a given product ID. The save_data_in_db function takes the product ID and the extracted product data, structures it according to the expected schema, and executes SQL queries to insert the data into the product_details table and update the product_id_tracker table to mark the product as crawled.
def create_connection():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT")
    )
    return conn

# This function fetches product IDs that have not been crawled yet.
def fetch_product_data():

    try:

        query = "SELECT product_id FROM product_id_tracker WHERE crawled = FALSE"

        with create_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as curr:
                curr.execute(query)
                results = curr.fetchall()
                return [row["product_id"] for row in results]
        
            
    except Exception as e:
        print(f"Error fetching product data: {str(e)}")
        return []

    finally:
        if conn is not None:
            conn.close()
