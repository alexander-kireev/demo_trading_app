from app.db_core import DBCore
from app.user.user_repo import (
    insert_user,
    get_user_by_email,
    get_user_by_id,
    remove_user,
    update_user_cash_balance,
    insert_user_email,
    insert_user_password
)
from app.utils import  (
    email_is_valid, 
    hash_password,
    verify_password
)
from app.user.user_model import User

# tested, functional
def register_user(first_name, last_name, dob, email, password):
    """ Accepts first_name, last_name, dob, email and raw password, 
        instantiates a user object and inserts it into the users table. """

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

                if not insert_user(cur, new_user):
                    return {
                        "success": False,
                        "message": "Failed to insert user."
                    }

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
    

# tested, functional
def delete_user(user_id, password):
    """ Accepts a user_id, authenticates user, deletes the user record from the users table. """

    try:
        with DBCore.get_connection() as conn:
            with conn.cursor() as cur:

                user = get_user_by_id(cur, user_id)
                
                if not verify_password(password, user.password_hash):
                    raise Exception("Incorrect password.")
                
                if not remove_user(cur, user.id):
                    return {
                    "success": False,
                    "message": "Failed to remove user from table."
                    }
                
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
        

# tested, functional
def update_user_email(user_id, new_email, password):
    """ Accepts a user_id, new_email and password, authenticates user, updates user email. """

    try:
        with DBCore.get_connection() as conn:
            with conn.cursor() as cur:

                user = get_user_by_id(cur, user_id)

                if get_user_by_email(cur, new_email):
                     return {
                        "success": False,
                        "message": "Email is already in use."
                    }                   

                if not verify_password(password, user.password_hash):
                    return {
                        "success": False,
                        "message": "Incorrect password."
                    }
                
                print(f"email passed in: {new_email}")
                if not insert_user_email(cur, user_id, new_email):
                    return {
                        "success": False,
                        "message": "Failed to update email in database."
                    }

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
    

# tested, functional
def update_user_password(user_id, current_password, new_password):
    """ Accepts a user_id, new_password and current_password, authenticates user, updates user password. """

    try:
        with DBCore.get_connection() as conn:
            with conn.cursor() as cur:

                
                user = get_user_by_id(cur, user_id)

                if not user:
                    return {
                        "success": False,
                        "message": "User not found."
                    }
       

                if not verify_password(current_password, user.password_hash):
                    return {
                        "success": False,
                        "message": "Incorrect password."
                    }

                new_password_hash = hash_password(new_password)
    
                if not insert_user_password(cur, user_id, new_password_hash):
                    return {
                        "success": False,
                        "message": "Failed to insert new password into database."
                    }
                
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
    

# tested, functional
def deposit_user_funds(user_id, amount):
    """ Accepts a user_id and amount to deposit, updates the users table with the new cash balance. """

    try:
        with DBCore.get_connection() as conn:
            with conn.cursor() as cur:
                user = get_user_by_id(cur, user_id)

                new_balance = user.cash_balance + amount

                if not update_user_cash_balance(cur, user_id, new_balance):
                    return {
                        "success": False,
                        "message": "Failed to update user cash balance is databas."
                    }

                conn.commit()

                return {
                    "success": True,
                    "message": "Funds successfully deposited."
                }

    except Exception as e:
        return {
                "success": False,
                "message": f"Error. Failed to deposit funds: {e}."
        }
    

# tesyed, functional
def withdraw_user_funds(user_id, amount):
    """ Accepts a user_id and amount to withdraw, validates amount, updates cash balance to reflect withdrawl. """
    
    try:
        with DBCore.get_connection() as conn:
            with conn.cursor() as cur:

                user = get_user_by_id(cur, user_id)

                new_balance = user.cash_balance - amount

                if new_balance < 0:
                    return {
                        "success": False,
                        "message": "Insufficient cash balance to withdraw requested sum."
                    }            
     
                if not update_user_cash_balance(cur, user_id, new_balance):
                    return {
                        "success": False,
                        "message": "Failed to update user cash balance in database."
                    }            

                conn.commit()

                return {
                    "success": True,
                    "message": "Funds successfully withdrawn."
                }            

    except Exception as e:
        return {
                "success": False,
                "message": f"Error. Failed to withdraw funds: {e}."
        }   
 

# TODO: IMPLEMENT UPDATING OF USER.TOTAL_BALANACE (WHEN PORTFOLIO FUNCTIONALITY IS READY)