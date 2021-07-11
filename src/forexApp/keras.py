import pandas as pd 
import numpy as np 
import investpy
import datetime
from datetime import datetime
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras .layers import Dense , LSTM ,Conv2D, Flatten

import re
import time
import math
from sklearn.preprocessing import MinMaxScaler

from tensorflow.keras.models import load_model

model = load_model('./model.h5' , compile=False)

def predict(stock,country,start_date,end_date):
    df = investpy.get_stock_historical_data(stock=stock, country=country, from_date=start_date, to_date=end_date)
    df.drop('Currency',axis=1,inplace=True)
    data = df.filter(['Close'])
    dataset = data.values
    scaler = MinMaxScaler(feature_range =(0,1))
    scaled_data = scaler.fit_transform(dataset)
    df = investpy.get_stock_historical_data(stock=stock, country=country, from_date=start_date, to_date=end_date)
    df.drop('Currency' ,axis=1,inplace=True)
    pred_data = df.filter(['Close'])
    last_60_days = pred_data[-60:].values
    last_60_days_scaled = scaler.fit_transform(last_60_days)
    X_test = []
    X_test.append(last_60_days_scaled)
    X_test = np.array(X_test)
    X_test = np.reshape(X_test , (X_test.shape[0] , X_test.shape[1] , 1))
    pred_price = model.predict(X_test)
    pred_price = scaler.inverse_transform(pred_price)
    pred = []
    pred.append(pred_price)


    return pred[0]

def get_signal(stock , country ):
    signal = investpy.technical_indicators(name=stock, country=country, product_type="stock", interval='daily')


    return signal

def get_news():
    
    important = ['high','medium' , 'low']
    news = investpy.news.economic_calendar(importances=important )
    return news

def last_close(stock,country,start_date,end_date):
    df = investpy.get_stock_historical_data(stock=stock, country=country, from_date=start_date, to_date=end_date)
    last_close = df['Close'].tail(1)[0]
    last_open = df['Open'].tail(1)[0]
    return last_close , last_open

def get_stock_info(stock,country):
    stock = investpy.stocks.get_stock_information(stock = stock ,country=country , as_json = True)

'''
stock_information = {
    "Stock Symbol": "AAPL",
    "Prev. Close": 267.25,
    "Todays Range": "263.45 - 268.25",
    "Revenue": 260170000000.00003,
    "Open": 267.27,
    "52 wk Range": "142 - 268.25",
    "EPS": 11.85,
    "Volume": 23693550.0,
    "Market Cap": 1173730000000.0,
    "Dividend (Yield)": "3.08 (1.15%)",
    "Average Vol. (3m)": 25609925.0,
    "P/E Ratio": 22.29,
    "Beta": 1.23,
    "1-Year Change": "47.92%",
    "Shares Outstanding": 4443236000.0,
    "Next Earnings Date": "04/02/2020"
}
'''



