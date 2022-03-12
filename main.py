
import pandas
import yfinance as yf
import numpy
import urllib.request as ur
import datetime
import sys
from pandas_datareader import data as pdr
import pandas as pd

# Slack API Key:
slackAPIKey = 'xoxb-3591523609-1102501300515-4Z3zXYHR8jjiXqMkue49rHZS'

yf.pdr_override()

def stockList():
    stocks = ["FM.TO", "NA.TO", "TD.TO"]
    # stocks = ["FM.TO"]
    return stocks

def macdDiff(day12Values, day26Values, idx):
    macdDiff = day12Values[idx][0] - day26Values[idx][0]
    return macdDiff

stockArray = stockList()

for stock in stockArray :
    temp = yf.Ticker(str(stock))
    hist_data = temp.history(period="max") 
    prices = []
    c=0
    # print(hist_data)
    while c < len(hist_data):
        if hist_data.iloc[c,4] > float(2.00):
            # print(hist_data.iloc[c, 3])
            prices.append(hist_data.iloc[c,3])
        c += 1
    # print(prices)
    prices_df = pd.DataFrame(prices)
    day12 = prices_df.ewm(span=50).mean()
    day26 = prices_df.ewm(span=200).mean()
    macd = []

    day12Values = day12.values.tolist()
    day26Values = day26.values.tolist()


    # print(day12)
    # print(day26)
    # Find where last day was positive but day before was negative
    lastDay = macdDiff(day12Values, day26Values, len(day12)-1)
    dayPrevious = macdDiff(day12Values, day26Values, len(day12)-2)
    dayPrevious2 = macdDiff(day12Values, day26Values, len(day12)-3)
    
    if lastDay - dayPrevious > 0 and dayPrevious - dayPrevious2 <= 0:
        print(stock + " just crossed over potential buying time: " + str(lastDay - dayPrevious))
    elif lastDay - dayPrevious > 0 and dayPrevious - dayPrevious2 > 0:
        print(stock + " still postive: " + str(lastDay - dayPrevious))
    else:
        print(stock + " time to watch out: " + str(lastDay - dayPrevious))
    # counter = 0
    # while counter < (len(day12)):
    #     macd.append(day12.iloc[counter,0] - day26.iloc[counter,0])
    #     counter += 1
    # print(macd)
    # macd_df = pd.DataFrame(macd)
    # signal_df = macd_df.ewm(span=9).mean()

    # signal = signal_df.values.tolist()
    # print(signal)

