import pandas as pd

def analyze_data(data):
    """Analyze stock data by calculating key financial metrics."""
    # Moving Averages
    data['50 Day MA'] = data['Close'].rolling(window=50).mean()
    data['200 Day MA'] = data['Close'].rolling(window=200).mean()
    
    # RSI Calculation
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    data['RSI'] = 100 - (100 / (1 + rs))
    
    # MACD Calculation
    data['12 Day EMA'] = data['Close'].ewm(span=12, adjust=False).mean()
    data['26 Day EMA'] = data['Close'].ewm(span=26, adjust=False).mean()
    data['MACD'] = data['12 Day EMA'] - data['26 Day EMA']
    data['Signal Line'] = data['MACD'].ewm(span=9, adjust=False).mean()

    return data
