from app.db_core import DBCore
from app.user.user_repo import (
    get_user_by_id,
    update_user_cash_balance
)

from app.user.user_model import User

from trade_model import Trade
from trade_repo import (
    log_trade,

)

from app.position.position_model import Position
from app.position.positions_model import Positions

from app.position.position_repo import (
    get_user_single_position_of_equity,
    get_user_positions_of_equity,
    log_position,
    close_position,
    update_position
    
)

class TradeService:

    def buy_stock(self, user_id, stock, number_of_shares):
        """ Accepts stock object, number of shares to buy, user_id and updates the holdings
            and trades_log tables. """
        
        # get user_balance
        try:
            with DBCore.get_connection() as conn:
                with conn.cursor() as cur:

                    user = get_user_by_id(cur, user_id)

                    transaction_amount = stock.price * number_of_shares

                    if user.balance < transaction_amount:
                        return {
                            "success": False,
                            "message": "Insufficient cash balance to purchases shares."
                        }

                    trade = Trade(user_id=user_id, stock=stock, number_of_shares=number_of_shares,
                                transaction_type="BUY", transaction_total=transaction_amount)       

                    if not log_trade(cur, trade):
                        return {
                            "success": False,
                            "message": "Failed to log trade."
                        }
                
                    position = Position(stock, number_of_shares)

                    if not log_position(cur, position):
                        return {
                            "success": False,
                            "message": "Failed to log position."
                        }
                    
                    new_cash_balace = user.cash_balance - transaction_amount
                    if not update_user_cash_balance(user_id, new_cash_balace):
                        return {
                            "success": False,
                            "message": "Failed to update user cash balance."
                        }           

                    conn.commit()

                    return {
                        "success": True,
                        "message": "Shares successfully purchased."
                    }                 
                      
        except Exception as e:
            return {
                "success": False,
                "message": f"Error. Failed to purchase shares: {e}."
            }
                

    def sell_stock(self, stock, number_of_shares, user_id):

        """ Accepts stock object, number of shares to sell and user_id. Ensures user has
            sufficient long position(s) open to sell desired number of shares. This function
            DOES NOT allow for short selling. """

        try:
            with DBCore.get_connection() as conn:
                with conn.cursor() as cur:

                    positions = get_user_positions_of_equity(cur, user_id, stock.symbol)

                    if number_of_shares > positions.total_number_of_shares:
                        return {
                            "success": False,
                            "message": "Insufficient shares to sell."
                        }


                    transaction_type = "SELL"
                    total_value_shares_sold = 0

                    position_number = 0

                    while number_of_shares > 0: 
                        # get earliest opened position
                        first_position = positions.positions[position_number]
                        # if number_of_shares > trade.number_of_shares
                        if number_of_shares > first_position.number_of_shares:
                            max_number_of_shares_for_trade = first_position.number_of_shares
                        else:
                            max_number_of_shares_for_trade = number_of_shares

                        trade = Trade(user_id, stock, max_number_of_shares_for_trade, transaction_type)

                        

                        if not log_trade(cur, trade):
                            return {
                                "success": False,
                                "message": "Failed to log trade."
                            }
                        
                        if first_position.number_of_shares - number_of_shares < 1:

                            if not close_position(cur, first_position):
                                return {
                                    "success": False,
                                    "message": "Failed to close position."
                                }
                        
                        else:
                            
                            updated_number_of_shares = first_position.number_of_shares - number_of_shares
                            updated_total_value = updated_number_of_shares * first_position.price_per_share

                            first_position.number_of_shares = updated_number_of_shares
                            first_position.total_value = updated_total_value

                            if not update_position(cur, first_position):
                                return {
                                    "success": False,
                                    "message": "Insufficient shares to sell."
                                }
                            
                        number_of_shares -= max_number_of_shares_for_trade
                        total_value_shares_sold += first_position.total_value

                        position_number += 1
                    
                    user = get_user_by_id(cur, user_id)

                    new_user_cash_balance = user.cash_balance + total_value_shares_sold

                    if not update_user_cash_balance(cur, user_id, new_user_cash_balance):
                        return {
                            "success": False,
                            "message": "Failed to update user cash balance."
                        }

                    conn.commit()

                    return {
                            "success": True,
                            "message": "Shares successfully sold."
                        }
           
        except Exception as e:
            return {
                "success": False,
                "message": (f"Error. Failed to sell shares: {e}.")
            }







if __name__ == "__main__":

    pass

    ## init stock
    # company_name = "apple"
    # symbol = "aapl"
    # price = 125.8
    # appl_stock = Stock(company_name, symbol, price)

    # # init trade
    # user_id = 1
    # number_of_shares = 1
    # transaction_type = "SELL"

    # ts = TradingService()
    # ts.sell_stock(stock=appl_stock, num_shares=number_of_shares, user_id=user_id)
    # # ts.sell_stock(stock=appl_stock, num_shares=3, user_id=user_id)

