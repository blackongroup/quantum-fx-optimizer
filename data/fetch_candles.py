import pandas as pd
import yfinance as yf

def fetch_ohlcv(pair="EUR_USD", period="60d", interval="1d"):
    """
    Fetches recent FX rates from Yahoo Finance for ticker like 'EURUSD=X'.
    Returns a DataFrame with a 'close' column indexed by date.
    """
    # Yahoo tickers use e.g. 'EURUSD=X' for EUR/USD
    yf_ticker = pair.replace("/", "") + "=X"
    df = yf.download(yf_ticker, period=period, interval=interval)
    df = df.rename(columns={"Close": "close"})
    return df[["close"]]

