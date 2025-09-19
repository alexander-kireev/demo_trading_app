from app.db_core import DBCore
from user_repo import (
    insert_user,
    get_user_by_email,
    get_user_by_id,
    remove_user,
    update_user_cash_balance
)
from app.utils import  (
    email_is_valid, 
    hash_password,
    verify_password
)
from user_model import User

def register_user(first_name, last_name, dob, email, password):
    """ Accepts a user object, inserts it into the users table. """

    try:
        with DBCore.get_connection() as conn:
            with conn.cursor() as cur:

                if get_user_by_email(cur, email):
                    return {
                        "success": False,
                        "message": "Email is already in use."
                    }
                
                # hash the raw password
                password_hash = hash_password(password)

                # default balance set for new users. adjust as needed.
                default_balance = 10000.00

                new_user = User(first_name=first_name,
                                last_name=last_name,
                                dob=dob,
                                email=email,
                                password_hash=password_hash,
                                cash_balance=default_balance,
                                total_balance=default_balance
                )

                insert_user(cur, new_user)
                conn.commit()
                return {
                        "success": True,
                        "message": "User successfully registered."
                }
                
    except Exception as e:
        return {
                "success": False,
                "message": f"Error. Failed to insert user: {e}."
        }
    

def delete_user(user_id, password):
    """ Accepts a user_id, authenticates user, deletes the user record from the users table. """

    try:
        with DBCore.get_connection() as conn:
            with conn.cursor() as cur:

                user = get_user_by_id(cur, user_id)
                
                if not verify_password(password, user.password_hash):
                    raise Exception("Incorrect password.")
                
                remove_user(cur, user.id)
                conn.commit()
                return {
                    "success": True,
                    "message": "User deleted successfully."
                }
              
    except Exception as e:
        return {
                "success": False,
                "message": f"Error. Failed to delete user: {e}."
        }
        

def update_user_email(user_id, new_email, password):
    """ Accepts a user_id, new_email and password, authenticates user, updates user email. """

    try:
        with DBCore.get_connection() as conn:
            with conn.cursor() as cur:

                user = get_user_by_id(cur, user_id)

                if not verify_password(password, user.password_hash):
                    raise Exception("Incorrect password.")
                
                update_user_email(cur, user_id, new_email)
                conn.commit()
                return {
                    "success": True,
                    "message": "Email successfully updated."
                }
                
    except Exception as e:
        return {
                "success": False,
                "message": f"Error. Failed to update user email: {e}."
        }
    

def update_user_password(user_id, current_password, new_password):
    """ Accepts a user_id, new_password and current_password, authenticates user, updates user password. """

    try:
        with DBCore.get_connection() as conn:
            with conn.cursor() as cur:

                user = get_user_by_id(cur, user_id)

                if not verify_password(current_password, user.password_hash):
                    raise Exception("Incorrect password.")
                
                update_user_password(cur, user_id, new_password)
                conn.commit()
                return {
                    "success": True,
                    "message": "Password successfully updated."
                }
                
    except Exception as e:
        return {
                "success": False,
                "message": f"Error. Failed to update user password: {e}."
        }
    

def deposit_funds(user_id, amount):
    """ Accepts a user_id and amount to deposit, updates the users table with the new cash balance. """

    try:
        with DBCore.get_connection() as conn:
            with conn.cursor() as cur:
                user = get_user_by_id(cur, user_id)

                new_balance = user.cash_balance + amount

                update_user_cash_balance(cur, user_id, new_balance)

                return {
                    "success": True,
                    "message": "Funds successfully deposited."
                }

    except Exception as e:
        return {
                "success": False,
                "message": f"Error. Failed to deposit funds: {e}."
        }
    

def withdraw_user_funds(user_id, amount):
    """ Accepts a user_id and amount to withdraw, validates amount, updates cash balance to reflect withdrawl. """
    
    try:
        with DBCore.get_connection() as conn:
            with conn.cursor() as cur:

                user = get_user_by_id(cur, user_id)

                new_balance = user.cash_balance - amount

                if new_balance < 0:
                    raise Exception("Insufficient cash balance to withdraw requested sum.")
                
                update_user_cash_balance(cur, user_id, new_balance)
                return {
                    "success": True,
                    "message": "Funds successfully deposited."
                }            

    except Exception as e:
        return {
                "success": False,
                "message": f"Error. Failed to withdraw funds: {e}."
        }   
 

