from app.db_core import DBCore
from app.user.user_repo import (
    get_user_by_id,
    update_user_cash_balance
)
from trade_model import Trade
from trade_repo import (
    log_trade,
    get_user_single_holding,
    log_position
)

from app.position.position_model import Position

class TradeService:

    def buy_stock(self, user_id, stock, num_shares):
        """ Accepts stock object, number of shares to buy, user_id and updates the holdings
            and trades_log tables. """
        
        # get user_balance
        try:
            with DBCore.get_connection() as conn:
                with conn.cursor() as cur:

                    user = get_user_by_id(cur, user_id)

                    transaction_amount = stock.price * num_shares

                    if user.balance < transaction_amount:
                        return {
                            "success": False,
                            "message": "Insufficient cash balance to purchases shares."
                        }

                    trade = Trade(user_id=user_id, stock=stock, number_of_shares=num_shares,
                                transaction_type="BUY", transaction_total=transaction_amount)       


                    if not log_trade(cur):
                        return {
                            "success": False,
                            "message": "Failed to log trade."
                        }

                    if current_position := get_user_single_holding(user_id, stock.symbol):
                        # make new holding
                        new_position = Position(stock, trade.number_of_shares)

                    else:
                        # TODO: IMPLEMENT POSITION CLASS
                        new_position = Position(stock, trade.number_of_shares)

                    if not log_position(cur, new_position):
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
                      
        except Exception as e:
            return {
                "success": False,
                "message": f"Error. Failed to purchase shares: {e}."
            }
                
    # DOES NOT ALLOW FOR SHORT SELLING
    def sell_stock(self, stock, num_shares, user_id):

        """ accepts stock object, number of shares to sell, user id and sells the stock.
            DOES NOT ALLOW FOR SHORT SELLING """

        db = DB()

        try:

            # get user's current holding of this company
            current_holding = db.get_user_single_holding(user_id=user_id, symbol=stock.symbol)

            # if user DOES NOT have enough shares to sell
            if current_holding.number_of_shares < num_shares:
                print("Insufficient shares held to sell.")
                return False
            
            # if user DOES have enough shares to sell
            else:

                # instantiate trade object, log the trade
                trade = Trade(user_id=user_id, stock=stock, number_of_shares=num_shares, transaction_type="SELL")
                trade_id = db.log_trade(trade)

                # update the user's holding to reflect change. if the update fails, remove the trade from the log
                if not db.update_user_single_holding(user_id=user_id, trade=trade, current_holding=current_holding):
                    db.remove_trade(trade_id)
                    raise Exception
                
                # update user's balance to reflect sale
                db.update_user_balance(user_id, trade.transaction_total)
                
                return True
                
        except Exception as e:
            print(f"Error. Failed to liquidate shares: {e}.")



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

