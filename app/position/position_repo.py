from app.stock.stock_model import Stock

from app.position.position_model import Position
from app.position.positions_model import Positions

def get_user_single_position_of_equity(cur, user_id, symbol):
    cur.execute(""" SELECT * FROM positions WHERE user_id=%s AND symbol=%s """, (user_id, symbol))

    row = cur.fetchone()

    if row:
        (position_id, user_id, company_name, symbol, number_of_shares, 
        average_price_per_share, total_value) = row

        stock = Stock(company_name=company_name, symbol=symbol, price=average_price_per_share)
        return Position(stock=stock, number_of_shares=number_of_shares, 
                        user_id=user_id, position_id=position_id, total_value=total_value)
    else:
        return None


def get_user_equity_symbols(cur, user_id):
    cur.execute(""" 
        SELECT symbol FROM positions WHERE user_id=%s 
        """, (
        user_id
        ))

    rows = cur.fetchall()
    symbols = []

    for row in rows:
        (symbol,) = row
        symbols.append(symbol)

def get_user_positions_of_equity(cur, user_id, symbol):
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
        (position_id, user_id, company_name, symbol, number_of_shares, 
        average_price_per_share, total_value) = row

        stock = Stock(company_name=company_name, symbol=symbol, price=average_price_per_share)
        position = Position(stock=stock, number_of_shares=number_of_shares, user_id=user_id, 
                            position_id=position_id, total_value=total_value)

        positions.append(position)

    return Positions(positions, user_id, symbol)


def close_position(cur, position):
    cur.execute(""" DELETE FROM positions WHERE position_id=%s """, (position.position_id,))

    return cur.rowcount > 0


def update_position(cur, position):
    cur.execute(""" 
        UPDATE positions SET number_of_shares=%s, total_value=%s WHERE position_id=%s 
    """, (
        position.number_of_shares,
        position.total_value,
        position.position_id
    ))


def log_position(cur, position):
    cur.execute(""" 
        INSERT INTO positions (user_id, company_name, symbol, number_of_shares,
        average_price_per_share, position_total)
        VALUES (%s, %s, %s, %s, %s, %s) 
    """, (
        position.user_id,
        position.company_name,
        position.symbol,
        position.number_of_shares,
        position.average_price_per_share,
        position.total
    ))