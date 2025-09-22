from app.db_core import DBCore

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


# table setup modules
from app.setup.positions_table_setup import define_positions_table
from app.setup.trades_log_table_setup import define_trades_log_table
from app.setup.transactions_table_setup import define_transactions_table
from app.setup.users_table_setup import define_users_table

# stock modules
from app.stock.stock_model import Stock


# trade modules
from app.trade.trade_model import Trade
from app.trade.trade_service import (
    buy_stock,
    sell_stock
)

from app.position.position_repo import (
    get_user_equity_symbols,
    get_user_positions_of_equity
)

from app.portfolio.portfolio_service import (
    get_portfolio
)

# register a user
first_name = "bob"
last_name = "grimes"
dob = "24-09-1995"
email = "bob@email.com"
password = "password"


print(register_user(first_name, last_name, dob, email, password))

# user_id = 1

# # apple stock
# company_name = "Apple"
# symbol = "AAPL"
# price = 200
# stock_1 = Stock(company_name, symbol, price)

# # google stock
# company_name = "Google"
# symbol = "GOOG"
# price = 150
# stock_2 = Stock(company_name, symbol, price)

# # microsoft stock
# company_name = "Microsoft"
# symbol = "MSFT"
# price = 185.90
# stock_3 = Stock(company_name, symbol, price)


# print(buy_stock(user_id, stock_1, 4))
# print(buy_stock(user_id, stock_2, 6))
# print(buy_stock(user_id, stock_3, 8))



# # positions = get_portfolio(user_id)

# # print(positions)


# with DBCore.get_connection() as conn:
#     with conn.cursor() as cur:
        
#         user_id = 1
#         symbol = "aapl"
#         positions = get_user_positions_of_equity(cur, user_id, symbol)
#         # symbols = get_user_equity_symbols(cur, user_id)

#         print(positions)







