import bcrypt
import re

# tested, functional, commented
def email_is_valid(email):
    """ Accepts an email, returns true if the email is valid based on a regex function. """
    
    # ensure email is a string
    if not isinstance(email, str):
        return False
    
    # ensure string fits pattern of email type
    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    match = re.match(pattern, email)
    if match is not None:
        return True
    else:
        return False


# tested, functional, commented
def hash_password(password):
    """ Accepts a password and returns a hash of it. """

    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


# tested, functional, commented
def verify_password(password, hashed_password):
    """ Accepts a plaintext password and a hash of a password, returns true if they match. """

    return bcrypt.checkpw(password.encode(), hashed_password.encode())


# TODO: implement validation of user data at point of registration
def validate_registration_data(data):
    if not valid_first_name(data["first_name"]):
        return "Invalid first name."
    
    if not valid_last_name(data["last_name"]):
        return "Invalid last name."
    
    if not valid_dob(data["dob"]):
        return "Invalid date of birth."
    
    if not valid_email(data["email"]):
        return "Invalid email address."
    
    if not valid_password(data["first_password"]):
        return "Invalid password."
    
    if not passwords_match(data["first_password"], data["second_password"]):
        return "Passwords do not match."
    
    return None

def valid_first_name(first_name):
    try:
        return first_name.lower()
    except (ValueError, TypeError):
        return None

def valid_last_name(last_name):
    try:
        return last_name.lower()
    except (ValueError, TypeError):
        return None

def valid_dob(dob):
    return dob

def valid_email(email):
    return True

def valid_password(password):
    return True

def passwords_match(password_1, password_2):
    return password_1 == password_2