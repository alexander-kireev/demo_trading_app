from app.db_core import DBCore

def define_trades_log_table():
    """ Creates the table trades_log, logging the trade history of all users.  """

    with DBCore.get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS trades_log (
                    trade_id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                    company_name VARCHAR(100) NOT NULL,
                    symbol VARCHAR(20) NOT NULL,
                    date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    price_per_share NUMERIC(10, 2) NOT NULL,
                    number_of_shares INTEGER NOT NULL CHECK (number_of_shares > 0),
                    transaction_total NUMERIC(12, 2) NOT NULL,
                    transaction_type VARCHAR(4) NOT NULL CHECK (transaction_type IN ('BUY', 'SELL'))
                );
            """)
    
        conn.commit()





