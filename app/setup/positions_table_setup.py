from app.db_core import DBCore

def define_positions_table():
    """ Creates the table cataloging all open positions of all users. """

    with DBCore.get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS positions(
                    position_id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                    company_name VARCHAR(100) NOT NULL,
                    symbol VARCHAR(20) NOT NULL,
                    number_of_shares INTEGER NOT NULL,
                    average_price_per_share NUMERIC(10, 2) NOT NULL,
                    last_price_per_share NUMERIC(10, 2) NOT NULL,
                    position_total NUMERIC(12, 2) NOT NULL,
                    timestamp_opened TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP       
                );
            """)
    
        conn.commit()



