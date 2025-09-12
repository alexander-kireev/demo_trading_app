class Stock:
    def __init__(self, company_name, symbol, price):
        self.company_name = company_name.title()
        self.symbol = symbol.upper()
        self.price = float(price)