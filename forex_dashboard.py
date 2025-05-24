import os
import streamlit as st
import pandas as pd
from data.fetch_candles import fetch_ohlcv
from signals.quantum_fx import quantum_portfolio
from signals.mean_rev_fx import mean_reversion
from signals.momentum_fx import momentum
from aggregator import aggregate

st.title("🌐 Quantum-Inspired FX Optimizer")
risk = st.slider("Risk Tolerance", 0.0, 1.0, 0.8)

# Define your FX pairs
pairs = [
    "EUR_USD","USD_JPY","GBP_USD","USD_CHF",
    "AUD_USD","NZD_USD","USD_CAD","EUR_GBP",
    "EUR_JPY","GBP_JPY"
]

# Fetch historical FX data
dfs = {p: fetch_ohlcv(p) for p in pairs}
# Build a DataFrame of closing prices
df_close = pd.concat(
    [dfs[p]["close"].rename(p) for p in pairs],
    axis=1
).dropna()

# Compute returns and covariance matrix
returns = df_close.pct_change().dropna()
cov = returns.cov()

# Generate signals
quantum_signals = quantum_portfolio(returns, cov, risk)

mean_rev_signals = {}
for p in pairs:
    sig = mean_reversion(df_close[p])
    mean_rev_signals.update(sig)

momentum_signals = {}
for p in pairs:
    sig = momentum(df_close[p])
    momentum_signals.update(sig)

signals = {
    "quantum": quantum_signals,
    "mean_rev": mean_rev_signals,
    "momentum": momentum_signals
}

# Aggregate into final allocations
alloc = aggregate(signals)

# Display results
st.markdown("### Portfolio Allocations")
st.table(pd.DataFrame([{"Pair": k, "Weight": v} for k, v in alloc.items()]))
