import pandas as pd

def mean_reversion(series: pd.Series, lookback: int = 24, z: float = 2.0):
    """
    Mean-reversion signal: +1 if oversold (z-score < -z),
    –1 if overbought (z-score > z), else 0.
    Returns zero for any series shorter than lookback+1.
    """
    # 1) Enough data?
    if len(series) <= lookback:
        return {series.name: 0.0}

    # 2) Compute rolling statistics
    m = series.rolling(window=lookback).mean()
    s = series.rolling(window=lookback).std()
    zscore = (series - m) / s

    # 3) Safely grab the latest z-score
    last_z = zscore.dropna().iloc[-1] if not zscore.dropna().empty else 0.0

    # 4) Generate signal
    if last_z < -z:
        val = 1.0
    elif last_z > z:
        val = -1.0
    else:
        val = 0.0

    return {series.name: val}
