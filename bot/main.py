from data import get_data
from strategy import get_signals
from sentiment import get_news_sentiment
from portfolio import load_state, update_portfolio, save_state
from ml_model import predict_error_risk
import datetime
import os
import sys

tickers = ["AAPL", "MSFT", "GOOG", "TSLA"]

initial_capital = float(sys.argv[1]) if len(sys.argv) > 1 else 10000
state = load_state(initial_capital)

def run_bot():
    now = datetime.datetime.now().strftime("%Y%m%d_%H%M")
    log_file = f"bot/logs/recommendations_{now}.txt"
    os.makedirs("bot/logs", exist_ok=True)

    with open(log_file, "w") as f:
        f.write(f"STARTING BALANCE: ${state['capital']:.2f}\n\n")
        for ticker in tickers:
            df = get_data(ticker)
            signal, indicators = get_signals(df)
            sentiment = get_news_sentiment(ticker)
            current_price = df.iloc[-1]['Close']

            # ML prediction of error risk
            risk = predict_error_risk(indicators)
            recommendation = "HOLD"
            if signal == "BUY" and sentiment == "POSITIVE" and risk == "LOW":
                recommendation = "BUY"
            elif signal == "SELL" and sentiment == "NEGATIVE" and risk == "LOW":
                recommendation = "SELL"

            state = update_portfolio(state, ticker, current_price, recommendation)

            line = f"{ticker} | Price: ${current_price:.2f} | Signal: {signal} | Sentiment: {sentiment} | ML-Risk: {risk} | Recommendation: {recommendation}"
            print(line)
            f.write(line + "\n")

        save_state(state)
        f.write(f"\nENDING BALANCE: ${state['capital']:.2f}\n")

run_bot()
