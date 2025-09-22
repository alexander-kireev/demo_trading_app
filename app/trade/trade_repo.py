# tested, functional, commented
def log_trade(cur, trade):
    """ Accepts cursor and trade object, inserts trade into trades_log table. """

    cur.execute(
        """ INSERT INTO trades_log (
                user_id, 
                company_name, 
                symbol, 
                price_per_share,
                number_of_shares,
                trade_total,
                trade_type
        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            trade.user_id,
            trade.company_name,
            trade.symbol,
            trade.price_per_share,
            trade.number_of_shares,
            trade.trade_total,
            trade.trade_type
        ))
    return cur.rowcount > 0


    


