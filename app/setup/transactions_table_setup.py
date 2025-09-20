from app.db_core import DBCore

def define_transactions_table():
    """ Creates the table logging all cash deposits and withdrawls of users. """

    with DBCore.get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS transactions(
                    transaction_id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                    amount NUMERIC(12, 2) NOT NULL,
                    transaction_type VARCHAR(8) NOT NULL CHECK (transaction_type IN ('DEPOSIT', 'WITHDRAW')),
                    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP    
                );
            """)
    
        conn.commit()


def main():
    try:
        define_transactions_table()
        print("Table transactions successfully defined.")
    except Exception as e:
        print(f"Error. Failed to define transactions table: {e}.")


if __name__ == '__main__':
    main()
