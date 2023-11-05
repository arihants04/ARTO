from flask import Flask, render_template, request, jsonify


app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/search', methods=['POST'])
def search():
    if request.method == 'POST':
        res_dict = {}

        data = str(request.json['key']).upper()

        TICKERS = ["NVDA", "NFLX", "TSLA", "APPL", "META", "BBBY"]

        if data not in TICKERS:
            return jsonify("404")

        res_dict["sentiment"] = return_sentiment(data)
        pred, inf = get_stock_details(data)
        res_dict["stock_info"] = inf
        res_dict["regression_prediction"] = pred



        return jsonify(res_dict)


def last_business_day():
    today = datetime.now()
    offset = max(1, (today.weekday() + 6) % 7 - 3)
    timedelta(days=4)  # Thursday is the last business day if today is Sunday
    most_recent = today - timedelta(offset)

    return most_recent

def get_stock_details(data):
    prev_trading_day = last_business_day()
    stock = data
    start = '2023-05-01'
    end = prev_trading_day.strftime('%Y-%m-%d')
    data = yf.download(stock,start,end)
    data.head()
    df = data.reset_index()
    df.head()

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
        volume= data['Volume'][-1]
    else:
        print("No data found for the date range. The date may be a weekend or holiday.")

    #res = [open_price, high_price, low_price, close_price, volume]
    res = [open_price, high_price, low_price, close_price]

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

    return lrpred ,res


def return_sentiment(data):
    fname = ""

    if data == "NVDA":
        fname = "nvidia.pkl"
    elif data == TICKERS[1]:
        fname = "netflix.pkl"
    elif data == TICKERS[2]:
        fname = "tesla.pkl"
    elif data == TICKERS[3]:
        fname = "apple.pkl"
    elif data == TICKERS[4]:
        fname = "meta.pkl"
    elif data == TICKERS[5]:
        fname = "BBBY.pkl"

    with open("../scraping/"+fname, 'rb') as file:
        arr = pickle.load(file)

    analyzer = SentimentIntensityAnalyzer()
    total = 0.0

    for key in arr.keys():
        outstr = key + " " + arr[key]['blurb']
        sentiment_scores = analyzer.polarity_scores(outstr)['compound']
        total += sentiment_scores

    print(len(arr.keys()))
    total /= len(arr.keys())

    if total < 0:
        total = -1/(1+math.exp(-total))

    return total

if __name__ == '__main__':
    # run app in debug mode on port 5000
    import nltk
    from nltk.sentiment.vader import SentimentIntensityAnalyzer

    import pickle

    import numpy as np
    from datetime import datetime, timedelta
    import matplotlib.pyplot as plt
    import pandas as pd
    from sklearn.linear_model import LinearRegression
    import warnings
    warnings.filterwarnings("ignore")

    import yfinance as yf

    nltk.download("vader_lexicon")






    app.run(debug=True, port=5000)
