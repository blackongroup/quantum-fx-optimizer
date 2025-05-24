import os
import oandapyV20, pandas as pd
from oandapyV20.endpoints.instruments import InstrumentsCandles

OANDA_TOKEN = os.getenv("OANDA_TOKEN")
CLIENT = oandapyV20.API(access_token=OANDA_TOKEN)

def fetch_ohlcv(pair="EUR_USD", granularity="H1", count=500):
    params = {"granularity": granularity, "count": count}
    req = InstrumentsCandles(instrument=pair, params=params)
    resp = CLIENT.request(req)
    data = resp["candles"]
    df = pd.DataFrame([{
        "time": c["time"],
        "open": float(c["mid"]["o"]),
        "high": float(c["mid"]["h"]),
        "low":  float(c["mid"]["l"]),
        "close":float(c["mid"]["c"])
    } for c in data if c["complete"]])
    df["time"] = pd.to_datetime(df["time"])
    return df.set_index("time")
