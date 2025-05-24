import pandas as pd

def mean_reversion(series: pd.Series, lookback: int = 24, z: float = 2.0):
    """
    Mean-reversion signal:
      +1 if the latest rolling z-score < -z (oversold),
      -1 if > +z (overbought), else 0.
    Always returns 0 if data is insufficient or any error occurs.
    """
    try:
        # Need at least lookback+1 valid points to compute
        clean = series.dropna()
        if clean.size <= lookback:
            return {series.name: 0.0}

        # Calculate rolling mean & std with strict window
        rolling_mean = series.rolling(window=lookback, min_periods=lookback).mean()
        rolling_std  = series.rolling(window=lookback, min_periods=lookback).std()

        # Compute z-score
        zscore = (series - rolling_mean) / rolling_std
        valid = zscore.dropna()
        if valid.empty:
            return {series.name: 0.0}

        last_z = valid.iloc[-1]

        # Signal logic
        if last_z < -z:
            return {series.name: 1.0}
        elif last_z > z:
            return {series.name: -1.0}
        else:
            return {series.name: 0.0}

    except Exception:
        # Fallback to no signal on any unexpected issue
        return {series.name: 0.0}
