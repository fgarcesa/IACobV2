import pandas as pd

def get_signals(df):
    df['EMA20'] = df['Close'].ewm(span=20).mean()
    df['EMA50'] = df['Close'].ewm(span=50).mean()
    df['RSI'] = compute_rsi(df['Close'])
    df['MACD'] = df['Close'].ewm(span=12).mean() - df['Close'].ewm(span=26).mean()

    latest = df.iloc[-1]
    signal = "HOLD"

    if latest['EMA20'] > latest['EMA50'] and latest['RSI'] < 70:
        signal = "BUY"
    elif latest['EMA20'] < latest['EMA50'] and latest['RSI'] > 30:
        signal = "SELL"

    indicators = {
        "ema20": latest['EMA20'],
        "ema50": latest['EMA50'],
        "rsi": latest['RSI'],
        "macd": latest['MACD']
    }

    return signal, indicators

def compute_rsi(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))
