import datetime as dt
import numpy as np
import pandas_datareader as web
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import cm
from colorspacious import cspace_converter
from collections import OrderedDict

cmaps = plt.get_cmap('seismic')
plt.rcParams['figure.facecolor'] = '#fff1df'
plt.rcParams['axes.facecolor'] = '#fff1df'
hfont = {'fontname':'Times New Roman'}
counter = 0
prices = []
total = []

while True:
    what_cryptos = input("Enter Crypto Ticker Symbols: ")
    if counter < 1:
        add_usd = what_cryptos.split()
        for i in range(len(add_usd)):
            add_usd[i] += "-USD"
        crypto_ticker_symbols = [i.upper() for i in add_usd]
    else:
        if " " not in what_cryptos:
            crypto_ticker_symbols.append(what_cryptos.upper()+"-USD")
        else:
            [crypto_ticker_symbols.append(i.upper()+"-USD") for i in what_cryptos.split()]
    done = input("Done? (Yes/No): ")
    if done == "Yes" or done == "yes":
        break
    else:
        counter += 1

counter = 0
while True:
    coins_held = input("Enter Number of Coins Held: ")
    if counter < 1:
        crypto_coins_held = [int(i) for i in coins_held.split()]
    else:
        if " " not in coins_held:
            crypto_coins_held.append(int(coins_held))
        else:
            [crypto_coins_held.append(int(i)) for i in coins_held.split()]
    done1 = input("Done? (Yes/No): ")
    if done1 == "Yes" or done1 == "yes":
        break
    else:
        counter += 1

for coins in crypto_ticker_symbols:
    data_frame = web.DataReader(coins, "yahoo", dt.datetime(2021,1,1), dt.datetime.now())
    price = data_frame[-1:]["Close"][0]
    prices.append(price)
    index = crypto_ticker_symbols.index(coins)
    total.append(price * crypto_coins_held[index])

color_counter = 0
color_array = []
for i in range(len(crypto_ticker_symbols)):
    color_counter += 30
    color_array.append(color_counter)

fib, ax = plt.subplots(figsize=(16,8))
my_circle = plt.Circle((0,0), 0.55,edgecolor="black",facecolor='#fff1df')
plt.gca().add_artist(my_circle)
plt.pie(total,colors=cmaps(np.array(color_array)), wedgeprops={'edgecolor': 'black'},textprops={'color':"#007dd3", 'fontsize': 15}, startangle=180, autopct='%1.1f%%',pctdistance=1.15, labeldistance=0.9)
plt.text(-2, 1, "Current Portfolio Value", weight="bold", fontsize=25, color="#007dd3", **hfont, verticalalignment="center", horizontalalignment="center")

counter = 0.15
for i in crypto_ticker_symbols:
    plt.text(-2, 1 - counter, f'{i}: ${total[crypto_ticker_symbols.index(i)]:.2f}', **hfont, fontsize=16, color="black",verticalalignment="center",horizontalalignment="center")
    counter += 0.15
plt.text(-2, 1 - counter, "Total: ${:.2f}".format(sum(total)), fontsize=17, color="black", **hfont, verticalalignment="center", horizontalalignment="center")

plt.title("Crypto Holdings", color="#007dd3", weight="bold", **hfont, fontsize=50)
plt.legend(crypto_ticker_symbols,prop={"family":"Times New Roman", 'size': 16}, shadow=True, borderpad=1, labelcolor="black", edgecolor="black", bbox_to_anchor=(1.1,0.94), loc='upper left')
plt.tight_layout()
plt.savefig('Crypto_Holdings.jpg')
plt.show()


