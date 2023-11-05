from flask import Flask, render_template, request, jsonify


app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/getai', methods=['POST'])
def getai():
    if request.method == 'POST':
        tick = str(request.json['tick']).upper()
        sen = str(request.json['sen'])
        rMod = str(request.json['reg'])
        clo = str(request.json['close'])
        insT = str(request.json['ins'])


        output = replicate.run(
          "meta/llama-2-13b-chat:f4e2de70d66816a838a89eeeb621910adffb0dd0baba3976c96980970978018d",
          input={
            "top_k": 50,
            "top_p": 1,
            "prompt": f"Will {tick} value go up or down? The current consumer sentiment is {sen}, \
            a regression model is predicting a change of {rMod}, and it closed at {clo} today. Most insiders \
              are currently {insT}",
            "temperature": 0.75,
            "system_prompt": "You answer the prompt without any greetings.You answer in short replies of 2 to 3 sentences",
            "max_new_tokens": 800,
            "min_new_tokens": -1,
            "repetition_penalty": 1
          }
        )
        bruh = ""

        for i in output:
            bruh += (i)

        return jsonify(bruh)

@app.route('/search', methods=['POST'])
def search():
    if request.method == 'POST':
        res_dict = {}

        data = str(request.json['key']).upper()

        TICKERS = ["NVDA", "NFLX", "TSLA", "AAPL", "META"]

        if data not in TICKERS:
            return jsonify("404")

        res_dict["sentiment"] = return_sentiment(data)
        pred, inf = get_stock_details(data)
        res_dict["stock_info"] = inf
        res_dict["regression_prediction"] = pred

        res_dict["insider_trading"] = get_insider_trading(data)



        return jsonify(res_dict)

def get_insider_trading(stock):
    df = pd.read_csv('trading.csv')
    df = df[df['Symbol'] == stock]
    bruh = []

    for index, row in df.iterrows():
        bruh.append(row['Transaction Date'])
        bruh.append(str(row['Transaction Total']))
        bruh.append(row['Transaction'])
    #return as a row where each one is 3

    return bruh

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
    TICKERS = ["NVDA", "NFLX", "TSLA", "AAPL", "META"]

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
    import replicate

    import pandas as pd

    nltk.download("vader_lexicon")






    app.run(debug=True, port=5000)
