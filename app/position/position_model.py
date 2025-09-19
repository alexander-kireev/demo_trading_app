class Position:
    def __init__(self, stock, number_of_shares):
        self.company_name = stock.company_name
        self.symbol = stock.symbol
        self.price = stock.price
        self.number_of_shares = number_of_shares
        self.total_value = self.price * self.number_of_shares


