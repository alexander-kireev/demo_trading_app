from app.db_core import DBCore

def define_holdings_table():
    """ Creates the table cataloging all open positions of all users. """

    with DBCore.get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS all_holdings(
                    holding_id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                    company_name VARCHAR(100) NOT NULL,
                    symbol VARCHAR(20) NOT NULL,
                    number_of_shares INTEGER NOT NULL,
                    average_price_per_share NUMERIC(10, 2) NOT NULL,
                    holdings_total NUMERIC(12, 2) NOT NULL    
                );
            """)
    
        conn.commit()


def main():
    try:
        define_holdings_table()
        print("Table holdings successfully defined.")
    except Exception as e:
        print(f"Error. Failed to define holdings table: {e}.")


if __name__ == '__main__':
    main()
