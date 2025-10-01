from yfinance import Ticker, Tickers

from app.stock.stock_model import Stock


# tested, functional, commented
def create_stock(symbol):
    """ Accepts a stock symbol, fetches live stock data and returns stock object. """
    
    try:
        
        # format and retrieve data
        symbol = symbol.upper()
        data = Ticker(symbol).info
        price = data["regularMarketPrice"]

        company_name = data["shortName"]
        
        return Stock(company_name, symbol, price)
    
    except Exception as e:
        return None
    

# tested, functional, commented
def create_stocks(symbols):
    """ Accepts a list of stock symbols, returns a dictionary with stock symbols as keys and stock objects
        as values. """
    
    stocks = {}

    for symbol in symbols:
        stocks[symbol] = create_stock(symbol)
    
    return stocks


# tested, functional, commented 
def live_stock_price(symbol):
    """ Accepts a symbol of equity and returns a live price from the API. """

    return Ticker(symbol).fast_info["lastPrice"]



    

