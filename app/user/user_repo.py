from app.user.user_model import User

# tested, functional, commented
def insert_user(cur, user):
    """ Accepts cursor and user object, inserts it into users table. """

    cur.execute("""
        INSERT INTO users (first_name, last_name, dob, email, password_hash, cash_balance, total_balance)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        user.first_name, 
        user.last_name, 
        user.dob, 
        user.email, 
        user.password_hash, 
        user.cash_balance,
        user.total_balance
    ))

    return cur.rowcount > 0


# tested, functional, commented
def get_user_by_email(cur, email):
    """ Accepts cursor and email address, queries users table to find user based on
        email address, returns user object. """
    cur.execute("""SELECT * FROM users WHERE email=%s""", (email,))
    
    row = cur.fetchone()
    
    if row:
        id, first_name, last_name, dob, email, password_hash, cash_balance, total_balance = row
        return User(id=id, 
                    first_name=first_name, 
                    last_name=last_name,
                    dob=dob, 
                    password_hash=password_hash,
                    email=email, 
                    cash_balance=cash_balance, 
                    total_balance=total_balance)           
    else:
        return None
    

# tested, functional, commented
def get_user_by_id(cur, id):
    """ Accepts cursor and user id, queries users table to find user based on
    id, returns user object. """

    cur.execute(""" SELECT * FROM users WHERE id=%s """, (id,))
    
    row = cur.fetchone()

    if row:
        id, first_name, last_name, dob, email, password_hash, cash_balance, total_balance = row
        return User(id=id, 
                    first_name=first_name, 
                    last_name=last_name,
                    dob=dob, 
                    password_hash=password_hash,
                    email=email, 
                    cash_balance=cash_balance, 
                    total_balance=total_balance)           
    else:
        return None


# tested, functional, commented
def remove_user(cur, user_id):
    """ Accepts cursor and user_id, removes user from users table based on user_id. """

    cur.execute(""" DELETE FROM users WHERE id=%s """, (user_id,))
    return cur.rowcount > 0


# tested, functional, commented
def insert_user_email(cur, user_id, new_email):
    """  Accepts cursor, user_id and new_email, updates user's email in users table. """

    cur.execute(""" UPDATE users SET email=%s WHERE id=%s """, (new_email, user_id))
    return cur.rowcount > 0


# tested, functional, commented
def insert_user_password(cur, user_id, new_password):
    """  Accepts cursor, user_id and new_password, updates user's password in users table. """

    cur.execute(""" UPDATE users SET password_hash=%s WHERE id=%s """, (new_password, user_id))
    return cur.rowcount > 0


# tested, functional, commented
def update_user_cash_balance(cur, user_id, new_balance):
    """  Accepts cursor, user_id and new_balance, updates user's cash balance in users table. """

    cur.execute(""" UPDATE users SET cash_balance=%s WHERE id=%s """, (new_balance, user_id))
    return cur.rowcount > 0