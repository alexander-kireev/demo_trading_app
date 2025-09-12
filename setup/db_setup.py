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



# define user table in db
def define_users_table():
    """ Creates the table users in DB. """

    with psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    ) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users(
                    id SERIAL PRIMARY KEY,
                    first_name VARCHAR(50) NOT NULL,
                    last_name VARCHAR(50) NOT NULL,
                    dob DATE NOT NULL,
                    email VARCHAR(100) NOT NULL,
                    password_hash TEXT NOT NULL,
                    balance NUMERIC(12,2) NOT NULL
                )
            """)
    
        conn.commit()


def main():
    try:
        define_users_table()
        print("setup_db.py executed")
    except:
        print("some error occured")


if __name__ == '__main__':
    main()