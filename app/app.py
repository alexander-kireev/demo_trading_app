from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash
)

from app.exchange_data.exchange_service import (
    ALL_SYMBOLS
)



from app.trade.trade_service import (
    buy_stock,
    sell_stock,
    get_user_trade_history
)

from app.portfolio.portfolio_model import Portfolio

from app.portfolio.portfolio_service import (
    get_portfolio
)

from functools import wraps
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

from app.user.user_service import (
    register_user,
    authenticate_user,
    get_user,
    update_user_email,
    insert_user_password,
    update_user_password,
    delete_user,
    update_user_details,
    deposit_user_funds,
    withdraw_user_funds
)

from app.transaction.transaction_service import (
    get_user_transaction_history
)

from app.position.position_model import Position

from app.position.position_service import (
    aggregate_all_equity_positions,
    aggregate_positions_of_single_equity,
    aggregate_total_value_of_equity_positions,
    get_user_position_by_symbol
)

from app.user.user_repo import (
    get_user_by_email,
    get_user_by_id
)

from app.utils import (
    validate_registration_data,
    email_is_valid,
    passwords_match,
    verify_password,
    hash_password,
    valid_dob,
    valid_email,
    valid_first_name,
    valid_last_name,
    valid_password,
    valid_deposit_amount
)

from app.stock.stock_model import Stock

from app.stock.stock_service import (
    create_stock,
    create_stocks
)

load_dotenv()
app = Flask(__name__)



def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("log_in"))
        return f(*args, **kwargs)
    return decorated_function



@app.route("/")
def home():
    return render_template("index.html")


# tested, functional, commented
@app.route("/log_in", methods=["GET", "POST"])
def log_in():

    # POST request
    if request.method == "POST":

        # get input
        email = request.form["email"]
        password = request.form["password"]

        # log user in
        result = authenticate_user(email, password)

        # log user in if authentication was successful
        if result["success"]:
            user = result["message"]
            session["user_id"] = user.id
            return redirect("/")
        
        # TODO: FIX THIS (RETURN REDIRECT, NOT RENDER TEMPLATE)
        # if authetication was unsuccessful, display message
        else:
            error = result["message"]
            return render_template("log_in.html", error=error)

    # GET  request
    else:   
        return render_template("log_in.html")


# tested, functional, commented
@app.route("/sign_up", methods=["GET", "POST"])
def signup():

    # POST method
    if request.method == "POST":

        # collect input into object
        data = {
            "first_name": request.form["first_name"],
            "last_name": request.form["last_name"],
            "dob": request.form["dob"],
            "email": request.form["email"],
            "first_password": request.form["first_password"],
            "second_password": request.form["second_password"]
        }
        
        # validate input
        error = validate_registration_data(data)
        if error:
            return render_template("sign_up.html", error=error)

        # register user
        result = register_user(data)

        # if registration was successful, log user in
        if result["success"]:
            user = result["message"]
            session["user_id"] = user.id
            return redirect("/")
        
        # TODO: THIS NEEDS FIXING (WITH REDIRECT, NOT RENDER TEMPLATE)
        # if registration was unsuccessful, display message
        else:
            error = "Sorry, something went wrong. Please try to register again."
            error = result["message"]
            return render_template("sign_up.html", error=error)

    # GET request   
    else:
        return render_template("sign_up.html")


# tested, functional
@app.route("/log_out")
@login_required
def log_out():
    session.clear()
    return redirect("/")


# tested, functional
@app.route("/my_details")
@login_required
def my_details():
    return render_template("my_details.html")


# tested, functional, commented
@app.route("/change_email", methods=["GET", "POST"])
@login_required
def change_email():
    """ Loads the change_email.html, allows user to change email address. """

    # POST request
    if request.method == "POST":

        # get input
        new_email = request.form.get("new_email", "").strip()
        password = request.form.get("password", "")

        # get user object
        user_id = session["user_id"]
        user = get_user(user_id)

        # ensure new email provided is valid
        if not email_is_valid(new_email):
            flash("Invalid email address.")
            return redirect("/change_email", "danger")

        
        # ensure user entered correct password
        if not verify_password(password=password, hashed_password=user.password_hash):
            flash("Incorrect password.", "danger")
            return redirect("/change_email")

        # update user email in table
        result = update_user_email(user_id, new_email, password)

        # if email was changed successfully
        if result["success"]:
            flash("Email address changed successfully.", "success")

        # if error occured
        else:
            error = result["message"]
            flash(error, "danger")

        return redirect("/change_email")
    
    # GET request
    else:

        # get user object
        user_id = session["user_id"]
        user = get_user(user_id)
        
        return render_template("change_email.html", current_email=user.email)


# tested, functional, commented
@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():

    # POST request
    if request.method == "POST":

        # get input
        current_password = request.form.get("current_password", "")
        new_password_1 = request.form.get("new_password_1", "")
        new_password_2 = request.form.get("new_password_2", "")

        # ensure input was provided
        if not current_password or not new_password_1 or not new_password_2:
            flash("Please enter your current and new passwords.", "danger")
            return redirect("/change_password")

        # get user
        user_id = session["user_id"]
        user = get_user(user_id)

        # ensure current password is correct
        if not verify_password(current_password, user.password_hash):     
            flash("Incorrect current password.", "danger")
            return redirect("/change_password")
        
        # ensure new passwords match
        if not passwords_match(new_password_1, new_password_2):
            flash("New passwords do not match.", "danger")
            return redirect("/change_password")
           

        # hash new password
        hashed_password = hash_password(new_password_1)

        # update password in table
        result = update_user_password(user_id, hashed_password)

        # if password was updated successfully
        if result["success"]:
            flash("Password changed successfully", "success")
        
        # if error occured
        else:
            flash("Something went wrong. Please try again.", "danger")
           
        return redirect("/change_password")
    
    # GET request
    else:
        return render_template("change_password.html")


# tested, functional, commented
@app.route("/change_user_details", methods=["GET", "POST"])
@login_required
def change_user_details():

    # get user object
    user_id = session["user_id"]
    user = get_user(user_id)

    # POST request
    if request.method == "POST":

        # get input
        first_name = request.form.get("first_name", "").strip()
        last_name = request.form.get("last_name", "").strip()
        dob = request.form.get("dob", "").strip()

        # validate and format input
        first_name = valid_first_name(first_name)
        last_name = valid_last_name(last_name)
        dob = valid_dob(dob)

        # ensure all input provided exists and is valid
        if not first_name:
            flash("Please enter a valid first name.")
            return redirect("/change_user_details")
        if not last_name:
            flash("Please enter a valid last name.")
            return redirect("/change_user_details")
        if not dob:
            flash("Please enter a valid date of birth.")
            return redirect("/change_user_details")

        # update user details in users table        
        result = update_user_details(user_id=user_id, user=user, first_name=first_name,
                                     last_name=last_name, dob=dob)
        
        # if update was unsuccessful
        if not result["success"]:
            flash("Sorry, something went wrong. Please try again.")
        # if update was successful
        else:
            flash("Your personal details have been successfully updated.")

        return redirect("/change_user_details")

    # GET request
    else:

        # render html with user details
        return render_template("change_user_details.html", first_name=user.first_name, 
                               last_name=user.last_name, dob=user.dob)
   

# tested, functional, commented
@app.route("/delete_account", methods=["GET", "POST"])
@login_required
def delete_account():

    # POST request
    if request.method == "POST":

        # get input
        password = request.form.get("password", "")

        # ensure input is present
        if not password:
            flash("Enter your password.", "danger")
            return redirect("/delete_account")
        
        # get user object
        user_id = session["user_id"]
        user = get_user(user_id)

        # ensure password is correct
        if not verify_password(password, user.password_hash):
            flash("Incorrect password.", "danger")
            return redirect("/delete_account")
        
        # delete user from table
        result = delete_user(user_id)

        # if deletion was successful, log user out
        if result["success"]:
            return redirect("/log_out")
        
        # if error occured
        else:
            flash("Something went wrong. Please try again.", "danger")
            return redirect("/delete_account")

    # GET request
    else:
        return render_template("delete_account.html")



@app.route("/market", methods=["GET", "POST"])
@login_required
def market():

    if request.method == "POST":
        return render_template("market.html")
    else:
        
        symbol = request.args.get("ticker", "").strip().lower()
        

        if len(symbol) > 0:
            
            
            if symbol.upper() not in ALL_SYMBOLS:
                flash("Please enter a valid ticker.", "danger")
                return redirect("/market")
            
            stock = create_stock(symbol)

            if not stock:
                flash("Something went wrong. Please try again.", "danger")
                return redirect("/market")
            
            # FETCH USER DATA
            user_id = session["user_id"]
            result = get_user_position_by_symbol(user_id, symbol)

            if result["success"]:
                position = result["message"]

                shares_held = position.number_of_shares
                average_price_per_share = position.price_per_share
                total_position_value = position.total_value
            
            else:
                shares_held = 0
                average_price_per_share = 0.00
                total_position_value = 0.00
            
            return render_template("market.html", stock=stock, shares_held=shares_held,
                                   average_price_per_share=average_price_per_share, total_position_value=total_position_value)

        return render_template("market.html")


@app.route("/place_order", methods=["POST"])
@login_required
def place_order():

    if request.method == "POST":

        action = request.form.get("action")
        symbol = request.form.get("display_stock_symbol").strip().lower()
        
        user_id = session["user_id"]

        try:
            num_shares = int(request.form.get("order_amount"))
        except (ValueError, TypeError):
            flash("Please enter a valid number of shares.", "danger")
            return redirect("/market")

        if not num_shares:
            flash("Please enter a valid number of shares.", "danger")
            return redirect("/market")
        
        if num_shares < 1 or num_shares > 100000:
            flash("Please enter a valid number of shares.", "danger")
            return redirect("/market")

        if symbol.upper() not in ALL_SYMBOLS:
            flash("Something went wrong. Please try again.", "danger")
            return redirect("/market")
        
        stock = create_stock(symbol)

        if not stock:
            flash("Something went wrong. Please try again.", "danger")
            return redirect("/market")

        

        if action == "BUY":
            result = buy_stock(user_id, symbol, num_shares)
            if result["success"]:
                flash("Shares purchased successfully.", "success")
            else:
                flash("Failed to purchase shares.", "danger")


        elif action == "SELL":
            result = sell_stock(user_id, symbol, num_shares)
            if result["success"]:
                flash("Shares sold successfully.", "success")
            else:
                flash("Failed to sell shares.", "danger")
        
        else:
            flash("Invalid action. Please try again.", "danger")
            return redirect("/market")
        
        return redirect("/market")
        



@app.route("/portfolio", methods=["GET"])
@login_required
def portfolio():

    if request.method == "GET":

        user_id = session["user_id"]
        portfolio = get_portfolio(user_id)
        

        

        return render_template("portfolio.html", portfolio=portfolio)




@app.route("/trade_history", methods=["GET"])
@login_required
def trade_history():

    if request.method == "GET":

        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")

        user_id = session["user_id"]

        result = get_user_trade_history(user_id, start_date, end_date)

        if result["success"]:
            trades = result["message"]
        else:
            flash(result["message"], "danger")
            trades = []


        return render_template("trade_history.html", trades=trades)



@app.route("/account", methods=["GET"])
@login_required
def account():

    if request.method == "GET":

        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")

        user_id = session["user_id"]
        
        result = get_user_transaction_history(user_id, start_date, end_date)

        if result["success"]:
            transactions = result["message"]
        else:
            flash(result["message"], "danger")
            transactions = []

        return render_template("account.html", transactions=transactions)


@app.route("/deposit_funds", methods=["POST"])
@login_required
def deposit_funds():

    if request.method == "POST":

        deposit_amount = request.form.get("deposit_amount")

        deposit_amount = valid_deposit_amount(deposit_amount)

        if not deposit_amount:
            flash("Please enter a valid deposit amount." "danger")
            return redirect("/account")
        

        user_id = session["user_id"]

        result = deposit_user_funds(user_id, deposit_amount)

        if result["success"]:
            flash(result["message"], "success")
        else:
            flash(result["message"], "danger")
            return redirect("/account")
        
        return redirect("/account")



        

if __name__ == "__main__":
    app.secret_key = os.getenv("SECRET_KEY")
    app.run(debug=True)


