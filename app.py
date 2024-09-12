from flask import Flask, render_template, request
from scripts.fetch_data import fetch_stock_data
from scripts.analyze_data import analyze_data
from scripts.visualize_data import plot_stock_data
from scripts.investment_advice import give_investment_advice
import os

app = Flask(__name__)

# Home page where the user inputs the stock ticker
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle stock data fetching and display
@app.route('/stock', methods=['POST'])
def stock():
    ticker = request.form['ticker'].upper()  # Get ticker from form
    period = request.form.get('period', '1mo')  # Get period from form (default to 1 month)

    try:
        # Fetch, analyze, and plot stock data
        stock_data = fetch_stock_data(ticker, period)
        analyzed_data = analyze_data(stock_data)

        # Save the plot image in the 'static' directory
        plot_filename = os.path.join('static', 'stock_plot.png')
        plot_stock_data(analyzed_data, ticker, save_path=plot_filename)

        # Generate in-depth investment advice with Beta included
        advice = give_investment_advice(analyzed_data, ticker, period)

        # Render the result page with the plot, advice, and final recommendation
        return render_template(
            'stock.html', 
            ticker=ticker, 
            image_file=plot_filename, 
            current_price=advice['current_price'], 
            beta=advice['beta'], 
            signals=advice['signals'], 
            final_recommendation=advice['final_recommendation'],
            hold_period=advice['hold_period'],  # Pass hold period to template
            expected_increase=advice['expected_increase']  # Pass expected increase to template
        )

    except ValueError as e:
        # Handle error by rendering the form again with an error message
        error_message = f"Could not find data for ticker '{ticker}'. Please try again with a valid ticker."
        return render_template('index.html', error_message=error_message)

if __name__ == "__main__":
    app.run(debug=True)
