import psycopg2
import os
from dotenv import load_dotenv
from user_model import User
from stock_model import Stock
from trade_model import Trade
from holding_model import Holding
import datetime
import bcrypt


# load db
load_dotenv()
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

class DB:
    """ class handles all database operations related to users: creation, authentication, updates,
        deletion, querying """
    
###   --------------------   USER QUERIES START   --------------------   ###
    
    def establish_connection(self):
        """ returns a psycopg2 db connection """
        
        conn = psycopg2.connect(
                host=DB_HOST,
                port=DB_PORT,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
            )
        conn.autocommit = False
        return conn
    
    
    def add_user(self, user):
        # default balance set for new users. adjust as needed.
        default_balance = 10000.00

        """ accepts a user object, inserts it into users table """

        try:
            with self.establish_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        INSERT INTO users (first_name, last_name, dob, email, password_hash, balance)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (
                        user.first_name, user.last_name, user.dob, user.email, user.password_hash, default_balance
                    ))

                conn.commit()
                return True

        except Exception as e:
            print(f"Error. Failed to insert user: {e}.")
            return False


    def get_user_by_email(self, email):
        """ accepts a user's email and returns a user object """
        
        try:
            with self.establish_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""SELECT * FROM users WHERE email=%s""", (email,))
                    
                    row = cur.fetchone()

                    # ensure user was found
                    # the user object is returned with password_hash = None
                    if row:
                        id, first_name, last_name, dob, email, password_hash, balance = row
                        return User(id=id, first_name=first_name, last_name=last_name,
                                    dob=dob, email=email, balance=balance)           
                    else:
                        print("User not found.")
                        return None
                    
        except Exception as e:
            print(f"Error. Failed to retrieve user by email: {e}.")
            return None


    def get_user_by_id(self, id):
        """ accepts a user's id and returns a user object """
        
        try:
            with self.establish_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""SELECT * FROM users WHERE id=%s""", (id,))
                    
                    row = cur.fetchone()

                    # ensure user was found
                    # the user object is returned with password_hash = None
                    if row:
                        id, first_name, last_name, dob, email, password_hash, balance = row
                        return User(id=id, first_name=first_name, last_name=last_name,
                                    dob=dob, email=email, balance=balance)             
                    else:
                        print("User not found.")
                        return None
                    
        except Exception as e:
            print(f"Error. Failed to retrieve user by ID: {e}.")
            return None


    def delete_user(self, id):
        """ accepts a user_id and removes a user from the users table """
        
        try:
            with self.establish_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""DELETE FROM users WHERE id=%s""", (id,))

                    # check if user was found and deleted
                    if cur.rowcount == 0:
                        print("User not found.")
                        return False
                    else:
                        return True
                    
        except Exception as e:
            print(f"Error. Failed to delete user: {e}.")
            return False

    
    def get_user_password_hash(self, id):
        """ accepts a user id and returns the user's password_hash from db """
        
        try:
            with self.establish_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(""" SELECT password_hash FROM users WHERE id=%s""", (id,))

                    row = cur.fetchone()

                    # ensure password_hash was found
                    if row:
                        (password_hash,) = row
                        return password_hash
                    else:
                        print("Password hash not found.")
                        return None

        except Exception as e:
            print(f"Error. Failed to retrieve user password hash: {e}.")
            return None
        

    def update_user_balance(self, id, amount):
        """ accepts a user's id and amount, updating the user's current balance """
        
        try:
            with self.establish_connection() as conn:
                with conn.cursor() as cur:
                    
                    # get user object and balance, update balance
                    user = self.get_user_by_id(id)
                    new_balance = float(user.balance) + amount
                    cur.execute(""" UPDATE users SET balance=%s WHERE id=%s""", (new_balance, user.id))

                    conn.commit()
                    return True

        except Exception as e:
            print(f"Error. Could not update user's balance: {e}.")
            return False


    def check_email_exists(self, email):
        """ accepts an email and returns true if email is already in use """
        
        try:
            with self.establish_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(""" SELECT email FROM users WHERE email=%s""", (email,))

                    row = cur.fetchone()

                    if row:
                        return True
                    
                    return False
                
        except Exception as e:
            print(f"Error. Could not validate email: {e}.")
            return False


    def authenticate_user(self, email, password):
        """ accepts user's email and password, returns user id if login is successful """
        
        try:
            with self.establish_connection() as conn:
                with conn.cursor() as cur:

                    # ensure email is register to an account
                    if self.check_email_exists(email):
                        cur.execute("""SELECT id, password_hash FROM users WHERE email=%s""", (email,))

                        row = cur.fetchone()

                        # ensure query returned valid result
                        if row:
                            id, stored_hash = row

                            # ensure password is correct
                            if bcrypt.checkpw(password.encode(), stored_hash.encode()):
                                return self.get_user_by_id(id)
                            else:
                                print("Incorrect password.")
                                return None
                        else:
                            print("Error. Unable to fetch user details.")
                            return None
                    else:
                        print("Email is not registered to an account.")
                        return None
        except Exception as e:
            print(f"Error. Could not authenticate user: {e}.")
            return None

    
    def update_user_email(self, id, new_email, password):
        """ accepts id, new email and current password, updates user's email in db """
        
        try:
            with self.establish_connection() as conn:
                with conn.cursor() as cur:
                    
                    # ensure new email is not taken
                    if not self.check_email_exists(new_email):

                        # ensure password is valid
                        stored_hash = self.get_user_password_hash(id)
                        if bcrypt.checkpw(password.encode(), stored_hash.encode()):
                            cur.execute(""" UPDATE users SET email=%s WHERE id=%s""", (new_email, id))
                            conn.commit()
                            return True
                        else:
                            print("Incorrect password.")
                            return False
                    else:
                        print("Email is already in use.")
                        return True
        except Exception as e:
            print(f"Error. Unable to update user email: {e}")
            return False

        
    def update_user_password(self, id, current_password, new_password):
        """ accepts id, new password and current password, updates user's password in db """
        
        try:
            with self.establish_connection() as conn:
                with conn.cursor() as cur:

                    # ensure password is valid
                    stored_hash = self.get_user_password_hash(id)
                    if bcrypt.checkpw(current_password.encode(), stored_hash.encode()):

                        # hash new password
                        new_hashed_password = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
                        cur.execute(""" UPDATE users SET password_hash=%s WHERE id=%s""", (new_hashed_password, id))

                        conn.commit()
                        return True
                    else:
                        print("Incorrect password.")
                        return False

        except Exception as e:
            print(f"Error. Unable to update user password: {e}")
            return False

    
###   --------------------   USER QUERIES END   --------------------   ###

###   --------------------   TRADE QUERIES START   --------------------   ###

    def log_trade(self, trade):

        """ accepts a trade object and inserts it into trades_log database, returns trade id logged """

        try:
            with self.establish_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        INSERT INTO trades_log (user_id, company_name, symbol, price_per_share, 
                                                number_of_shares, transaction_total, transaction_type)
                        VALUES (%s, %s, %s, %s, %s, %s, %s) 
                        RETURNING trade_id                       
                    """, (
                        trade.user_id, trade.company_name, trade.symbol, trade.price_per_share,
                        trade.number_of_shares, trade.transaction_total, trade.transaction_type
                    ))

                    (trade_id,) = cur.fetchone()
                    conn.commit()
                    return trade_id
                    
                    # THIS SEEMS REDUNDANT, AS RETURNING FROM QUERY WORKED?
                    cur.execute("""
                            SELECT trade_id FROM trades_log
                            WHERE user_id = %s AND symbol = %s AND price_per_share = %s
                            AND number_of_shares = %s AND transaction_total = %s AND transaction_type = %s
                            ORDER BY trade_id DESC
                            LIMIT 1
                        """, (
                            trade.user_id, trade.symbol, trade.price_per_share,
                            trade.number_of_shares, trade.transaction_total, trade.transaction_type
                    ))
                    
                    
        except Exception as e:
            print(f"Error. Failed to log trade: {e}.")
            return None  

    # THIS SEEMS REDUNDANT, AS RETURNING FROM QUERY WORKED?
    def get_last_trade_id(self, trade):
        try:
            with self.establish_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                            SELECT trade_id FROM trades_log
                            WHERE user_id = %s AND symbol = %s AND price_per_share = %s
                            AND number_of_shares = %s AND transaction_total = %s AND transaction_type = %s
                            ORDER BY trade_id DESC
                            LIMIT 1
                        """, (
                            trade.user_id, trade.symbol, trade.price_per_share,
                            trade.number_of_shares, trade.transaction_total, trade.transaction_type
                    ))
                    result = cur.fetchone()
                    print(result)
                    if result:
                        return (result[0],)
                    else:
                        raise Exception
        except Exception as e:
            print(f"Error. Failed to retrieve last trade_id: {e}.")
            return None



    def remove_trade(self, trade_id):

        """ accepts a trade_id and removes a trade entry from the trades_log database """

        try:    
            with self.establish_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(""" DELETE FROM trades_log WHERE trade_id=%s """, (trade_id,))

                    
                    
                    return True
        except Exception as e:
            print(f"Error. Failed to remove trade from database: {e}.")
            return False


    def get_user_single_holding(self, user_id, symbol):

        """ accepts user's id and a stock object, returns holding object """

        try:
            with self.establish_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""SELECT * FROM all_holdings WHERE user_id=%s AND symbol=%s""",
                                (user_id, symbol))
                    
                    row = cur.fetchone()

                    # check if holding was found
                    if row:
                        (holding_id, user_id, company_name, symbol, shares_held, 
                        average_price_per_share, holdings_total) = row

                        return Holding(Stock(company_name=company_name, symbol=symbol, 
                                                price=average_price_per_share), number_of_shares=shares_held)       
                    else:
                        return None
                    
        except Exception as e:
            print(f"Error. Failed to retrieve single stock holding: {e}.")
            return None


    def update_user_single_holding(self, user_id, trade, current_holding=None):
        try:    
            with self.establish_connection() as conn:
                with conn.cursor() as cur:
                    if current_holding:
                        
                        # check type of trade (BUY OR SELL) 
                        if trade.transaction_type == "BUY":
                            updated_number_of_shares = current_holding.number_of_shares + trade.number_of_shares
                        elif trade.transaction_type == "SELL":
                            updated_number_of_shares = current_holding.number_of_shares - trade.number_of_shares
                        else:
                            raise Exception
                        
                        
                        if updated_number_of_shares == 0:
                            cur.execute("""
                                        DELETE FROM all_holdings WHERE user_id=%s AND symbol=%s
                                        """,
                                        (user_id, trade.symbol))
                        else:
                            updated_price_per_share = (trade.transaction_total + 
                                                    (current_holding.number_of_shares * current_holding.price)) / updated_number_of_shares
                            
                            updated_holding = Holding(Stock(company_name=trade.company_name, symbol=trade.symbol,
                                                    price=updated_price_per_share), number_of_shares=updated_number_of_shares)

                            cur.execute(""" 
                                        UPDATE all_holdings SET shares_held=%s, average_price_per_share=%s, holdings_total=%s
                                        WHERE user_id=%s
                                        """,
                                        (updated_holding.number_of_shares, updated_holding.price, updated_holding.total_value, user_id)
                            )
                                 

                    else:
                        holding = Holding(Stock(company_name=trade.company_name, symbol=trade.symbol,
                                                price=trade.price_per_share), number_of_shares=trade.number_of_shares)
                        
                        
                        cur.execute(""" 
                                    INSERT INTO all_holdings (user_id, company_name, symbol, 
                                    shares_held, average_price_per_share, holdings_total)
                                    VALUES (%s, %s, %s, %s, %s, %s)
                                    """,
                                    (user_id, holding.company_name, holding.symbol, holding.number_of_shares,
                                     holding.price, holding.total_value)
                                    )

                    conn.commit()
                    return True  

        except Exception as e:
            print(f"Error. Failed to update user holding: {e}.")
            return False











        # try:    
        #     with self.establish_connection() as conn:
        #         with conn.cursor() as cur:
        #             pass
        # except Exception as e:
        #     print("Error. : {e}.")
        #     return False






if __name__ == "__main":
    db = DB()

    # make user
    # f_name = "alex"
    # l_name = "smith"
    # now = datetime.datetime.now()
    # dob = now.date()
    # email = "alex.s@email.com"
    # password = "password"
    # user = User(f_name, l_name, dob, email, password)
    # db.add_user(user)


    # init stock
    company_name = "apple"
    symbol = "aapl"
    price = 125.8
    stock = Stock(company_name, symbol, price)

    # init trade
    user_id = 1
    number_of_shares = 3
    transaction_type = "BUY"

    trade = Trade(user_id, stock, number_of_shares, transaction_type)





    db.log_trade(trade)