import datetime as dt
import numpy as np
import pandas_datareader as web
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import cm
from colorspacious import cspace_converter
from collections import OrderedDict

cmaps = plt.get_cmap('hot')
plt.rcParams['figure.facecolor'] = '#dfd8d2'
plt.rcParams['axes.facecolor'] = '#dfd8d2'
hfont = {'fontname':'Times New Roman'}
counter = 0
prices = []
total = []

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

counter = 0
while True:
    how_many_shares = input("Enter Number of Shares Held: ")
    if counter < 1:
        personal_shares_held = [int(i) for i in how_many_shares.split()]
    else:
        if " " not in what_stocks:
            personal_shares_held.append(int(how_many_shares))
        else:
            [personal_shares_held.append(int(i)) for i in how_many_shares.split()]
    done1 = input("Done? (Yes/No): ")
    if done1 == "Yes" or done1 == "yes":
        break
    else:
        counter += 1

for stocks in stock_ticker_symbols:
    data_frame = web.DataReader(stocks, "yahoo", dt.datetime(2021,1,1), dt.datetime.now())
    price = data_frame[-1:]["Close"][0]
    prices.append(price)
    index = stock_ticker_symbols.index(stocks)
    total.append(price * personal_shares_held[index])
color_counter = 0
color_array = []

for i in range(len(stock_ticker_symbols)):
    color_counter += 15
    color_array.append(color_counter)

fib, ax = plt.subplots(figsize=(16,8))
# Add a circle design in the middle if you like
my_circle = plt.Circle((0,0), 0.5,edgecolor='black',facecolor='#d0cac5')
plt.gca().add_artist(my_circle)
plt.pie(total, colors=cmaps(np.array(color_array)), wedgeprops={'edgecolor': 'black'}, textprops={'color':"#ff4d4d", 'fontsize': 15}, autopct='%1.1f%%',pctdistance=1.15, labeldistance=0.9)
plt.text(-2, 1, "Current Portfolio Value", weight='bold', fontsize=25, color="#ff4d4d", **hfont, verticalalignment="center", horizontalalignment="center")

counter = 0.15
for i in stock_ticker_symbols:
    plt.text(-2, 1 - counter, f'{i}: ${total[stock_ticker_symbols.index(i)]:.2f}', **hfont, fontsize=16, color="black",verticalalignment="center",horizontalalignment="center")
    counter += 0.15
plt.text(-2, 1 - counter, "Total: ${:.2f}".format(sum(total)), fontsize=17, color="black", **hfont, verticalalignment="center", horizontalalignment="center")

plt.title("Equity Holdings", color="#ff4d4d", weight="bold", **hfont, fontsize=50)
plt.legend(stock_ticker_symbols,prop={"family":"Times New Roman", 'size': 16}, shadow=True, borderpad=1, labelcolor='black', edgecolor="black", bbox_to_anchor=(1.1,0.94), loc="upper left")
plt.tight_layout()
plt.savefig('Equity_holdings.jpg')
plt.show()