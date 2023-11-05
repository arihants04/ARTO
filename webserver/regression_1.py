import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LinearRegression

import warnings
warnings.filterwarnings("ignore")

import yfinance as yf
yf.pdr_override()


# Function to get the last business day
def last_business_day():
    today = datetime.now()
    offset = max(1, (today.weekday() + 6) % 7 - 3)
    timedelta(days=4)  # Thursday is the last business day if today is Sunday
    most_recent = today - timedelta(offset)

    return most_recent

# Determine the previous trading day (assuming the current day is not a trading day)
prev_trading_day = last_business_day()

def get_regression_prediction(stockTicker):
    stock = stockTicker
    start = '2023-05-01'
    end = prev_trading_day.strftime('%Y-%m-%d')
    data = yf.download(stock,start,end)
    data.head()
    df = data.reset_index()
    df.head()
    print(data)

# Format the date for yfinance
    prev_trading_day_str = end #prev_trading_day.strftime('%Y-%m-%d')

    df = yf.download(stock, start=start, end=end)
    df = df.reset_index()

    if not data.empty:
    # The 'Open' column contains the opening prices
        open_price = data['Open'][-1]  # Get the last (or only) open price
        high_price = data['High'][-1]
        low_price = data['Low'][-1]
        close_price = data['Close'][-1]
        volume_price = data['Volume'][-1]
        print(f"The opening price for {stock} on {prev_trading_day_str} was {open_price}")
        print(f"The high price for {stock} on {prev_trading_day_str} was {high_price}")
        print(f"The low price for {stock} on {prev_trading_day_str} was {low_price}")
        print(f"The close price for {stock} on {prev_trading_day_str} was {close_price}")
        print(f"The volume of {stock} on {prev_trading_day_str} was {volume_price}")
    else:
        print("No data found for the date range. The date may be a weekend or holiday.")

    X_train = df[df.columns[1:5]] # data_aal[['open', 'high', 'low', 'close']]
    Y_train = df['Adj Close']

    X_train = X_train.values[:-1]
    Y_train = Y_train.values[1:]
    lr = LinearRegression()

    lr.fit(X_train, Y_train)

    X_test = df[df.columns[1:5]].values[:-1]
    Y_test = df['Adj Close'].values[1:]

    lr.score(X_test, Y_test)

    lrpred = lr.predict([[open_price, high_price, low_price, close_price]])[0]

    return lrpred


print(get_regression_prediction("META"))
