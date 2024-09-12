import matplotlib
matplotlib.use('Agg')  # Use Agg backend before importing pyplot
import matplotlib.pyplot as plt

def plot_stock_data(data, ticker, save_path='static/stock_plot.png'):
    plt.figure(figsize=(10, 6))
    plt.plot(data['Close'], label=f'{ticker} Closing Price')
    plt.title(f'{ticker} Stock Price')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()

    # Save the plot to a file instead of displaying it with Tkinter
    plt.savefig(save_path)
    plt.close()  # Close the plot to avoid display issues
