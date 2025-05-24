def momentum(series, lookback=24):
    ret = series.pct_change(lookback).iloc[-1]
    return {series.name: float(ret)}
