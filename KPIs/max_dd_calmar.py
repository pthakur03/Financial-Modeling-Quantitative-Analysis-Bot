import yfinance as yf

"""
Python implementation for Maximum Drawdown and Calmar Ratio:
    A KPI that measures the maximum loss experienced by an investment from its peak value and compares it to its average annual return, providing insights into risk-adjusted returns.
"""

tickers = ["AXP", "AMGN", "AAPL", "BA", "CAT", "CSCO", "CVX", "GS", "HD", "HON", "IBM", "INTC", "JNJ", "KO", "JPM", "MCD", "MMM", "MRK", "MSFT", "NKE", "PG", "TRV", "UNH", "CRM", "VZ", "V", "WBA", "WMT", "DIS", "DOW"]
ohlcv_data = {}


for ticker in tickers:
    temp = yf.download(ticker,period='7mo',interval='1d')
    temp.dropna(how="any",inplace=True)
    ohlcv_data[ticker] = temp
    
def CAGR(DF):
    df = DF.copy()
    df["return"] = DF["Adj Close"].pct_change()
    df["cum_return"] = (1 + df["return"]).cumprod()
    n = len(df)/252
    CAGR = (df["cum_return"][-1])**(1/n) - 1
    return CAGR

def max_dd(DF):
    df = DF.copy()
    df["return"] = df["Adj Close"].pct_change()
    df["cum_return"] = (1+df["return"]).cumprod()
    df["cum_roll_max"] = df["cum_return"].cummax()
    df["drawdown"] = df["cum_roll_max"] - df["cum_return"]
    return (df["drawdown"]/df["cum_roll_max"]).max()
    
def calmar(DF):
    df = DF.copy()
    return CAGR(df)/max_dd(df)

for ticker in ohlcv_data:
    print("max drawdown of {} = {}".format(ticker,max_dd(ohlcv_data[ticker])))
    print("calmar ratio of {} = {}".format(ticker,calmar(ohlcv_data[ticker])))