import os
from functools import wraps
from datetime import datetime
from dotenv import load_dotenv

from app.transaction.transaction_service import get_user_transaction_history
from app.position.position_service import get_user_position_by_symbol
from app.portfolio.portfolio_service import get_portfolio
from app.stock.stock_service import create_stock
from app.exchange_data.exchange_service import ALL_SYMBOLS

from flask import (
    Flask,
    session,
    request,
    render_template,
    redirect,
    url_for,
    flash,
    send_file
)

from app.trade.trade_service import (
    buy_stock,
    sell_stock,
    get_user_trade_history
)

from app.user.user_service import (
    register_user,
    authenticate_user,
    get_user,
    update_user_email,
    update_user_password,
    delete_user,
    update_user_details,
    deposit_user_funds,
    withdraw_user_funds
)

from app.utils import (
    validate_registration_data,
    email_is_valid,
    passwords_match,
    verify_password,
    hash_password,
    valid_first_name,
    valid_last_name,
    valid_password,
    valid_deposit_and_withdraw_amount,
    valid_num_shares
)

from app.pdf_generator import (
    generate_portfolio_statement,
    generate_transaction_statement,
    generate_trade_statement
)

load_dotenv()

app = Flask(__name__)


# tested, functional, commented
@app.template_filter()
def currency(value):
    """ Format a number as currency with commas and 2 decimals. """

    try:
        return f"{float(value):,.2f}"
    except (ValueError, TypeError):
        return value


# tested, functional, commented
@app.template_filter()
def toupper(value):
    """ Convert string to uppercase. """

    if value:
        return str(value).upper()
    return value


# tested, functional, commented
@app.template_filter()
def titlecase(value):
    """ Convert string to Title Case. """

    if value:
        return str(value).title()
    return value


# tested, functional, commented
@app.template_filter()
def shorttime(value):
    """ Format a datetime to show date + hours:minutes (no seconds/millis).
        Example: 2025-10-01 14:30 """
    
    if isinstance(value, datetime):
        return value.strftime("%d %b %Y %H:%M")
    try:
        parsed = datetime.fromisoformat(str(value))
        return parsed.strftime("%d %b %Y %H:%M")
    except Exception:
        return value


# tested, functional, commented
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        """ Ensures user is logged in before providing access to route. """

        if "user_id" not in session:
            return redirect(url_for("log_in"))
        return f(*args, **kwargs)
    
    return decorated_function


# tested, functional, commented
@app.route("/")
def home():
    """ Index html route, based on whether user is logged in or not. """

    try:

        # if user is logged in, redirect to /portfolio
        if session["user_id"]:
            return redirect("/portfolio")
        
        # else, redirect to index
        else:
            return render_template("index.html")
    
    # else, redirect to index
    except:
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
            return redirect("/portfolio")
        
        # if authetication was unsuccessful, display message
        else:
            flash(result["message"], "danger")
            return redirect("/log_in")

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
        result = validate_registration_data(data)
        if not result["success"]:
            flash(result["message"], "danger")
            return redirect("/sign_up")

        # register user
        result = register_user(data)

        # if registration was successful, log user in
        if result["success"]:
            user = result["message"]
            session["user_id"] = user.id
            return redirect("/portfolio")
        
        # if registration was unsuccessful, display message
        else:
            flash(result["message"], "danger")
            return redirect("/sign_up")

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

        # ensure password is valid
        password_result = valid_password(new_password_1)
        if not password_result["success"]:
            flash(password_result["message"], "danger")
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


# tested, functional, commented
@app.route("/market", methods=["GET", "POST"])
@login_required
def market():

    # POST request
    if request.method == "POST":
        return render_template("market.html")
    
    # GET request
    else:
        
        # get input
        symbol = request.args.get("ticker", "").strip().lower()
        
        # if symbol was provided (not initial page load)
        if len(symbol) > 0:
            
            # ensure symbol is valid
            if symbol.upper() not in ALL_SYMBOLS:
                flash("Please enter a valid ticker.", "danger")
                return redirect("/market")
            
            # instantiate stock object
            stock = create_stock(symbol)

            # ensure stock object was instantiated successfully
            if not stock:
                flash("Something went wrong. Please try again.", "danger")
                return redirect("/market")
            
            # instantiate user object
            user_id = session["user_id"]

            # get total position of user of particular equity
            result = get_user_position_by_symbol(user_id, symbol)

            # ensure position was fetched successfully
            if result["success"]:
                position = result["message"]
                shares_held = position.number_of_shares
                average_price_per_share = position.price_per_share
                total_position_value = position.total_value
            
            # if position was not fetched successfully
            else:
                shares_held = 0
                average_price_per_share = 0.00
                total_position_value = 0.00
            
            return render_template("market.html", stock=stock, shares_held=shares_held,
                                   average_price_per_share=average_price_per_share, total_position_value=total_position_value)

        # initial page load without symbol
        return render_template("market.html")


# tested, functional, commented
@app.route("/sample_market", methods=["GET"])
def sample_market():

    # POST request
    if request.method == "POST":
        return redirect("/sample_market")
    
    # GET request
    else:
        
        # get input
        symbol = request.args.get("ticker", "").strip().lower()
        
        # if symbol was provided (not initial page load)
        if len(symbol) > 0:
            
            # ensure symbol is valid
            if symbol.upper() not in ALL_SYMBOLS:
                flash("Please enter a valid ticker.", "danger")
                return redirect("/sample_market")
            
            # instantiate stock object
            stock = create_stock(symbol)

            # ensure stock object was instantiated successfully
            if not stock:
                flash("Something went wrong. Please try again.", "danger")
                return redirect("/sample_market")
            
            # set base values
            shares_held = 0
            average_price_per_share = 0.00
            total_position_value = 0.00
            
            return render_template("sample_market.html", stock=stock, shares_held=shares_held,
                                   average_price_per_share=average_price_per_share, total_position_value=total_position_value)

        # initial page load without symbol
        return render_template("sample_market.html")


# tested, functional, commented
@app.route("/place_order", methods=["POST"])
@login_required
def place_order():

    # POST request
    if request.method == "POST":

        # get type of order, symbol and user_id
        action = request.form.get("action")
        symbol = request.form.get("display_stock_symbol").strip().lower()
        user_id = session["user_id"]
        num_shares = request.form.get("order_amount")

        # format number of shares
        num_shares = valid_num_shares(num_shares)

        # ensure number of shares is valid
        if num_shares is None:
            flash("Please enter a valid number of shares.", "danger")
            return redirect("/market")
        
        # ensure symbol provided is valid
        if symbol.upper() not in ALL_SYMBOLS:
            flash("Something went wrong. Please try again.", "danger")
            return redirect("/market")
        
        # instantiate stock object
        stock = create_stock(symbol)

        # ensure stock was instantiated successfully
        if not stock:
            flash("Something went wrong. Please try again.", "danger")
            return redirect("/market")

    
        # BUY action branch
        if action == "BUY":

            # ensure stock was purchased successfully
            result = buy_stock(user_id, symbol, num_shares)
            if result["success"]:
                flash("Shares purchased successfully.", "success")
            else:
                flash("Failed to purchase shares.", "danger")

        # SELL action branch
        elif action == "SELL":

            # ensure stock was sold successfully
            result = sell_stock(user_id, symbol, num_shares)
            if result["success"]:
                flash("Shares sold successfully.", "success")
            else:
                flash("Failed to sell shares.", "danger")
        
        # INVALID action branch
        else:
            flash("Invalid action. Please try again.", "danger")
            return redirect("/market")
        
        return redirect("/market")
        

# tested, functional, commented TODO: handle if portfolio was not fetched
@app.route("/portfolio", methods=["GET"])
@login_required
def portfolio():

    # GET request
    if request.method == "GET":
        
        # get user_id and portfolio
        user_id = session["user_id"]
        portfolio = get_portfolio(user_id)
        
        return render_template("portfolio.html", portfolio=portfolio)


# tested, functional, commented
@app.route("/trades", methods=["GET"])
@login_required
def trades():

    # GET request
    if request.method == "GET":

        # get input, user_id
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")
        user_id = session["user_id"]

        # get user trade history
        result = get_user_trade_history(user_id, start_date, end_date)

        # if history was fetched successfully
        if result["success"]:
            trades = result["message"]
        
        # if it wasn't
        else:
            
            trades = []

        return render_template("trades.html", trades=trades)


# tested, functional, commented
@app.route("/account", methods=["GET"])
@login_required
def account():

    # GET request
    if request.method == "GET":

        # get input, user_id
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")
        user_id = session["user_id"]
        
        # get user transaction history
        result = get_user_transaction_history(user_id, start_date, end_date)

        # if results were fetched successfully
        if result["success"]:
            transactions = result["message"]
        
        # if results were not fetched
        else:
            flash(result["message"], "danger")
            transactions = []
        
        # get user portfolio
        portfolio = get_portfolio(user_id)

        return render_template("account.html", transactions=transactions, portfolio=portfolio)


# tested, functional, commented
@app.route("/deposit_funds", methods=["POST"])
@login_required
def deposit_funds():

    # POST request
    if request.method == "POST":

        # get input and user_id
        deposit_amount = request.form.get("deposit_amount")
        user_id = session["user_id"]

        # ensure deposit amount is valid
        if not valid_deposit_and_withdraw_amount(deposit_amount):
            flash("Please enter a valid deposit amount.", "danger")
            return redirect("/account")
        
        # log deposit
        result = deposit_user_funds(user_id, float(deposit_amount))

        # if deposit was successful
        if result["success"]:
            flash(result["message"], "success")
        
        # if deposit was unsuccessful
        else:
            flash(result["message"], "danger")
            return redirect("/account")
        
        return redirect("/account")


# tested, functional, commented
@app.route("/withdraw_funds", methods=["POST"])
@login_required
def withdraw_funds():

    # POST request
    if request.method == "POST":

        # get input and user_id
        withdraw_amount = request.form.get("withdraw_amount")
        user_id = session["user_id"]

        # ensure withdrawl amount is valid
        if not valid_deposit_and_withdraw_amount(withdraw_amount):
            flash("Please enter a valid withdraw amount.", "danger")
            return redirect("/account")
        
        # log withdrawl
        result = withdraw_user_funds(user_id, float(withdraw_amount))

        # if withdrawl was successful
        if result["success"]:
            flash(result["message"], "success")
        
        # if withdrawl was unsuccessful
        else:
            flash(result["message"], "danger")
            return redirect("/account")
        
        return redirect("/account")


# tested, functional, commented
@app.route("/portfolio_statement", methods=["GET"])
@login_required
def portfolio_statement():

    # get user object
    user_id = session["user_id"]

    # generate pdf file
    pdf_file = generate_portfolio_statement(user_id)

    # ensure it was generated
    if not pdf_file:
        flash("Failed generating portfolio statement.", "danger")
        return redirect("/portfolio")

    return send_file(pdf_file, as_attachment=True)


# tested, functional, commented
@app.route("/trade_history", methods=["POST"])
@login_required
def trade_history():

    # get user object and input
    user_id = session.get("user_id")  
    history_type = request.form.get("history_type")

    # check date constraints on query
    if history_type == "all":
        trades_result = get_user_trade_history(user_id)
    else:
        start_date = request.form.get("start_date")
        end_date = request.form.get("end_date")
        trades_result = get_user_trade_history(user_id, start_date, end_date)

    # ensure trades were fetched
    if not trades_result["success"]:
        flash("No trades found for the selected period.", "danger")
        return redirect("/trades")

    # extract list of trade objects
    trades = trades_result["message"]  

    # generate pdf file
    pdf_file = generate_trade_statement(user_id, trades)  

    return send_file(pdf_file, as_attachment=True)


# tested, functional, commented
@app.route("/transaction_history", methods=["POST"])
@login_required
def transaction_history():

    # get user object, input
    user_id = session["user_id"]
    history_type = request.form.get("history_type")

    # check date constraints on query
    if history_type == "all":
        tx_result = get_user_transaction_history(user_id)
    else:
        start_date = request.form.get("start_date")
        end_date = request.form.get("end_date")
        tx_result = get_user_transaction_history(user_id, start_date, end_date)

    # ensure transactions were fetched
    if not tx_result["success"]:
        flash("No transactions found for the selected period.", "danger")
        return redirect("/account")

    # extract list of transaction objects
    transactions = tx_result["message"]

    # generate pdf file
    pdf_file = generate_transaction_statement(user_id, transactions)

    return send_file(pdf_file, as_attachment=True)





if __name__ == "__main__":
    app.secret_key = os.getenv("SECRET_KEY")
    app.run(debug=True)