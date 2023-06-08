import requests
from bs4 import BeautifulSoup
import pandas as pd
from yahoofinancials import YahooFinancials
import datetime as dt

"""
Data sourcing straegy #1: Web Scraping

Quick, efficent, minimal dependencies but heavily provider reliant 
and easily susceptible to change based on provider system.

"""

tickers = ["AXP", "AMGN", "AAPL", "BA", "CAT", "CSCO", "CVX", "GS", "HD", "HON", "IBM", "INTC", "JNJ", "KO", "JPM", "MCD", "MMM", "MRK", "MSFT", "NKE", "PG", "TRV", "UNH", "CRM", "VZ", "V", "WBA", "WMT", "DIS", "DOW"]
key_statistics = {}

for ticker in tickers:
    url = "https://finance.yahoo.com/quote/{}/key-statistics?p={}".format(ticker,ticker)    
    headers = {"User-Agent" : "Chrome/96.0.4664.110"}
    page = requests.get(url, headers=headers)
    page_content = page.content
    soup = BeautifulSoup(page_content,"html.parser")
    tabl = soup.find_all("table" , {"class" : "W(100%) Bdcl(c)"})
    
    temp_stats = {}
    for t in tabl:
        rows = t.find_all("tr")
        for row in rows:
            temp_stats[row.get_text(separator="|").split("|")[0]] = row.get_text(separator="|").split("|")[-1]
    
    key_statistics[ticker] = temp_stats
    
"""
Data sourcing straegy #2: API

Reliable and consistent data but entirely provider dependent.

"""

all_tickers = ["AXP", "AMGN", "APPL", "BA", "CAT", "CSCO", "CVX", "GS", "HD", "HON", "IBM", "INTC", "JNJ", "KO", "JPM", "MCD", "MMM", "MRK", "MSFT", "NKE", "PG", "TRV", "UNH", "CRM", "VZ", "V", "WBA", "WMT", "DIS", "DOW"]

close_prices = pd.DataFrame()
end_date = (dt.date.today()).strftime('%Y-%m-%d')
beg_date = (dt.date.today()-dt.timedelta(1825)).strftime('%Y-%m-%d') #unique to yahoofinancials - must pass in string data
for ticker in all_tickers:
    yahoo_financials = YahooFinancials(ticker)
    json_obj = yahoo_financials.get_historical_price_data(beg_date,end_date,"daily")
    ohlv = json_obj[ticker]['prices']
    temp = pd.DataFrame(ohlv)[["formatted_date","adjclose"]]
    temp.set_index("formatted_date",inplace=True)
    temp.dropna(inplace=True)
    close_prices[ticker] = temp["adjclose"]
    
    
ohlv_dict = {}
end_date = (dt.date.today()).strftime('%Y-%m-%d')
beg_date = (dt.date.today()-dt.timedelta(1825)).strftime('%Y-%m-%d')
for ticker in all_tickers:
    yahoo_financials = YahooFinancials(ticker)
    json_obj = yahoo_financials.get_historical_price_data(beg_date,end_date,"daily")
    ohlv = json_obj[ticker]['prices']
    temp = pd.DataFrame(ohlv)[["formatted_date","adjclose","open","low","high","volume"]]
    temp.set_index("formatted_date",inplace=True)
    temp.dropna(inplace=True)
    ohlv_dict[ticker] = temp