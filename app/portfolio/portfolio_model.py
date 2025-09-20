class Portfolio:
    def __init__(self, user, total_equities_value=None, positions=None):
        self.user_id = user.id
        self.cash_balance = user.cash_balance

        if positions:
            self.positions = positions
    