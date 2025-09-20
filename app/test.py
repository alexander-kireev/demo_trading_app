from user.user_model import User
from user.user_service import (
    register_user
)

from setup.users_table_setup import define_users_table

# # register a user
# first_name = "bob"
# last_name = "grimes"
# dob = "24-09-1995"
# email = "bob@email.com"
# password = "password"

# register_user(first_name, last_name, dob, email, password)

define_users_table()