def momentum(series, lookback=24):
    """
    Momentum signal: percentage change over lookback period.
    Safe guard: returns 0 if series is too short or no change.
    """
    if len(series) < lookback + 1:
        return {series.name: 0.0}
    ret = series.pct_change(lookback).iloc[-1]
    if pd.isna(ret):
        ret = 0.0
    return {series.name: float(ret)}
