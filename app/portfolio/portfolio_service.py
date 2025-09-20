from app.user.user_model import User
from app.user.user_service import (
    get_user_by_id
)

from db_core import DBCore

from portfolio_model import Portfolio

from app.position.position_model import Position
from app.position.positions_model import Positions

from app.position.position_service import (
    aggregate_positions_of_single_equity,
    aggregate_all_equity_positions,
    aggregate_total_value_of_equity_positions
)

from app.position.position_repo import (
    get_user_positions_of_equity,
    get_user_single_position_of_equity,
    get_user_all_positions,
    get_user_equity_symbols
)
def get_portfolio(user_id):
    try:
        with DBCore.get_connection() as conn:
            with conn.cursor() as cur:
            
                user = get_user_by_id(cur, user_id)

                if not user:
                    return {
                        "success": False,
                        "message": "Failed to fetch user."
                    }
                
                if equity_symbols := get_user_equity_symbols(cur, user_id):

                    
                    positions = aggregate_all_equity_positions(user, equity_symbols)

                    if not positions:
                        return {
                            "success": False,
                            "message": "Failed to aggregate positions."
                        }
                    
                    total_equities_value = aggregate_total_value_of_equity_positions(positions)

                    if not total_equities_value:
                        return {
                            "success": False,
                            "message": "Failed to tabulate total value of equities."
                        }
                    
                    conn.commit()
                    return Portfolio(user, positions, total_equities_value)

                else:
                    return Portfolio(user)
                
    except Exception as e:
        return {
            "success": False,
            "message": f"Error. Failed to fetch portfolio: {e}."
        }




