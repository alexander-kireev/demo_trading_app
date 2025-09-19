from app.db_core import DBCore

def define_users_table():
    """ Creates the table users, storing all user details. """
    
    with DBCore.get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users(
                    id SERIAL PRIMARY KEY,
                    first_name VARCHAR(50) NOT NULL,
                    last_name VARCHAR(50) NOT NULL,
                    dob DATE NOT NULL,
                    email VARCHAR(100) NOT NULL,
                    password_hash TEXT NOT NULL,
                    cash_balance NUMERIC(12,2) NOT NULL,
                    total_balance NUMERIC(12, 2) NOT NULL
                );
            """)
    
        conn.commit()


def main():
    try:
        define_users_table()
        print("Table users successfully defined.")
    except Exception as e:
        print(f"Error. Failed to define users table: {e}.")


if __name__ == '__main__':
    main()