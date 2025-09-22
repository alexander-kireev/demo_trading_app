from app.stock.stock_model import Stock

from app.position.position_model import Position
from app.position.positions_model import Positions

# POSSIBLY REDUNDANT, OR WILL HAVE TO REFACTOR TO USE SOME OTHER ARGS
def get_user_single_position_of_equity(cur, user_id, symbol):

    cur.execute(""" SELECT * FROM positions WHERE user_id=%s AND symbol=%s """, (user_id, symbol))

    row = cur.fetchone()

    # ensure query returned result
    if row:

        # unpack position
        (position_id, user_id, company_name, symbol, number_of_shares, 
        average_price_per_share, total_value) = row

        # refactor and return position as object Position
        stock = Stock(company_name=company_name, symbol=symbol, price=average_price_per_share)
        return Position(stock=stock, number_of_shares=number_of_shares, 
                        user_id=user_id, position_id=position_id, total_value=total_value)
    else:
        return None


# tested, functional, commented
def get_user_equity_symbols(cur, user_id):
    """ Accepts a cursor and user_id, returns list of unique symbols of stocks
        the user has open positions on. """

    cur.execute(""" 
        SELECT DISTINCT symbol FROM positions WHERE user_id=%s 
        """, (
        user_id,
        ))

    rows = cur.fetchall()
    symbols = []

    # unpack and fill list with symbols
    for row in rows:
        (symbol,) = row
        symbols.append(symbol)

    return symbols


# tested, functional, commented
def get_user_positions_of_equity(cur, user_id, symbol):
    """ Accepts cursor, user_id and symbol. Returns list of all open equity positions
        a user has of particular equity, as a list of object Position. """

    cur.execute(""" 
        SELECT * FROM positions WHERE user_id=%s AND symbol=%s ORDER BY position_id ASC 
        """, (
        user_id, 
        symbol
        ))
    
    rows = cur.fetchall()

    if not rows:
        return None
    
    positions = []

    for row in rows:
        # unpack each row returned
        (position_id, user_id, company_name, symbol, number_of_shares, 
        average_price_per_share, position_total, timestamp) = row

        # refactor into Stock and then Position objects
        stock = Stock(company_name=company_name, symbol=symbol, price=average_price_per_share)
        position = Position(stock=stock, number_of_shares=number_of_shares, user_id=user_id, 
                            position_id=position_id, total_value=position_total)

        positions.append(position)

    return positions


# tested, functional, commented
def close_position(cur, position):
    """ Accepts a cursor and position object, removes the position from table positions
        using position_id. """

    cur.execute(""" DELETE FROM positions WHERE position_id=%s """, (position.position_id,))
    
    return cur.rowcount > 0

# tested, functional, commented
def update_position(cur, position):
    """ Accepts cursor and position object, updates the shares and total of position
        using position_id. """

    cur.execute(""" 
        UPDATE positions SET number_of_shares=%s, position_total=%s WHERE position_id=%s 
    """, (
        position.number_of_shares,
        position.total_value,
        position.position_id
    ))

    return cur.rowcount > 0


# tested, functional, commented
def log_position(cur, position):
    """  Accepts a cursor and position object, inserts the position into 
         positions table. """

    cur.execute(""" 
        INSERT INTO positions (user_id, company_name, symbol, number_of_shares,
        average_price_per_share, position_total)
        VALUES (%s, %s, %s, %s, %s, %s) 
    """, (
        position.user_id,
        position.company_name,
        position.symbol,
        position.number_of_shares,
        position.price_per_share,
        position.total_value
    ))

    return cur.rowcount > 0