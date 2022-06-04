import yfinance as yf
import pandas as pd

def get_stock_history(symbol):
    res = []
    try:
        data = yf.download(tickers=symbol, period='1mo')['Adj Close']
    except:
        return []

    if any(data):
        data = data.reset_index()
        for i, d in data.iterrows():
            res.append({"x": int(d['Date'].timestamp()*1000), "y": round(d['Adj Close'], 2)})
        return res
    else: return []

#print(get_stock_history('AAPL'))