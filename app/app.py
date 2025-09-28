from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash
)

from functools import wraps

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
    update_user_first_name,
    update_user_last_name,
    update_user_dob
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
    valid_password
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


# tested, functional
@app.route("/log_in", methods=["GET", "POST"])
def log_in():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        result = authenticate_user(email, password)

        if result["success"]:
            user = result["message"]
            session["user_id"] = user.id
            return redirect("/")
        else:
            error = result["message"]
            return render_template("log_in.html", error=error)
              
    return render_template("log_in.html")



# tested, functional
@app.route("/sign_up", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        data = {
            "first_name": request.form["first_name"],
            "last_name": request.form["last_name"],
            "dob": request.form["dob"],
            "email": request.form["email"],
            "first_password": request.form["first_password"],
            "second_password": request.form["second_password"]
        }
        
        error = validate_registration_data(data)
        if error:
            return render_template("sign_up.html", error=error)

        result = register_user(data)
        if result["success"]:
            user = result["message"]
            session["user_id"] = user.id
            return redirect("/")
        else:
            error = "Sorry, something went wrong. Please try to register again."
            return render_template("sign_up.html", error=error)
        

    return render_template("sign_up.html")


# tested, functional
@app.route("/log_out")
@login_required
def log_out():
    session.clear()
    return redirect("/")


# tested, functional
@app.route("/account")
@login_required
def account():
    return render_template("account.html")


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


# TODO: CHECK THIS! NOT TESTED AT ALL!
@app.route("/change_user_details", methods=["GET", "POST"])
@login_required
def change_user_details():

    if request.method == "POST":
        first_name = request.form.get("first_name", "").strip()
        last_name = request.form.get("last_name", "").strip()
        dob = request.form.get("dob", "").strip()

        if first_name := valid_first_name(first_name):
            if not update_user_first_name(user_id, first_name):
                flash("Failed updating first name. Please try again.", "danger")
                return redirect("/change_user_details")

        if last_name := valid_last_name(last_name):
            if not update_user_last_name(user_id, last_name):
                flash("Failed updating last name. Please try again.", "danger")
                return redirect("/change_user_details")
            
        if dob := valid_dob(dob):
            if not update_user_dob(user_id, dob):
                flash("Failed updating date of birth. Please try again.", "danger")
                return redirect("/change_user_details")

        flash("Your personal details have been successfully updated.")
        return redirect("/change_user_details")


    else:
        user_id = session["user_id"]
        user = get_user(user_id)

        first_name = user.first_name
        last_name = user.last_name
        dob = user.dob

        return render_template("change_user_details.html", 
                               first_name=first_name, last_name=last_name, dob=dob)
    return

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



if __name__ == "__main__":
    app.secret_key = os.getenv("SECRET_KEY")
    app.run(debug=True)




