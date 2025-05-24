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

pairs = ["EUR_USD","USD_JPY","GBP_USD","USD_CHF","AUD_USD","NZD_USD","USD_CAD","EUR_GBP","EUR_JPY","GBP_JPY"]
# Fetch data
dfs = {p: fetch_ohlcv(p) for p in pairs}
price_df = pd.concat([df["close"].rename(p) for p, df in dfs.items()], axis=1).dropna()

returns = price_df.pct_change().dropna()
cov = returns.cov()

# Build signals
signals = {
    "quantum": quantum_portfolio(returns, cov, risk),
    "mean_rev": {**mean_reversion(price_df[p]) for p in pairs},
    "momentum": {**momentum(price_df[p]) for p in pairs}
}
alloc = aggregate(signals)

st.markdown("### Portfolio Allocations")
st.table(pd.DataFrame([{"Pair": k, "Weight": v} for k, v in alloc.items()]))
