import datetime as dt
import yfinance as yf
import pandas as pd

tickers = ["AAPL","MSFT","JPM","DIS"]
start = dt.datetime.today()-dt.timedelta(3650)
end = dt.datetime.today()
cl_price = pd.DataFrame()


for ticker in tickers:
    cl_price[ticker] = yf.download(ticker,start,end)["Adj Close"]
    
cl_price.dropna(axis=0,how='any',inplace=True)

daily_return = cl_price.pct_change()
  
cl_price.plot() 
cl_price.plot(subplots=True, layout = (2,2), title = "Stock Price Evolution", grid =True)
  
   
daily_return.plot()
(1+daily_return).cumprod().plot(title = "Stock Price Evolution", grid =True)    
    
    
    
    
    
    