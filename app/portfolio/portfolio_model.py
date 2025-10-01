# tested, functional, commented
class Portfolio:
    def __init__(self, user, total_equities_value=None, positions=None):
        self.user = user
        self.cash_balance = user.cash_balance

        # if user has open equity positions
        if positions:
            self.positions = positions
            self.positions_value = total_equities_value
            self.portfolio_value = float(self.positions_value) + float(self.cash_balance)
        # if user has no open equity positions
        else:
            self.positions = None
            self.positions_value = 0
            self.portfolio_value = float(self.cash_balance)
    
    # prints portfolio. this is more of a testing function for now
    def print_portfolio(self):
        print(f"User ID: {self.user.id}.")
        print(f"User's cash balance: ${self.cash_balance}.")

        # if user has no open equity positions
        if not self.positions:
            print("User has no equities.")
        # if he does
        else:
            print(f"User's value of equities: ${self.positions_value}.")
        

        print(f"User's portfolio value: ${self.portfolio_value}.")
        
        # print equity position totals line by line, if present
        if self.positions:
            print()
            print(f"User's equity holdings:")
            for position in self.positions.values():
                print(f"Symbol : {position.symbol}.")
                print(f"Company name: {position.company_name}.")
                print(f"Average price per share: ${position.price_per_share}.")
                print(f"Live price per share: ${position.last_price_per_share}.")
                print(f"Number of shares: {position.number_of_shares}.")
                print(f"Total value: ${position.total_value}")
                print()
        