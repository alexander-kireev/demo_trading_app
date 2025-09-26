from app.user.user_model import User
from app.user.user_service import (
    get_user_by_id
)

from pprint import pprint
from app.stock.stock_service import (
    live_stock_price
)
from app.db_core import DBCore

from app.portfolio.portfolio_model import Portfolio

from app.position.position_model import Position
from app.position.positions_model import Positions

from app.position.position_service import (
    aggregate_positions_of_single_equity,
    aggregate_all_equity_positions,
    aggregate_total_value_of_equity_positions
)

from app.position.position_repo import (
    get_user_positions_of_equity,
    get_user_single_position_of_equity,
    get_all_user_positions,
    get_user_equity_symbols,
    update_list_of_positions
)

# tested, functional, commented
def get_portfolio(user_id):
    """ Accepts a user_id and returns a portfolio object with NON-LIVE stock price data. """

    try:
        with DBCore.get_connection() as conn:
            with conn.cursor() as cur:
                
                # get user object
                user = get_user_by_id(cur, user_id)

                # ensure user is found
                if not user:
                    return {
                        "success": False,
                        "message": "Failed to fetch user."
                    }
                
                # check if user has any equities in positions table
                if equity_symbols := get_user_equity_symbols(cur, user_id):

                    # if they do, aggregate all positions into a single Position object
                    all_positions = aggregate_all_equity_positions(cur, user_id, equity_symbols)


                    # ensure positions are found
                    if not all_positions:
                        return {
                            "success": False,
                            "message": "Failed to aggregate positions."
                        }
                    
                    # get total value of all equities
                    total_equities_value = aggregate_total_value_of_equity_positions(all_positions)
                    
                    # ensure it is found
                    if not total_equities_value:
                        return {
                            "success": False,
                            "message": "Failed to tabulate total value of equities."
                        }

                    # instantiate portfolio object with equities and cash_balance
                    return Portfolio(user, total_equities_value, all_positions)

                # if user has no open equity positions, instantiate portfolio object with cash_balance only
                else:
                    return Portfolio(user)
                
    except Exception as e:
        return {
            "success": False,
            "message": f"Error. Failed to fetch portfolio: {e}."
        }


###
def get_live_portfolio(user_id):
    """ Accepts a user_id and returns the user's portfolio as an object with updated  """

    portfolio = get_portfolio(user_id)
    positions = portfolio.positions
    
    for position in positions:
        live_price = live_stock_price(positions[position].symbol)
        positions[position].price_per_share = live_price

    return portfolio

# TODO: IMPLEMENT THIS
def update_stocks_in_table(user_id):
    # fetch all user symbols of equities
    # for each equity, update its price 
    try:
        with DBCore.get_connection() as conn:
            with conn.cursor() as cur:

                symbols = get_user_equity_symbols(cur, user_id)

                symbols_with_live_prices = {}
                for symbol in symbols:
                    live_price = live_stock_price(symbol)
                    symbols_with_live_prices[symbol] = live_price

                
                positions = get_all_user_positions(cur, user_id)

                for position in positions:
                    symbol = position.symbol
                    live_price = symbols_with_live_prices[symbol]
                    new_total_value = position.number_of_shares * live_price
                    position.last_price_per_share = live_price
                    position.total_value = new_total_value
                
                if not update_list_of_positions(cur, positions):
                    return {
                        "success": False,
                        "message": "Failed to update list of positions in positions table."
                    }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error. Failed to update stock prices in table: {e}."
        }
            

    #
    return
    # update

# TODO: IMPLEMENT! or redundant, can update via instantiating a portfolio objecT?
def update_portfolio(user_id):
    #update stock prices
    #update balance?
    return 