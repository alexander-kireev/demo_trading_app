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
                
                # update user's balance to reflect purchase
                db.update_user_balance(user_id, (transaction_amount * -1 ))
      
            except Exception as e:
                print(f"Error. Failed to purchase shares: {e}.")
                
    # TODO: MUST COMPLETE, SIMILAR TO BUY_STOCK()
    def sell_stock(self, stock, num_shares, user_id):

        """ accepts stock object, number of shares to buy, user id and buys the stock """

        # get user_balance
        db = DB()
        user = db.get_user_by_id(user_id)

        try:
            current_holding = db.get_user_single_holding(user_id=user_id, symbol=stock.symbol)

            if current_holding.number_of_shares < num_shares:
                print("Insufficient shares held to sell.")
            else:
                trade = Trade(user_id=user_id, stock=stock, number_of_shares=num_shares, transaction_type="SELL")
                trade_id = db.log_trade(trade)

                if not db.update_user_single_holding(user_id=user_id, trade=trade, current_holding=current_holding):
                    db.remove_trade(trade_id)

        except Exception as e:
            print(f"Error. Failed to purchase shares: {e}.")



if __name__ == "__main__":


    # init stock
    company_name = "apple"
    symbol = "aapl"
    price = 125.8
    appl_stock = Stock(company_name, symbol, price)

    # init trade
    user_id = 1
    number_of_shares = 3
    transaction_type = "BUY"

    ts = TradingService()
    ts.buy_stock(stock=appl_stock, num_shares=3, user_id=user_id)
    # ts.sell_stock(stock=appl_stock, num_shares=3, user_id=user_id)

