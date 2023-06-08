import datetime as dt
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

tickers = ["AAPL","MSFT","JPM","DIS"]
start = dt.datetime.today()-dt.timedelta(3650)
end = dt.datetime.today()
cl_price = pd.DataFrame() 


for ticker in tickers:
    cl_price[ticker] = yf.download(ticker,start,end)["Adj Close"]
    

cl_price.dropna(axis=0,how='any',inplace=True)


daily_return = cl_price.pct_change()
 
fig, ax = plt.subplots()
plt.style.available
plt.style.use('ggplot')
ax.set(title="Daily return on chosen stocks", xlabel="Example Stocks", ylabel = "Daily Returns")
plt.bar(daily_return.columns,daily_return.mean(),color=["red","blue","green","orange"])