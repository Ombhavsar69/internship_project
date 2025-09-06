import psycopg2
from psycopg2 import sql
import yaml
from dotenv import load_dotenv
from threading import Thread
load_dotenv()

# DB_CONFIG = {
#     "host": os.getenv("host"),
#     "dbname": os.getenv("database"),
#     "user": 'postgres',
#     "password":os.getenv("password"),
#     "port": 5432
# }

USERS_DATA = [
    (1, "Alice", "alice@example.com"),
    (2, "Bob", "bob@example.com"),
    (3, "Charlie", "charlie@example.com"),
    (4, "David", "david@example.com"),
    (5, "Eve", "eve@example.com"),
    (6, "Frank", "frank@example.com"),
    (7, "Grace", "grace@example.com"),
    (8, "Alice", "alice@example.com"),
    (9, "Henry", "henry@example.com"),
    (10, None, "jane@example.com"),
]

PRODUCTS_DATA = [
    (1, "Laptop", 1000.00),
    (2, "Smartphone", 700.00),
    (3, "Headphones", 150.00),
    (4, "Monitor", 300.00),
    (5, "Keyboard", 50.00),
    (6, "Mouse", 30.00),
    (7, "Laptop", 1000.00),
    (8, "Smartwatch", 250.00),
    (9, "Gaming Chair", 500.00),
    (10, "Earbuds", -50.00),
]

ORDERS_DATA = [
    (1, 1, 1, 2),
    (2, 2, 2, 1),
    (3, 3, 3, 5),
    (4, 4, 4, 1),
    (5, 5, 5, 3),
    (6, 6, 6, 4),
    (7, 7, 7, 2),
    (8, 8, 8, 0),
    (9, 9, 1, -1),
    (10, 10, 11, 2),
]

with open("config.yml", "r") as f:
    config = yaml.safe_load(f)

DB_CONFIG = config["db_config"]

def get_connection():
    """Connection for PostgreSQL with credentials from config.yml"""
    return psycopg2.connect(**DB_CONFIG)

def create_tables():
    """Create the required tables oonly if they do not exist"""
    queries = [
        """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name TEXT,
            email TEXT
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS products (
            id SERIAL PRIMARY KEY,
            name TEXT,
            price NUMERIC
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS orders (
            id SERIAL PRIMARY KEY,
            user_id INT,
            product_id INT,
            quantity INT
        );
        """
    ]

    conn = get_connection()
    cur = conn.cursor()
    for query in queries:
        cur.execute(query)
    conn.commit()
    cur.close()
    conn.close()
    print("Tables created successfully.")

def insert_data_if_it_does_not_exists(table, data):
    """Insert rows into the table only if the id do not exists"""
    conn = get_connection()
    cur = conn.cursor()

    for row in data:
        row_id = row[0]
        cur.execute(sql.SQL("SELECT id FROM {} WHERE id = %s").format(sql.Identifier(table)), (row_id,))
        exists = cur.fetchone()
        if not exists:
            placeholders = ", ".join(["%s"] * len(row))
            cur.execute(
                sql.SQL("INSERT INTO {} VALUES ({})").format(
                    sql.Identifier(table),
                    sql.SQL(placeholders)
                ), row
            )
            print(f"Inserted into {table}: {row}")
        else:
            print(f"skipping duplicates {row_id} in {table}")

    conn.commit()
    cur.close()
    conn.close()

def validate_data():
    """as the data in some fields was missing so added validation logic to alert"""
    print("validation of data")
    # For users
    for user in USERS_DATA:
        if not user[1]:  
            print(f"Invalid user : {user}")

    # for products
    for product in PRODUCTS_DATA:
        if product[2] < 0:
            print(f"Invalid product price: {product}")

    # for orders
    for order in ORDERS_DATA:
        if order[3] <= 0:
            print(f"Invalid order quantity: {order}")

def initialize_database_concurrent():
    """uses threading to process request parallely saves time"""
    create_tables()

    threads = [
        Thread(target=insert_data_if_it_does_not_exists, args=("users", USERS_DATA)),
        Thread(target=insert_data_if_it_does_not_exists, args=("products", PRODUCTS_DATA)),
        Thread(target=insert_data_if_it_does_not_exists, args=("orders", ORDERS_DATA)),
    ]

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    validate_data()

if __name__ == "__main__":
    initialize_database_concurrent()
