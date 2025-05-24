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

# Define your FX universe (input list)
input_pairs = [
    "EUR_USD","USD_JPY","GBP_USD","USD_CHF",
    "AUD_USD","NZD_USD","USD_CAD","EUR_GBP",
    "EUR_JPY","GBP_JPY"
]

# Fetch historical FX data into dict
dfs = {}
for p in input_pairs:
    try:
        df = fetch_ohlcv(p)
        if "close" in df.columns:
            dfs[p] = df
        else:
            st.warning(f"No 'close' column for {p}; skipping.")
    except Exception as e:
        st.warning(f"Error fetching {p}: {e}")

if not dfs:
    st.error("No data fetched. Check your data source and symbols.")
    st.stop()

# Build DataFrame of closing prices, aligned
df_close = pd.concat(
    [df["close"].rename(p) for p, df in dfs.items()],
    axis=1
).dropna()

# Use only successfully fetched pairs
pairs = df_close.columns.tolist()

# Compute returns and covariance
returns = df_close.pct_change().dropna()
cov = returns.cov()

# Generate signals
quantum_signals = quantum_portfolio(returns, cov, risk)

mean_rev_signals = {}
for _, series in df_close.items():
    mean_rev_signals.update(mean_reversion(series))

momentum_signals = {}
for _, series in df_close.iteritems():
    momentum_signals.update(momentum(series))

signals = {
    "quantum": quantum_signals,
    "mean_rev": mean_rev_signals,
    "momentum": momentum_signals
}

# Aggregate into final allocations
alloc = aggregate(signals)

# Display results
st.markdown("### Portfolio Allocations")
if alloc:
    st.table(pd.DataFrame([{"Pair": k, "Weight": v} for k, v in alloc.items()]))
else:
    st.warning("No allocations to display. Adjust risk tolerance or check data.")
