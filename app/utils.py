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


# tested, functional, commented
def validate_registration_data(data):
    """ Accepts a dict containing user registration data, validates it, returns true
        if all inputs are valid. """

    if not valid_first_name(data["first_name"]):
        return {
            "success": False,
            "message": "Invalid first name."
        }
    
    if not valid_last_name(data["last_name"]): #
        return {
            "success": False,
            "message": "Invalid last name."
        }
    
    if not email_is_valid(data["email"]): #
        return {
            "success": False,
            "message": "Invalid email address."
        }
    
    if not valid_password(data["first_password"]): #
        return {
            "success": False,
            "message": """Password must contain at least one lowercase character, one uppercase character,
                        one number and be between 12 and 24 characters long."""
        }
    
    if not passwords_match(data["first_password"], data["second_password"]): #
        return {
            "success": False,
            "message": "Passwords must match."
        }

    return {
        "success": True,
        "message": "Registration data is valid."
    }   


# tested, functional, commented
def valid_first_name(first_name):
    """ Accepts first_name, returns true if it is within length boundaries and contains only 
        alphanumerical characters. """

    # establish mix/max boundaries
    min_length = 1
    max_length = 50

    try:
        
        # format
        first_name = first_name.strip().lower()

        # check length
        if len(first_name) < min_length or len(first_name) > max_length:
            return False
        
        return first_name.isalpha()
    
    except (ValueError, TypeError):
        return None


# tested, functional, commented
def valid_last_name(last_name):
    """ Accepts last_name, returns true if it is within length boundaries and contains only 
        alphanumerical characters. """

    # establish mix/max boundaries
    min_length = 1
    max_length = 50

    try:
        
        # format
        last_name = last_name.strip().lower()

        # check length
        if len(last_name) < min_length or len(last_name) > max_length:
            return False
        
        return last_name.isalpha()
    
    except (ValueError, TypeError):
        return None


# tested, functional, commented
def valid_password(password):
    """ Accepts a password and checks if it is valid (is betwen 8 and 24 characters long,
        contains at least one digit, one uppercase and lowercase characters.) """

    # set flags to false
    has_lowercase = False
    has_uppercase = False
    has_digit = False

    # ensure length is between 8 and 24 chars
    if len(password) < 12 or len(password) > 24:
        return False

    # ensure digit, lower and upper case chars are present
    for char in password:
        if char.isdigit():
            has_digit = True
        elif char.islower():
            has_lowercase = True
        elif char.isupper():
            has_uppercase = True
        else:
            return False

    # check if all conditions have been met
    if has_digit and has_lowercase and has_uppercase:
        return True
    else:
        return False


# tested, functional, commented
def passwords_match(password_1, password_2):
    """ Accepts two passwords, ensures they match. """

    return password_1 == password_2


# tested, functional, commented
def valid_deposit_and_withdraw_amount(amount):
    """  Accepts amount and ensure it is of correct type and is within min/max boundaries. """

    # set min/max boundaries
    min = 10
    max = 1000000

    try:
        amount = float(amount)
        if amount > min and amount < max:
            return True
        return False
    except (ValueError, TypeError):
        return False
    

#TODO: FIX! 
def valid_num_shares(num_shares):
    
    try:
        num_shares = int(num_shares)

        if num_shares < 1 or num_shares > 100000:
            return None
        
        return num_shares
    
    except (ValueError, TypeError):
        return None