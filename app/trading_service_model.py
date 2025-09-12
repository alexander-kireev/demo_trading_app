from app.db import DB
from app.user_model import User
from app.stock_model import Stock

class TradingService:

    def buy_stock(self, stock, num_shares, user_id):
        # get user_balance
        user = DB.get_user_by_id(user_id)

        transaction_amount = stock.price * num_shares

        if user.balance < transaction_amount:
            print("Insufficient funds to purchase requested shares.")
        else:

            try:
                DB.log_trade(stock, num_shares, user_id)
                DB.log_holding(stock)
            except Exception as e:
                print(f"Error. Failed to purchase shares: {e}.")
            # log transactions in trades_log
            # log holding to all_holdings

            new_user_balance = user.balance - transaction_amount
            DB.update_user_balance(new_user_balance)

        # if user has enough money 
