import os
import streamlit as st
import pandas as pd
from data.fetch_candles import fetch_ohlcv
from signals.quantum_fx import quantum_portfolio
from signals.mean_rev_fx import mean_reversion
from signals.momentum_fx import momentum
from aggregator import aggregate

# --- Streamlit UI ---
st.title("🌐 Quantum-Inspired FX Optimizer")
risk = st.slider("Risk Tolerance", min_value=0.0, max_value=1.0, value=0.8)

# --- Define your FX universe ---
pairs_list = [
    "EUR_USD", "USD_JPY", "GBP_USD", "USD_CHF",
    "AUD_USD", "NZD_USD", "USD_CAD", "EUR_GBP",
    "EUR_JPY", "GBP_JPY"
]

# --- Fetch historical data ---
dfs = {}
for p in pairs_list:
    try:
        df = fetch_ohlcv(p)
        if "close" in df.columns:
            dfs[p] = df
        else:
            st.warning(f"No 'close' column for {p}; skipping.")
    except Exception as e:
        st.warning(f"Error fetching {p}: {e}")

if not dfs:
    st.error("Unable to fetch data for any pair. Check your data source and symbols.")
    st.stop()

# --- Build closing price DataFrame ---
df_close = pd.concat(
    [df["close"].rename(p) for p, df in dfs.items()],
    axis=1
).dropna()

# Use only successfully fetched pairs
pairs = df_close.columns.tolist()

# --- Compute returns and covariance ---
returns = df_close.pct_change().dropna()
cov = returns.cov()

# --- Generate signals ---

# 1) Quantum-inspired portfolio
quantum_signals = quantum_portfolio(returns, cov, risk)

# 2) Mean-reversion signals
mean_rev_signals = {}
for _, series in df_close.items():
    try:
        mean_rev_signals.update(mean_reversion(series))
    except Exception:
        mean_rev_signals[series.name] = 0.0

# 3) Momentum signals
momentum_signals = {}
for _, series in df_close.items():
    try:
        momentum_signals.update(momentum(series))
    except Exception:
        momentum_signals[series.name] = 0.0

signals = {
    "quantum": quantum_signals,
    "mean_rev": mean_rev_signals,
    "momentum": momentum_signals
}

# --- Aggregate into final allocations ---
alloc = aggregate(signals)

# --- Display allocations ---
if alloc:
    st.markdown("### Portfolio Allocations")
    st.table(pd.DataFrame([
        {"Pair": k, "Weight": f"{v:.2%}"} for k, v in alloc.items()
    ]))
else:
    st.warning("No allocations to display. Try adjusting the risk slider or check data availability.")
