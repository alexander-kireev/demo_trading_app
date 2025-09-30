from app.db_core import DBCore

from datetime import datetime, timedelta

from app.transaction.transaction_repo import (
    get_transactions
)

# tested, functional, commented
def get_user_transaction_history(user_id, start_date=None, end_date=None):
    """ Accepts a user_id and optionally start and end dates. Queries
        transactions table and returns list of transaction objects of user. """

    try:
        with DBCore.get_connection() as conn:
            with conn.cursor() as cur:

                # format end date to catch all trades until end of day
                if end_date:
                    end_date = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1) - timedelta(seconds=1)

                # get list of transaction objects from transactions table
                transactions_list = get_transactions(cur, user_id, start_date, end_date)

                # ensure list exists
                if len(transactions_list) < 1:
                    return {
                        "success": False,
                        "message": "User has no transactions to date."
                    }
                else:
                    return {
                        "success": True,
                        "message": transactions_list
                    }
            
    except Exception as e:
        return {
            "success": False,
            "message": f"Error. Failed to retrieve user transactions: {e}."
        }
      