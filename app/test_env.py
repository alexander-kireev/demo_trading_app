from app.db_core import DBCore

from datetime import datetime

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

# # register a user
# first_name = "john"
# last_name = "markson"
# dob = "11-06-1999"
# email = "john@email.com"
# password = "password"


# print(register_user(first_name, last_name, dob, email, password))

user_id = 3
transactions_list = get_user_transaction_history(user_id)
# print(transactions_list)
for transaction in transactions_list:
    print(transaction)
    print(f"trans id: {transaction.transaction_id}")
    print(f"trans type: {transaction.transaction_type}")
    print(f"trans total: {transaction.amount}")

# with DBCore.get_connection() as conn:
#     with conn.cursor() as cur:

#         s_date = None
#         e_date = None
#         trades_list = get_trades(cur, user_id, start_date=s_date, end_date=e_date)

#         for trade in trades_list:
#             print(f"trade id: {trade.trade_id}")
#             print(f"trade type: {trade.trade_type}")
#             print(f"trade total: {trade.trade_total}")

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



# portfolio = get_portfolio(user_id)


# portfolio.print_portfolio()

# # print(positions)


# with DBCore.get_connection() as conn:
#     with conn.cursor() as cur:
        
#         user_id = 1
#         symbol = "goog"
#         symbols = get_user_equity_symbols(cur, user_id)
        
        

#         for symbol in symbols:
#             positions = get_user_positions_of_equity(cur, user_id, symbol)
#             agg = aggregate_positions_of_single_equity(cur, user_id, symbol)
#             print()
#             print(f'company name: {agg["company_name"]}')
#             print(f'num shares: {agg["number_of_shares"]}')
#             print(f'av p: {agg["average_price_per_share"]}')
#             print(f'total pos val: {agg["total_position_value"]}')
#             print()
        

            # for position in positions:
            #     print(position.company_name)







