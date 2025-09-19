class Trade:
    def __init__(self, user_id, stock,
                 number_of_shares, transaction_type, transaction_total=None, trade_id=None):
        self.user_id = user_id
        self.company_name = stock.company_name
        self.symbol = stock.symbol
        self.price_per_share = stock.price
        self.number_of_shares = number_of_shares
        self.transaction_type = transaction_type
        
        if trade_id:
            self.trade_id = trade_id

        if transaction_total:
            self.transaction_total = transaction_total
        else:
            self.transaction_total = self.number_of_shares * self.price_per_share

    