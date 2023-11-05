import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LinearRegression

import warnings
warnings.filterwarnings("ignore")

import yfinance as yf
yf.pdr_override()


# In[102]:


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
    stock = 'NVDA'
    start = '2023-05-01'
    end = prev_trading_day.strftime('%Y-%m-%d')
    data = yf.download(stock,start,end)
    data.head()
    df = data.reset_index()
    df.head()

# Format the date for yfinance
    prev_trading_day_str = end #prev_trading_day.strftime('%Y-%m-%d')

# Download the data
# We will download a small interval to ensure we're getting the previous day's data
    df = yf.download(stock, start=start, end=end)
    df = df.reset_index()

# Check if we got any data back, if not, we may need to adjust the dates for holidays, etc.
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
        print(f"The volume price for {stock} on {prev_trading_day_str} was {volume_price}")
    else:
        print("No data found for the date range. The date may be a weekend or holiday.")




# In[103]:


    X_train = df[df.columns[1:5]] # data_aal[['open', 'high', 'low', 'close']]
    Y_train = df['Adj Close']


# In[104]:


    X_train = X_train.values[:-1]
    Y_train = Y_train.values[1:]


# In[105]:


    lr = LinearRegression()


# In[106]:


    lr.fit(X_train, Y_train)


# In[107]:


    X_test = df[df.columns[1:5]].values[:-1]
    Y_test = df['Adj Close'].values[1:]


# In[108]:


    lr.score(X_test, Y_test)


# In[109]:


#opening_price = float(input('Open: '))
#high = float(input('High: '))
#low = float(input('Low: '))
#close = float(input('Close: '))
    lrpred = lr.predict([[open_price, high_price, low_price, close_price]])[0]
    return lrpred


