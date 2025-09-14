from db import DB
from user_model import User
from stock_model import Stock
from trade_model import Trade

class TradingService:

    def buy_stock(self, stock, num_shares, user_id):

        """ accepts stock object, number of shares to buy, user id and buys the stock """
        # get user_balance
        db = DB()
        user = db.get_user_by_id(user_id)

        transaction_amount = stock.price * num_shares

        if user.balance < transaction_amount:
            print("Insufficient funds to purchase requested shares.")
            return False
        else:

            try:
                current_holding = db.get_user_single_holding(user_id=user_id, symbol=stock.symbol)
                trade = Trade(user_id=user_id, stock=stock, number_of_shares=num_shares,
                              transaction_type="BUY", transaction_total=transaction_amount)
                
                trade_id = db.log_trade(trade)
                print(f"output of log_trade: {trade_id}")

                if not db.update_user_single_holding(user_id=user_id, trade=trade, current_holding=current_holding):
                    print("in wrong loop!")
                    db.remove_trade(trade_id)
                    raise Exception
                
                # update user's balance to reflect purchase
                db.update_user_balance(user_id, (transaction_amount * -1 ))

                return True
      
            except Exception as e:
                print(f"Error. Failed to purchase shares: {e}.")
                
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

