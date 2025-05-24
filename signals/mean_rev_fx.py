# signals/mean_rev_fx.py

import pandas as pd

def mean_reversion(series: pd.Series, lookback: int = 24, z: float = 2.0):
    """
    Mean-reversion signal:
      +1 if oversold (z-score < -z),
      -1 if overbought (z-score > +z),
       0 otherwise.
    Always returns 0 if data is insufficient or any error occurs.
    """
    try:
        # 1) Drop NaNs, need more than 'lookback' points
        clean = series.dropna()
        if clean.size <= lookback:
            return {series.name: 0.0}

        # 2) Compute rolling stats with strict min_periods
        m = series.rolling(window=lookback, min_periods=lookback).mean()
        s = series.rolling(window=lookback, min_periods=lookback).std()
        zscore = (series - m) / s

        # 3) Drop NaNs and grab the last valid z-score
        valid = zscore.dropna()
        if valid.empty:
            return {series.name: 0.0}
        last_z = valid.iat[-1]

        # 4) Return the signal
        if last_z < -z:
            return {series.name: 1.0}
        elif last_z > z:
            return {series.name: -1.0}
        else:
            return {series.name: 0.0}

    except Exception:
        # On *any* unexpected error, default to no signal
        return {series.name: 0.0}
