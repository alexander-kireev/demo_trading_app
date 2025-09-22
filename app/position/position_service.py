
from app.position.position_repo import (
    get_user_equity_symbols,
    get_user_positions_of_equity,
    get_user_single_position_of_equity
)
from app.stock.stock_model import Stock

from app.position.position_model import Position

# tested, functional, commented
def aggregate_positions_of_single_equity(cur, user_id, symbol):
    """ Accepts a cursor, user_id and symbol of equity. Queries positions
        table for ALL positions of this equity. Then, calculates the total
        number of shares held of this equity, the average price per share of
        this equity and the total value of all the shares. Returns a dictionary
        containing this information. """

    # gets a list of objects of class Position
    # (all positions held by user of certain equity as a list of objects)
    positions = get_user_positions_of_equity(cur, user_id, symbol)

    # set counters
    total_shares = 0
    total_position_value = 0

    # calculate how many shares user owns and their total value
    for position in positions:
        total_shares += position.number_of_shares
        total_position_value += position.total_value

    # get average price per share
    company_name = positions[0].company_name
    average_price_per_share = total_position_value / total_shares
    
    # refactor data into stock and position objects, return position object
    stock = Stock(company_name=company_name, symbol=symbol, price=average_price_per_share)
    return Position(stock=stock, number_of_shares=total_shares, user_id=user_id,
                    total_value=total_position_value)


# tested, functional, commented
def aggregate_all_equity_positions(cur, user_id, equity_symbols):
    """ Accepts a cursor, user_id and list of symbols of equities owned by the user.
        It then calculates how many shares of each equity the user has, the average
        price per share and the total value of a holding. It stores these values in a
        dictionary. The function does this for EVERY symbol of equity provided,
        storing the resulting dictionary in a dictionary, with each equity accessed
        by its symbol. """

    # empty dictionary to store resulting dictionaries
    positions = {}

    # aggregate positions of an equity, for every symbol provided
    for symbol in equity_symbols:

        # store the resulting dictionary in a dictionary of dictionaries, accessed by symbol
        positions[symbol] = aggregate_positions_of_single_equity(cur, user_id, symbol)
        
    return positions


# tested, functional, commented
def aggregate_total_value_of_equity_positions(positions):
    """ Accepts dictionary of position objects, which can be accessed via
        their symbol, calculates the total value of positions, returns it
        as a float. """

    total_equities_value = 0
    for symbol in positions:
        total_equities_value += positions[symbol].total_value

    return float(total_equities_value)

