from django.shortcuts import render
from textblob import TextBlob
import re
import pandas as pd
from datetime import datetime
from . import keras
from . import profile
import json


def index(request):
    return render (request , 'index.html')


def home(request):
    global text , sent
    import requests
    import json

    # Grab Crypto Price Data
    price_request = requests.get (
        "https://min-api.cryptocompare.com/data/pricemultifull?fsyms=BTC,ETH,XRP,BCH,EOS,LTC,XLM,ADA,USDT,MIOTA,TRX&tsyms=USD")
    price = json.loads (price_request.content)

    api_request = requests.get ("https://min-api.cryptocompare.com/data/v2/news/?lang=EN")
    res = json.loads (api_request.content)

    def getAnalysis(score):
        if score < 0:
            return 'Negative'
        elif score == 0:
            return 'Neutral'
        else:
            return 'Positive'

    for d in res['Data']:
        txt = (d['body'])
        txt = ' '.join (re.sub ("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)" , " " , txt).split ())
        # twitter = pd.DataFrame([tweet.full_text for tweet in post], columns=['Tweets'])
        df = pd.DataFrame ([d['body'] for d in res['Data']] , columns = ['Text'])

        df['Subjectivity'] = TextBlob (txt).sentiment.subjectivity
        df['Polarity'] = TextBlob (txt).sentiment.polarity
        df['Analysis'] = df['Polarity'].apply (getAnalysis)
        sent = df['Analysis']
        text = df['Text']
    return render (request , 'news.html' , {'res': res , 'price': price , 'sent': sent , 'text': text})


def prices(request):
    if request.method == 'POST':
        import requests
        import json
        quote = request.POST['quote']
        quote = quote.upper()
        crypto_request = requests.get("https://min-api.cryptocompare.com/data/pricemultifull?fsyms=" + quote + "&tsyms=USD")
        crypto = json.loads(crypto_request.content)
        return render(request, 'prices.html', {'quote':quote, 'crypto': crypto})


    else:
        notfound = "Enter a crypto currency symbol into the form above..."
        return render(request, 'prices.html', {'notfound': notfound})

def pred_price(request):
    return render(request,'pred_price.html')

def result(request ):

    stock = request.GET["stockName"].upper()
    country = request.GET['country'].upper()
    start = request.GET['startDate']
    end = request.GET['endDate']
    start_date = datetime.strptime(start, "%Y-%m-%d").strftime("%d/%m/%Y")
    end_date = datetime.strptime(end, "%Y-%m-%d").strftime("%d/%m/%Y")



    co_profile = profile.get_profile(stock , country)

    pred = keras.predict(stock,country,start_date,end_date)

    signal = keras.get_signal(stock , country)
    json_records = signal.reset_index().to_json(orient ='records')
    signal = []
    signal = json.loads(json_records)

    news = keras.get_news()
    last_event = news['event'][0]
    last_news = news['importance'][0]
    time = news['time'][0]

    last_close , last_open = keras.last_close(stock,country,start_date,end_date)



    return render(request, 'result.html',{'stock' : stock ,
    'country' : country , 'startDate' : start_date ,
    'endDate' : end_date , 'co_profile': co_profile ,
    'pred':pred, 'signal' : signal , 'last_event':last_event,'last_news':last_news,'time':time,
    'last_close' : last_close , 'last_open' :last_open

        })

