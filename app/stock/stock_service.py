from yfinance import Ticker, Tickers

from app.stock.stock_model import Stock


# tested, functional, commented
def create_stock(symbol):
    """ Accepts a stock symbol, fetches live stock price and returns stock object. """
    
    info = Ticker(symbol).info
    return Stock(info["shortName"], symbol, info["regularMarketPrice"])
    

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

    return Ticker(symbol).info["regularMarketPrice"]