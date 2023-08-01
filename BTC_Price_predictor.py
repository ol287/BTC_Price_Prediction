import requests
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def price_prediction(data):
    timestamps = []
    prices = []
    for entry in data['Time Series (Digital Currency Monthly)']:
        timestamps.append(entry)
        prices.append(float(data['Time Series (Digital Currency Monthly)'][entry]['4a. close (USD)']))
    
    # Prepare the data for linear regression
    X = np.arange(len(prices)).reshape(-1, 1)
    y = np.array(prices)

    # Perform linear regression
    slope, intercept = np.polyfit(X.ravel(), y, 1)

    # Predict the next price
    next_price = slope * (len(prices) + 1) + intercept

    return next_price

def plot_prediction(data, prediction):
    timestamps = []
    prices = []
    for entry in data['Time Series (Digital Currency Monthly)']:
        timestamps.append(entry)
        prices.append(float(data['Time Series (Digital Currency Monthly)'][entry]['4a. close (USD)']))

    # Convert timestamps to datetime objects
    dates = [datetime.strptime(ts, '%Y-%m-%d') for ts in timestamps]

    # Extend dates to include the prediction date
    today_date = datetime.today().date()
    next_date = today_date + timedelta(days=30)  # Assuming monthly data, extend by 30 days
    extended_dates = dates + [next_date]

    # Prepare data for plotting
    X = np.arange(len(extended_dates)).reshape(-1, 1)
    y = np.array(prices + [prediction])

    # Plot the data and prediction line
    plt.figure(figsize=(10, 6))
    plt.plot(extended_dates, y, label='Price', color='blue')
    plt.plot(next_date, prediction, 'ro', label='Prediction')
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.title('Bitcoin Price Prediction')
    plt.legend()
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

url = 'https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_MONTHLY&symbol=BTC&market=USD&apikey=IOBHACZOQONDVU8B'
r = requests.get(url)
data = r.json()

prediction = price_prediction(data)
print(f"Predicted price of Bitcoin for next month: ${prediction:.2f}")

plot_prediction(data, prediction)