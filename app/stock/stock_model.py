class Stock:
    def __init__(self, company_name, symbol, price):
        self.company_name = company_name.lower()
        self.symbol = symbol.lower()
        self.price = float(price)