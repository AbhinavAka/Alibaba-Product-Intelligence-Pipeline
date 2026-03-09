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

# This function saves the extracted product data into the database.
def save_data_in_db(product_id, products_data):

    for product in products_data:

        data = product.model_dump()

        product_url = data.get("url", "")
        product_name = data.get("product_name", "")
        machine_type = data.get("machine_type", "")
        model = data.get("model", "")
        brand = data.get("brand", "")
        power = data.get("power", "")
        capacity = data.get("capacity", "")
        price = data.get("price", "")
        min_order = data.get("min_order", "")
        supplier_name = data.get("supplier_name", "")
        supplier_type = data.get("supplier_type", "")
        rating = data.get("rating", "")
        years_in_business = data.get("years_in_business", "")
        city = data.get("city", "")
        state = data.get("state", "")
        delivery_time = data.get("delivery_time", "")
        warranty = data.get("warranty", "")
        platform = data.get("platform", "")
        scrape_date = data.get("scrape_date", "")


    query1 = """
        INSERT INTO product_details (product_id, product_url, product_name, machine_type, model, brand, power, capacity, price, min_order, supplier_name, supplier_type, rating, years_in_business, city, state, delivery_time, warranty, platform, scrape_date)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (product_id, product_url, product_name, machine_type, model, brand, power, capacity, price, min_order, supplier_name, supplier_type, rating, years_in_business, city, state, delivery_time, warranty, platform, scrape_date)

    query2 = """
        UPDATE product_id_tracker
        SET crawled = TRUE
        WHERE product_id = %s
    """, (product_id,)

    try:

        # Execute both queries within the same transaction to ensure data integrity.
        with create_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as curr:
                curr.execute(*query1)
                curr.execute(*query2)
                conn.commit()

    except Exception as e:
        print(f"Error saving data for product_id {product_id}: {str(e)}")
        conn.rollback()
        
    finally:
        if conn is not None:
            conn.close()