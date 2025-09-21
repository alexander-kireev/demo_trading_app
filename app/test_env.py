# user modules
from app.user.user_model import User
from app.user.user_service import (
    register_user,
    delete_user,
    deposit_user_funds,
    withdraw_user_funds,
    update_user_email,
    update_user_password
)


# stock modules
from app.stock.stock_model import Stock


# trade modules
from app.trade.trade_model import Trade
from app.trade.trade_service import (
    buy_stock,
    sell_stock
)



# # register a user
# first_name = "bob"
# last_name = "grimes"
# dob = "24-09-1995"
# email = "bob@email2.com"
# password = "password"

# new_email = "new_email@email.com"
# new_password = "password"


company_name = "Apple"
symbol = "AAPL"
price = 200

stock = Stock(company_name, symbol, price)

#print(buy_stock(4, stock, 10))
print(sell_stock(stock, 4, 4))











