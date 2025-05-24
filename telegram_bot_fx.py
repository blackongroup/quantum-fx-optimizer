import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from forex_dashboard import aggregate, fetch_ohlcv, quantum_portfolio

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
updater = Updater(TOKEN)

def start(update: Update, context: CallbackContext):
    update.message.reply_text("FX Optimizer Bot online!")

def portfolio(update: Update, context: CallbackContext):
    # reuse dashboard logic
    risk = 0.8
    pairs = ["EUR_USD","USD_JPY","GBP_USD","USD_CHF","AUD_USD","NZD_USD","USD_CAD","EUR_GBP","EUR_JPY","GBP_JPY"]
    dfs = {p: fetch_ohlcv(p) for p in pairs}
    price_df = pd.concat([df["close"].rename(p) for p,df in dfs.items()],axis=1).dropna()
    returns = price_df.pct_change().dropna()
    cov = returns.cov()
    alloc = quantum_portfolio(returns, cov, risk)
    msg = "\n".join(f"{p}: {w:.2%}" for p,w in alloc.items())
    update.message.reply_text(f"Today's FX allocations:\n{msg}")

updater.dispatcher.add_handler(CommandHandler("start", start))
updater.dispatcher.add_handler(CommandHandler("portfolio", portfolio))

if __name__ == "__main__":
    updater.start_polling()
