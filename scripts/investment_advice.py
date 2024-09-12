import numpy as np
import yfinance as yf

def fetch_market_data(period='3y'):
    """Fetch historical S&P 500 data for the specified period."""
    market = yf.Ticker('^GSPC')  # S&P 500 index ticker
    return market.history(period=period)

def calculate_beta(stock_returns, market_returns):
    """Calculate the beta of the stock compared to the market."""
    # Ensure the returns are properly aligned and non-NaN
    aligned_returns = stock_returns.align(market_returns, join='inner')
    stock_returns_aligned, market_returns_aligned = aligned_returns
    
    # Drop any remaining NaN values (in case of partial overlap)
    stock_returns_aligned = stock_returns_aligned.dropna()
    market_returns_aligned = market_returns_aligned.dropna()
    
    # Ensure there is enough data to compute beta
    if len(stock_returns_aligned) < 10 or len(market_returns_aligned) < 10:  # Arbitrary threshold to ensure enough data points
        return np.nan  # Not enough data to calculate beta

    # Calculate beta as covariance(stock, market) / variance(market)
    covariance = np.cov(stock_returns_aligned, market_returns_aligned)[0, 1]
    variance = np.var(market_returns_aligned)
    beta = covariance / variance
    return beta


def fetch_pe_ratio(ticker):
    """Fetch the Price-to-Earnings ratio from Yahoo Finance."""
    stock = yf.Ticker(ticker)
    return stock.info.get('trailingPE', None)  # Fetch the P/E ratio

def give_investment_advice(data, ticker, period='1y'):
    current_price = data['Close'][-1]
    ma50 = data['50 Day MA'][-1]
    ma200 = data['200 Day MA'][-1]
    rsi = data['RSI'][-1]
    macd = data['MACD'][-1]
    signal_line = data['Signal Line'][-1]

    advice = {
        'current_price': current_price,
        'beta': None,
        'signals': [],
        'final_recommendation': None,
        'hold_period': None,  # How long to hold the stock
        'expected_increase': None  # Expected price increase in percentage
    }

    # Signal counters
    buy_count = 0
    sell_count = 0
    hold_count = 0

    # Moving Averages Strategy
    if current_price > ma50 and current_price > ma200:
        advice['signals'].append({'text': "The stock is in an uptrend based on moving averages. Consider buying.", 'type': 'buy'})
        buy_count += 1
    elif current_price < ma50 or current_price < ma200:
        advice['signals'].append({'text': "The stock is showing weakness (below moving averages). Consider selling or monitoring closely.", 'type': 'sell'})
        sell_count += 1

    # RSI Strategy
    if rsi < 30:
        advice['signals'].append({'text': "The stock is oversold (RSI < 30). This might be a buy signal.", 'type': 'buy'})
        buy_count += 1
    elif rsi > 70:
        advice['signals'].append({'text': "The stock is overbought (RSI > 70). This might be a sell signal.", 'type': 'sell'})
        sell_count += 1
    else:
        advice['signals'].append({'text': "The stock has neutral momentum based on RSI. Consider holding.", 'type': 'hold'})
        hold_count += 1

    # MACD Strategy
    if macd > signal_line:
        advice['signals'].append({'text': "The MACD line is above the Signal line. Buy signal.", 'type': 'buy'})
        buy_count += 1
    elif macd < signal_line:
        advice['signals'].append({'text': "The MACD line is below the Signal line. Sell signal.", 'type': 'sell'})
        sell_count += 1

    # Fetch P/E Ratio and give advice
    pe_ratio = fetch_pe_ratio(ticker)
    if pe_ratio:
        advice['signals'].append({'text': f"P/E Ratio: {pe_ratio:.2f}", 'type': 'neutral'})
        if pe_ratio < 15:
            advice['signals'].append({'text': "This stock has a low P/E ratio compared to the industry. Buy signal.", 'type': 'buy'})
            buy_count += 1
        elif pe_ratio > 25:
            advice['signals'].append({'text': "This stock has a high P/E ratio compared to the industry. Sell signal.", 'type': 'sell'})
            sell_count += 1
        else:
            advice['signals'].append({'text': "This stock has a moderate P/E ratio. Hold signal.", 'type': 'hold'})
            hold_count += 1
    else:
        advice['signals'].append({'text': "P/E ratio not available for this stock.", 'type': 'neutral'})

    # Fetch market data and calculate Beta
    market_data = fetch_market_data(period)
    stock_returns = data['Close'].pct_change().dropna()
    market_returns = market_data['Close'].pct_change().dropna()

    # Calculate Beta
    beta = calculate_beta(stock_returns, market_returns)
    advice['beta'] = beta

    # Handle missing or NaN beta
    if beta is not None and not np.isnan(beta):
        if beta > 1:
            advice['signals'].append({'text': "This stock is more volatile than the market. Be cautious if you are risk-averse.", 'type': 'sell'})
            sell_count += 1
        elif beta < 1:
            advice['signals'].append({'text': "This stock is less volatile than the market. This might be a safer investment.", 'type': 'buy'})
            buy_count += 1
        else:
            advice['signals'].append({'text': "This stock has a volatility similar to the market.", 'type': 'neutral'})
    else:
        advice['signals'].append({'text': "Beta could not be calculated for this period due to insufficient data.", 'type': 'neutral'})

    # Final recommendation based on the counts of buy/sell/hold signals
    if buy_count > sell_count and buy_count > hold_count:
        advice['final_recommendation'] = "Buy"
        # Estimate holding period and expected increase based on historical performance
        advice['hold_period'] = "6 months"  # Example: You could base this on trends
        advice['expected_increase'] = f"Expected price increase: {round((current_price * 0.1), 2)}%"  # Example: 10% increase
    elif sell_count > buy_count and sell_count > hold_count:
        advice['final_recommendation'] = "Sell"
    else:
        advice['final_recommendation'] = "Hold"

    return advice
