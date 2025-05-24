def mean_reversion(series, lookback=24, z=2.0):
    m = series.rolling(lookback).mean()
    s = series.rolling(lookback).std()
    zscore = (series - m) / s
    # returns +1 if oversold, -1 if overbought, else 0
    val = 1 if zscore.iloc[-1] < -z else (-1 if zscore.iloc[-1] > z else 0)
    return {series.name: float(val)}
