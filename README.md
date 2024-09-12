The Stock Market Analyzer is a Python-based tool that fetches, processes, and analyzes stock market data to provide investment insights. The application offers personalized recommendations, such as Buy, Sell, or Hold, based on key financial indicators like Moving Averages (MA), Relative Strength Index (RSI), and Moving Average Convergence Divergence (MACD).

The tool uses web scraping to fetch real-time stock data from Yahoo Finance and processes it to generate detailed financial insights and visualizations. It provides a final recommendation, such as how long to hold a stock and expected price increases if the recommendation is to Buy.

Project Features:
1) Stock Data Fetching: Pulls historical stock data for a user-specified time period using Yahoo Finance.
2) Technical Analysis: Computes key financial indicators like:
3) 50-day and 200-day moving averages (MA)
4) Relative Strength Index (RSI)
5) Moving Average Convergence Divergence (MACD) and its Signal Line
6) Beta value relative to the market
7) Buy, Hold, Sell Recommendations: Based on the stock's technical analysis, the tool provides investment recommendations.
8) Graphical Visualization: Generates a plot of the stock's historical price trends, which is displayed on the website.
9) Error Handling: Gracefully handles invalid ticker symbols and allows users to input correct stock information without crashing.

How the Project Works:
1) Stock Data Fetching:
The stock data is fetched using Yahoo Finance through the yfinance package. Users input a stock ticker and select a time period, and the system scrapes historical data for the stock within the specified period.

2) Stock Data Analysis:
The core analysis is done in the analyze_data.py file, which computes key financial metrics:

50 Day & 200 Day Moving Averages (MA): Used to identify long-term trends.
Relative Strength Index (RSI): Used to determine if the stock is overbought or oversold.
MACD & Signal Line: Used to determine momentum shifts and buy/sell signals.
Beta Calculation: Compares stock volatility to the market for risk analysis.

3) Buy, Hold, Sell Recommendations:
Based on the financial indicators, the tool provides a Buy, Hold, or Sell recommendation. If the recommendation is Buy, it also suggests a holding period and an expected price increase based on historical data.

4) Graphical Visualization:
The tool plots the stock's closing prices over time, overlaying the moving averages to provide visual insight into stock performance. The graph is displayed on the web interface.

Requirements:
To run this project, you will need:

Python 3.6+

Flask: For the web interface

Pandas: For data processing and analysis

Matplotlib: For plotting stock price trends

yfinance: For fetching stock data from Yahoo Finance

To install the required packages, run the following line in your terminal:
pip install -r requirements.txt
