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
            a regression model is predicting a change of {rMod} from open, and it closed at {clo} today. Most of the inside \
              trading is currently {insT}",
            "temperature": 0.75,
            "system_prompt": "You answer the prompt without any greetings.You answer in short replies of 5 to 6 sentences",
            "max_new_tokens": 800,
            "min_new_tokens": -1,
            "repetition_penalty": 1
          }
        )
        bruh = ""

        for i in output:
            bruh += (i)

        return jsonify(bruh.strip())

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

        pain = {'NVDA': [['Where Will Nvidia Stock Be in 3 Years?',
   'https://www.fool.com//investing/2023/10/13/where-will-nvidia-stock-be-in-3-years/'],
  ['How Nvidia Is Trouncing Amazon, Google, and Microsoft on 1 Critical Investing Metric',
   'https://www.fool.com//investing/2023/10/13/how-nvidia-trouncing-amazon-google-microsoft/'],
  ['Advanced Micro Devices And Nvidia Just Made Big AI Moves This Week, but Nvidia Still Seems Far Ahead',
   'https://www.fool.com//investing/2023/10/12/advanced-micro-devices-and-nvidia-just-made-moves/'],
  ['Nvidia Is Far Behind These 3 Semiconductor Stocks In 1 Key Metric -- Is the AI Growth Stock Still a Buy?',
   'https://www.fool.com//investing/2023/10/12/nvidia-is-far-behind-these-3-semiconductor-stocks/'],
  ['1 Green Flag for Nvidia Stock in 2023, and 1 Red Flag',
   'https://www.fool.com//investing/2023/10/12/1-green-flag-nvidia-stock-2023-1-red-flag/']],
 'NFLX': [['What Is the Straight Line Method?',
   'https://www.fool.com//terms/s/straight-line-method/'],
  ['2 Popular Tech Stocks Investors Dropped in July',
   'https://www.fool.com//investing/2023/08/02/2-popular-tech-stocks-investors-dropped-in-july/'],
  ['Netflix Stock: Is the Party Over?',
   'https://www.fool.com//investing/2023/07/31/netflix-stock-is-the-party-over/'],
  ['Should You Buy This Unstoppable FAANG Stock Right Now?',
   'https://www.fool.com//investing/2023/07/28/should-you-buy-unstoppable-faang-stock-right-now/'],
  ['The Streaming Stock to Hold as Hollywood Strikes',
   'https://www.fool.com//investing/2023/07/27/the-streaming-stock-to-hold-as-hollywood-strikes/']],
 'TSLA': [['Why Tesla Stock Is Plunging Today',
   'https://www.fool.com//investing/2023/10/19/why-tesla-stock-is-plunging-today/'],
  ['1 EV Stock to Buy Hand Over Fist Right Now',
   'https://www.fool.com//investing/2023/10/19/1-ev-stock-to-buy-hand-over-fist-right-now/'],
  ['Tesla, Netflix Earnings: Everything You Need to Know',
   'https://www.fool.com//investing/2023/10/19/tesla-netflix-earnings-everything-you-need-to-know/'],
  ['1 Reason to Buy This "Magnificent Seven" Stock, and 1 Reason to Avoid It Like the Plague',
   'https://www.fool.com//investing/2023/10/19/1-reason-buy-and-sell-this-magnificent-seven-stock/'],
  ["Tesla's War Chest of Cash and Investments Surpasses $26 Billion",
   'https://www.fool.com//investing/2023/10/19/teslas-war-chest-of-cash-and-investments-swells-to/']],
 'AAPL': [['How Many Small-Cap Stocks Are There?',
   'https://www.fool.com//investing/stock-market/types-of-stocks/small-cap-stocks/how-many-small-cap-stocks/'],
  ['Better Growth Stock: Apple vs. AMD',
   'https://www.fool.com//investing/2023/10/11/better-growth-stock-apple-vs-amd/'],
  ['What Is the Fortune 500?', 'https://www.fool.com//terms/f/fortune-500/'],
  ['3 Stocks That Can Help Build Generational Wealth for Patient Investors',
   'https://www.fool.com//investing/2023/10/10/3-stocks-that-can-help-build-generational-wealth/'],
  ["Almost Half of Warren Buffett's $337 Billion Portfolio Is Invested in Only 1 Stock",
   'https://www.fool.com//investing/2023/10/09/half-warren-buffett-portfolio-1-stock/']],
 'META': [['1 Top Metaverse Stock Ready for a Bull Run',
   'https://www.fool.com//investing/2023/09/21/1-top-metaverse-stock-ready-for-a-bull-run/'],
  ['Why Meta Stock Retreated Today',
   'https://www.fool.com//investing/2023/09/15/why-meta-stock-retreated-today/'],
  ['Will This Be the Next $1 Trillion Company?',
   'https://www.fool.com//investing/2023/09/14/will-this-be-the-next-1-trillion-company/'],
  ["Up 155% This Year, Is Meta Platforms' Stock Still a Good Buy?",
   'https://www.fool.com//investing/2023/09/14/up-150-this-year-is-meta-platforms-stock-still-a-g/'],
  ['How to Invest in Reddit Stock',
   'https://www.fool.com//investing/how-to-invest/stocks/how-to-invest-in-reddit-stock/']]}


        res_dict["headlines"] = pain[data]


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

    import pandas as pd

    nltk.download("vader_lexicon")
    import os

    os.environ["REPLICATE_API_TOKEN"] = "r8_665IT7R7NxfzxuQM1tNpMa6bK2sVlnZ2lbbtF"
    import replicate


    app.run(debug=True, port=5000)
