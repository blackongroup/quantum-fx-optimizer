import pandas as pd

def mean_reversion(series: pd.Series, lookback: int = 24, z: float = 2.0):
    """
    Mean-reversion signal:
      +1 if the latest z-score < -z (oversold),
      -1 if the latest z-score > z (overbought),
      else 0.
    Returns zero if series is too short or z-score can't be computed.
    """
    # Ensure series is long enough for lookback
    if series.dropna().shape[0] <= lookback:
        return {series.name: 0.0}

    # Compute rolling mean and std
    rolling_mean = series.rolling(window=lookback, min_periods=lookback).mean()
    rolling_std = series.rolling(window=lookback, min_periods=lookback).std()
    zscore = (series - rolling_mean) / rolling_std

    # Drop NaNs and get last z-score safely
    valid_z = zscore.dropna()
    if valid_z.empty:
        return {series.name: 0.0}
    last_z = valid_z.iloc[-1]

    # Determine signal
    if last_z < -z:
        val = 1.0
    elif last_z > z:
        val = -1.0
    else:
        val = 0.0

    return {series.name: val}
