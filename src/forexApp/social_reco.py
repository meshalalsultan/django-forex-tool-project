import datetime as dt
import math
import investpy
import numpy as np
import pandas as pd
import tweepy
from sklearn import preprocessing
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from textblob import TextBlob
from tweepy import OAuthHandler 




# keys and tokens from the Twitter Dev Console 
consumer_key = 'pj6YNhZZBugJ2iVTzprRFeyVv'
consumer_secret = 'vV71WKQdcaMuhYIDKufIdSOAxwiydLGGskpj0bueAPeOKruwoT'
access_token = '1184086168608088064-863KtlQN4hww75kvv8J5OpAn0nNnzj'
access_token_secret = 'bdwBvlMmpLT2WYDBo9rQNMFtuldjduOoPXOHsi6rmehwT'
  
        # attempt authentication 

        # create OAuthHandler object 
auth = OAuthHandler(consumer_key, consumer_secret) 
            # set access token and secret 
auth.set_access_token(access_token, access_token_secret) 
        # create tweepy API object to fetch tweets 
api = tweepy.API(auth) 

def get_stock_data(symbol, from_date, to_date):
    data = investpy.get_stock_historical_data(stock=symbol, from_date=from_date, to_date=to_date)
    data.drop('Currency',axis=1,inplace=True)
    df = pd.DataFrame(data=data)

    df = df[['Open', 'High', 'Low', 'Close', 'Volume']]
    df['HighLoad'] = (df['High'] - df['Close']) / df['Close'] * 100.0
    df['Change'] = (df['Close'] - df['Open']) / df['Open'] * 100.0

    df = df[['Close', 'HighLoad', 'Change', 'Volume']]
    return df

def stock_forecasting(df):
    forecast_col = 'Close'
    forecast_out = int(math.ceil(0.1*len(df)))
    df['Label'] = df[[forecast_col]].shift(-forecast_out)

    X = np.array(df.drop(['Label'], axis=1))
    X = preprocessing.scale(X)
    X_forecast = X[-forecast_out:]
    X = X[:-forecast_out]

    df.dropna(inplace=True)
    y = np.array(df['Label'])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

    clf = LinearRegression(n_jobs=-1)
    clf.fit(X_train, y_train)
    accuracy = clf.score(X_test, y_test)
    forecast = clf.predict(X_forecast)

    df['Prediction'] = np.nan

    last_date = df.iloc[-1].name
    last_date = dt.datetime.strptime(str(last_date), "%Y-%m-%d %H:%M:%S")

    for pred in forecast:
        last_date += dt.timedelta(days=1)
        df.loc[last_date.strftime("%Y-%m-%d")] = [np.nan for _ in range(len(df.columns) - 1)] + [pred]
    return df, forecast_out

def retrieving_tweets_polarity(symbol):
    tweets = tweepy.Cursor(api.search, q=str(symbol), tweet_mode='extended', lang='en').items(ct.num_of_tweets)

    tweet_list = []
    global_polarity = 0
    for tweet in tweets:
        tw = tweet.full_text
        blob = TextBlob(tw)
        polarity = 0
        for sentence in blob.sentences:
            polarity += sentence.sentiment.polarity
            global_polarity += sentence.sentiment.polarity
        tweet_list.append(Tweet(tw, polarity))

    global_polarity = global_polarity / len(tweet_list)
    return global_polarity

def recommending(df, forecast_out, global_polarity):
    if df.iloc[-forecast_out-1]['Close'] < df.iloc[-1]['Prediction']:
        if global_polarity > 0:
             str(symbol)
        elif global_polarity < 0:
             str(symbol)
    else:
            str(symbol)



