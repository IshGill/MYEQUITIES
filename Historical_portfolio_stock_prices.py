import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import quandl

# Insert stock holdings and your Personal quadl API key
quandl.ApiConfig.api_key = '3bWuEzvjKS3863yeHftA'
stocks = ["TSLA", "FB", "AMZN", "GOOGL", "MSFT"]
data_table = quandl.get_table('WIKI/PRICES', ticker = stocks,
                        qopts = { 'columns': ['date', 'ticker', 'adj_close'] },
                        date = { 'gte': '2018-1-1', 'lte': '2020-12-31' }, paginate=True)

# We need the index to be based of the dates
df = data_table.set_index("date")
# We use .head() to check the output

# Now we need to insert our portolio ticker symbols as the column headers
table = df.pivot(columns="ticker")
table.columns = [i[1] for i in table.columns]
print(table)


# Analyse historical stock prices
plt.figure(figsize=(14, 7))
for i in table.columns.values:
    plt.plot(table.index, table[i], lw=3, alpha=0.8, label=i)
plt.legend(loc='upper left', fontsize=12)
plt.ylabel('price in $')

plt.show()