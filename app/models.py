class User:
    def __init__(self, first_name, last_name, dob, email, password_hash=None, balance=None, id=None):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.dob = dob
        self.email = email
        self.password_hash = password_hash
        self.balance = balance
    
    def get_password_hash(self):
        return self.password_hash