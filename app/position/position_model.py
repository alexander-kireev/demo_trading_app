# tested, functional, commented
class Position:
    def __init__(self, stock, number_of_shares, user_id, total_value=None, position_id=None, last_price_per_share=None):   
        self.user_id = user_id
        self.company_name = stock.company_name
        self.symbol = stock.symbol
        self.price_per_share = stock.price
        self.number_of_shares = number_of_shares
        self.total_value = total_value

        # optional
        if position_id:
            self.position_id = position_id

        # calculate total value of position if it was not provided as an arg
        if not total_value:
            self.total_value = self.price_per_share * self.number_of_shares

        # ensure last_price is not left as null
        if not last_price_per_share:
            self.last_price_per_share = stock.price
        else:
            self.last_price_per_share = last_price_per_share




