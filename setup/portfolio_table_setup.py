import psycopg2
import os
from dotenv import load_dotenv

# load db
load_dotenv()
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")


def define_all_holdings_table():
    """ creates the table storing all holdings of all users in database """

    with psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    ) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS all_holdings(
                    holding_id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                    company_name VARCHAR(100) NOT NULL,
                    symbol VARCHAR(20) NOT NULL,
                    date_purchased DATE NOT NULL,
                    purchase_price NUMERIC(10, 2) NOT NULL,
                    shares INTEGER NOT NULL
                );
            """)
    
        conn.commit()


def main():
    try:
        define_all_holdings_table()
        print("define_all_holdings_table executed.")
    except Exception as e:
        print(f"Error. Could not execute define_all_holdings_table(): {e}.")


if __name__ == '__main__':
    main()
