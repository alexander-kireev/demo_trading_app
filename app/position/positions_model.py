
# tested, functional
class Positions:
    def __init__(self, positions, user_id, symbol):
        self.user_id = user_id
        self.symbol = symbol
        self.positions = positions
        self.total_number_of_shares = self.calc_total_number_of_shares()

    
    def calc_total_number_of_shares(self):
        total_shares = 0
        for position in self.positions:
            total_shares += position.number_of_shares
        return total_shares
