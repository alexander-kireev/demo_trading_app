from user.user_model import User


def insert_user(cur, user):
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


def get_user_by_email(cur, email):
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
    

def get_user_by_id(cur, id):
    cur.execute("""SELECT * FROM users WHERE id=%s""", (id,))
    
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


def remove_user(cur, user_id):
    cur.execute(""" DELETE FROM users WHERE id=%s """, (user_id,))


def update_user_email(cur, user_id, new_email):
    cur.execute(""" UPDATE users SET email=%s WHERE id=%s """, (new_email, user_id))


def update_user_password(cur, user_id, new_password):
    cur.execute(""" UPDATE users SET password=%s WHERE id=%s """, (new_password, user_id))


def update_user_cash_balance(cur, user_id, new_balance):
    cur.execute(""" UPDATE users SET cash_balance=%s WHERE id=%s """, (user_id, new_balance))