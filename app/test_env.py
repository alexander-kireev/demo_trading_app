from app.user.user_model import User
from app.user.user_service import (
    register_user,
    delete_user,
    deposit_user_funds,
    withdraw_user_funds,
    update_user_email,
    update_user_password
)



# register a user
first_name = "bob"
last_name = "grimes"
dob = "24-09-1995"
email = "bob@email2.com"
password = "password"

new_email = "new_email@email.com"
new_password = "password"

# print(register_user(first_name, last_name, dob, email, password))
print(update_user_password(4, password, new_password))









