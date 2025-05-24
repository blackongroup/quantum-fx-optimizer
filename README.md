# Quantum-FX-Optimizer

A quantum-inspired FX portfolio optimizer that selects the optimal weights
for a basket of major currency pairs using QUBO and simulated annealing.

## FX Universe
- EUR/USD  
- USD/JPY  
- GBP/USD  
- USD/CHF  
- AUD/USD  
- NZD/USD  
- USD/CAD  
- EUR/GBP  
- EUR/JPY  
- GBP/JPY  

## Setup & Deployment

1. Add your API secrets in **Settings → Secrets**:
   - `OANDA_TOKEN`  
   - `OANDA_ACCOUNT`  
   - `TELEGRAM_TOKEN`  
   - `TELEGRAM_CHAT_ID`  
2. Deploy the dashboard on Streamlit Cloud:
   - Repo: `blackongroup/quantum-fx-optimizer`  
   - Main file: `forex_dashboard.py`  
3. Schedule your backtests and Telegram bot via GitHub Actions or Replit.

## Project Structure

