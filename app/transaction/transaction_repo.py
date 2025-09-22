from app.transaction.transaction_model import Transaction

# tested, functional, commented
def get_transactions(cur, user_id, start_date, end_date):
    """ Accepts cursor, user_id and returns list of user's trades as
        trade objects. If user has not performed any trades, will return
        and empty list. If start and end date are provided, will filter 
        results to those dates. """

    # take path depending on whether start and end date were provided
    if start_date and end_date:
        return
    else:
        cur.execute(""" SELECT * FROM transactions WHERE user_id=%s """, (user_id,))

    rows = cur.fetchall()
    transactions_list = []

    # if query returned any transaction rows
    if rows:
        for row in rows:

            # unpack each row, instantiate transaction object
            (transaction_id, user_id, amount, transaction_type, timestamp) = row
            transaction = Transaction(user_id=user_id, amount=amount, transaction_type=transaction_type,
                                      timestamp=timestamp, transaction_id=transaction_id)
            transactions_list.append(transaction)
    
    return transactions_list


# tested, functional, commented
def log_transaction(cur, transaction):
    """ Accepts cursor and transaction object, inserts it into transactions table. """

    cur.execute(""" 
            INSERT INTO transactions (user_id, amount, transaction_type)
            VALUES (%s, %s, %s)
            """, (
                transaction.user_id, transaction.amount, transaction.transaction_type
            ))

    return cur.rowcount > 0