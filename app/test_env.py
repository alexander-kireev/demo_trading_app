from app.db_core import DBCore

from pprint import pprint

from datetime import datetime

from app.exchange_data.exchange_service import (
    get_amex_tickers,
    get_nasdaq_tickers,
    get_nyse_tickers,
    load_nasdaq_tickers,
    load_amex_tickers,
    load_nyse_tickers
)


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
    sell_stock,
    get_user_trade_history
)
from app.trade.trade_repo import (
    get_trades
)

from app.transaction.transaction_service import (
    get_user_transaction_history
)

from app.position.position_repo import (
    get_user_equity_symbols,
    get_user_positions_of_equity
)

from app.portfolio.portfolio_service import (
    get_portfolio,
    aggregate_positions_of_single_equity,
    aggregate_total_value_of_equity_positions
)

from app.stock.stock_service import (
    live_stock_price
)

from app.position.position_service import (
    update_positions_in_table
)


# f_name = "alex"
# l_name = "smith"
# dob = "19-05-1999"
# email = "alex2@email.com"
# password = "password"


# print(register_user(f_name, l_name, dob, email, password))
user_id = 2

# # print(update_positions_in_table(user_id))
# symbol = "tsla"

# print(sell_stock(user_id, symbol, 1))

# portfolio = get_portfolio(2)

# portfolio.print_portfolio()

# symbol = "tsla"
# number_of_shares = 5

# print(buy_stock(user_id, symbol, number_of_shares))

# stock = Stock(company_name=company_name, symbol=symbol, price=price)

# number_of_shares = 4
# # print(buy_stock(user_id=user_id, stock=stock, number_of_shares=number_of_shares))
# # print(sell_stock(stock=stock, number_of_shares=number_of_shares, user_id=user_id))
# portfolio = get_portfolio(3)

# portfolio.print_portfolio()

# symbol = "tsla"
# num_shares = 5
# user_id = 1
# print(buy_stock(user_id, symbol, num_shares))


