
from app.position.position_repo import (
    get_user_equity_symbols,
    get_user_positions_of_equity,
    get_user_single_position_of_equity
)


def aggregate_positions_of_single_equity(user_id, symbol):
    positions = get_user_positions_of_equity(user_id, symbol)
    

    total_shares = 0
    total_position_value = 0


    for position in positions:
        total_shares += position["number_of_shares"]
        total_position_value += position["total_value"]

    company_name = positions[0]["company_name"]
    average_price_per_share = total_position_value / total_shares
    
    return {
        "company_name": company_name,
        "number_of_shares": total_shares,
        "average_price_per_share": average_price_per_share,
        "total_position_value": total_position_value
    }


def aggregate_all_equity_positions(user_id, equity_symbols):
    positions = {}
    for symbol in equity_symbols:
        positions[symbol] = aggregate_positions_of_single_equity(user_id, symbol)
        
    return positions

def aggregate_total_value_of_equity_positions(positions):
    total_equities_value = 0
    for symbol in positions:
        total_equities_value += positions[symbol]["total_value"]

    return total_equities_value

