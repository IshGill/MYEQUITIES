import pandas as pd
import datetime as dt
import numpy as np
import pandas_datareader as web
import matplotlib as mpl
from matplotlib import cm
from colorspacious import cspace_converter
import matplotlib.pyplot as plt
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from nltk.sentiment.vader import SentimentIntensityAnalyzer

fin_url_link = 'https://finviz.com/quote.ashx?t='
counter = 0
while True:
    what_stocks = input("Enter ticker symbols: ")
    if counter < 1:
        stock_ticker_symbols = [i.upper() for i in what_stocks.split()]
    else:
        if " " not in what_stocks:
            stock_ticker_symbols.append(what_stocks.upper())
        else:
            [stock_ticker_symbols.append(i.upper()) for i in what_stocks.split()]
    done = input("Done? (Yes/No): ")
    if done == "Yes" or done == "yes":
        break
    else:
        counter += 1

# Extract data for stocks and put into hash table
news_table_ids = {}
for i in stock_ticker_symbols:
    url_code = fin_url_link + i
    to_parse = Request(url=url_code, headers={'user-agent': 'program'})
    response = urlopen(to_parse)
    html_parse = BeautifulSoup(response, 'html')
    news_table = html_parse.find(id='news-table')
    news_table_ids[i] = news_table

# Parse through news table and extract data which we need for sentiment analysis
data_list= []
for ticker, news_table in news_table_ids.items():
    for row in news_table.find_all('tr'):
        heading = row.a.get_text()
        date_data = row.td.text.split(" ")
        if len(date_data) == 1:
            time_data = date_data[0]
        else:
            date = date_data[0]
            time_data = date_data[1]
        data_list.append([ticker, date, time_data, heading])

# Time to apply sentiment analysis
data_frame = pd.DataFrame(data_list, columns=['ticker', 'date', 'time', 'title'])
vader = SentimentIntensityAnalyzer()
lda_fucntion = lambda header: vader.polarity_scores(header)['compound']
data_frame['compound'] = data_frame['title'].apply(lda_fucntion)
data_frame['date'] = pd.to_datetime(data_frame.date).dt.date

# Build visualisations of the sentiment analysis data
cmaps = plt.get_cmap('spring')
plt.style.use('seaborn')
plt.rcParams['figure.facecolor'] = '#C1DBD4'
plt.rcParams['axes.facecolor'] = '#C1DBD4'
hfont = {'fontname':'Times New Roman'}

color_counter = 0
color_array = []
for i in range(len(stock_ticker_symbols)):
    color_counter += 50
    color_array.append(color_counter)

plt.figure(figsize=(16,8))
averages = data_frame.groupby(['ticker', 'date']).mean()
averages = averages.unstack()
averages = averages.xs('compound', axis='columns').transpose()
averages.plot(kind='bar', width=1.15, color=cmaps(np.array(color_array)))

plt.gcf().autofmt_xdate()
plt.legend(averages,prop={"family":"Times New Roman", 'size': 10}, shadow=True, borderpad=1, labelcolor='black', edgecolor="black", bbox_to_anchor=(1,1))
plt.title("Portfolio Financial News Sentiment Analysis", **hfont,weight="bold", fontsize=25)
plt.ylabel("Sentiment (Low to High)",fontsize=16, weight="bold", **hfont)
plt.xlabel("Date (Daily)",fontsize=16, weight="bold", **hfont)
plt.tight_layout()
plt.savefig('Financial_News_Sentiment_Analysis.jpg')
plt.show()


