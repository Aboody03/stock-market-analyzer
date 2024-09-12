import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import pytz

def fetch_stock_data(ticker, period='1mo'):
    """Fetch historical stock data for the given ticker."""
    stock = yf.Ticker(ticker)
    
    # Handle 3-year period manually
    if period == '3y':
        # Fetch 5 years of data and filter out the last 3 years
        data = stock.history(period='5y')
        
        # Get the current UTC time
        utc = pytz.UTC
        
        # Calculate the date 3 years ago, making it timezone-aware in UTC
        three_years_ago = utc.localize(datetime.now() - timedelta(days=3*365))
        
        # Filter the data to only include the last 3 years
        data = data.loc[three_years_ago:]
    else:
        data = stock.history(period=period)

    # Check if any data was returned
    if data.empty:
        raise ValueError(f"No data found for ticker symbol: {ticker}")

    return data
