import pandas as pd

def mean_reversion(series: pd.Series, lookback: int = 24, z: float = 2.0):
    """
    Mean-reversion signal:
      +1 if latest z-score < -z (oversold),
      -1 if latest z-score > z (overbought),
      else 0.  
    Always returns 0 if something goes wrong or data is insufficient.
    """
    try:
        # 1) Need at least lookback+1 non-NaN points
        if series.dropna().shape[0] <= lookback:
            return {series.name: 0.0}

        # 2) Compute z-score with a full-window requirement
        rolling_mean = series.rolling(window=lookback, min_periods=lookback).mean()
        rolling_std  = series.rolling(window=lookback, min_periods=lookback).std()
        zscore = (series - rolling_mean) / rolling_std

        # 3) Drop NaNs, take last
        valid = zscore.dropna()
        if valid.empty:
            return {series.name: 0.0}
        last_z = valid.iloc[-1]

        # 4) Compute signal
        if last_z < -z:
            return {series.name: 1.0}
        elif last_z > z:
            return {series.name: -1.0}
        else:
            return {series.name: 0.0}

    except Exception:
        # Any unexpected error → no signal
        return {series.name: 0.0}
